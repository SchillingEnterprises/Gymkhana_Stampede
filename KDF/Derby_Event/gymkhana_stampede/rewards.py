"""Pure reward-point calculation helpers.

This module intentionally performs no database access at import time. Callers
must load and validate checkpoint/event/reward records before using the result.
"""


def calculate_reward_total(current_total, event_point_value, checkpoint_is_valid):
    """Return the reward total after a checkpoint is accepted.

    Invalid or unapproved checkpoints do not award points. The function does
    not mutate models or persist records; persistence belongs to a validated
    application service/view with an explicit transaction.
    """
    if not checkpoint_is_valid:
        return current_total
    return current_total + event_point_value
