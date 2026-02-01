"""Compare wandb runs - triggered on PR comment."""

import os
import wandb


if __name__ == "__main__":
    base_wandb_run = "ma-hassan/cicd-quickstart/b7rpdt8a"
    PR_comment= os.environ.get("PR_COMMENT")
    PR_NUMBER= os.environ.get("PR_NUMBER")
    PAYLOAD= os.environ.get("PAYLOAD")

    print(f"PR_comment: {PR_comment}")
    print(f"PR_NUMBER: {PR_NUMBER}")
    print(f"PAYLOAD: {PAYLOAD}")

    pass
