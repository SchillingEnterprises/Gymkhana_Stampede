from .models import Checkpoint, Reward

if Checkpoint.isValid:
    Reward.point_total += 1
else:
    print("Point Total: ", Reward.point_total)
