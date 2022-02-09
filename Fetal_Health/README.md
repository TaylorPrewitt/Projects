# Introduction

#### Context
Reduction of child mortality is reflected in several of the United Nations' Sustainable Development Goals and is a key indicator of human progress.
The UN expects that by 2030, countries end preventable deaths of newborns and children under 5 years of age, with all countries aiming to reduce under‑5 mortality to at least as low as 25 per 1,000 live births.

Parallel to notion of child mortality is of course maternal mortality, which accounts for 295 000 deaths during and following pregnancy and childbirth (as of 2017). The vast majority of these deaths (94%) occurred in low-resource settings, and most could have been prevented.

In light of what was mentioned above, Cardiotocograms (CTGs) are a simple and cost accessible option to assess fetal health, allowing healthcare professionals to take action in order to prevent child and maternal mortality. The equipment itself works by sending ultrasound pulses and reading its response, thus shedding light on fetal heart rate (FHR), fetal movements, uterine contractions and more.


### Data
This dataset contains 2126 records of features extracted from Cardiotocogram exams, which were then classified by three expert obstetritians into 3 classes:

- Normal (1)
- Suspect (2)
- Pathological (3)

[Data Source](https://www.kaggle.com/andrewmvd/fetal-health-classification?select=fetal_health.csv) <br>
[Data Authors](https://onlinelibrary.wiley.com/doi/10.1002/1520-6661(200009/10)9:5%3C311::AID-MFM12%3E3.0.CO;2-9)


### Tasks
1) Create a multiclass model to classify the state of fetus. <br>
2) Find best evaluation metrics. 



<br><br>

# Results

### Training Feature Selection
Data is entirely numeric with no missing values. Many of the recorded values are statistical records of observations.  For these tasks, only using features for classification which could be easily available or determined in a clinical setting. For example, a histogram is not considered easily available in a clinical environment, but measuring uterine contractions would be.

### Model Performance

| **Model**  | **fit_time**  |  **score_time**  |  **test_score**  | 
| :----------: | :----------: | :----------: |:----------: |
| GBR  | 0.088762 | 0.001998  | 0.740584 |
| GNB  |  0.002326 | 0.001330  | 0.837366 |
| RF  | 0.140956 | 0.012633 | 0.931452 |
| SVM  | 0.023937 | 0.019281 | 0.831989 |


### Model Selection

While the random forest is the most costly model out of the models tested (by an order of magnitude), it is also the best scoring model. Since the dataset is not large and the number of features is small the cost is not prohibitive. Furthermore, this model is has better explainability than the others with human interpretable results by a non-technical audience. 

<br>

### Model Tuning and Testing

![output_16_0](https://user-images.githubusercontent.com/80305894/152451683-c3bba7d3-f00d-48f5-9569-fb6205e7ec2e.png)

<sup><i>The above plot shows the cross validation f1 score for models of differing depths (5-555 trees).</i></sup>

<br>

![output_18_1](https://user-images.githubusercontent.com/80305894/152451073-da85f79d-664e-4054-adce-577b695e90da.png)

<sup><i>The above is a confusion matrix using sklearn's random forest classifier.  This forest has a depth of 300 trees using all 11 features.</i></sup>

<br>

![output_22_1](https://user-images.githubusercontent.com/80305894/152451062-4d5201f3-1895-4e1f-b64e-7aec02bdd19f.png)

<sup><i>The above is a confusion matrix using sklearn's random forest classifier.  This forest has a depth of 300 trees using top-3 features.</i></sup>

<br>

Upon initial inspection of the confusion matrices seems to prove that a three metric evaluation can give a strong intuition for the state of the fetus.


In the data however, there is a class imbalance. Class 1 (healthy) has a much higher frequency than classes 2 (Suspect) or 3 (Pathological). To compensate for this, weighted scoring is be used.


### Classification Performance

| **Number of Features**  | **Precision**  |  **Recall**  |  **F1**  | 
| :----------: | :----------: | :----------: |:----------: |
| 11  | 0.9343 | 0.9357  | 0.9323 |
| 6  |  0.9316 | 0.9310  | 0.9274 |
| 3  | 0.8435 | 0.8495 | 0.8460  |


<br>

# Discussion

### Task 1
Each model ('GradientBoostingRegressor','RandomForestClassifier', 'GaussianNB', 'SVC') was able to appropriately label the multiclass data without any hyperparameter tuning. 

The models ranked as followed:  
- **Speed**: The GaussianNB model was the fastest of the four models and RandomForestClassifier was the slowest. GaussianNB was two orders of magnitude faster at training than the RandomForestClassifier.  

- **Scoring**: The RandomForestClassifier (score: 0.9315) was the best at labeling classes, and the GradientBoostingRegressor (score: 0.7406) was the worst out of the four.


### Task 2
The top features to determine the state of a fetus were: 'baseline value', 'prolongued_decelerations', 'abnormal_short_term_variability'. While the performance of the model trained was not fully optimized so it should not be used in a diagnostic setting, the metrics it uncovered could be.  
These metrics could be used by medical staff as key indicators in diagnostics and patient treatment.    Monitoring the fetal heart rate in a single office visit would be able to yield a strong intuition to the fetal health 







