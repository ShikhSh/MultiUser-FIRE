from utils import *

class DQN(nn.Module):

    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        #self.linear_relu_stack = nn.Sequential(
        #    nn.Linear(input_dim, 512),
        #    nn.ReLU(),
        #    nn.Linear(512, 512),
        #    nn.ReLU(),
        #    nn.Linear(512, 512),
        #    nn.ReLU(),
        #    nn.Linear(512, output_dim)
        #)
        # self.linear_relu_stack = nn.Sequential(
        #     nn.Linear(input_dim, 12),
        #     nn.ReLU(),
        #     nn.Linear(12, 24),
        #     nn.ReLU(),
        #     nn.Linear(24, 12),
        #     nn.ReLU(),
        #     nn.Linear(12, output_dim)
        # )
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(input_dim, 24),
            nn.ReLU(),
            nn.Linear(24, 48),
            nn.ReLU(),
            nn.Linear(48, 24),
            nn.ReLU(),
            nn.Linear(24, output_dim)
        )

        # self.linear_relu_stack = nn.Sequential(
        #     nn.Linear(input_dim, 96),
        #     nn.ReLU(),
        #     nn.Linear(96, 198),
        #     nn.ReLU(),
        #     nn.Linear(198, 96),
        #     nn.ReLU(),
        #     nn.Linear(96, output_dim)
        # )

    # Called with either one element to determine next action, or a batch
    # during optimization. Returns tensor([[left0exp,right0exp]...]).
    def forward(self, x):
        # print("---x")
        # print(x)
        x = x.to(device)
        return self.linear_relu_stack(x)

n_actions = TOT_NUM_ACTIONS

