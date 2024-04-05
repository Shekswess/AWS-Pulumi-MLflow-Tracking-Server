# AWS-Pulumi-MLflow-Remote-Tracking-Server

This is a README.md file for the the AWS Pulumi Stack for the creating MLflow Remote Tracking Server. 

This code repository has all the code needed to create the AWS Pulumi Stack for the MLflow Remote Tracking Server and examples of how to use it.

Blogpost: https://mlops.community/mlflow-on-aws-with-pulumi-a-step-by-step-guide/

## Prerequisites
- Install [Pulumi](https://www.pulumi.com/docs/get-started/install/)
- Install [Python](https://www.python.org/downloads/)
- Install [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- Configure AWS CLI with your credentials (see [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html))

## Cloud infrastructure

### Deploy the cloud infrastructure
- Clone this repository
- Open a terminal and navigate to the folder src/cloud_infrastructure/
- Run `pulumi up` and follow the instructions
- Once the stack is deployed, you can check the resources created in the AWS Console

### Update the cloud infrastructure
- Open a terminal and navigate to the folder src/cloud_infrastructure/
- Run `pulumi up` and follow the instructions

### Destroy the cloud infrastructure
- Open a terminal and navigate to the folder src/cloud_infrastructure/
- Run `pulumi destroy` and follow the instructions

### Automatic deployment of the cloud infrastructure
- The cloud infrastructure can be deployed automatically using Github Actions. To do so, you need to create a secret in the repository with the name `PULUMI_ACCESS_TOKEN` and the value the access token of your Pulumi account. Also you need to create a secret with the AWS credentials with the name `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and `AWS_REGION`. Then, you can push the code to the repository and the cloud infrastructure will be deployed automatically for every push on the main branch.

## Examples
To use the examples, you need to have the cloud infrastructure deployed and to have installed the requirements in the requirements.txt file, by running `pip install -r requirements.txt`.

### Simple example
The file `machine_learning_example.ipynb` is an example of how to use the MLflow Remote Tracking Server for simple machine learning experiments. To run the example, you need to have the cloud infrastructure deployed, to have installed the requirements in the requirements.txt file and than you can run the notebook.

### LLM example
The file `llm_example.ipynb` is an example of how to use the MLflow Remote Tracking Server for LLM evaluation experiments. To run the example, you need to have the cloud infrastructure deployed, to have installed the requirements in the requirements.txt file and than you can run the notebook.

## Nginx configuration
The file `nginx.conf` is the Nginx configuration file for the MLflow Remote Tracking Server to use reverse proxy server and basic authentication. This file is used in the cloud infrastructure, to be precise in the EC2 instance.

## Folder structure
```
.
├── .github                                         # Github actions
│   └── workflows                                   # Github actions workflows
│       └── deploy_cloud_infrastructure.yml         # Github actions workflow to deploy the cloud infrastructure
├── .vscode                                         # VSCode settings
│   └── settings.json                               # Settings for the formatting of the code
├── src                                             # Source code
│   ├── cloud_infrastructure                        # Pulumi stack for the cloud infrastructure
│   │   ├── services                                # Pulumi services
│   │   │   ├── ec2.py                              # Pulumi code for the EC2 service
│   │   │   ├── rds.py                              # Pulumi code for the RDS service
│   │   │   └── s3.py                               # Pulumi code for the S3 service
│   │   ├── __main__.py                             # Creation of the Pulumi stack
│   │   ├── Pulumi.dev.yaml                         # Pulumi configuration file for the development environment
│   │   ├── Pulumi.yaml                             # Pulumi configuration file
│   │   └── requirements.txt                        # Python Pulumi requirements
│   ├── examples                                    # Examples of how to use the MLflow Remote Tracking Server
│   │   ├── llm_example.py                          # Example of how to use the MLflow Remote Tracking Server for LLM evaluation experiments
│   │   ├── machine_learning_example.py             # Examples of how to use the MLflow Remote Tracking Server for simple machine learning experiments
│   │   └── requirements.txt                        # Python requirements for the examples
│   └── nginx_configuration                         # Nginx configuration files
│       └── nginx.conf                              # Nginx configuration file for the MLflow Remote Tracking Server to use reverse proxy server and basic authentication
├── .gitignore                                      # Git ignore file
└── README.md                                       # README file (this file)
```
