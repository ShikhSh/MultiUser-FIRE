from config import *

# changing the font size:
# plt.rcParams.update({'font.size': 15})
# Constants used:
INPUT_SHAPE = 4*NUM_USERS # adds the user number
BATCH_SIZE = 128#128#32#
TARGET_UPDATE = 10
# DIAG_DIRECTORY = "torch_diags_10APs/"
# used for cost and migration dictionaries
# LATENCY_MATRIX = None
# if NUM_ACCESS_POINTS == 3:
#     LATENCY_MATRIX = [[2.55316, 9.70525, 7.02418],
#                       [9.70525, 2.55389, 6.25835],
#                       [7.02418, 6.26684, 2.55398]]

# if NUM_ACCESS_POINTS == 9:
#     LATENCY_MATRIX = [[2.55316, 9.70525, 7.02418, 2.50611, 8.97695, 4.81203, 6.93397, 6.21317, 7.60077],
#                       [9.70525, 2.55389, 6.25835, 11.8198, 7.18656, 3.92144, 6.99266, 6.2124, 6.71018],
#                       [7.02418, 6.26684, 2.55398, 4.02147, 3.27882, 2.77404, 4.02353, 5.07656, 2.77417],
#                       [2.50611, 11.8198, 4.02147, 2.55354, 9.28922, 7.44114, 9.19819, 4.21866, 11.8622],
#                       [8.97695, 7.18656, 3.27882, 9.28922, 2.55301, 3.26512, 2.0394, 5.5403, 5.58373],
#                       [4.75385, 3.92267, 2.77457, 7.44114, 3.26512, 2.55366, 1.58549, 3.0197, 2.78874],
#                       [6.91204, 7.6288, 4.2441, 9.19819, 2.0394, 1.58474, 2.55359, 3.95576, 4.37348],
#                       [6.21317, 6.2124, 5.31069, 4.21866, 6.59593, 3.06604, 3.95576, 2.55396, 5.85478],
#                       [7.60077, 6.71018, 2.77417, 11.8622, 5.55827, 2.78874, 4.37348, 5.85478, 2.55313]]
# MIGR_COST = np.zeros((NUM_ACCESS_POINTS, NUM_ACCESS_POINTS))
# STORAGE_COST_temp = np.zeros((NUM_ACCESS_POINTS))
# for p in range(NUM_ACCESS_POINTS):
#   diff = random.uniform(-0.5, 0.5)
#   STORAGE_COST_temp[p] = 5+diff
#   for q in range(NUM_ACCESS_POINTS):
#     diff = random.uniform(-0.5, 0.5)
#     MIGR_COST[p][q] = LATENCY_MATRIX[p][q]+diff

# COST_DICT = MIGR_COST#np.random.rand(NUM_ACCESS_POINTS,NUM_ACCESS_POINTS)
# STORAGE_COST = STORAGE_COST_temp#np.random.rand(NUM_ACCESS_POINTS)

# ACTUAL_EPS = 0.01#0.15#
# GAMMA = 0.9#0.85
# #EPSILON = 1.0
# #EPSILON_MIN = 0.01
# EPSILON_DECAY = 0.9#0.995 #Exploration vs exploitation
# EPSILON_THRESHOLD = 30000

# LEARNING_RATE = 0.1 # learning rate
# TAU = 0.125
# NO_BACKUP = 100
# # BACKUP_ACTION=101
# USER_ACC_FACTOR=1.5
# K_ = 20
# PR_LU_TRANS = None
# if NUM_ACCESS_POINTS == 3:
#     PR_LU_TRANS = np.array([
#         [0.35,0.32,0.33],
#         [0.28,0.38,0.34],
#         [0.32,0.29,0.39]])

# if NUM_ACCESS_POINTS == 9:
#     PR_LU_TRANS = np.array([
#         [0.15,0.05,0.1,0.1,0.08,0.12,0.09,0.11,0.2],
#         [0.1,0.08,0.12,0.09,0.11,0.03,0.17,0.15,0.15],
#         [0.15,0.11,0.03,0.17,0.05,0.1,0.1,0.08,0.21],
#         [0.15,0.05,0.1,0.1,0.11,0.03,0.17,0.08,0.21],
#         [0.15,0.05,0.1,0.1,0.08,0.12,0.17,0.09,0.14],
#         [0.12,0.09,0.15,0.05,0.1,0.1,0.08,0.11,0.2],
#         [0.05,0.1,0.1,0.08,0.12,0.15,0.09,0.11,0.2],
#         [0.09,0.11,0.03,0.15,0.05,0.1,0.1,0.08,0.29],
#         [0.08,0.15,0.05,0.1,0.1,0.12,0.09,0.11,0.2]])
# DELTA = 0.005 # lower bound for estimate epsilon
# # # learning rate
# # LAMBDA = 0.7 # eligibility decay rate
# # # exploration rate
# # EPS=0.03#0.9

# ALPHA = 0.05#0.005
# #ALPHA_T = 0.05
# #ALPHA_U = 0.05

# #EXPLORATION_FIXED_RATE = 3000

# Calculated:
# states = <Lu,Ls,0/1,backup_loc>
NUM_STATES_PER_USER = (NUM_ACCESS_POINTS*NUM_ACCESS_POINTS*2*(NUM_ACCESS_POINTS+1))
TOT_NUM_STATES = NUM_STATES_PER_USER^NUM_USERS
# actions = <Ls,backup_loc>
NUM_ACTIONS_PER_USER = (NUM_ACCESS_POINTS*(NUM_ACCESS_POINTS+1))
TOT_NUM_ACTIONS = NUM_ACTIONS_PER_USER*NUM_USERS

INITIAL_STATE = []
for i in range(NUM_USERS):
    INITIAL_STATE.append(0)
INITIAL_ACTION = []
for i in range(NUM_USERS):
    INITIAL_ACTION.append(random.randint(0,NUM_ACTIONS_PER_USER-1))

AP_CAPACITIES = np.ones((NUM_ACCESS_POINTS))*AP_CAPACITY
AP_USER_LOADS = np.zeros((NUM_ACCESS_POINTS))
USER_LOADS = np.ones((NUM_USERS))