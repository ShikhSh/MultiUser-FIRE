from common_constants import *

MAIN_ALGO_NAME = "MainAlgo"
BL1_ALGO_NAME = "Baseline1"
BL2_ALGO_NAME = "Baseline2"
BL3_ALGO_NAME = "Baseline3"
BL4_ALGO_NAME = "Baseline4"

ALGO_NAMES = [MAIN_ALGO_NAME, BL1_ALGO_NAME, BL2_ALGO_NAME, BL3_ALGO_NAME, BL4_ALGO_NAME]

class TrainerModel:
    def __init__(self, Rewards, runningAvg) -> None:
        self.Rewards = Rewards
        self.runningAvg = runningAvg

class OnlineModel:
    def __init__(self, online_obj) -> None:
        self.Reward_online = online_obj.Reward_online
        self.runningAvg_online = online_obj.runningAvg_online
        
        self.NSreward_online = online_obj.NSreward_online
        self.REreward_online = online_obj.REreward_online

        self.mean_Reward_online =  online_obj.mean_Reward_online
        self.mean_REreward_online =  online_obj.mean_REreward_online
        self.mean_REmigration_online =  online_obj.mean_REmigration_online
        self.mean_REdelay_online =  online_obj.mean_REdelay_online
        self.mean_REstorage_online =  online_obj.mean_REstorage_online
        self.mean_REcompDelay_online =  online_obj.mean_REcompDelay_online
        self.mean_NSreward_online =  online_obj.mean_NSreward_online
        self.mean_NSmigration_online =  online_obj.mean_NSmigration_online
        self.mean_NSdelay_online =  online_obj.mean_NSdelay_online
        self.mean_NSstorage_online =  online_obj.mean_NSstorage_online
        self.mean_NScompDelay_online =  online_obj.mean_NScompDelay_online

def conv_to_tensor(x):
  return torch.tensor(np.array([[x]]), device=device, dtype = torch.float32)

# Utility function:
def path_creator(dir_path, generate_path = True):
    if not generate_path:
        return
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def create_dir(dir_path = None, generate_path = True):
    if not common_RUNNING_ON_COLAB:
        if not dir_path:
            dir_path = common_DIAG_DIRECTORY
        path_creator(dir_path, generate_path)

        dir_path += "APs_" + str(common_NUM_ACCESS_POINTS) + "/"
        path_creator(dir_path, generate_path)
        
        dir_path += "Users_" + str(common_NUM_USERS) + "/"
        path_creator(dir_path, generate_path)
        
        dir_path += "Rew_" + str(abs(common_NEGATIVE_REWARD)) + "/"
        path_creator(dir_path, generate_path)
        
        dir_path += "Onl_Users_" + str(common_USERS_TO_CARE_ABOUT) + "/"
        path_creator(dir_path, generate_path)

        dir_path += "CompDelay_Scale_" + str(common_COMPUTATIONAL_DELAY_SCALING_FACTOR) + "/"
        path_creator(dir_path, generate_path)

        if LOCATION_BASED_FAILURE_ENABLED:
            dir_path += "LocBasedRes" + str(abs(common_FAILED_AP_SERV_LOC_REW)) + "_DT" + str(common_LOCATION_BASED_FAILURE_TIME) + "/"
        else:
            dir_path += "NoLocBasedFailures" + "/"
        path_creator(dir_path, generate_path)

        if RANDOM_USER_PATTERNS_ENABLED:
            dir_path += "RandPatternsEn/"
        else:
            dir_path += "RandPatternsDis/"
        path_creator(dir_path, generate_path)

    return dir_path

def gen_working_sub_dir(run_no):
    SUB_DIR = create_dir() + str(run_no) + "/"
    path_creator(SUB_DIR)
    return SUB_DIR

def initial_setup(run_no, dir = None):
    if not common_RUNNING_ON_COLAB:
        if dir == None:
            dir = gen_working_sub_dir(run_no)
        file_path = dir + "message.log"
        print(file_path)
        LOG_FILE = open(file_path,"w")
        sys.stdout = LOG_FILE

def clean():
    if not common_RUNNING_ON_COLAB:
        LOG_FILE = sys.stdout
        sys.stdout = sys.__stdout__
        LOG_FILE.close()

def save_object(file_name, obj):
    with open(file_name, 'wb') as file:
        pickle.dump(obj, file)

def load_object(file_name):
    obj = None
    try:
        with open(file_name, 'rb') as file:
                obj = pickle.load(file)
        return obj
    except Exception as e:
        return None
