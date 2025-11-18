# Shooter Game

Shooter Game is an **arcade-style game** built using **Python** and **Pygame**.  
In this game, players control a shooter at the bottom of the screen, aiming to hit targets that appear at the top.  

The game features **increasing difficulty levels** and **bullet management**.

---

## Requirements

To run this game, you need to have **Python** installed on your system along with the **Pygame** library.  

You can install Pygame via `pip`:

```bash
pip install pygame
```

---

## How to Run

1. Clone the repository or download the game files to your local machine.  
2. Ensure you have the required Python version and Pygame installed.  
3. Run the game using Python:

```bash
python shooter_game.py
```

---

## Controls

- **Arrow Keys**: Move the shooter left and right  
- **Spacebar**: Shoot bullets  
- **Q Key**: Quit the game  
- **Mouse Click**: Click the play button to start or pause the game  

---

## Customization

Game settings can be adjusted in the `settings.py` file.

---

## AI Player (Deep Q-Learning)

A modified version of the game allows an AI to play using **Deep Q-learning**.  

### Requirements

Make sure **TensorFlow** is installed beforehand.

#### Installing TensorFlow in PyCharm

1. Download the TensorFlow library from the [official website](https://www.tensorflow.org/).  
2. Extract the folder and copy it to your PyCharm project directory.  
3. In PyCharm, go to `File -> Settings -> Project Interpreter`.  
4. Click on the **+** sign, search for `tensorflow`.  
5. Select the latest version and click **Install Package**.

### Running the AI

- Open and run `AI.py` in the `AI_Training` folder to **train the AI**.  
- Open and run `AI_Shoot.py` in the `AI_Testing` folder to **use the AI player mode**.
