from os import path

from rl_agent.encoder.factory import EncoderFactory
from rl_agent.encoder import BaseEncoder

"""
    ROSNAV MODEL TRAINED IN NAVREP ENVIRONMENT
"""


class Encoder(BaseEncoder):
    def __init__(self, agent_name: str, model_dir: str, hyperparams):
        model_path = path.join(model_dir, agent_name + ".zip")

        assert path.isfile(
            model_path
        ), f"Compressed model cannot be found at {model_path}!"

        self._agent = self._load_model(model_path)
        if hyperparams["normalize"]:
            self._obs_norm_func = self._load_vecnorm()

    def _load_model(self, model_path: str):
        """Import stable baseline here because it requires
        a different python version
        """
        from stable_baselines.ppo2 import PPO2

        return PPO2.load(model_path)

    def _load_vecnorm(self):
        return lambda obs: obs

    def get_observation(self, obs, *args, **kwargs):
        return obs[0].reshape(len(obs[0]), 1)

    def get_action(self, action):
        """
        Encodes the action produced by the nn
        Should always return an array of size 3 with entries
        [x_vel, y_vel, ang_vel]
        """
        assert (
            len(action) == 2
        ), f"Expected an action of size 2 but received {len(action)}: {action}"

        x_vel, ang_vel = action
        return [x_vel, 0, ang_vel]

class HolonomicEncoder(Encoder):
    def get_action(self, action):
        assert (
            len(action) == 3
        ), f"Expected an action of size 3 but received: {action}"

        return action


"""
    Jackal
    N: 720 
    offset: -3/4 * pi
    action: [x_vel, ang_vel]
"""

@EncoderFactory.register("navrep", "rosnav", "jackal")
class JackalEncoder(Encoder):
    pass


"""
    Turtlebot3
    N: 360
    offset: 0
    action: [x_vel, ang_vel]
"""


@EncoderFactory.register("navrep", "rosnav", "turtlebot3_burger")
class TurtleBot3BurgerEncoder(Encoder):
    pass


"""
    AGV
    N: 720
    offset: -pi
    action: [x_vel, ang_vel]
"""

# No model available
#@EncoderFactory.register("navrep", "rosnav", "turtlebot3_burger")
class TurtleBot3WaffleEncoder(Encoder):
    pass


"""
    AGV
    N: 720
    offset: -pi
    action: [x_vel, ang_vel]
"""


@EncoderFactory.register("navrep", "rosnav", "agv-ota")
class AgvEncoder(Encoder):
    pass


"""
    Ridgeback
    N: 720
    offset: -3/4 * pi
    action: [x_vel, y_vel, ang_vel]
"""


@EncoderFactory.register("navrep", "rosnav", "ridgeback")
class RidgebackEncoder(HolonomicEncoder):
    pass


@EncoderFactory.register("navrep", "rosnav", "rto")
class RtoEncoder(HolonomicEncoder):
    pass

@EncoderFactory.register("navrep", "rosnav", "youbot")
class YoubotEncoder(HolonomicEncoder):
    pass

@EncoderFactory.register("navrep", "rosnav", "cob4")
class Cob4Encoder(HolonomicEncoder):
    pass