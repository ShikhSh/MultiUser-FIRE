common_TRIALS = 15
common_TRIAL_LEN = 4000#50000#500

LOCATION_BASED_FAILURE_ENABLED = True#True

common_NUM_ACCESS_POINTS = 9
common_NUM_USERS = 13#12#20

# Run the algorithm multiple times to take an avg for the reward values and graphs
common_TOT_RUNS = 1#2

# ONLINE:
common_USERS_TO_CARE_ABOUT = common_NUM_USERS

common_NEGATIVE_REWARD = -8000
common_FAILED_AP_SERV_LOC_REW = -200

common_AP_CAPACITY = 25
common_COMPUTATIONAL_DELAY_SCALING_FACTOR = 20

common_RUNNING_ON_COLAB = False
common_DIAG_DIRECTORY = "./diags/"

# A list for all the APs which recover after 5 APs
common_WEAK_AP_LIST = {1,4,7}