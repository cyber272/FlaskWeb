from flask import Flask, render_template, redirect, url_for, flash  # Import necessary modules from Flask
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy for database handling
from flask_wtf import FlaskForm  # Import FlaskForm for form handling
from wtforms import StringField, TextAreaField, RadioField, SelectField, SubmitField, HiddenField  # Import form fields from WTForms
from wtforms.validators import InputRequired, Email  # Import validators from WTForms

app = Flask(__name__)  # Create a Flask application instance
app.secret_key = 'your_secret_key'  # Secret key for session management, replace with a real secret key in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'  # Configure the SQLite database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for better performance

db = SQLAlchemy(app)  # Initialize SQLAlchemy with the Flask app


# Define the Contact model for the database
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the Contact model
    first_name = db.Column(db.String(100), nullable=False)  # First name column, not nullable
    last_name = db.Column(db.String(100), nullable=False)  # Last name column, not nullable
    email = db.Column(db.String(100), nullable=False)  # Email column, not nullable
    country = db.Column(db.String(100), nullable=False)  # Country column, not nullable
    message = db.Column(db.Text, nullable=False)  # Message column, not nullable
    gender = db.Column(db.String(10), nullable=False)  # Gender column, not nullable
    subject = db.Column(db.String(100), nullable=False)  # Subject column, not nullable


# Define the ContactForm using FlaskForm
class ContactForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])  # First name field with required validator
    last_name = StringField('Last Name', validators=[InputRequired()])  # Last name field with required validator
    email = StringField('Email', validators=[InputRequired(), Email()])  # Email field with required and email format validators
    country = SelectField('Country', choices=[('us', 'United States'), ('ca', 'Canada'), ('uk', 'United Kingdom')],
                          validators=[InputRequired()])  # Country dropdown field with predefined choices and required validator
    message = TextAreaField('Message', validators=[InputRequired()])  # Message field with required validator
    gender = RadioField('Gender', choices=[('M', 'Male'), ('F', 'Female')], validators=[InputRequired()])  # Gender radio buttons with required validator
    subject = RadioField('Subject', choices=[('Repair', 'Repair'), ('Order', 'Order'), ('Others', 'Others')],
                         default='Others')  # Subject radio buttons with default value
    honeypot = HiddenField('Honeypot')  # Hidden honeypot field for anti-spam
    submit = SubmitField('Submit')  # Submit button


# Define the main route for the contact form
@app.route('/', methods=['GET', 'POST'])
def contact():
    form = ContactForm()  # Create an instance of the ContactForm
    if form.validate_on_submit():  # Check if form is submitted and validated
        if form.honeypot.data:  # Check if honeypot field is filled (indicating spam)
            flash('Spam detected!', 'danger')  # Flash spam message
            return redirect(url_for('contact'))  # Redirect back to the contact form

        # If the honeypot is empty, process the form and save to the database
        new_contact = Contact(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            country=form.country.data,
            message=form.message.data,
            gender=form.gender.data,
            subject=form.subject.data
        )  # Create a new Contact object with form data
        db.session.add(new_contact)  # Add the new contact to the database session
        db.session.commit()  # Commit the session to save the contact

        flash('Thank you for contacting us.', 'success')  # Flash success message
        return render_template('thankyou.html', form=form, first_name=form.first_name.data,
                               last_name=form.last_name.data, email=form.email.data, country=form.country.data,
                               message=form.message.data, gender=form.gender.data, subject=form.subject.data)  # Render thank you page with form data
    return render_template('contact.html', form=form)  # Render contact form template if form is not submitted or not valid


if __name__ == "__main__":
    with app.app_context():  # Ensure the application context is available
        db.create_all()  # Create database tables within the application context
    app.run(debug=True)  # Run the Flask app in debug mode
