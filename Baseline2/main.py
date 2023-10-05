from dqn import *

class BL2_RLalgo:

    def __init__(self, alpha = ALPHA):
        self.gamma = GAMMA
        self.trials  = TRIALS
        self.trial_len = TRIAL_LEN
        self.totalTS=self.trials*self.trial_len
        self.dqn_agent=DQN_wrapper()
        # env details!!
        self.numAP=NUM_ACCESS_POINTS
        self.numStatesPerUser = NUM_STATES_PER_USER
        self.numActionsPerUser = NUM_ACTIONS_PER_USER
        self.numUsers = NUM_USERS
        # self.noBackup=NO_BACKUP
        self.delta=DELTA # bounds for estimate epsilon.
        self.userAccFactor=USER_ACC_FACTOR
        self.K = K_
        self.create_dicts()
        self.alpha = alpha # learning rate
        self.alphaT = alpha#ALPHA_T
        self.alphaU = alpha#ALPHA_U
        # self.prev_backup_loc = []
        # for _ in range(self.numUsers):
        #     self.prev_backup_loc.append(self.noBackup)

    def create_dicts(self):
        self.pr_lu_trans=PR_LU_TRANS

        # self.QEst=np.zeros((self.numUsers, self.numStatesPerUser, self.numActionsPerUser))

        # self.anomalySamplingDist=np.zeros((self.numUsers, self.numStatesPerUser))
        # self.anomalySamplingDist[:,:]=0.5
        self.actualEps=ACTUAL_EPS
        
        self.ap_capacities = AP_CAPACITIES
        self.ap_user_load = AP_USER_LOADS
        self.user_loads = USER_LOADS

        # self.U_normal=np.zeros((self.numUsers, self.numStatesPerUser))
        # self.T_anomaly=np.zeros((self.numUsers, self.numStatesPerUser))

        self.migrationCost = COST_DICT
        self.commDelay= COST_DICT
        # self.storageCost = STORAGE_COST

        self.Rewards=np.zeros((self.numUsers, self.totalTS+1))
        self.runningAvg=np.zeros((self.numUsers, self.totalTS+1))
        # self.TDerror=0#np.zeros((self.totalTS+1))
        # self.importanceWeight=np.zeros((self.numUsers, self.numStatesPerUser))
        
        # self.ALL_ANOMALY_SAMPL_DISTR = np.zeros((self.numUsers, self.numStatesPerUser, self.totalTS+1))
        # self.T_ANOMALY_T = np.zeros((self.numUsers, self.numStatesPerUser, self.totalTS+1))
        # self.U_NORMAL_T = np.zeros((self.numUsers, self.numStatesPerUser, self.totalTS+1))

        self.actList=PER_USER_ACTION_LIST
        self.stateList=PER_USER_STATE_LIST
        # self.rsList=RARE_STATES
        print(self.actList)

        # Keep a track of the failed APs and how long will they take to recover
        self.failed_APs = {}
    
    """
    Updates the failed location at every time step
    """
    def update_failed_locations(self):
        if not LOCATION_BASED_FAILURE_ENABLED:
            return
        for key in list(self.failed_APs):
            value = self.failed_APs[key]
            if value <= 1:
                self.failed_APs.pop(key, None)
            else:
                self.failed_APs[key] = value - 1
    """
    Adds a failed state to 
    """
    def insert_failed_location(self, ap):
        if ap in common_WEAK_AP_LIST and LOCATION_BASED_FAILURE_ENABLED:
            self.failed_APs[ap] = 2

    def env(self, cur_states, actions, t):
        # curr_back_up_loc = []
        all_users_new_state = []
        all_users_rew = []
        all_users_service_loc = []
        self.ap_user_load = np.zeros((self.numAP))

        random_nos_aps = np.random.rand(self.numAP)

        self.update_failed_locations()

        for user in range(self.numUsers):
            user_state = cur_states[user]
            user_action = actions[user]
            prevUserLoc=int(self.stateList[user_state][0])
            prevSvcLoc=int(self.stateList[user_state][1])
            newSvcLoc=int(self.actList[user_action])
            # backupLoc=int(self.actList[user_action][1]) # initialization
            all_users_service_loc.append(newSvcLoc)
            self.ap_user_load[newSvcLoc] += self.user_loads[user]
            # user_prev_backup_loc = self.prev_backup_loc[user]
            
            user_reward = 0
            
            storCost=0
            # if backupLoc!=self.noBackup:
            #     storCost=self.storageCost[backupLoc]

            #     backup_migration_cost = 0
            #     if user_prev_backup_loc != self.noBackup and backupLoc!=self.noBackup and user_prev_backup_loc != backupLoc:#second condition is true for else block
            #         backup_migration_cost = self.migrationCost[user_prev_backup_loc,backupLoc]

            migration_cost=self.migrationCost[prevSvcLoc,int(newSvcLoc)]

            newUserLoc=np.random.choice(np.arange(0,self.numAP), 1, replace=False, p=self.pr_lu_trans[prevUserLoc,:])
            
            # self.eligibility[cur_state,action,t]=eligibility[cur_state,action,t]+1
            
            #if random number is smaller than the sampling prob, rare event has occured
            
            serv_loc_down = False
            if LOCATION_BASED_FAILURE_ENABLED and newSvcLoc in self.failed_APs:
                user_reward += common_FAILED_AP_SERV_LOC_REW
                serv_loc_down = True

            rare_event_occured = random_nos_aps[prevSvcLoc] < self.actualEps

            #if random number is smaller than the sampling prob, rare event has occured
            if serv_loc_down or rare_event_occured:
                # failureLoc= self.actList[user_action][0]
                # check if there is backup
                # if backupLoc==self.noBackup:
                user_reward += NEGATIVE_REWARD-migration_cost
                # else:
                #     if backupLoc==failureLoc: # we dont want this to happen.
                #         user_reward = NEGATIVE_REWARD-self.migrationCost[prevSvcLoc,newSvcLoc]-storCost-backup_migration_cost
                #     else:
                #         user_reward = -self.commDelay[newUserLoc,backupLoc]-self.migrationCost[prevSvcLoc,newSvcLoc]-storCost-backup_migration_cost

                new_state=get_state_id(newUserLoc, newSvcLoc, 1)                
                # self.importanceWeight[user, user_state]=1.0*self.actualEps/self.anomalySamplingDist[user, user_state]
                
                if not serv_loc_down and LOCATION_BASED_FAILURE_ENABLED and rare_event_occured:
                    self.insert_failed_location(newSvcLoc)
            
            else: # no rare event has occured.
                
                CommDelayCost=self.commDelay[newUserLoc,int(newSvcLoc)]
                
                user_reward += (-migration_cost-CommDelayCost)-storCost #- backup_migration_cost

                new_state=get_state_id(newUserLoc, newSvcLoc, 0)
            
                # compute importance sampling weight.
                # self.importanceWeight[user, user_state]=1.0*(1-self.actualEps)/(1-self.anomalySamplingDist[user, user_state])

            # curr_back_up_loc.append(backupLoc)
            all_users_new_state.append(new_state)
            all_users_rew.append(user_reward)
        for u in range(self.numUsers):
            computational_delay = COMPUTATIONAL_DELAY_SCALING_FACTOR*1/(self.ap_capacities[all_users_service_loc[u]] - self.ap_user_load[all_users_service_loc[u]])
            all_users_rew[u] -= computational_delay
        self.Rewards[:, t] = all_users_rew[:]
        # self.prev_backup_loc = curr_back_up_loc
        return all_users_new_state

    def run_algo(self):
        t=0
        cur_states = INITIAL_STATE
        for trial in range(self.trials):
            cur_states = INITIAL_STATE
            print("=======",trial,"=======")
            for step in range(self.trial_len):
                actions = self.dqn_agent.select_action(envSt_to_agentSt_all(cur_states))
                new_states = self.env(cur_states, actions, t)
                
                if t>EPSILON_THRESHOLD:
                    self.dqn_agent.eps=max(self.dqn_agent.eps-0.00005,0.01)

                # Q_estimates = self.dqn_agent.get_q_value(envSt_to_agentSt_all(new_states))
                # curr_imp_wts = []

                # if t>0:
                #     self.ALL_ANOMALY_SAMPL_DISTR[:, :, t] = self.ALL_ANOMALY_SAMPL_DISTR[:, :, t-1]
                #     self.T_ANOMALY_T[:, :, t] = self.T_ANOMALY_T[:, :, t-1]
                #     self.U_NORMAL_T[:, :, t] = self.U_NORMAL_T[:, :, t-1]

                # for user in range(self.numUsers):
                #     # # g) update T and U.
                #     user_curr_state = cur_states[user]
                #     user_action = actions[user]
                #     user_new_state = new_states[user]
                #     user_Q_estimate = max(Q_estimates[user]).item()
                #     user_rew = self.Rewards[user,t]
                #     # if user == 0:
                #     #   print("=================RS:" + str(user_new_state in self.rsList))
                #     #   print(self.T_anomaly[user,:])
                #     #   print(self.U_normal[user,:])
                #     #   print("--------------------")
                #     if user_new_state in self.rsList:
                #         self.T_anomaly[user, user_curr_state]=(1-self.alphaT)*self.T_anomaly[user, user_curr_state]+self.alphaT*self.actualEps*(user_rew + self.gamma*user_Q_estimate)
                #     else:
                #         self.U_normal[user, user_curr_state]=(1-self.alphaU)*self.U_normal[user, user_curr_state]+self.alphaU*(1-self.actualEps)*(user_rew + self.gamma*user_Q_estimate)
                #     # if user == 0:
                #     #   # print("=================RS:" + str(user_new_state in self.rsList))
                #     #   print(self.T_anomaly[user,:])
                #     #   print(self.U_normal[user,:])
                #     #   print("=================")
                #     #   breakpoint()

                #     # # h) update rare event probs
                #     est1=abs(self.T_anomaly[user, user_curr_state])/(abs(self.T_anomaly[user, user_curr_state])+abs(self.U_normal[user, user_curr_state]))
                #     # self.est11[t]=est1
                #     # for s in range(0,self.numStatesPerUser):
                #     #     self.anomalySamplingDist[s,t+1]=self.anomalySamplingDist[s,t]
                #     self.anomalySamplingDist[user, user_curr_state]=min(max(self.delta,est1),1-self.delta)
                #     curr_imp_wts.append(self.importanceWeight[user,user_new_state])
                    
                #     self.ALL_ANOMALY_SAMPL_DISTR[user, user_curr_state, t] = self.anomalySamplingDist[user, user_curr_state]
                #     self.T_ANOMALY_T[user, user_curr_state, t] = self.T_anomaly[user, user_curr_state]
                #     self.U_NORMAL_T[user, user_curr_state, t] = self.U_normal[user, user_curr_state]
                
                self.dqn_agent.memory.push(envSt_to_agentSt_all(cur_states, return_list=True), actions.tolist(), envSt_to_agentSt_all(new_states, return_list=True), self.Rewards[:,t])
                self.dqn_agent.optimize_model()
                
                t=t+1
                cur_states = new_states
                if t>=1:
                    if t<self.K:
                        self.runningAvg[:,t]=np.average(self.Rewards[:,0:t])
                    else:
                        self.runningAvg[:,t]=np.average(self.Rewards[:,t-self.K:t])
                
            # out of step, inside trials
            if trial % TARGET_UPDATE == 0:
                self.dqn_agent.train_target_pytorch()#self.dqn_agent.target_net.load_state_dict(self.dqn_agent.policy_net.state_dict())

            if self.numUsers == 1:
                for s in range(self.numStatesPerUser):
                    if s not in [0,1,2,3,4]:
                        break
                    with torch.no_grad():
                        q_vals = self.dqn_agent.get_q_value(envSt_to_agentSt_all([s]))[0]
                        for a in range(TOT_NUM_ACTIONS):
                            print("State: ", str(s), "-----Actions: " , str(a), "-----Pred: ", q_vals[a])
            else:
                s = random.sample(range(0, self.numStatesPerUser), self.numUsers)
                with torch.no_grad():
                    q_vals = self.dqn_agent.get_q_value(envSt_to_agentSt_all(s))
                    # for u in range(obj.numUsers):
                    u = 0
                    q_val_user = q_vals[u]
                    user_st = s[u]
                    for a in range(NUM_ACTIONS_PER_USER):
                        print("User: ", str(u), "State: ", str(user_st), "-----Actions: " , str(a), "-----Pred: ", q_val_user[a])