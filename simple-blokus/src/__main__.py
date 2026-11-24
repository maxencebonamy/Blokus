import threading
from stable_baselines3 import A2C, PPO
from stable_baselines3.common.callbacks import BaseCallback
from game.piece import Piece
from game.game import Game
from graphics.window import Window
from simulation.train import GameEnvWithOpponent
from terminal.terminal import Terminal
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.monitor import Monitor
import sys
import select


class CustomStopTrainingCallback(BaseCallback):
    def __init__(self, verbose=0):
        super(CustomStopTrainingCallback, self).__init__(verbose)
        self.stop_training = False

    def _on_step(self) -> bool:
        if self.stop_training:
            return False
        return True

    def stop(self):
        self.stop_training = True


def key_listener(callback: CustomStopTrainingCallback):
    print("Press 'q' to stop training.")
    while True:
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            line = sys.stdin.readline().strip()
            if line == 'q':
                callback.stop()
                break


configs = [
    {
        "board_size": 4,
        "pieces": [
            Piece([(0, 0)]),
            Piece([(0, 0), (0, -1)]),
            Piece([(0, 0), (0, 1), (0, -1)]),
        ]
    },
    {
        "board_size": 6,
        "pieces": [
            Piece([(0, 0)]),
            Piece([(0, 0), (0, -1)]),
            Piece([(0, 0), (0, 1), (0, -1)]),
            Piece([(0, 0), (0, -1), (1, 0)]),
        ]
    },
    {
        "board_size": 7,
        "pieces": [
            Piece([(0, 0)]),
            Piece([(0, 0), (0, -1)]),
            Piece([(0, 0), (0, 1), (0, -1)]),
            Piece([(0, 0), (0, -1), (1, 0)]),
            Piece([(0, 0), (0, -1), (0, -2), (0, 1)]),
            Piece([(0, 0), (0, -1), (0, -2), (-1, 0)]),
        ]
    },
    {
        "board_size": 8,
        "pieces": [
            Piece([(0, 0)]),
            Piece([(0, 0), (0, -1)]),
            Piece([(0, 0), (0, 1), (0, -1)]),
            Piece([(0, 0), (0, -1), (1, 0)]),
            Piece([(0, 0), (0, -1), (0, -2), (0, 1)]),
            Piece([(0, 0), (0, -1), (0, -2), (-1, 0)]),
            Piece([(0, 0), (0, -1), (0, 1), (1, 0)]),
        ]
    },
    {
        "board_size": 10,
        "pieces": [
            Piece([(0, 0)]),
            Piece([(0, 0), (0, -1)]),
            Piece([(0, 0), (0, 1), (0, -1)]),
            Piece([(0, 0), (0, -1), (1, 0)]),
            Piece([(0, 0), (0, -1), (0, -2), (0, 1)]),
            Piece([(0, 0), (0, -1), (0, -2), (-1, 0)]),
            Piece([(0, 0), (0, -1), (0, 1), (1, 0)]),
            Piece([(0, 0), (-1, 0), (0, 1), (1, 1)]),
            Piece([(0, 0), (0, -1), (0, -2), (0, 1), (0, 2)]),
            Piece([(0, 0), (-1, -1), (0, -1), (0, -1), (0, -2)]),
        ]
    },
    {
        "board_size": 14,
        "pieces": [
            Piece([(0, 0)]),
            Piece([(0, 0), (0, -1)]),
            Piece([(0, 0), (0, 1), (0, -1)]),
            Piece([(0, 0), (0, -1), (1, 0)]),
            Piece([(0, 0), (0, -1), (0, -2), (0, 1)]),
            Piece([(0, 0), (0, -1), (0, -2), (-1, 0)]),
            Piece([(0, 0), (0, -1), (0, 1), (1, 0)]),
            Piece([(0, 0), (0, 1), (1, 1), (1, 0)]),
            Piece([(0, 0), (-1, 0), (0, 1), (1, 1)]),
            Piece([(0, 0), (0, -1), (0, -2), (0, 1), (0, 2)]),
            Piece([(-1, 1), (0, 1), (0, 0), (0, -1), (0, -2)]),
            Piece([(0, 0), (0, -1), (-1, -1), (0, 1), (-1, 1)]),
            Piece([(0, 0), (-1, 0), (-1, 1), (0, -1), (0, -2)]),
            Piece([(0, 0), (0, -1), (0, 1), (-1, 0), (-1, 1)]),
            Piece([(0, 0), (0, -1), (0, 1), (-1, -1), (1, 1)]),
            Piece([(0, 0), (0, -1), (0, 1), (0, 2), (1, 0)]),
            Piece([(0, 0), (0, -1), (0, -2), (-1, 0), (1, 0)]),
            Piece([(0, 0), (0, -1), (0, -2), (1, 0), (2, 0)]),
            Piece([(0, 0), (0, -1), (-1, -1), (1, 0), (1, 1)]),
            Piece([(0, 0), (0, 1), (-1, -1), (-1, 0), (1, 0)]),
            Piece([(0, 0), (0, -1), (0, 1), (-1, 0), (1, 0)])
        ]
    }
]

current_board_size = 14
current_config = configs.index([config for config in configs if config["board_size"] == current_board_size][0])
current_simulation = "ppo"  # ppo, a2c
board_size, pieces = current_board_size, configs[current_config]["pieces"]


def terminal():
    game = Game(board_size, pieces)
    terminal = Terminal(game)
    terminal.run()


def graphics():
    game = Game(board_size, pieces)
    window = Window(game, 1000, 600, "Blokus")
    window.run()


# TODO: idée: voir si on peut update les actions possible à chaque step pour mettre que les actions qui fonctionnent
# TODO: Mettre des meilleurs rewards


def train():
    env = Monitor(GameEnvWithOpponent(board_size, pieces))
    check_env(env, warn=True)

    policy_kwargs = dict(
        net_arch=[dict(pi=[256, 128], vf=[256, 128])]  # Réseau dense pour la policy et value function
    )

    model = PPO(
        "MultiInputPolicy",  # Politique adaptée aux observations sous forme de dictionnaire
        env,
        verbose=1,
        learning_rate=0.0001,
        gamma=0.99,
        n_steps=2048,  # Plus grande pour des environnements complexes
        batch_size=64,
        policy_kwargs=policy_kwargs,  # Ajout des couches personnalisées
        clip_range=0.2,
        ent_coef=0.01,  # Exploration plus efficace
        vf_coef=0.5,
        seed=42
    )

    callback = CustomStopTrainingCallback()
    listener_thread = threading.Thread(target=key_listener, args=(callback,))
    listener_thread.daemon = True
    listener_thread.start()

    model.learn(total_timesteps=int(20_000_000), callback=callback)
    model.save(f"{current_simulation}_blokus_{board_size}.zip")
    callback.stop()


def play():
    game = Game(board_size, pieces)
    window = Window(game, 1000, 600, "Blokus")
    model = A2C.load(f"{current_simulation}_blokus_{board_size}.zip")

    while window.is_running():
        if game.get_current_player().get_id() == 2:
            action, _ = model.predict(game.get_state(), deterministic=False)
            print(action)
            game.play(*action)
        window.update()


if __name__ == "__main__":
    choice = input("Choose mode (1=terminal, 2=graphics, 3=train, 4=play): ")
    if choice == "1":
        terminal()
    elif choice == "2":
        graphics()
    elif choice == "3":
        train()
    elif choice == "4":
        play()
    else:
        print("Invalid choice")
