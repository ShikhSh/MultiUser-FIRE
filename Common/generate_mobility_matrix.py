from common_config import *
from imports import *

def generate_user_mobility_patterns(num_aps = common_NUM_ACCESS_POINTS):
    user_mobility_pattern = np.random.rand(num_aps,num_aps)
    user_mobility_pattern = user_mobility_pattern/user_mobility_pattern.sum(axis=1,keepdims = True)
    with open('user_mobolity_pattern.npy', 'wb') as f:
        np.save(f, user_mobility_pattern)

if __name__ == "__main__":
    generate_user_mobility_patterns()