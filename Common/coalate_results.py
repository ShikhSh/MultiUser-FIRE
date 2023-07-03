from common_config import *
from online_const import *
from common_utils import *
from plots import *

import sys
 
# setting path
sys.path.append('../MainAlgo')
sys.path.append('../Baseline3')
sys.path.append('../Baseline2')

class Coalate_Results:
    def __init__(self):
        self.numUsers = common_NUM_USERS

        self.Rewards = []
        self.runningAvg = []

        self.Reward_online = []
        self.runningAvg_online = []
        self.NSreward_online = []
        self.REreward_online = []

        self.mean_Reward_online = []

        self.mean_REreward_online = []
        self.mean_REmigration_online = []
        self.mean_REdelay_online = []
        self.mean_REstorage_online = []
        self.mean_REcompDelay_online = []
        
        self.mean_NSreward_online = []
        self.mean_NSmigration_online = []
        self.mean_NSdelay_online = []
        self.mean_NSstorage_online = []
        self.mean_NScompDelay_online = []
    
    def stack_n_mean(self, var, axis = 2):
        return np.mean(np.dstack(var),axis = axis)
    
    def generate_results(self):
        self.Rewards = self.stack_n_mean(self.Rewards)
        self.runningAvg = self.stack_n_mean(self.runningAvg)
        self.Reward_online = self.stack_n_mean(self.Reward_online)
        self.runningAvg_online = self.stack_n_mean(self.runningAvg_online)
        self.NSreward_online = self.stack_n_mean(self.NSreward_online)
        self.REreward_online = self.stack_n_mean(self.REreward_online)

        self.mean_Reward_online = mean(self.mean_Reward_online)
        self.mean_REreward_online = mean(self.mean_REreward_online)
        self.mean_REmigration_online = mean(self.mean_REmigration_online)
        self.mean_REdelay_online = mean(self.mean_REdelay_online)
        self.mean_REstorage_online = mean(self.mean_REstorage_online)
        self.mean_REcompDelay_online = mean(self.mean_REcompDelay_online)
        self.mean_NSreward_online = mean(self.mean_NSreward_online)
        self.mean_NSmigration_online = mean(self.mean_NSmigration_online)
        self.mean_NSdelay_online = mean(self.mean_NSdelay_online)
        self.mean_NSstorage_online = mean(self.mean_NSstorage_online)
        self.mean_NScompDelay_online = mean(self.mean_NScompDelay_online)
    
    def load_data_from_dir(self, path):
        trainer = load_object(path+"trainer_obj.pkl")
        online_obj = load_object(path+"online_obj.pkl")

        self.Rewards.append(trainer.Rewards)
        self.runningAvg.append(trainer.runningAvg)
        self.Reward_online.append(online_obj.Reward_online)
        self.runningAvg_online.append(online_obj.runningAvg_online)
        self.NSreward_online.append(online_obj.NSreward_online)
        self.REreward_online.append(online_obj.REreward_online)

        self.mean_Reward_online.append(online_obj.mean_Reward_online)
        self.mean_REreward_online.append(online_obj.mean_REreward_online)
        self.mean_REmigration_online.append(online_obj.mean_REmigration_online)
        self.mean_REdelay_online.append(online_obj.mean_REdelay_online)
        self.mean_REstorage_online.append(online_obj.mean_REstorage_online)
        self.mean_REcompDelay_online.append(online_obj.mean_REcompDelay_online)
        self.mean_NSreward_online.append(online_obj.mean_NSreward_online)
        self.mean_NSmigration_online.append(online_obj.mean_NSmigration_online)
        self.mean_NSdelay_online.append(online_obj.mean_NSdelay_online)
        self.mean_NSstorage_online.append(online_obj.mean_NSstorage_online)
        self.mean_NScompDelay_online.append(online_obj.mean_NScompDelay_online)
        
    def coalate(self):
        n = len(sys.argv)
        path = None
        if n<2:
            print("No directory path passed to coalate, using WORKING DIR")
            path = WORKING_DIR
        else:
            path = sys.argv[1]
        
        # the path which is scanned for the objects of various runs
        iteration_dirs = [filename for filename in os.listdir(path) if os.path.isdir(os.path.join(path,filename))]

        for sub_dir in iteration_dirs:
            # open pkl files in these, load the objects, add to class variables
            print(sub_dir)
            self.load_data_from_dir(path + sub_dir + "/")
        
        # now we have all the trained and online algorithms with us,
        # find averages for them, and generate results
        
        # All the matrices will have the following dimensions:
        # 1. Users
        # 2. Time Steps
        # 3. Iterations -> new dimension added

        # Earlier, the plots were plotted iterating over the users
        # Same plots can be plotted after averaging over the 3rd dimension, which is the user's dimension
        self.generate_results()
        gen_plot_rew(self,dir=WORKING_DIR)
        gen_plot_runningAvg(self,dir=WORKING_DIR)

        initial_setup(None, dir = WORKING_DIR)
        gen_online_plots(self, dir = WORKING_DIR)
        clean()

if __name__ == '__main__':
    runner = Coalate_Results()
    runner.coalate()