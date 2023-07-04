from main import *
from plots import *
from online_main import *

class Runner_BL3:

    def __init__(self):
        self.start_afresh = START_AFRESH

    def run_1_iteration(self, run_no):
        print("RUNNING BL3: please check logs file for more")
        
        initial_setup(run_no)
        sub_dir = gen_working_sub_dir(run_no)

        trainer = BL3_RLalgo()
        trainer.run_algo()
        gen_plot_rew(trainer, sub_dir)
        gen_plot_runningAvg(trainer, sub_dir)

        trainer_model = TrainerModel(trainer.Rewards, trainer.runningAvg)
        save_object( sub_dir + "trainer_obj.pkl", trainer_model)

        online_obj = BL3_Online_Algo(users_to_care_about = USERS_TO_CARE_ABOUT)
        online_obj.run(trainer)
        gen_online_plots(online_obj, sub_dir)

        online_model = OnlineModel(online_obj)
        save_object( sub_dir + "online_obj.pkl", online_model)
        
        clean()

    def run_program(self):
        WORKING_DIR = create_dir()
        starting_dir = 0
        if not self.start_afresh and len(os.listdir(WORKING_DIR)):
            starting_dir = int(max(os.listdir(WORKING_DIR))) + 1
        
        for i in range(TOT_RUNS):
            self.run_1_iteration( run_no= i + starting_dir)

if __name__ == '__main__':
    runner = Runner_BL3()
    runner.run_program()