from utils import *
from online_const import *
class Online_Algo():
    def __init__(self, dqn_wrapper, tot_users = NUM_USERS, users_to_care_about = NUM_USERS):
        self.dqn_wrapper = dqn_wrapper
        self.numAP=NUM_ACCESS_POINTS
        self.numActions = NUM_ACTIONS_PER_USER
        self.noBackup=NO_BACKUP
        self.tot_users = tot_users
        self.users_to_care_about = users_to_care_about
        self.failed_APs = {}

        self.pr_lu_trans_online = PR_LU_TRANS
        print(self.pr_lu_trans_online)
        print("--------------------------")
        
        self.stateList = PER_USER_STATE_LIST
        self.actList=PER_USER_ACTION_LIST
        # self.whichState=np.zeros((totalTS, NUM_USERS))

        self.Reward_online = np.zeros((totalTS, self.users_to_care_about))
        self.runningAvg_online = np.zeros((totalTS))
        self.Action=np.zeros((totalTS+1, self.users_to_care_about))

        self.REreward_online=[]
        self.REmigration_online=[]
        self.REdelay_online=[]
        self.REstorage_online=[]
        self.REcompDelay_online=[]

        self.NSreward_online=[]
        self.NSmigration_online=[]
        self.NSdelay_online=[]
        self.NSstorage_online=[]
        self.NScompDelay_online=[]

        MIGR_COST = np.zeros((self.numAP, self.numAP))
        STORAGE_COST_temp = np.zeros((self.numAP))
        for p in range(self.numAP):
          diff = random.uniform(-0.5, 0.5)
          STORAGE_COST_temp[p] = 5+diff
          for q in range(self.numAP):
            diff = random.uniform(-0.5, 0.5)
            MIGR_COST[p][q] = LATENCY_MATRIX[p][q]+diff
        
        self.storageCost_online=5*np.ones((NUM_ACCESS_POINTS))
        self.commDelay_online=LATENCY_MATRIX#np.array([[2.55316,9.70525, 7.02418], [9.70525, 2.55389,6.25835], [7.02418,6.26684,2.55398]])
        self.migrationCost_online=MIGR_COST

        self.states = self.generate_init_state()
        self.actions = self.gen_init_actions()
        self.prev_backup_locs = self.get_init_backups()

        self.Action[0]=self.actions #initialising
        self.ap_capacities = AP_CAPACITIES
        self.user_loads = USER_LOADS
        print("USERS to care about = " + str(self.users_to_care_about))
    
    # def find_mean(self, arr):
    #     if len(arr) > 0:
    #         return np.mean(arr)
    #     else:
    #         return 0
    
    # def gen_results(self):
    #     self.mean_Reward_online = self.find_mean(self.Reward_online)
    
    #     self.mean_REreward_online = self.find_mean(self.REreward_online)
    #     self.mean_REmigration_online = self.find_mean(self.REmigration_online)
    #     self.mean_REdelay_online = self.find_mean(self.REdelay_online)
    #     self.mean_REstorage_online = self.find_mean(self.REstorage_online)
    #     self.mean_REcompDelay_online = self.find_mean(self.REcompDelay_online)
        
    #     self.mean_NSreward_online = self.find_mean(self.NSreward_online)
    #     self.mean_NSmigration_online = self.find_mean(self.NSmigration_online)
    #     self.mean_NSdelay_online = self.find_mean(self.NSdelay_online)
    #     self.mean_NSstorage_online = self.find_mean(self.NSstorage_online)
    #     self.mean_NScompDelay_online = self.find_mean(self.NScompDelay_online)

    # """
    # Updates the failed location at every time step
    # """
    # def update_failed_locations(self):
    #     if not LOCATION_BASED_FAILURE_ENABLED:
    #         return
    #     for key in list(self.failed_APs):
    #         value = self.failed_APs[key]
    #         if value <= 1:
    #             self.failed_APs.pop(key, None)
    #         else:
    #             self.failed_APs[key] = value - 1
    # """
    # Adds a failed state to 
    # """
    # def insert_failed_location(self, ap):
    #     if ap in WEAK_AP_LIST and LOCATION_BASED_FAILURE_ENABLED:
    #         self.failed_APs[ap] = LOCATION_BASED_FAILURE_TIME
    
    def get_random_user_state(self):
        return random.randint(0,NUM_STATES_PER_USER-1)

    def generate_init_state(self):
        states = []
        for i in range(NUM_USERS):
          if i < self.users_to_care_about:
            states.append(self.get_random_user_state())
          else:
            states.append(0)
        return states
    
    def get_random_user_action(self):
        return random.randint(0,NUM_ACTIONS_PER_USER-1)
    
    def gen_init_actions(self):
        actions = []
        for i in range(self.users_to_care_about):
            actions.append(self.get_random_user_action())
        return actions
    
    def get_init_backups(self):
        prev_backup_locs = []
        for i in range(NUM_USERS):
            prev_backup_locs.append(self.noBackup)
        return prev_backup_locs
    
    def get_user_info(self, user, states, actions, prev_backup_locs):
        user_state = states[user]
        user_action = actions[user]
        prevUserLoc=int(self.stateList[user_state][0])
        prevSvcLoc=int(self.stateList[user_state][1])
        newSvcLoc=int(self.actList[user_action][0])
        backupLoc=int(self.actList[user_action][1]) # initialization
        user_prev_backup_loc = prev_backup_locs[user]

        return prevUserLoc, prevSvcLoc, newSvcLoc, backupLoc, user_prev_backup_loc
    
    def get_storage_cost(self, backupLoc):
        storCost=0
        if backupLoc!=self.noBackup:
            storCost=self.storageCost_online[backupLoc]
        return storCost
    
    def get_backup_migr_cost(self, backupLoc, user_prev_backup_loc):
        backup_migration_cost = 0
        if user_prev_backup_loc != self.noBackup and backupLoc!=self.noBackup and user_prev_backup_loc != backupLoc:
            backup_migration_cost = self.migrationCost_online[user_prev_backup_loc,backupLoc]
        return backup_migration_cost
    
    def get_migr_cost(self,prevSvcLoc,newSvcLoc):
        return self.migrationCost_online[prevSvcLoc,newSvcLoc]
    
    def get_new_user_loc(self, prevUserLoc):
        return np.random.choice(np.arange(0,self.numAP), 1, replace=False, p=self.pr_lu_trans_online[prevUserLoc,:])[0]
    
    def get_predicted_actions(self, all_users_new_state):
        Q_estimates = self.dqn_wrapper.get_q_value(envSt_to_agentSt_all(all_users_new_state))
        Q_estimates = Q_estimates.reshape((NUM_USERS, NUM_ACTIONS_PER_USER))
        predicted_actions = []
        for user in range(self.users_to_care_about):
            policy = softmax(Q_estimates[user].cpu())
            actionNew=np.random.choice(np.arange(0,NUM_ACTIONS_PER_USER), 1, replace=False, p=policy)[0]
            predicted_actions.append(actionNew)
        return predicted_actions
    
    def run(self):
        for t in range(0,totalTS):
            self.update_failed_locations()

            ap_user_load = np.zeros((self.numAP))
            random_nos_aps = np.random.rand(self.numAP)

            all_users_new_state = []
            back_up_locs = []
            all_rewards = []
            new_service_locs = []
            user_anomalies = []

            for user in range(self.users_to_care_about):
                user_reward = 0
                prevUserLoc, prevSvcLoc, newSvcLoc, backupLoc, user_prev_backup_loc = self.get_user_info(user, self.states, self.actions, self.prev_backup_locs)
                
                storCost=self.get_storage_cost(backupLoc)
                backup_migration_cost = self.get_backup_migr_cost(backupLoc, user_prev_backup_loc)
                migration_cost=self.get_migr_cost(prevSvcLoc,newSvcLoc)

                newUserLoc=self.get_new_user_loc(prevUserLoc)
                #eligibility[state,action,t]=eligibility[state,action,t]+1
                
                ap_user_load[newSvcLoc] += self.user_loads[user]
                new_service_locs.append(newSvcLoc)

                # Check if the new service location is already down due to some previous failure
                serv_loc_down = False
                if LOCATION_BASED_FAILURE_ENABLED and newSvcLoc in self.failed_APs:
                    user_reward += common_FAILED_AP_SERV_LOC_REW
                    serv_loc_down = True
                    
                rare_event_occured = random_nos_aps[prevSvcLoc] < actualEPS
                
                if not serv_loc_down and rare_event_occured and LOCATION_BASED_FAILURE_ENABLED:
                    self.insert_failed_location(newSvcLoc)

                #if random number is smaller than the sampling prob, rare event has occured
                if serv_loc_down or rare_event_occured:
                    failureLoc= newSvcLoc
                    # check if there is backup
                    if backupLoc==self.noBackup or backupLoc==failureLoc or backupLoc in self.failed_APs:
                        user_reward += NEGATIVE_REWARD
                        if backupLoc==self.noBackup:
                            print("NO BACKUP: State: ")
                        else:
                            print("BACKUP==FAILURE: State: ")#, stateList0[state], "\t Action: ", actList0[action])
                    else:
                        user_reward += -self.commDelay_online[newUserLoc][backupLoc]
                        delay=-self.commDelay_online[newUserLoc][backupLoc]
                        self.REdelay_online.append(delay)
                    
                    user_reward += -migration_cost-storCost-backup_migration_cost
                    
                    self.REstorage_online.append(-storCost)
                    self.REreward_online.append(user_reward)
                    migr=-migration_cost-backup_migration_cost
                    self.REmigration_online.append(migr)
                    
                    nextState=get_state_id(newUserLoc, newSvcLoc, 1, backupLoc)
                    user_anomalies.append(True)
                else: # no rare event has occured.
                    
                    MigrationCost=migration_cost+backup_migration_cost
                    CommDelayCost=self.commDelay_online[newUserLoc][newSvcLoc]
                    
                    user_reward += (-MigrationCost-CommDelayCost)-storCost
                    self.NSreward_online.append(user_reward)
                    self.NSmigration_online.append(-MigrationCost)
                    self.NSdelay_online.append(-CommDelayCost)
                    self.NSstorage_online.append(-storCost)
                    nextState=get_state_id(newUserLoc, newSvcLoc, 0, backupLoc)
                    user_anomalies.append(False)

                all_rewards.append(user_reward)
                back_up_locs.append(backupLoc)
                all_users_new_state.append(nextState)
            
            for u in range(NUM_USERS-self.users_to_care_about):
                if t==0:
                  print("Lesser users to care about")
                new_service_locs.append(0)
                back_up_locs.append(0)
                all_users_new_state.append(0)
            
            for u in range(self.users_to_care_about):
                if self.ap_capacities[new_service_locs[u]] - ap_user_load[new_service_locs[u]] == 0:
                    print("*****************")
                computational_delay = COMPUTATIONAL_DELAY_SCALING_FACTOR*1/(self.ap_capacities[new_service_locs[u]] - ap_user_load[new_service_locs[u]])
                all_rewards[u] -= computational_delay
                if user_anomalies[u]:
                    self.REcompDelay_online.append(computational_delay)
                else:
                    self.NScompDelay_online.append(computational_delay)
            self.Reward_online[t,:] = all_rewards[:]
            self.prev_backup_locs = back_up_locs

            predicted_actions = self.get_predicted_actions(all_users_new_state)

            self.Action[t+1, :]=predicted_actions
            
            self.actions=predicted_actions
            self.states=all_users_new_state
            
            if t>=1:
                if t<K:
                    self.runningAvg_online[t]=np.average(self.Reward_online[0:t])
                else:
                    self.runningAvg_online[t]=np.average(self.Reward_online[t-K:t])
            
        self.gen_results()