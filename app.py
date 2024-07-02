from flask import Flask, render_template, redirect, url_for, flash  
from flask_sqlalchemy import SQLAlchemy 
from flask_wtf import FlaskForm 
from wtforms import StringField, TextAreaField, RadioField, SelectField, SubmitField, HiddenField
from wtforms.validators import InputRequired, Email  

app = Flask(__name__)  # Create a Flask application instance
app.secret_key = 'your_secret_key'  # Secret key for session management, replace with a real secret key in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'  # Configure the SQLite database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for better performance

db = SQLAlchemy(app)  # Initialize SQLAlchemy with the Flask app


# Define the Contact model for the database
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    first_name = db.Column(db.String(100), nullable=False) 
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)  
    country = db.Column(db.String(100), nullable=False) 
    message = db.Column(db.Text, nullable=False) 
    gender = db.Column(db.String(10), nullable=False)  
    subject = db.Column(db.String(100), nullable=False)  


# Define the ContactForm using FlaskForm
class ContactForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])  
    last_name = StringField('Last Name', validators=[InputRequired()])  
    email = StringField('Email', validators=[InputRequired(), Email()])  
    country = SelectField('Country', choices=[('us', 'United States'), ('ca', 'Canada'), ('uk', 'United Kingdom')],
                          validators=[InputRequired()])  
    message = TextAreaField('Message', validators=[InputRequired()])  
    gender = RadioField('Gender', choices=[('M', 'Male'), ('F', 'Female')], validators=[InputRequired()]) 
    subject = RadioField('Subject', choices=[('Repair', 'Repair'), ('Order', 'Order'), ('Others', 'Others')],
                         default='Others') 
    honeypot = HiddenField('Honeypot') 
    submit = SubmitField('Submit')  


# Define the main route for the contact form
@app.route('/', methods=['GET', 'POST'])
def contact():
    form = ContactForm()  
    if form.validate_on_submit():  
        if form.honeypot.data:  
            flash('Spam detected!', 'danger')  
            return redirect(url_for('contact'))  

        # If the honeypot is empty, process the form and save to the database
        new_contact = Contact(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            country=form.country.data,
            message=form.message.data,
            gender=form.gender.data,
            subject=form.subject.data
        )  
        db.session.add(new_contact)  
        db.session.commit()  

        flash('Thank you for contacting us.', 'success') 
        return render_template('thankyou.html', form=form, first_name=form.first_name.data,
                               last_name=form.last_name.data, email=form.email.data, country=form.country.data,
                               message=form.message.data, gender=form.gender.data, subject=form.subject.data)
    return render_template('contact.html', form=form)  


if __name__ == "__main__":
    with app.app_context():  # Ensure the application context is available
        db.create_all()  # Create database tables within the application context
    app.run(debug=True)  
