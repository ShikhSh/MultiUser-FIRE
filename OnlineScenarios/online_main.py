import sys
sys.path.append('../Common')

from common_config import *
from online_const import *
from common_utils import *
from plots import *

class Combined_Online_Algo():
    def __init__(self, eta, Main_algo_online_onj, BL3_online_obj, tot_users = common_NUM_USERS, users_to_care_about = common_NUM_USERS):
        self.numAP=common_NUM_ACCESS_POINTS
        self.eta = eta
        self.noBackup=NO_BACKUP
        self.tot_users = tot_users
        self.users_to_care_about = users_to_care_about
        self.failed_APs = {}

        self.Main_algo_online_onj = Main_algo_online_onj
        self.BL3_online_obj = BL3_online_obj

        self.pr_lu_trans_online = PR_LU_TRANS

        self.Reward_online = np.zeros((totalTS, self.users_to_care_about))
        self.runningAvg_online = np.zeros((totalTS))
        self.Action=np.zeros((totalTS+1, self.users_to_care_about, 2))

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
        
        self.storageCost_online=5*np.ones((common_NUM_ACCESS_POINTS))
        self.commDelay_online=LATENCY_MATRIX#np.array([[2.55316,9.70525, 7.02418], [9.70525, 2.55389,6.25835], [7.02418,6.26684,2.55398]])
        self.migrationCost_online=MIGR_COST

        self.states = self.generate_init_states()

        self.actions = self.generate_init_actions()

        self.prev_backup_locs = []
        for i in range(common_NUM_USERS):
            self.prev_backup_locs.append(self.noBackup)

        self.Action[0]=self.actions #initialising
        self.ap_capacities = AP_CAPACITIES
        self.user_loads = USER_LOADS
        print("USERS to care about = " + str(self.users_to_care_about))
        self.RISK_AWARE_PER_USER_ACTION_LIST = self.gen_per_user_actions_list()

        self.risk_taking_ct = 0
        self.risk_aware_ct = 0
    def is_risk_taking(self):
        return random.random() < self.eta

    def get_random_int(self, end):
        return random.randint(0,end-1)
    
    def generate_init_states(self):
        states = []
        for i in range(self.tot_users):
            curr_st = []
            curr_st.append(self.get_random_int(self.numAP))
            curr_st.append(self.get_random_int(self.numAP))
            curr_st.append(self.get_random_int(2))
            lb = self.get_random_int(self.numAP+1)
            if lb == self.numAP:
                lb = self.noBackup
            curr_st.append(lb)
            states.append(curr_st)
        return states
    
    def generate_init_actions(self):
        actions = []
        for i in range(self.tot_users):
            curr_act = []
            curr_act.append(self.get_random_int(self.numAP))
            lb = self.get_random_int(self.numAP+1)
            if lb == self.numAP:
                lb = self.noBackup
            curr_act.append(lb)
            actions.append(curr_act)
        return actions

    def find_mean(self, arr):
        if len(arr) > 0:
            return np.mean(arr)
        else:
            return 0
    
    def gen_results(self):
        self.mean_Reward_online = self.find_mean(self.Reward_online)
    
        self.mean_REreward_online = self.find_mean(self.REreward_online)
        self.mean_REmigration_online = self.find_mean(self.REmigration_online)
        self.mean_REdelay_online = self.find_mean(self.REdelay_online)
        self.mean_REstorage_online = self.find_mean(self.REstorage_online)
        self.mean_REcompDelay_online = self.find_mean(self.REcompDelay_online)
        
        self.mean_NSreward_online = self.find_mean(self.NSreward_online)
        self.mean_NSmigration_online = self.find_mean(self.NSmigration_online)
        self.mean_NSdelay_online = self.find_mean(self.NSdelay_online)
        self.mean_NSstorage_online = self.find_mean(self.NSstorage_online)
        self.mean_NScompDelay_online = self.find_mean(self.NScompDelay_online)

        print(f"REW: {self.mean_Reward_online}")
        print(f"RE-REW: {self.mean_REreward_online}")
        print(f"RE-mig: {self.mean_REmigration_online}")
        print(f"RE-del: {self.mean_REdelay_online}")
        print(f"RE-stor: {self.mean_REstorage_online}")
        print(f"RE-comp: {self.mean_REcompDelay_online}")
        print(f"NS-REW: {self.mean_NSreward_online}")
        print(f"NS-mig: {self.mean_NSmigration_online}")
        print(f"NS-del: {self.mean_NSdelay_online}")
        print(f"NS-stor: {self.mean_NSstorage_online}")
        print(f"NS-comp: {self.mean_NScompDelay_online}")

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
            self.failed_APs[ap] = common_LOCATION_BASED_FAILURE_TIME

    def get_user_info(self, user, states, actions, prev_backup_locs):
        user_state = states[user]
        user_action = actions[user]
        prevUserLoc=int(user_state[0])
        prevSvcLoc=int(user_state[1])
        newSvcLoc=int(user_action[0])
        backupLoc=int(user_action[1]) # initialization
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
    
    def gen_per_user_actions_list(self):
        back_up_options = list(range(self.numAP))
        back_up_options.append(self.noBackup)
        actlists = [
            list(range(self.numAP)),#[0,1, 2],
            back_up_options
        ]
        NUM_ACTIONS_PER_USER = (self.numAP*(self.numAP+1))
        actList0=np.zeros((NUM_ACTIONS_PER_USER,2))
        a=0
        # b=0
        for element in itertools.product(*actlists):
            actList0[a,:]=element
            a=a+1
        return actList0

    def get_risk_aware_actions(self, all_users_new_state):
        t = torch.tensor(np.array(all_users_new_state), dtype=torch.float32)
        t = torch.reshape(t, (-1,))
        Q_estimates = self.Main_algo_online_onj.get_q_value(t)
        Q_estimates = Q_estimates.reshape((self.tot_users, -1))
        num_actions_per_user = Q_estimates.shape[1]
        predicted_actions = []
        for user in range(self.users_to_care_about):
            policy = softmax(Q_estimates[user].cpu())
            actionNew=np.random.choice(np.arange(0,num_actions_per_user), 1, replace=False, p=policy)[0]
            actionNew = self.RISK_AWARE_PER_USER_ACTION_LIST[actionNew]
            predicted_actions.append(actionNew)
        
        return predicted_actions

    def get_risk_taking_actions(self, all_users_new_state):
        t = torch.tensor(np.array(all_users_new_state), dtype=torch.float32)
        t = t[:,0:-1] # exclude the last 
        t = torch.reshape(t, (-1,))
        Q_estimates = self.BL3_online_obj.get_q_value(t)
        Q_estimates = Q_estimates.reshape((self.tot_users, -1))
        num_actions_per_user = Q_estimates.shape[1]
        predicted_actions = []
        for user in range(self.users_to_care_about):
            policy = softmax(Q_estimates[user].cpu())
            actionNew=np.random.choice(np.arange(0,num_actions_per_user), 1, replace=False, p=policy)[0]
            predicted_actions.append(actionNew)
        # the action of the risk taking algorithm just has Ls = AP num
        # so add NoBackup to it for Lb
        predicted_actions = np.array(predicted_actions)
        predicted_actions = predicted_actions.reshape((predicted_actions.shape[0], 1))
        new_column = np.full((predicted_actions.shape[0], 1), self.noBackup)
        predicted_actions = np.hstack((predicted_actions, new_column))
        return predicted_actions

    def get_predicted_actions(self, isRiskTaking, all_users_new_state):
        if isRiskTaking:
            self.risk_taking_ct += 1
            return self.get_risk_taking_actions(all_users_new_state)
        else:
            self.risk_aware_ct += 1
            return self.get_risk_aware_actions(all_users_new_state)

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

            isRiskTaking = self.is_risk_taking()

            for user in range(self.tot_users):
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
                        user_reward += common_NEGATIVE_REWARD
                        # if backupLoc==self.noBackup:
                        #     print("NO BACKUP: State: ")
                        # else:
                        #     print("BACKUP==FAILURE: State: ")#, stateList0[state], "\t Action: ", actList0[action])
                    else:
                        user_reward += -self.commDelay_online[newUserLoc][backupLoc]
                        delay=-self.commDelay_online[newUserLoc][backupLoc]
                        self.REdelay_online.append(delay)
                    
                    user_reward += -migration_cost-storCost-backup_migration_cost
                    
                    self.REstorage_online.append(-storCost)
                    self.REreward_online.append(user_reward)
                    migr=-migration_cost-backup_migration_cost
                    self.REmigration_online.append(migr)
                    
                    nextState=[newUserLoc, newSvcLoc, 1, backupLoc]
                    user_anomalies.append(True)
                else: # no rare event has occured.
                    
                    MigrationCost=migration_cost+backup_migration_cost
                    CommDelayCost=self.commDelay_online[newUserLoc][newSvcLoc]
                    
                    user_reward += (-MigrationCost-CommDelayCost)-storCost
                    self.NSreward_online.append(user_reward)
                    self.NSmigration_online.append(-MigrationCost)
                    self.NSdelay_online.append(-CommDelayCost)
                    self.NSstorage_online.append(-storCost)

                    nextState=[newUserLoc, newSvcLoc, 0, backupLoc]
                    user_anomalies.append(False)

                all_rewards.append(user_reward)
                back_up_locs.append(backupLoc)
                all_users_new_state.append(nextState)
            
            for u in range(self.tot_users):
                if self.ap_capacities[new_service_locs[u]] - ap_user_load[new_service_locs[u]] == 0:
                    print("*****************")
                computational_delay = common_COMPUTATIONAL_DELAY_SCALING_FACTOR*1/(self.ap_capacities[new_service_locs[u]] - ap_user_load[new_service_locs[u]])
                all_rewards[u] -= computational_delay
                if user_anomalies[u]:
                    self.REcompDelay_online.append(computational_delay)
                else:
                    self.NScompDelay_online.append(computational_delay)
            self.Reward_online[t,:] = all_rewards[:]
            self.prev_backup_locs = back_up_locs

            predicted_actions = self.get_predicted_actions(isRiskTaking, all_users_new_state)

            self.Action[t+1, :]=predicted_actions
            
            self.actions=predicted_actions
            self.states=all_users_new_state
            
            if t>=1:
                if t<K:
                    self.runningAvg_online[t]=np.average(self.Reward_online[0:t])
                else:
                    self.runningAvg_online[t]=np.average(self.Reward_online[t-K:t])
        print(f"RiskAware = {self.risk_aware_ct}")
        print(f"RiskTaking = {self.risk_taking_ct}")
        self.gen_results()