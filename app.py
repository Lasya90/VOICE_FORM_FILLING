from flask import Flask, render_template, request, redirect, flash, session
import os
import whisper
from werkzeug.security import generate_password_hash, check_password_hash

from googletrans import Translator

# Flask app setup
app = Flask(__name__)
app.secret_key = os.urandom(24)




# Load the Whisper model
model = whisper.load_model("base")

# Translator for multilingual support
translator = Translator()

# Function to sanitize inputs
def sanitize_input(value):
    return value.strip()

# Function to transcribe speech and translate it
def transcribe_speech(audio_path, target_language='en'):
    result = model.transcribe(audio_path)
    original_text = result['text']
    
    # Handle specific terms for special characters
    # Replace "at" with "@"
    original_text = original_text.replace(" at ", "@")
    # Optionally, replace "dot" with "."
    original_text = original_text.replace(" dot ", ".")
    # Handle other potential keywords for special characters if needed

    if target_language != 'en':
        translated_text = translator.translate(original_text, dest=target_language).text
        return translated_text
    return original_text


# Home route
@app.route('/')
def home():
    if 'user_id' in session:
        return render_template('index.html')  # Pass user data if logged in
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_name = sanitize_input(request.form['userName'])
        email = sanitize_input(request.form['email'])
        password = sanitize_input(request.form['password'])

        # In-memory validation (since database is removed)
        flash("Signup successful! You can now log in.", "success")
        return redirect('/login')  # Redirect to the login page after successful signup

    return render_template('login_signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check if user is already logged in
    if 'user_id' in session:
        flash("You are already logged in.", "info")
        return redirect('/')  # Redirect to home if the user is already logged in

    if request.method == 'POST':
        email = sanitize_input(request.form['email'])
        password = sanitize_input(request.form['password'])

        # In-memory validation (since database is removed)
        if email == "test@example.com" and password == "password":  # Example credentials
            session['user_id'] = 1
            flash("Login successful!", "success")
            return redirect('/')
        else:
            flash("Invalid credentials. Please try again.", "error")

    return render_template('login_signup.html')

@app.route('/form', methods=['GET', 'POST'])
def form_filling():
    if request.method == 'POST':
        try:
            # Extracting form data
            first_name = request.form['firstName']
            last_name = request.form['lastName']
            father_name = request.form['fatherName']
            mother_name = request.form['motherName']
            dob = request.form['dob']
            branch = request.form['branch']
            section = request.form['section']
            roll_number = request.form['rollNumber']
            year_of_study = request.form['yearOfStudy']
            percentage = request.form['percentage']
            phone = request.form['phone']
            email = request.form['email']
            blood_group = request.form.get('bloodGroup', '')
            address = request.form['address']

            # No database save as it has been removed
            flash("Student details submitted successfully!", "success")
            return redirect('/success')
        except Exception as err:
            print(f"Error: {err}")
            flash("There was an error while submitting the form. Please try again.", "error")
            return redirect('/form')

    return render_template('forms.html')

@app.route('/success')
def success_page():
    return render_template('thnx.html')

@app.route('/secondpg')
def second_page():
    return render_template('login_signup.html')


if __name__ == "__main__":
    app.run(debug=True)