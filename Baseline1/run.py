from main import *
from plots import *
from online_main import *

class Runner_BL1:

    def __init__(self):
        self.start_afresh = START_AFRESH

    def run_1_iteration(self, run_no):
        print("RUNNING BL1: please check logs file for more")
        
        initial_setup(run_no)
        sub_dir = gen_working_sub_dir(run_no)

        # CHANGE:
        trainer = BL1_RLalgo()
        trainer.run_algo()
        gen_plot_rew(trainer, sub_dir)
        gen_plot_runningAvg(trainer, sub_dir)

        trainer_model = TrainerModel(trainer.Rewards, trainer.runningAvg)
        save_object( sub_dir + "trainer_obj.pkl", trainer_model)

        # CHANGE:
        online_obj = BL1_Online_Algo(users_to_care_about = USERS_TO_CARE_ABOUT)
        online_obj.run(trainer)
        gen_online_plots(online_obj, sub_dir)
        save_object( sub_dir + "online_obj.pkl", online_obj)

        clean()
  
    def run_program(self):
        starting_dir = 0
        if not self.start_afresh and len(os.listdir(WORKING_DIR)):
            starting_dir = int(max(os.listdir(WORKING_DIR))) + 1

        for i in range(TOT_RUNS):
            self.run_1_iteration(i+ starting_dir)
        # now we have all the trained and online algorithms with us,
        # find averages for them, and generate results

if __name__ == '__main__':
    # print("RUNNING BL1: please check logs file for more")
    # initial_setup()
    # obj = BL1_RLalgo()
    # obj.run_algo()
    # # obj.gen_plot()
    # gen_plot_rew(obj)
    # gen_plot_runningAvg(obj)

    # online_obj_curr = BL1_Online_Algo(users_to_care_about = USERS_TO_CARE_ABOUT)
    # online_obj_curr.run(obj)
    # gen_online_plots(online_obj_curr)
    # clean()

    runner = Runner_BL1()
    runner.run_program()