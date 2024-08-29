from typing import Optional

import numpy as np

from tessellation.procgen.generator import Action, Generator, GenerationResult

VALID_ACTIONS = [
    Action.UP,
    Action.UP_RIGHT,
    Action.RIGHT,
    Action.DOWN,
    Action.DOWN_RIGHT,
]


class RNGGenerator(Generator):
    """Generator that uses a random number generator to generate the tesselation mask."""

    def __init__(self, seed: int = 42):
        self.rng = np.random.default_rng(seed)

    def generate(
        self,
        side_len: int,
        action_probs: Optional[list[Action]] = None,
    ) -> GenerationResult:
        """Generate a tesselation mask using a random number generator."""
        if action_probs is None:
            action_probs = [1 / len(VALID_ACTIONS)] * len(VALID_ACTIONS)

        assert len(VALID_ACTIONS) == len(action_probs)

        y_axis_mask, y_line_actions = self._generate_side(side_len, action_probs)
        x_axis_mask, x_line_actions = self._generate_side(side_len, action_probs)
        # Transpose the x_mask to make the line run along the x-axis
        x_axis_mask = x_axis_mask.T
        return GenerationResult(
            mask=x_axis_mask | y_axis_mask,
            line_actions=[y_line_actions, x_line_actions],
        )

    def _generate_side(
        self, side_len: int, action_probs: list
    ) -> tuple[np.ndarray, list[Action]]:
        cursor = {"x": 0, "y": 0}
        action_list = []
        while cursor["x"] < side_len - 1:

            action = self._get_rand_action(
                actions_list=VALID_ACTIONS, action_probs=action_probs
            )
            action_list.append(action)

            if action == Action.UP:
                cursor["y"] -= 1
            elif action == Action.UP_RIGHT:
                cursor["y"] -= 1
                cursor["x"] += 1
            elif action == Action.RIGHT:
                cursor["x"] += 1
            elif action == Action.DOWN:
                cursor["y"] += 1
            elif action == Action.DOWN_RIGHT:
                cursor["y"] += 1
                cursor["x"] += 1
            else:
                raise ValueError(f"Unsupported action: {action}")

        mask = np.zeros((side_len, side_len), dtype=int)
        return self._draw_line(mask, (0, 0), action_list), action_list

    def _get_rand_action(
        self, actions_list: list[Action], action_probs: list[float]
    ) -> Action:
        """Choose a random action from the list of actions with the given probabilities."""
        return self.rng.choice(np.array(actions_list), p=action_probs)
