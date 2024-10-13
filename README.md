# ThetaCredit

A web application of a *fictional* credit organization that uses machine learning to assess credit risk and determine if the user gets the loan based on input data.

# Model Description
The project utilizes a classifier on loan dataset for predicting loan defaults and a regressor for predicting interest rates for approved loans. The models are implemented in a simple web application created with Flask and deployed on Heroku.

# Goal
The primary goal is to accurately assess credit risk to make informed loan approval decisions.

# Models Used
Random Forest for both classification and regression (Scikit-learn's RandomForestClassifier and RandomForestRegressor respectively).

# Results
Around 90% F1 macro score for classifier, which implies that the model is capable of accurately making loan decisions within the limits of training data (35000USD or lower loans), and 0.4 Root Mean Squared Error for regressor (with target variable and predictions being normalized).
