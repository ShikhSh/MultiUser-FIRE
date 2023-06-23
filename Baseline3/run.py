from main import *
from plots import *
from online_main import *

class Runner_BL3:

    def __init__(self):
        self.numUsers = NUM_USERS
        self.trainer_objects = []
        self.online_objects = []

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

    def run_1_iteration(self, run_no):
        print("RUNNING BL3: please check logs file for more")
        initial_setup(run_no)

        # CHANGE:
        trainer = BL3_RLalgo()
        
        trainer.run_algo()
        gen_plot_rew(trainer, gen_working_sub_dir(run_no))
        gen_plot_runningAvg(trainer, gen_working_sub_dir(run_no))

        # CHANGE:
        online_obj = BL3_Online_Algo(users_to_care_about = USERS_TO_CARE_ABOUT)

        online_obj.run(trainer)
        gen_online_plots(online_obj, gen_working_sub_dir(run_no))
        clean()

        self.trainer_objects.append(trainer)
        self.online_objects.append(online_obj)

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
        
    def run_program(self):
        for i in range(TOT_RUNS):
            self.run_1_iteration(i)
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
    # print("RUNNING BL2: please check logs file for more")
    # initial_setup()
    # obj = ()
    # obj.run_algo()
    # # obj.gen_plot()
    # gen_plot_rew(obj)
    # gen_plot_runningAvg(obj)

    # online_obj_curr = (users_to_care_about = USERS_TO_CARE_ABOUT)
    # online_obj_curr.run(obj)
    # gen_online_plots(online_obj_curr)
    # clean()
    runner = Runner_BL3()
    runner.run_program()