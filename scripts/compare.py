"""Compare script - triggered on PR comment. Add your compare logic here."""

import os
import wandb
import wandb_workspaces.reports.v2 as wr
from ghapi.all import GhApi
import json

if __name__ == "__main__":
    base_wandb_run_id = "b7rpdt8a"
    GITHUB_ACTIONS_FLAG = os.environ.get("GITHUB_ACTIONS", "false")
    api = GhApi(token=os.environ.get("GITHUB_TOKEN"))
    if GITHUB_ACTIONS_FLAG != "true":  # mainly for debugging purposes
        print("This script is not running in a GitHub action, we are using predefined PR comment and PR number")
        PR_NUMBER = 5
        COMMENT_ID = 3831559100
        COMMENT = api.issues.get_comment(owner="MoH-assan", repo="CI_CD_4_ML", comment_id=COMMENT_ID)
        COMMENT = dict(COMMENT)  # or comment.model_dump() if it's a Pydantic model
          
        
        

    else:
        print("This script is running in a GitHub action, we are using PR comment and PR number from the environment variables")
        PR_NUMBER = os.environ.get("PR_NUMBER")
        PAYLOAD = json.loads(os.environ.get("PAYLOAD", "{}"))
        COMMENT = PAYLOAD["comment"]
    

    PR_comment = COMMENT.get("body", "").strip()
    print(f"COMMENT: {PR_comment}")

    # Validate WANDB_API_KEY before creating report (W&B keys are 40+ characters)
    wandb_key = os.environ.get("WANDB_API_KEY")
    if wandb_key and len(wandb_key) < 40:
        raise ValueError(
            f"WANDB_API_KEY invalid: API key must have 40+ characters, has {len(wandb_key)}. "
            "Get a valid key from https://wandb.ai/authorize and set it in repo Secrets."
        )

    # Parse /wandb/{owner}/{project}/{run_id} from comment
    # e.g. /wandb/ma-hassan/cicd-quickstart/yi4sittf
    parts = PR_comment.split("/")
    # ['', 'wandb', 'ma-hassan', 'cicd-quickstart', 'yi4sittf'] or with extra text
    if len(parts) >= 5 and parts[1] == "wandb":
        wandb_owner = parts[2]
        wandb_project = parts[3]
        wandb_run_id = parts[4].split()[0] if parts[4] else ""  # strip trailing text
        print(f"WandB owner: {wandb_owner}")
        print(f"WandB project: {wandb_project}")
        print(f"WandB run_id: {wandb_run_id}")
        wandb_run_path = f"{wandb_owner}/{wandb_project}/{wandb_run_id}"
        PROJECT = wandb_project
        ENTITY = wandb_owner

        wandb_api = wandb.Api()
        base_wandb_run = wandb_api.run(f"{ENTITY}/{PROJECT}/{base_wandb_run_id}")
        run = wandb_api.run(f"{ENTITY}/{PROJECT}/{wandb_run_id}")
        base_run_name = base_wandb_run.name
        run_name = run.name
        print(f'Creating report for {base_run_name} and {run_name}')
        report = wr.Report(
            entity=ENTITY,
            project=PROJECT,
            title='Compare Runs'
        )
        pg = wr.PanelGrid(
            runsets=[
                wr.Runset(ENTITY, PROJECT, "Run Comparison", filters=f"Name in ['{base_run_name}', '{run_name}']")
            ],
            panels=[
                wr.RunComparer(diff_only='split', layout={'w': 24, 'h': 15}),
            ]
        )

        report.blocks = report.blocks[:1] + [pg] + report.blocks[1:]
        report.save()
        report_url = report.url
        print(f"Report saved to {report_url}")

        # Reply to the PR comment with the report URL (requires GITHUB_TOKEN)
        if os.environ.get("GITHUB_TOKEN"):
            owner, repo = os.environ.get("GITHUB_REPOSITORY", "MoH-assan/CI_CD_4_ML").split("/")
            pr_num = int(PR_NUMBER)
            reply_body = f"Here's the comparison report: {report_url}"
            api.issues.create_comment(owner=owner, repo=repo, issue_number=pr_num, body=reply_body)
            print(f"Posted reply to PR #{pr_num}")
        else:
            print("Skipping PR comment (local run - set GITHUB_TOKEN to post locally)")

    else:
        wandb_owner = wandb_project = wandb_run_id = None
        print("No valid /wandb/owner/project/run_id found in comment")

    pass
