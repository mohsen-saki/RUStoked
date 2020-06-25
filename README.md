# RUStoked

**`Important note : This project is yet under development and all parts are not available.`**

This project is a Sentiment Analysis (NLP) app driven by Machine Learning. The model is trained on a data set collected from employers’ review on  [SEEK](www.seek.com.au) This repo consists of:

* Folder [`rustoked`](https://github.com/mohsen-saki/RUStoked/tree/master/rustoked) which contains a library of core functions for the app
* Folder [`notebooks`](https://github.com/mohsen-saki/RUStoked/tree/master/notebooks) which contains some notebooks to demonstrate data and model engineering process
* Folder [`withdrawn`](https://github.com/mohsen-saki/RUStoked/tree/master/withdrawn) which contains my first try to develop the model,  successful though.

## Setup Environment

_Step 1 : Download repo on your machine_

`$ git clone https://github.com/mohsen-saki/RUStoked.git`

_Step 2 : Set up Environment_

`$ cd RUStoked`

`$ python3 -m venv <virtualenv>`

`$ source <virtualenv>/bin/activate`

_Step 3 : Install required packages_

`$ pip install -r requirements.txt`

`$ python -m spacy download en_core_web_lg`
