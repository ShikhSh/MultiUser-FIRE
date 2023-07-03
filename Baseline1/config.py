import sys
 
# setting path
sys.path.append('../Common')
from common_utils import *

TRIALS = common_TRIALS
TRIAL_LEN = common_TRIAL_LEN#4000#50000#500

NUM_ACCESS_POINTS = common_NUM_ACCESS_POINTS#9
NUM_USERS = common_NUM_USERS#15#20

# Run the algorithm multiple times to take an avg for the reward values and graphs
TOT_RUNS = common_TOT_RUNS#5

START_AFRESH = False

# ONLINE:
USERS_TO_CARE_ABOUT = common_USERS_TO_CARE_ABOUT#NUM_USERS

NEGATIVE_REWARD = common_NEGATIVE_REWARD#-1500

AP_CAPACITY = common_AP_CAPACITY#25
COMPUTATIONAL_DELAY_SCALING_FACTOR = common_COMPUTATIONAL_DELAY_SCALING_FACTOR#20

RUNNING_ON_COLAB = common_RUNNING_ON_COLAB#False
DIAG_DIRECTORY = common_DIAG_DIRECTORY#"./diags/"