R.U.Stoked
==========

![Image](photos/icon.jpeg "icon")

**RUStoked** is an experimental **NLP** (_Sentiment Analysis_) project. An effort to orchestrate a pipe line of data from the early stage of data collection through Machine Learning model `deployment`.  

This blog post is more of a guide through the project stages, challenges, and lessons learned rather than a code review. The code is available on [GitHub](https://github.com/mohsen-saki/RUStoked) and I have tried to keep notebooks and code libraries explanatory as much as possible.  

**`IMPORTANT NOTE : This project is yet under development and some parts of `repo` may get updated accordingly`**  

This [GitHub](https://github.com/mohsen-saki/RUStoked) `repo` consists of:

* Folder [`data`](https://github.com/mohsen-saki/RUStoked/tree/master/data) which contains raw data and some lines of code for scraping data.
* Folder [`rustoked`](https://github.com/mohsen-saki/RUStoked/tree/master/rustoked) which contains a library of core functions used during data exploration and model development
* Folder [`notebooks`](https://github.com/mohsen-saki/RUStoked/tree/master/notebooks) which contains some notebooks to demonstrate data and model engineering process
* Folder [`app`](https://github.com/mohsen-saki/RUStoked/tree/master/app) which contains codes and functions for a small [streamlit](https://www.streamlit.io/) application running and maintaining the model.
* Folder [`withdrawn`](https://github.com/mohsen-saki/RUStoked/tree/master/withdrawn) which contains my first try to develop the model, not successful though.

----------------

Setup Environment
-----------------

This repository has been tested on `python 3.8`

Clone the repo on a local machine

`$ git clone https://github.com/mohsen-saki/RUStoked.git`

Python Environment

`$ cd RUStoked`  
`$ python3 -m venv <virtualenv>`  
`$ source <virtualenv>/bin/activate`  

Install required packages

`$ pip install -r requirements.txt`  
`$ pip install -r requirements-app.txt`  
`$ python -m spacy download en_core_web_sm`  
`$ python -m spacy download en_core_web_lg`

To run the app locally:

`cd app`  
`streamlit run app.py`

**Deployment**

It has been automated through [GitHub Action](https://github.com/features/actions) to deploy [docker container](https://www.docker.com/resources/what-container) on both [Heroku](https://www.heroku.com/free) and [AWS ECS Instances](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_instances.html). But, both processes cannot be triggered at the same time due to Heruko’s method for handling server side ports. See [Dockerfile](https://github.com/mohsen-saki/RUStoked/blob/master/Dockerfile) for differences and adjustment required.

To deploy on Heroku (or vice versa for aws)

`$ cd .github/workflows`  
`$ mv heroku.yml.deactivated heroku.yml`  
`$ mv aws.yml aws.yml.deactivated`

Heroku Prerequisite
* grab your Heroku account `api_token` and put it into _github repository secrets_ as `HEROKU_API_KEY = api_token` ([see here](https://help.heroku.com/PBGP6IDE/how-should-i-generate-an-api-key-that-allows-me-to-use-the-heroku-platform-api))
* creat an application instance on Heroku and put it's `"name"` into _github repository secrets_ as `HEROKU_APP_NAME = name` ([see here](https://devcenter.heroku.com/articles/creating-apps#creating-a-named-app))

AWS Prerequisite
* Need (recommended) an IAM account ([see here](https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started_create-admin-group.html))
* May need to create an ECS instance IAM role ([see here](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/instance_IAM_role.html))
* Create an ECR repository ([see here](https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html))
* May need to create security keay-pair (to SSH into container if needed) ([see here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html#prepare-key-pair))
* Need to create a "load ballancer", a "security group" (to open up port 80), and register a "target group" ([see here](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/create-application-load-balancer.html))
* Need to create a "task-definition", "cluster", and "service" (using already created load-balancer, target-froup, secutity group, etc) ([see here](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/getting-started-ecs-ec2.html))
* Probably need to revisit created security group to add a new inbound rule for port 8501 (from ECS dashboard)


**-->** And it is live [here](https://rustoked.herokuapp.com/) on Heroku.

About the Project
-------------------
to do


--------
Thanks to open spurce and free world.
![Image](photos/foot.jpeg)