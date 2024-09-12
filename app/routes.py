"""
This module contains the routes for the Credit Risk Assessment Tool.
Routes:
- `/`: Renders the home page template with the title 'Home'.
- `/loan/<loan_type>`: Renders the loan page template with a loan form. Processes the form data and redirects to the interest_rate or decision route based on the prediction result.
- `/interest_rate`: Renders the interest_rate page template with the loan type, interest rate, title, and name parameters.
- `/decision`: Renders the decision page template with the loan status, loan type, title, and name parameters.
"""



from flask import render_template, redirect, url_for, request  # Import necessary Flask functions and classes
from app import app  # Import the Flask application instance
from app.forms import LoanForm  # Import the LoanForm class from the forms module
from app.utils import process_form_data, get_prediction  # Import utility functions for processing form data and getting predictions

@app.route('/')
def home():
    # Render the home page template with the title 'Home'
    return render_template('home.html', title='Home')

@app.route('/loan/<loan_type>', methods=['GET', 'POST']) 
def loan(loan_type):  # loan_type is a variable whose value is passed from the url_for in both @app.route and function call
    # Construct the title based on the loan_type
    title = f'{loan_type.replace("-", " ").title()} Loan'

    form = LoanForm()  # Create an instance of the LoanForm
    if form.validate_on_submit():
        # Process the form data
        processed_data = process_form_data(form, loan_type)

        # Get the prediction
        status, interest_rate = get_prediction(processed_data)

        if status == 'approved':
            # Redirect to the interest_rate route with the necessary parameters
            return redirect(url_for('interest_rate', loan_type=loan_type, interest_rate=interest_rate, title=title, name=form.first_name.data.title()))
        else:
            # Redirect to the decision route with the necessary parameters
            return redirect(url_for('decision', status='rejected', loan_type=loan_type, name=form.first_name.data.title()))
    else:
        # Print form errors if validation fails
        print(form.errors)
        
    # Render the loan page template with the form, title, and loan_type
    return render_template('loan.html', form=form, title=title, loan_type=loan_type) 

@app.route('/interest_rate')
def interest_rate():
    # Get parameters from the URL
    loan_type = request.args.get('loan_type')
    interest_rate = request.args.get('interest_rate')
    interest_rate = round(float(interest_rate), 2)  # Round the interest rate to 2 decimal places
    title = request.args.get('title')
    name = request.args.get('name')
    # Render the interest_rate page template with the necessary parameters
    return render_template('interest_rate.html', title=title, loan_type=loan_type, interest_rate=interest_rate, name=name)

@app.route('/decision')
def decision():
    # Get the value of the status parameter from the URL (the value is passed from the redirect function and url_for)
    status = request.args.get('status')
    loan_type = request.args.get('loan_type')
    # Construct the title based on the loan_type
    title = f'{loan_type.replace("-", " ").title()} Loan Decision' if loan_type else 'Loan Decision'
    name = request.args.get('name')
    # Render the decision page template with the necessary parameters
    return render_template('decision.html', status=status, loan_type=loan_type, title=title, name=name)