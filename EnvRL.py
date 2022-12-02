import numpy as np
import gym
from gym.spaces import Discrete, MultiDiscrete
from Action import Actions
from attack1 import dp, ddos, attack3, attack4
import pickle
X_train = pickle.load(open("xtrain", "rb"))
y_train = pickle.load(open("ytrain", "rb"))
X_test = pickle.load(open("xtest", "rb"))
y_test = pickle.load(open("ytest", "rb"))

class EnvRL_v0(gym.Env):

    def __init__(self):
        super().__init__()

        self.current_accuracy = 1
        self.previous_accuracy = 1
        self.action_space = Discrete(4)
        self.observation_space = MultiDiscrete([self.previous_accuracy, self.current_accuracy])




    def take_action(self, action):
        nids_success_rate = 2
        # attack happen

        if action == Actions.Defence1:
            # dp
            # dp(X_train,sa,sd,Defence1)
            self.previous_accuracy = self.current_accuracy
            self.current_accuracy = dp(X_train, 0.8, 0.2, Actions.Defence1)

            # at time T, run the defence for dp and update two accuracies
            # self.previous_accuracy = self.current_accuracy # save the accuracy at time T-1
            # self.current_accuracy = 0  # get the accuracy from cnn at time T
        elif action == Actions.Defence2:
            self.previous_accuracy = self.current_accuracy
            self.current_accuracy = ddos(X_train, 0.8, 0.2, Actions.Defence2)
        elif action == Actions.Defence3:
            self.previous_accuracy = self.current_accuracy
            self.current_accuracy = attack3(X_train, 0.8, 0.2, Actions.Defence3)
        elif action == Actions.Defence4:
            self.previous_accuracy = self.current_accuracy
            self.current_accuracy = attack4(X_train, 0.8, 0.2, Actions.Defence4)

    def step(self, action):

        self.take_action(action)
        state = np.array([self.previous_accuracy, self.current_accuracy])
        done = 1
        reward = self.current_accuracy - self.previous_accuracy
        info = {}

        return state, reward, done, info

    def reset(self):
        self.current_accuracy = 0
        self.previous_accuracy = 0
        return np.array([self.previous_accuracy, self.current_accuracy])

    def render(self, mode='human', action=0, reward=0):
        if mode == 'human':
            print(f"{Actions(action): <4}: ({self.previous_accuracy},{self.current_accuracy}) reward = {reward}")
        else:
            super().render(mode=mode)  # just raise an exception
