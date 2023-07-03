import pickle
import os
import sys

sys.path.append('../../../../../../../MainAlgo')
sys.path.append('../../../../../../../Common')

class TrainerModel:
    def __init__(self, Rewards, runningAvg) -> None:
        self.Rewards = Rewards
        self.runningAvg = runningAvg

def save_object(file_name, obj):
    with open(file_name, 'wb') as file:
        pickle.dump(obj, file)

def load_object(file_name):
    obj = None
    with open(file_name, 'rb') as file:
        obj = pickle.load(file)
    return obj

trainer = load_object("trainer_obj.pkl")
trainer_new = TrainerModel(trainer.Rewards, trainer.runningAvg)
        
save_object("trainer_obj_new.pkl", trainer_new)

os.remove("trainer_obj.pkl")
os.rename('trainer_obj_new.pkl', 'trainer_obj.pkl')