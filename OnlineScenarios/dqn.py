import sys
sys.path.append('../Common')

from common_config import *
from online_const import *
from common_utils import *
from plots import *
class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(input_dim, 24),
            nn.ReLU(),
            nn.Linear(24, 48),
            nn.ReLU(),
            nn.Linear(48, 24),
            nn.ReLU(),
            nn.Linear(24, output_dim)
        )

    # Called with either one element to determine next action, or a batch
    # during optimization. Returns tensor([[left0exp,right0exp]...]).
    def forward(self, x):
        x = x.to(device)
        return self.linear_relu_stack(x)

class DQN_wrapper:
    def __init__(self, input_dim, output_dim):
         # lu, ls, anomaly/not, backup_loc
        self.input_dim = input_dim
        self.output_dim = output_dim
    
    def get_q_value(self, state, users = common_NUM_USERS):
        with torch.no_grad():
            Q_estimates = self.policy_net(state)
            Q_estimates = reshape_nn_outputs(Q_estimates, users)
            return Q_estimates
    
    def load_model(self, PATH):
        self.policy_net = DQN(self.input_dim, self.output_dim).to(device)
        self.policy_net.load_state_dict(torch.load(PATH))
        self.policy_net.eval()