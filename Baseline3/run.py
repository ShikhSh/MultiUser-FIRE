from main import *
from plots import *
from online_main import *

if __name__ == '__main__':
    print("RUNNING BL2: please check logs file for more")
    initial_setup()
    obj = BL3_RLalgo()
    obj.run_algo()
    # obj.gen_plot()
    gen_plot_rew(obj)
    gen_plot_runningAvg(obj)

    online_obj_curr = BL3_Online_Algo(users_to_care_about = USERS_TO_CARE_ABOUT)
    online_obj_curr.run(obj)
    gen_online_plots(online_obj_curr)
    clean()