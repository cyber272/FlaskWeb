#  Welcome to the FlaskWeb project! 

---
## Overview
This project demonstrates how to create a web form using Flask in Python. 

## Project Structure

- `app.py`: The main Flask application file.
- `static/`: Directory containing static files (e.g., CSS).
- `styles.css`: Custom styles for the application.
- `templates/`: Directory containing HTML templates.
- `contact_form.html`: The contact form page.
- `thank_you.html`: The thank you page displayed after a successful submission.
- `README.md`: Project documentation.



# Project: Form in Python with Flask

## Problem statement:
The company Hackers Poulette™ sells DIY kits and accessories for Rasperri Pi. They want to allow their users to contact their technical support. Your mission is to develop a Python script that displays a contact form and processes its response: sanitization, validation, and then sending feedback to the user.

## Performance criteria:
* If the user makes an error, the form should be returned to them with valid responses preserved in their respective input fields.
* Ideally, display error messages near their respective fields.
* The form will perform server-side sanitization and validation.
* If sanitization and validation are successful, a "Thank you for contacting us." page will be displayed, summarizing all the encoded information.
* Implementation of the honeypot anti-spam technique.

#### Form fields
First name & last name + email + country (list) + message + gender (M/F) (Radio box) + 3 possible subjects (Repair, Order, Others) (checkboxes). All fields are mandatory, except for the subject (in this case, the value should be "Others").

## Contact Form (Python)
* Presentation: server/client architecture (transmissive, 10")
* Sanitization: neutralizing any harmful encoding (<script>)
* Validation: mandatory fields + valid email
* Sending + Feedback
* NO NEED FOR JAVASCRIPT OR CSS

#### At the end of this project, you should be able to:
- Explain the difference between a POST request and a GET request.
- Protect yourself against XSS vulnerabilities.
- Protect yourself against SSTI attacks.
- Use a micro framework.
- Perform a deployment.
