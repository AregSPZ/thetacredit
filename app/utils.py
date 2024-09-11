import os, joblib

def process_form_data(form, loan_type):

    first_name = form.first_name.data
    last_name = form.last_name.data
    age = form.age.data
    annual_income = form.annual_income.data
    employment_length = form.employment_length.data
    loan_amount = form.loan_amount.data
    loan_percent_income = loan_amount / annual_income
    home_ownership = form.home_ownership.data
    loan_intent = loan_type
    q1 = int(form.q1.data)
    q2 = int(form.q2.data)
    q3 = int(form.q3.data)
    q4 = int(form.q4.data)
    q5 = int(form.q5.data)
    student = 1 if age < 25 and loan_type == 'education' else 0

    # One-hot encode home ownership
    home_ownership = [0, 0, 0, 0]
    if home_ownership == 'MORTGAGE':
        home_ownership[0] = 1
    elif home_ownership == 'OWN':
        home_ownership[2] = 1
    elif home_ownership == 'RENT':
        home_ownership[3] = 1
    else:
        home_ownership[1] = 1

    # One-hot encode loan intent
    loan_intent = [0, 0, 0, 0, 0]
    if loan_type == 'debt-consolidation':
        loan_intent[0] = 1
    elif loan_type == 'education':
        loan_intent[1] = 1
    elif loan_type == 'home-improvement':
        loan_intent[2] = 1
    elif loan_type == 'medical':
        loan_intent[3] = 1
    elif loan_type == 'venture':
        loan_intent[4] = 1

    # get loan grade
    points = q1 + q2 + q3 + q4 + q5
    loan_grade = [0, 0, 0, 0, 0, 0, 0]

    if points >= 18:
        loan_grade[0] = 1
    elif points >= 15:
        loan_grade[1] = 1
    elif points >= 12:
        loan_grade[2] = 1
    elif points >= 9:
        loan_grade[3] = 1
    elif points >= 6:
        loan_grade[4] = 1
    elif points >= 3:
        loan_grade[5] = 1
    else:
        loan_grade[6] = 1


    return {
        'first_name': first_name,
        'last_name': last_name,
        'age': age,
        'annual_income': annual_income,
        'employment_length': employment_length,
        'loan_amount': loan_amount,
        'loan_percent_income': loan_percent_income,
        'home_ownership': home_ownership,
        'loan_intent': loan_intent,
        'loan_grade': loan_grade,
        'student': student 
    }


def get_prediction(data):
    
        # Define the base path for the training directory
        base_path = os.path.join(os.path.dirname(__file__), '..', 'training')

        # Load models using joblib
        forest_clf = joblib.load(os.path.join(base_path, 'models', 'forest_clf.pkl'))
        forest_reg = joblib.load(os.path.join(base_path, 'models', 'forest_reg.pkl'))

        # Load variables using joblib
        age_mean = joblib.load(os.path.join(base_path, 'variables', 'age_mean.pkl'))
        age_std = joblib.load(os.path.join(base_path, 'variables', 'age_std.pkl'))
        annual_income_mean = joblib.load(os.path.join(base_path, 'variables', 'income_mean.pkl'))
        annual_income_std = joblib.load(os.path.join(base_path, 'variables', 'income_std.pkl'))
        employment_length_mean = joblib.load(os.path.join(base_path, 'variables', 'emp_length_mean.pkl'))
        employment_length_std = joblib.load(os.path.join(base_path, 'variables', 'emp_length_std.pkl'))
        loan_percent_income_mean = joblib.load(os.path.join(base_path, 'variables', 'percent_income_mean.pkl'))
        loan_percent_income_std = joblib.load(os.path.join(base_path, 'variables', 'percent_income_std.pkl'))
        interest_mean = joblib.load(os.path.join(base_path, 'variables', 'interest_mean.pkl'))
        interest_std = joblib.load(os.path.join(base_path, 'variables', 'interest_std.pkl'))
        threshold_1 = joblib.load(os.path.join(base_path, 'variables', 'threshold_1.pkl'))
        threshold_2 = joblib.load(os.path.join(base_path, 'variables', 'threshold_2.pkl'))


        # scale the data

        age_scaled = (data['age'] - age_mean) / age_std

        annual_income_scaled = (data['annual_income'] - annual_income_mean) / annual_income_std

        employment_length_scaled = (data['employment_length'] - employment_length_mean) / employment_length_std

        loan_percent_income_scaled = (data['loan_percent_income'] - loan_percent_income_mean) / loan_percent_income_std


        # prepare the data for prediction
        input_data = [[age_scaled, annual_income_scaled, employment_length_scaled, loan_percent_income_scaled, data['home_ownership'][0], data['home_ownership'][1], data['home_ownership'][2], data['home_ownership'][3], data['loan_intent'][0], data['loan_intent'][1], data['loan_intent'][2], data['loan_intent'][3], data['loan_intent'][4], data['loan_grade'][0], data['loan_grade'][1], data['loan_grade'][2], data['loan_grade'][3], data['loan_grade'][4], data['loan_grade'][5], data['loan_grade'][6], data['student']]]


       # Predict using the classifier and apply the appropriate threshold
        probas = forest_clf.predict_proba(input_data)[0] # extract the one and only row of 2d array which contains 2 values: probability of class 0 and probability of class 1


        # if the loan is high risk, use the threshold_2, otherwise use threshold_1
        

        if data['loan_intent'][1] == 1 or data['loan_intent'][4] == 1: # if the loan intent is education or venture, the risky threshold for loan_percent_income is 2

            if data['loan_percent_income'] > 2: 
                
                if probas[1] >= threshold_2:    # probas[1] is the probability of positive class 1 (the loan defaulting)
                    prediction = 'rejected'
                else:
                    prediction = 'approved'

            else:
                
                if probas[1] >= threshold_1:
                    prediction = 'rejected'
                else:
                    prediction = 'approved'


        else: # for the other loan intents, it's 0.7

            if data['loan_percent_income'] > 0.7: 
            
                if probas[1] >= threshold_2:    # probas[1] is the probability of positive class 1 (the loan defaulting)
                    prediction = 'rejected'
                else:
                    prediction = 'approved'

            else:
                
                if probas[1] >= threshold_1:
                    prediction = 'rejected'
                else:
                    prediction = 'approved'

        interest_rate = forest_reg.predict(input_data)[0] * interest_std + interest_mean
            
        return prediction, interest_rate