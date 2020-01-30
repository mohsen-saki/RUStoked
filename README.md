# RUStoked

## This is a NPL Machine Learning (Text Classification) Project

It has been conducted under Four discrete stages:
1. [Data Collection & Web Scraping](https://github.com/mohsen-saki/RUStoked/tree/master/00_data_scraping)
2. [Data Preparation](https://github.com/mohsen-saki/RUStoked/tree/master/01_data_preparation) (ongoing...)
3. [Feature Engineering and Model Development](https://github.com/mohsen-saki/RUStoked/tree/master/02_model_development) (ongoing...)
4. Deployment (Django App on docker Container) (yet to come...)

#### Models to be Trained and Tested
* Random Forest
* Support Vector Machine
* K Nearest Neighbors
* Multinomial Naïve Bayes
* Multinomial Logistic Regression
* Gradient Boosting


### Dataset
The data has been collected from [SEEK.COM.AU](https://www.seek.com.au/) using `python` web scraping tools; **`requests`**, 
__`BeautifulSoup`__, and __`Selenium`__. The dataset includes about __4,000__ employees’ review for two large supermarkets
in Australia: **_Woolworths_** & **_Coles_**.

### Git Log History
I would like to keep a diary of some specially picked `git-logs` with elaborated explanation (more specifically, of those 
logged during _feature engineering and model development_). I believe it will shed some light on how the model has 
developed, its problems, and solutions.

__commit 30e09a5b8ea57eacb234fdd5fb6c794081e979cc__  
`TFIDF` technique has been used to create data features. A `pipeline` of `TfidfVectorizer()` data transformation and 
`RandomForestClassifier()` has been run. `Hyperparameters` have been optimized using `RandomizedSearchCV()` over
__`500`__ data fitting which took almost __`30 minutes`__ to complete. The **_best score_** over training dataset 
was **_0.378_** (__very low__)
