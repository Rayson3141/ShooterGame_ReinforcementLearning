# Dependencies for AI
import random
import numpy as np
import tensorflow as tf
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from shooter_game import ShooterGame

'''Increase speed fot simulation'''
tf.compat.v1.disable_eager_execution()

'''Define Agent'''

state_size = 2
action_size = 3
action_space = [0, 1, 2]


class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.action_space = action_space
        self.memory = deque(
            maxlen=2000)  # double-ended queue; acts like list, but elements can be added/removed from either end
        self.epsilon = 0.4  # exploration rate: how much to act randomly; more initially than later due to epsilon decay
        self.epsilon_decay = 1.0  # decrease number of random explorations as the agent's performance (hopefully)
        # improves over time
        self.epsilon_min = 0.01  # minimum amount of random exploration permitted
        self.learning_rate = 0.001  # rate at which NN adjusts models parameters via SGD to reduce cost
        self.model = self._build_model()  # private method

    def _build_model(self):
        # neural net to approximate Q-value function:
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))  # 1st hidden layer; states as input
        model.add(Dense(24, activation='relu'))  # 2nd hidden layer
        model.add(Dense(self.action_size, activation='linear'))  # 2 actions, so 2 output neurons: 0 and 1 (L/R)
        model.compile(loss='mse',
                      optimizer=Adam(learning_rate=self.learning_rate))
        return model
    def act(self, state):
        if np.random.rand() <= self.epsilon:  # if acting randomly, take random action
            return random.choice(self.action_space)
        act_values = self.model.predict(state,
                                        verbose=0)  # if not acting randomly, predict reward value based on current
        # state
        return np.argmax(act_values[0])  # pick the action that will give the highest reward (i.e., go left or right?)
    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)


'''Choose weights for AI'''
agent = DQNAgent(state_size, action_size)  # initialise agent
agent.load("./model_output/trial_18/weights_0120.hdf5")

'''Play'''
if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = ShooterGame(agent)
    ai.run()
