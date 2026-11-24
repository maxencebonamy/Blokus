# Blokus

A two-player Blokus game in Python, with reinforcement learning agents.

The repository holds two versions of a school project. `full-blokus` is the first one: a pygame implementation on a 14x14 board with piece rotation. `simple-blokus` is a later rewrite with a reduced piece set, a configurable board size, a terminal mode and PPO agents trained against a random opponent.

## Table of contents

- [Blokus](#blokus)
	- [Table of contents](#table-of-contents)
	- [How it works](#how-it-works)
	- [Tech stack](#tech-stack)
	- [Repository structure](#repository-structure)
	- [Prerequisites](#prerequisites)
	- [Installation](#installation)
	- [Running locally](#running-locally)
	- [Useful scripts](#useful-scripts)
	- [Tests and quality](#tests-and-quality)
	- [License](#license)

## How it works

1. **Game**: two players, orange and purple, take turns placing pieces on a square board.
2. **Full version**: pieces are drawn in a side panel for each player. A left click places the selected piece, the left and right arrow keys rotate it.
3. **Simple version**: the board size and the set of pieces are chosen in `simple-blokus/src/__main__.py`. Six presets are defined, from a 4x4 board with 3 pieces to a 14x14 board with 21 pieces. Moves are given by piece index and coordinates.
4. **Environment**: both versions expose the game as a Gymnasium environment. An action is a piece index and a position. The simple version rewards the size of the placed piece, penalizes invalid moves (-10) and rewards a win (+5) or a loss (-5) at the end.
5. **Training**: agents are trained with Stable-Baselines3. The simple version trains PPO against a random opponent and saves the model as `<algorithm>_blokus_<board size>.zip`.
6. **Play against the AI**: in the simple version, a trained model plays the second player in the graphical window.

## Tech stack

| Layer | Technologies |
| --- | --- |
| Language | Python 3.9 |
| Game and UI | pygame |
| Reinforcement learning | Gymnasium, Stable-Baselines3 (PPO, A2C), PyTorch |
| Tooling | VS Code settings (Pylance, autopep8) |

## Repository structure

```
.
├── full-blokus/                First version, pygame game on a 14x14 board
│   └── src/
│       ├── game/               Board, pieces, players, panels and main loop
│       ├── simulation/         Gymnasium environment (Blocus-v0)
│       ├── utils/              Colors and fonts
│       ├── tests/              Gymnasium grid world experiments
│       ├── custom_cnn.py       Custom feature extractor for Stable-Baselines3
│       ├── main.py             Launches the game
│       └── train_*.py          Training scripts (model, robots, agents)
├── simple-blokus/              Second version, simplified rules and training
│   ├── src/
│   │   ├── game/               Board, pieces, players and game logic
│   │   ├── graphics/           pygame views
│   │   ├── terminal/           Terminal mode
│   │   ├── simulation/         Gymnasium environment and training opponent
│   │   └── __main__.py         Mode menu, board presets, training and play
│   ├── *.zip                   Trained PPO and A2C models
│   └── setup.sh                Creates a virtual environment and installs dependencies
├── LICENSE
└── README.md
```

Each version is run from its own folder and has its own `requirements.txt`. Both keep the original Git history of their former repositories: `full-blokus` was `Blokus`, `simple-blokus` was `Simple-Blokus`.

## Prerequisites

- [Python](https://www.python.org/) 3.9
- A display, for the pygame window

## Installation

```bash
git clone git@github.com:maxencebonamy/Blokus.git
cd Blokus
```

Full version:

```bash
cd full-blokus
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Simple version:

```bash
cd simple-blokus
./setup.sh
```

## Running locally

Full version, from `full-blokus/src`:

```bash
python main.py
```

Simple version, from `simple-blokus`:

```bash
source .venv/bin/activate
python src
```

The simple version asks for a mode:

1. Terminal
2. Graphical window
3. Training, stopped by typing `q` in the terminal
4. Play against a trained model

The board size is set by `current_board_size` in `simple-blokus/src/__main__.py` (default `14`). Mode 4 loads the model named after it, for example `ppo_blokus_14.zip`.

## Useful scripts

| Command | Effect |
| --- | --- |
| `python main.py` (in `full-blokus/src`) | Start the full game |
| `python train_model.py` (in `full-blokus/src`) | Train a PPO model on `Blocus-v0` |
| `python train_robots.py` (in `full-blokus/src`) | Train two PPO models, `ppo_robot1` and `ppo_robot2` |
| `python train_agents.py` (in `full-blokus/src`) | Train two PPO models with `CustomCNN`, `ppo_agent1` and `ppo_agent2` |
| `python play_robots.py` (in `full-blokus/src`) | Make the two `ppo_robot*` models play each other |
| `python play_agents.py` (in `full-blokus/src`) | Make the two `ppo_agent*` models play each other |
| `python src` (in `simple-blokus`) | Open the mode menu of the simple version |

## Tests and quality

There is no automated test suite. `full-blokus/src/tests` holds Gymnasium grid world experiments, and `python run_simulation.py` in `full-blokus/src` runs random actions in the environment. The simple version checks its environment with Stable-Baselines3 `check_env` before training.

## License

This project is licensed under the [MIT License](LICENSE).
