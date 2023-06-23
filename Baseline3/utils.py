from constants import *

Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))

class ReplayMemory(object):

    def __init__(self, capacity):
        self.memory = deque([],maxlen=capacity)

    def push(self, *args):
        """Save a transition"""
        s, a, ns, r = args
        # print(type(s), type(a), type(ns), type(r))
        # print(s,a,ns,r,iw)
        s = conv_to_tensor(s)
        a = conv_to_tensor(a)#torch.tensor([[a]], device=device, dtype = torch.int64)
        ns = conv_to_tensor(ns)
        r = conv_to_tensor(r)
        # print("in push",s.size(), type(a), type(ns), type(r))
        self.memory.append(Transition(s, a, ns, r))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

def gen_per_user_states_list():
    rsList = set()
    # back_up_options = list(range(NUM_ACCESS_POINTS))
    # back_up_options.append(NO_BACKUP)
    combinations = [
      list(range(NUM_ACCESS_POINTS)),#[0,1, 2],
      list(range(NUM_ACCESS_POINTS)),#[0,1,2],
      [0,1], # Anomaly/Not
    #   back_up_options # Backup_loc: [0,1, 2]
    ]
    stateList0=np.zeros((NUM_STATES_PER_USER,3), dtype = np.int)
    a=0
    for element in itertools.product(*combinations):
        stateList0[a,:]=element[:]
        if stateList0[a,2]==1:
            rsList.add(a)
        a+=1
    return stateList0, rsList
PER_USER_STATE_LIST, RARE_STATES = gen_per_user_states_list()
# print(list(enumerate(PER_USER_STATE_LIST))) # <Lu,Ls,A/N,Lb>
print("RARE_STATES:")
print(RARE_STATES)

def gen_per_user_actions_list():
    # back_up_options = list(range(NUM_ACCESS_POINTS))
    # back_up_options.append(NO_BACKUP)
    actlists = [
        list(range( NUM_ACCESS_POINTS)),#[0,1, 2],
        # back_up_options
    ]
    actList0=np.zeros((NUM_ACTIONS_PER_USER))
    a=0
    # b=0
    for element in actlists[0]:
        actList0[a]=element
        a=a+1
    print(actList0)
    return actList0
PER_USER_ACTION_LIST = gen_per_user_actions_list()

def get_tensor_state(state): # state_transformation
    st = PER_USER_STATE_LIST[state]
    t = torch.tensor(st, dtype=torch.float32)
    return t

def convert_to_tensor(state):
    t = torch.tensor(state, dtype=torch.float32)
    return t

def get_state_tuple(state): # state_transformation2
    st = PER_USER_STATE_LIST[state]
    return st

def get_state_id(newUserLoc, newSvcLoc, anomaly):
    stateName=np.array([int(newUserLoc),int(newSvcLoc),int(anomaly)])
    new_state=np.where(np.all(PER_USER_STATE_LIST==stateName,axis=1))[0][0]
    return new_state

'''
Input: Numpy array (array of all the actions or their q-values -  dim = 1, shape = (user X action))
Output: Reshaped Numpy Array (reshaped array of the shape of (user, actions))
'''

def reshape_nn_outputs(outputs, users = NUM_USERS):
    return outputs.reshape((users, -1))

# test = np.array([1,2,3,4,5,6])
# print(reshape_nn_outputs(test, 2)[0])

def envSt_to_agentSt_perUser(state):
    """
    Processes state for 1 User
    Agent requires state in the form -> tuples of 4 for each user
    """
    return get_state_tuple(state)
def envSt_to_agentSt_all(states, users = NUM_USERS, return_list = False):
    """
    Processes state for 1 User
    Agent requires state in the form -> tuples of 4 for each user
    """
    expanded_states = []
    for u in range(users):
        user_st = states[u]
        user_expanded_st = envSt_to_agentSt_perUser(user_st)
        expanded_states.append(user_expanded_st)
    expanded_states = convert_to_tensor(expanded_states)
    expanded_states = torch.reshape(expanded_states, (-1,))
    
    # assert len(expanded_states.shape) == 1
    # assert expanded_states.shape[0] == INPUT_SHAPE
    if return_list:
        return expanded_states.tolist()
    return expanded_states

def agentSt_to_envSt_perUser(state, users = NUM_USERS):
    """
    Processes state for 1 User
    Env requires the state in the form -> 1 number for each user
    """
    # for u in range(users):
    return get_state_id(state[0], state[1], state[2], state[3])

# print(envSt_to_agentSt_perUser(5))
# print(envSt_to_agentSt_perUser(3))
# print(envSt_to_agentSt_all([5,3], 2))
# print(envSt_to_agentSt_all([5,3], 2, True))
# assert agentSt_to_envSt_perUser([0,0,1,100]) == 7
# assert agentSt_to_envSt_perUser([0,2,1,0]) == 20 # 20
# assert agentSt_to_envSt_perUser([1,0,1,1]) == 29 # 20