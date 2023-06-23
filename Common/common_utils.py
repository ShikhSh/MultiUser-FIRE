from imports import *
from common_config import *

def conv_to_tensor(x):
  return torch.tensor([[x]], device=device, dtype = torch.float32)

# Utility function:
def path_creator(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def create_dir():
    dir_path = None
    if not common_RUNNING_ON_COLAB:
        dir_path = common_DIAG_DIRECTORY
        path_creator(dir_path)

        dir_path += "APs_" + str(common_NUM_ACCESS_POINTS) + "/"
        path_creator(dir_path)
        
        dir_path += "Users_" + str(common_NUM_USERS) + "/"
        path_creator(dir_path)
        
        dir_path += "Rew_" + str(abs(common_NEGATIVE_REWARD)) + "/"
        path_creator(dir_path)
        
        dir_path += "Onl_Users_" + str(common_USERS_TO_CARE_ABOUT) + "/"
        path_creator(dir_path)
    return dir_path
WORKING_DIR = create_dir()

def gen_working_sub_dir(run_no):
    SUB_DIR = WORKING_DIR + str(run_no) + "/"
    path_creator(SUB_DIR)
    return SUB_DIR

def initial_setup(run_no):
    if not common_RUNNING_ON_COLAB:
        file_path = gen_working_sub_dir(run_no) + "message.log"
        print(file_path)
        LOG_FILE = open(file_path,"w")
        sys.stdout = LOG_FILE

def clean():
    if not common_RUNNING_ON_COLAB:
        LOG_FILE = sys.stdout
        sys.stdout = sys.__stdout__
        LOG_FILE.close()