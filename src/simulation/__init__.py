from gymnasium.envs.registration import register

register(
    id='Blocus-v0',
    entry_point='simulation.blocus_env:BlocusEnv',
)