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


__commit ad13f24b809a2aeed3730ea642c44182cb87ae99__
By reducing `target labels` from 5 rating categories to 3 sentiment_category, **_best score_** is improved to **_0.627_**. Model is still RandomForest but parameters has been optimized using `GridSearchCS()`.

__commit 1a3b43a5fca96e0d692df28162daa4144cce9ed5__  
Various models trained and tested on `tfidf` features. The `accuracy_score` for all models is between __`60`__ and __`63%`__.


__commit 2b5155164c7153e769130b4846873808dda517c1__
Using `word2vec` model both trained on data and using `GloVe` pretrained model. Tested on `SVM`model (which had the best performance so far) but not much progress with `accuracy_score` about __`58%`__.
