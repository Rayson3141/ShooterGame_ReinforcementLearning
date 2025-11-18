# Dependencies for HI
import random
import numpy as np
from shooter_game import ShooterGame

'''Define Agent'''

state_size = 2
action_size = 3
action_space = [0, 1, 2]


class HIAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.action_space = action_space
        self.epsilon = 0.4  # exploration rate: how much to act randomly; more initially than later due to epsilon decay

    def act(self, state, vertical, speed):
        target_x = state[0]
        shooter_x = state[1]
        shoot_check = abs(target_x + speed * (vertical / (2.5 * abs(speed))) - shooter_x)
        if np.random.rand() <= self.epsilon:  # if acting randomly, take random action
            return random.choice(self.action_space)
        # elif (target_x+speed*(vertical/2.5*speed)-shooter_x):
        elif shoot_check < 10:
            return 0
        elif target_x > shooter_x:
            return 1
        else:
            return 2


'''Choose weights for AI'''
agent = HIAgent(state_size, action_size)  # initialise agent

'''Play'''
if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = ShooterGame(agent)
    ai.run()
