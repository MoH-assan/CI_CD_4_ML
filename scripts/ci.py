import wandb
print(f'Ther version of wandb is {wandb.__version__}')

assert wandb.__version__ == '0.24.0', f"WandB version is {wandb.__version__}, but 0.24.0 is required"

