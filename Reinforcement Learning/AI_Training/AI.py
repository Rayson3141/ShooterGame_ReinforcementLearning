'''
Reference
https://github.com/the-deep-learners/TensorFlow-LiveLessons/
blob/master/notebooks/cartpole_dqn.ipynb
'''
import random
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from alien_invasion_AI_Train import AlienInvasion
import os  # for creating directories

'''Create Environment'''


class gym:
    def __init__(self):
        self.state = self.reset()
        self.action_size = 3
        self.observation_size = 2
        self.action_space = [0, 1, 2]
        self.alien_invasion = AlienInvasion(self.state)

    def reset(self):
        state = np.array([
            random.randrange(450, 550),  # Horizontal position of alien
            random.randrange(550, 750 - 70),  # Vertical position of alien
            7,  # random.randrange(-50, 50), # Speed of alien/ Speed of Ship
            500
            #             random.randrange(60, 1200-60), # Horizontal position of ship
        ])
        return state

    def step(self, action):
        next_state, reward, done = self.alien_invasion.run_game(action)
        return next_state, reward, done, self.alien_invasion.win


'''Variable for defining model'''
state_size = gym().observation_size
action_size = gym().action_size
action_space = gym().action_space
batch_size = 32
n_episodes = 500  # n games we want agent to play (default 1001)
output_dir = 'model_output/trial_11/'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

'''Define agent'''


class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.action_space = action_space
        self.memory = deque(
            maxlen=2000)  # double-ended queue; acts like list, but elements can be added/removed from either end
        self.gamma = 0.95  # decay or discount rate: enables agent to take into account future actions in addition to the immediate ones, but discounted at this rate
        self.epsilon = 1.0  # exploration rate: how much to act randomly; more initially than later due to epsilon decay
        self.epsilon_decay = 0.995  # decrease number of random explorations as the agent's performance (hopefully) improves over time
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
                      optimizer=Adam(learning_rate=self.learning_rate), metrics=['accuracy'])
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append(
            (state, action, reward, next_state, done))  # list of previous experiences, enabling re-training later

    def act(self, state):
        if np.random.rand() <= self.epsilon:  # if acting randomly, take random action
            return random.choice(self.action_space)
        act_values = self.model.predict(state,
                                        verbose=0)  # if not acting randomly, predict reward value based on current
        # state
        return np.argmax(act_values[0])  # pick the action that will give the highest reward

    def replay(self, batch_size):  # method that trains NN with experiences sampled from memory
        minibatch = random.sample(self.memory, batch_size)  # sample a minibatch from memory
        for state, action, reward, next_state, done in minibatch:  # extract data for each minibatch sample
            target = reward  # if done (boolean whether game ended or not, i.e., whether final state or not),
            # then target = reward
            if not done:  # if not done, then predict future discounted reward
                target = (reward + self.gamma *  # (target) = reward + (discount rate gamma) *
                          np.amax(self.model.predict(next_state, verbose=0)[
                                      0]))  # (maximum target Q based on future action a')
            target_f = self.model.predict(state,
                                          verbose=0)  # approximately map current state to future discounted reward
            target_f[0][action] = target
            self.model.fit(state, target_f,epochs=1)  # single epoch of training with x=state, y=target_f; fit decreases loss btwn
            # target_f and y_hat
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def reset_cumulative_reward(self):
        self.cumulative_reward = 0

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)


'''Initialize the agent'''
agent = DQNAgent(state_size, action_size)  # initialise agent

'''Begin Training'''
done = False
for e in range(n_episodes):  # iterate over new episodes of the game
    env = gym()  # initialize enviroment
    state = env.state  # reset state at start of each new episode of the game
    state = np.delete(state, 1)
    state = np.delete(state, 1)
    agent.reset_cumulative_reward()
    state = np.reshape(state, [1, state_size])

    alien_x = state[0][0]
    n = 400

    for time in range(n):  # time represents a frame of the game
        delta_bfr = abs(state[0][1] - alien_x)
        action = agent.act(state)  # action is either 0 or 1 (move cart left or right); decide on one or other here
        next_state, reward, done, win = env.step(
            action)  # agent interacts with env, gets feedback; 4 state data points, e.g., pole angle, cart position
        delta_aftr = abs(next_state[1] - alien_x)

        if delta_aftr < delta_bfr:
            reward += 1000 * np.float_power(delta_aftr / 60 + 1, -1)

        next_state = np.reshape(next_state, [1, state_size])
        agent.remember(state, action, reward, next_state,
                       done)  # remember the previous timestep's state, actions, reward, etc.
        state = next_state  # set "current state" for upcoming iteration to the current next state
        if done or time == n - 1:  # episode ends if agent drops pole or we reach timestep 5000
            print("episode: {}/{}, kill_time: {}, e: {:.2}"  # print the episode's score and agent's epsilon
                  .format(e, n_episodes, time, agent.epsilon))
            break  # exit loop
    if len(agent.memory) > batch_size:
        agent.replay(batch_size)  # train the agent by replaying the experiences of the episode
    if e % 20 == 0:
        agent.save(output_dir + "weights_" + '{:04d}'.format(e) + ".hdf5")
