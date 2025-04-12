import sys
# setting path
sys.path.append('../Common')
from dqn import DQN_wrapper
from online_main import *

class Model_RiskAware_RiskTaking:
    def __init__(self) -> None:
        self.numUsers = common_NUM_USERS

        self.Reward_online = []
        self.runningAvg_online = []

        self.mean_Reward_online = None

        self.mean_REreward_online = None
        self.mean_REmigration_online = None
        self.mean_REdelay_online = None
        self.mean_REstorage_online = None
        self.mean_REcompDelay_online = None
        
        self.mean_NSreward_online = None
        self.mean_NSmigration_online = None
        self.mean_NSdelay_online = None
        self.mean_NSstorage_online = None
        self.mean_NScompDelay_online = None


        self.mean_Reward_online_over_runs = []

        self.mean_REreward_online_over_runs = []
        self.mean_REmigration_online_over_runs = []
        self.mean_REdelay_online_over_runs = []
        self.mean_REstorage_online_over_runs = []
        self.mean_REcompDelay_online_over_runs = []
        
        self.mean_NSreward_online_over_runs = []
        self.mean_NSmigration_online_over_runs = []
        self.mean_NSdelay_online_over_runs = []
        self.mean_NSstorage_online_over_runs = []
        self.mean_NScompDelay_online_over_runs = []

    def add_results(self, online_obj):
        self.Reward_online.append(online_obj.Reward_online)
        self.runningAvg_online.append(online_obj.runningAvg_online)

        self.mean_Reward_online_over_runs.append(online_obj.mean_Reward_online)
        self.mean_REreward_online_over_runs.append(online_obj.mean_REreward_online)
        self.mean_REmigration_online_over_runs.append(online_obj.mean_REmigration_online)
        self.mean_REdelay_online_over_runs.append(online_obj.mean_REdelay_online)
        self.mean_REstorage_online_over_runs.append(online_obj.mean_REstorage_online)
        self.mean_REcompDelay_online_over_runs.append(online_obj.mean_REcompDelay_online)
        self.mean_NSreward_online_over_runs.append(online_obj.mean_NSreward_online)
        self.mean_NSmigration_online_over_runs.append(online_obj.mean_NSmigration_online)
        self.mean_NSdelay_online_over_runs.append(online_obj.mean_NSdelay_online)
        self.mean_NSstorage_online_over_runs.append(online_obj.mean_NSstorage_online)
        self.mean_NScompDelay_online_over_runs.append(online_obj.mean_NScompDelay_online)

    def stack_n_mean(self, var, axis = 2):
        return np.mean(np.dstack(var),axis = axis)
    
    def generate_results(self):
        
        self.Reward_online = self.stack_n_mean(self.Reward_online)
        self.runningAvg_online = self.stack_n_mean(self.runningAvg_online)
            
        self.mean_Reward_online = mean(self.mean_Reward_online_over_runs)
        
        self.mean_REreward_online = mean(self.mean_REreward_online_over_runs)
        self.mean_REmigration_online = mean(self.mean_REmigration_online_over_runs)
        self.mean_REdelay_online = mean(self.mean_REdelay_online_over_runs)
        self.mean_REstorage_online = mean(self.mean_REstorage_online_over_runs)
        self.mean_REcompDelay_online = mean(self.mean_REcompDelay_online_over_runs)
        
        self.mean_NSreward_online = mean(self.mean_NSreward_online_over_runs)
        self.mean_NSmigration_online = mean(self.mean_NSmigration_online_over_runs)
        self.mean_NSdelay_online = mean(self.mean_NSdelay_online_over_runs)
        self.mean_NSstorage_online = mean(self.mean_NSstorage_online_over_runs)
        self.mean_NScompDelay_online = mean(self.mean_NScompDelay_online_over_runs)

        self.stdev_Reward_online = stdev(self.mean_Reward_online_over_runs)
        
        self.stdev_REreward_online = stdev(self.mean_REreward_online_over_runs)
        self.stdev_REmigration_online = stdev(self.mean_REmigration_online_over_runs)
        self.stdev_REdelay_online = stdev(self.mean_REdelay_online_over_runs)
        self.stdev_REstorage_online = stdev(self.mean_REstorage_online_over_runs)
        self.stdev_REcompDelay_online = stdev(self.mean_REcompDelay_online_over_runs)
        
        self.stdev_NSreward_online = stdev(self.mean_NSreward_online_over_runs)
        self.stdev_NSmigration_online = stdev(self.mean_NSmigration_online_over_runs)
        self.stdev_NSdelay_online = stdev(self.mean_NSdelay_online_over_runs)
        self.stdev_NSstorage_online = stdev(self.mean_NSstorage_online_over_runs)
        self.stdev_NScompDelay_online = stdev(self.mean_NScompDelay_online_over_runs)

class Run_RiskAware_RiskTaking:
    def create_wrapper_obj(self):
        NUM_ACTIONS_PER_USER = (common_NUM_ACCESS_POINTS*(common_NUM_ACCESS_POINTS+1))
        TOT_NUM_ACTIONS = NUM_ACTIONS_PER_USER*common_NUM_USERS
        ma_obj = DQN_wrapper(4*common_NUM_USERS, TOT_NUM_ACTIONS)
        NUM_ACTIONS_PER_USER = (common_NUM_ACCESS_POINTS)
        TOT_NUM_ACTIONS = NUM_ACTIONS_PER_USER*common_NUM_USERS
        bl3_obj = DQN_wrapper(3*common_NUM_USERS, TOT_NUM_ACTIONS)
        return ma_obj, bl3_obj

    def run(self):
        curr_dir = create_dir()
        initial_setup(None, dir = curr_dir)

        etas = [0, 0.2, 0.4, 0.6, 0.8, 1]
        ma_path = create_dir(dir_path = "../MainAlgo/diags/", generate_path = False)
        bl3_path = create_dir(dir_path = "../Baseline3/diags/", generate_path = False)

        iteration_dirs = [filename for filename in os.listdir(ma_path) if os.path.isdir(os.path.join(ma_path,filename)) and filename.isdigit()]
        eta_to_models = {}
        
        for eta in etas:
            obj = Model_RiskAware_RiskTaking()
            for fn in iteration_dirs:
                ma_iteration_dir = os.path.join(ma_path,fn)
                bl3_iteration_dir = os.path.join(bl3_path,fn)
                print(ma_iteration_dir)
                print(bl3_iteration_dir)
                ma_obj, bl3_obj = self.create_wrapper_obj()
                ma_obj.load_model(ma_iteration_dir + "/policy_net.pt")
                bl3_obj.load_model(bl3_iteration_dir + "/policy_net.pt")

                online_algo = Combined_Online_Algo(eta, ma_obj, bl3_obj)
                online_algo.run()
                obj.add_results(online_algo)
                sys.stdout.flush()
            # Earlier, the plots were plotted iterating over the users
            # Same plots can be plotted after averaging over the 3rd dimension, which is the user's dimension
            obj.generate_results()
            eta_to_models[eta] = obj
            sys.stdout.flush()

        for k in eta_to_models.keys():
            print(f"ETA = {k}")
            gen_online_plots(obj, curr_dir, True)
        sys.stdout.flush()
        generate_risk_aware_n_risk_taking_graphs(eta_to_models, curr_dir)
        sys.stdout.flush()
        clean()

if __name__ == '__main__':
    runner = Run_RiskAware_RiskTaking()
    runner.run()