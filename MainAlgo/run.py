from main import *
from plots import *
from online_main import *

class Runner_main:

    def __init__(self):
        self.start_afresh = START_AFRESH

    def run_1_iteration(self, run_no):
        print("RUNNING MAIN ALGO: please check logs file for more")
        
        initial_setup(run_no)
        sub_dir = gen_working_sub_dir(run_no)

        trainer = RLalgo()
        trainer.run_algo()
        gen_plot_rew(trainer, sub_dir)
        gen_plot_runningAvg(trainer, sub_dir)
        
        trainer_model = TrainerModel(trainer.Rewards, trainer.runningAvg)
        save_object( sub_dir + "trainer_obj.pkl", trainer_model)


        online_obj = Online_Algo(users_to_care_about = USERS_TO_CARE_ABOUT)
        online_obj.run(trainer)
        gen_online_plots(online_obj, sub_dir)
        save_object( sub_dir + "online_obj.pkl", online_obj)
        
        clean()

        # self.trainer_objects.append(trainer)
        # self.online_objects.append(online_obj)

        # self.Rewards.append(trainer.Rewards)
        # self.runningAvg.append(trainer.runningAvg)
        # self.Reward_online.append(online_obj.Reward_online)
        # self.runningAvg_online.append(online_obj.runningAvg_online)
        # self.NSreward_online.append(online_obj.NSreward_online)
        # self.REreward_online.append(online_obj.REreward_online)

        # self.mean_Reward_online.append(online_obj.mean_Reward_online)
        # self.mean_REreward_online.append(online_obj.mean_REreward_online)
        # self.mean_REmigration_online.append(online_obj.mean_REmigration_online)
        # self.mean_REdelay_online.append(online_obj.mean_REdelay_online)
        # self.mean_REstorage_online.append(online_obj.mean_REstorage_online)
        # self.mean_REcompDelay_online.append(online_obj.mean_REcompDelay_online)
        # self.mean_NSreward_online.append(online_obj.mean_NSreward_online)
        # self.mean_NSmigration_online.append(online_obj.mean_NSmigration_online)
        # self.mean_NSdelay_online.append(online_obj.mean_NSdelay_online)
        # self.mean_NSstorage_online.append(online_obj.mean_NSstorage_online)
        # self.mean_NScompDelay_online.append(online_obj.mean_NScompDelay_online)
    
    # def stack_n_mean(self, var, axis = 2):
    #     return np.mean(np.dstack(var),axis = axis)
    
    # def generate_results(self):
    #     assert False
    #     self.Rewards = self.stack_n_mean(self.Rewards)
    #     self.runningAvg = self.stack_n_mean(self.runningAvg)
    #     self.Reward_online = self.stack_n_mean(self.Reward_online)
    #     self.runningAvg_online = self.stack_n_mean(self.runningAvg_online)
    #     self.NSreward_online = self.stack_n_mean(self.NSreward_online)
    #     self.REreward_online = self.stack_n_mean(self.REreward_online)

    #     self.mean_Reward_online = mean(self.mean_Reward_online)
    #     self.mean_REreward_online = mean(self.mean_REreward_online)
    #     self.mean_REmigration_online = mean(self.mean_REmigration_online)
    #     self.mean_REdelay_online = mean(self.mean_REdelay_online)
    #     self.mean_REstorage_online = mean(self.mean_REstorage_online)
    #     self.mean_REcompDelay_online = mean(self.mean_REcompDelay_online)
    #     self.mean_NSreward_online = mean(self.mean_NSreward_online)
    #     self.mean_NSmigration_online = mean(self.mean_NSmigration_online)
    #     self.mean_NSdelay_online = mean(self.mean_NSdelay_online)
    #     self.mean_NSstorage_online = mean(self.mean_NSstorage_online)
    #     self.mean_NScompDelay_online = mean(self.mean_NScompDelay_online)
        
    def run_program(self):
        starting_dir = 0
        if not self.start_afresh and len(os.listdir(WORKING_DIR)):
            starting_dir = int(max(os.listdir(WORKING_DIR))) + 1
        
        for i in range(TOT_RUNS):
            self.run_1_iteration( run_no= i + starting_dir)
        # now we have all the trained and online algorithms with us,
        # find averages for them, and generate results

if __name__ == '__main__':
    runner = Runner_main()
    runner.run_program()