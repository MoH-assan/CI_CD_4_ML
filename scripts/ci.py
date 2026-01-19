import wandb
print(f'Ther version of wandb is {wandb.__version__}')

assert wandb.__version__ == '1.36.0', f"WandB version is {wandb.__version__}, but 1.36.0 is required"

