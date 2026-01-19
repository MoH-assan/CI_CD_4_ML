# CI_CD_4_ML

Repository for CI/CD for Machine Learning course.

These are resources resources. 

Course repo is: https://github.com/hamelsmu/wandb-cicd

Below is summary of concepts covered in this course:

1. Workflow file is a YAML file that defines the steps to be executed in a CI/CD pipeline.
2. Each workflow file is triggered by an event, such as a push to a repository or a pull request.
3. In the workflow file, we define the jobs to be executed, and the steps to be executed in each job.
4. Each job is executed on a runner, which is a machine that runs the steps in the job.
5. You can have variables in the workflow file, and you can use them in the steps.
6. One kind of variable is the secret variable, which is a variable that is encrypted and can only be accessed by the runner.
7. Another variable is the context variable, which is a variable that is available to all steps in the job and mainly contains github related information. For example, the context variable can be used to get the name of the branch that triggered the workflow or the username of the person who triggered the workflow as so on. More about context variables: https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#github-context
8. Anything written in ${{}} is an expression, and it is evaluated by GitHub Actions.Think of it as a function that returns a value. 
More about expressions: https://docs.github.com/en/actions/using-workflows/expressions
9. toJSON() is a function that can be used to convert a variable to a JSON string.
10. github.event is a context variable that all the information about the job that triggered the workflow.
11. Job is when a workflow is triggered, it is executed on a runner, and it is a collection of steps to be executed.
12. Environment variables are variables that are available to all steps in the job. And you can define them in the workflow file. And you can use them in the steps or Python code using os.getenv('VariableName'). You can define context variables in the workflow file using env: or you can define the output of expression as a Environment variable. e.g. 
env: 
    PAYLOAD: ${{ toJSON(github.event) }}

13. Some Environment variables are available by default, and you can use them in the steps or Python code using os.getenv('VariableName'). e.g. CI is true when you are running in a GitHub Actions environment. So if the python file is run in a GitHub Actions environment, it will be true, but if run locally it will be false. 

14. You can save the output of a step and use it in another step. For example in the io.yaml file, we save the output of the set-var step and use it in the print-value step. Note that you must give each step an id to be able to refer to it later and get its outputs. Note the the output is written to a file called GITHUB_OUTPUT and it is unique to each step. This is why the id is needed so you can recall the correct GITHUB_OUTPUT file. 

