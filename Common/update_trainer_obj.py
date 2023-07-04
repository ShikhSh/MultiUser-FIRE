import pickle
import os
import sys

sys.path.append('../../../../../../Baseline1/')
sys.path.append('../../../../../../Common')

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

def save_object(file_name, obj):
    with open(file_name, 'wb') as file:
        pickle.dump(obj, file)

def load_object(file_name):
    obj = None
    with open(file_name, 'rb') as file:
        obj = pickle.load(file)
    return obj

path = "./"
iteration_dirs = [os.path.join(path,filename) for filename in os.listdir(path) if os.path.isdir(os.path.join(path,filename))]
print(iteration_dirs)
# breakpoint()
for sub_dir in iteration_dirs:
    # open pkl files in these, load the objects, add to class variables
    sub_dir += "/"
    print(sub_dir)
    # breakpoint()
    trainer = load_object(sub_dir + "online_obj.pkl")
    trainer_new = OnlineModel(trainer)
    os.rename(sub_dir + 'online_obj.pkl', sub_dir + 'online_obj_old.pkl')
    save_object(sub_dir+"online_obj.pkl", trainer_new)
    # breakpoint()

# os.remove("trainer_obj.pkl")