class DQN_wrapper:
    def __init__(self, input_dim = INPUT_SHAPE, output_dim = TOT_NUM_ACTIONS):
         # lu, ls, anomaly/not, backup_loc
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.policy_net = DQN(input_dim, output_dim).to(device)
        self.target_net = DQN(input_dim, output_dim).to(device)
        print(self.policy_net)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()

        self.optimizer = optim.Adam(self.policy_net.parameters(), lr = LEARNING_RATE)
        self.criterion = nn.MSELoss()

        self.memory = ReplayMemory(10000)

        self.steps_done = 0
        self.eps = EPSILON_DECAY
        self.tau = TAU
    
    def select_action(self, state, sample = random.random(), users = NUM_USERS):
        if sample > self.eps:
            with torch.no_grad():
                users_all_actions = self.policy_net(state)
                # shape (UxA,) U = no of users, A = actions per user 
                users_all_actions = reshape_nn_outputs(users_all_actions, users)
                # shape (U,A) U = no of users, A = actions per user
                assert users_all_actions.shape == (NUM_USERS, NUM_ACTIONS_PER_USER), "select_action:: users_all_actions shape wrong"
                best_actions = torch.argmax(users_all_actions, dim = 1)
                assert best_actions.shape == (NUM_USERS,), "select_action:: best_actions shape wrong"
                return best_actions
        else:
            random_actions = []
            for i in range(users):
                random_actions.append(random.randrange(NUM_ACTIONS_PER_USER))
            random_actions = torch.tensor(random_actions)
            assert random_actions.shape == (NUM_USERS,), "select_action:: best_actions shape wrong"
            return random_actions
    
    def get_q_value(self, state, users = NUM_USERS):
        with torch.no_grad():
            Q_estimates = self.policy_net(state)
            Q_estimates = reshape_nn_outputs(Q_estimates, users)
            return Q_estimates
            # return torch.max(Q_estimates, dim = 1)
    
    def optimize_model(self):
        if len(self.memory) < BATCH_SIZE:
            return
        transitions = self.memory.sample(BATCH_SIZE)
        # Transpose the batch (see https://stackoverflow.com/a/19343/3343043 for
        # detailed explanation). This converts batch-array of Transitions
        # to Transition of batch-arrays.
        batch = Transition(*zip(*transitions))

        # Compute a mask of non-final states and concatenate the batch elements
        # (a final state would've been the one after which simulation ended)
        # print(batch.next_state)

        """
        from the memory, convert each to tensor:
        List of True since neither state is None [True, True, ....] x BatchSize
        """
        """
        Original Purpose of this is to generate a mask with True everywhere where next state != Null;
        Next_state = NUll as the final state only, so basically, mask stores True for all non final states
        """
        non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                              batch.next_state)), device=device, dtype=torch.bool)
        # This picks up the all the Non-Null state (original purpose - to exclude last state which is NULL)
        non_final_next_states = torch.cat([s for s in batch.next_state
                                                    if s is not None])
        # print("nfm",non_final_mask.size()) # [B]
        # print("nfns_b4:",non_final_next_states.size()) # [B, 1, state_size] state_size = 4*num_of_users or INPUT_DIM
        """
        Our state is defined by 4 values, so just a reshape where each row represents 1 possible next-state.
        """
        non_final_next_states = torch.reshape(non_final_next_states, (BATCH_SIZE, self.input_dim))
        # print("nfns_af:",non_final_next_states.size()) # [B, state_size] state_size = 4*num_of_users or INPUT_DIM
        
        state_batch = torch.cat(batch.state).squeeze(dim=1)
        action_batch = torch.cat(batch.action).long().reshape(BATCH_SIZE, NUM_USERS, 1)
        reward_batch = torch.cat(batch.reward).squeeze(dim=1)
        # imp_wt_batch = torch.cat(batch.imp_wt).squeeze(dim=1)
        # print("sb",state_batch.size()) # [B,state_size]
        # print("ab",action_batch.size()) # [B,numOfUsers,1] -> extra 1 needed for gather action below
        # print("rb",reward_batch.size()) # [B,numOfUsers]
        # print("iw",imp_wt_batch.size()) # [B,numOfUsers]
        
        """
        Each Converted to tensor now
        """

        """
        Compute Q(s_t, a) - the model computes Q(s_t), then we select the
        columns of actions taken. These are the actions which would've been taken
        for each batch state according to policy_net and we just select the Q-values behind those actions.
        
        For each row above, for each User, we have per user actions = NUM_ACTIONS_PER_USER, just a reshape into this,
        since Neural Network returns all actions together and we interpret them as 1st NUM_ACTIONS_PER_USER outputs
        correspond to the first user, next NUM_ACTIONS_PER_USER correspond to the second user and so on.
        """
        state_action_values = self.policy_net(state_batch)
        # print("sav_b4:",state_action_values.size()) # [B,TOT_ACTS]
        state_action_values = torch.reshape(state_action_values, (BATCH_SIZE, NUM_USERS, NUM_ACTIONS_PER_USER))
        # print("sav_af:",state_action_values.size()) # [B,U,ActsPerUser]
        
        """
        Now, predictions are for 6 actions, pick out the value which is for the current action
        Dim used is 2 since dim0 = Batch, dim1 = User, dim2 = ActionPerUser
        """
        # print(state_action_values)
        # print(action_batch)
        state_action_values = state_action_values.gather(2, action_batch).squeeze()
        state_action_values = state_action_values.reshape((BATCH_SIZE,NUM_USERS))
        # print(state_action_values)
        # print("sav_action_batch: ", state_action_values.size()) # [B,U] -> pick up value for the action stored in action batch for each user
        
        """
        Above, for the current states, we used Policy network. Now for next state values, we use target network.

        Compute V(s_{t+1}) for all next states.
        Expected values of actions for non_final_next_states are computed based
        on the "older" target_net; selecting their best reward with max(1)[0].
        This is merged based on the mask, such that we'll have either the expected
        state value or 0 in case the state was final.
        """
        next_state_values = torch.zeros((BATCH_SIZE, NUM_USERS), device=device) # store the values for best actions based on next states
        # print("sav",next_state_values.size())
        target_vals = self.target_net(non_final_next_states).reshape(BATCH_SIZE, NUM_USERS, NUM_ACTIONS_PER_USER)
        # print("TargetSHape",target_vals.size()) # [B,U,ActsPerUser]
        target_vals = torch.max(target_vals,dim = 2)
        target_vals = target_vals[0]
        # print("0MaxTargetSHape",target_vals.size())
        next_state_values[non_final_mask] = target_vals.detach()
        
        """
        Compute the expected Q values:
        We take the values from the target network for the next state,
        multiply them with Gamma,
        to that, we add the rewards,
        and multiply the importance weights.
        
        This gives us 1 value per user (for which the 'Q-value' based on 'target net' was 'max').
        """
        expected_state_action_values = (next_state_values * GAMMA).reshape((BATCH_SIZE,NUM_USERS))#( + reward_batch)*imp_wt_batch
        # print("=====**********EXP1=====", expected_state_action_values.size(), "=====**********EXP1=====",reward_batch.size())
        expected_state_action_values = (expected_state_action_values + reward_batch)
        # print("=====**********EXP2=====", expected_state_action_values.size())
        # print("=====**********EXP222=====", imp_wt_batch.size())
        # expected_state_action_values = (expected_state_action_values)*imp_wt_batch
        # print("=====**********EXP3=====", expected_state_action_values.size())
        # print("=====**********EXP4=====", expected_state_action_values.unsqueeze(1).size())
        expected_state_action_values = expected_state_action_values.reshape((BATCH_SIZE,NUM_USERS))
        
        """
        Compute Huber loss:
        Now we have state_values also per user for just the action which was taken,
        we have the next_state_values per user for which the Q-val based on target net was the max,
        so we can calculate the loss between the two and update the network based on it.

        Our total outputs = BATCH_SIZE x NUM_USERS x NUM_ACTIONS_PER_USER
        The losses we found = BATCH_SIZE x NUM_USERS
        """
        # print(state_action_values.size(), "-------", expected_state_action_values.size())#unsqueeze(1).size())
        loss = self.criterion(state_action_values, expected_state_action_values)#.unsqueeze(1))
        
        # print("=====LOSS=====", loss)
        # print("=====LOSS=====", loss.data)
        # print("=====NonFinnextSt=====", non_final_next_states)
        # print("=====REW=====", reward_batch)
        # print("=====ACT=====", action_batch)
        # print("=====ST-Batch=====", state_batch)
        # print("=====IMP_WT=====", imp_wt_batch)
        # print("=====NSV=====", next_state_values)
        # print("=====EXP-size=====", expected_state_action_values)
        # print("=====ST-Act-size=====", state_action_values)
        # Optimize the model
        self.optimizer.zero_grad()
        loss.backward()
        for param in self.policy_net.parameters():
            param.grad.data.clamp_(-1, 1)
        self.optimizer.step()
        # # TODO: Remove
        # print(action_batch)

    def train_target_pytorch(self):
        self.target_net.load_state_dict(self.policy_net.state_dict())
    def save_model(self, name):
        name = "./"+name
        torch.save(self.policy_net.state_dict(), name)