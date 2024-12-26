from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
import whisper
from googletrans import Translator

# Flask app setup 
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load the Whisper model
model = whisper.load_model("base")

# Translator for multilingual support
translator = Translator()

# In-memory user store (for demonstration, can be replaced with other storage)
users = {}  # Format: email -> {user_data}
submissions = []  # Store form submissions

# Function to sanitize inputs
def sanitize_input(value):
    return value.strip()

# Function to transcribe speech and translate it
def transcribe_speech(audio_path, target_language='en'):
    result = model.transcribe(audio_path)
    original_text = result['text']
    
    # Handle specific terms for special characters
    original_text = original_text.replace(" at ", "@")  # Replace "at" with "@"
    original_text = original_text.replace(" dot ", ".")  # Replace "dot" with "."
    
    # Translate the text if target language is not 'en'
    if target_language != 'en':
        translated_text = translator.translate(original_text, dest=target_language).text
        return translated_text
    return original_text

# Home route
@app.route('/')
def home():
    if 'user_id' in session:
        user = users.get(session['user_id'])
        return render_template('index.html', user=user)  # Pass user data if logged in
    return render_template('index.html')

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            user_name = sanitize_input(request.form['userName'])
            email = sanitize_input(request.form['email'])
            password = sanitize_input(request.form['password'])

            # Check if the user already exists
            if email in users:
                flash("User already exists. Please log in.", "error")
                return redirect('/login')

            hashed_password = generate_password_hash(password)
            users[email] = {'username': user_name, 'password_hash': hashed_password}
            flash("Signup successful! You can now log in.", "success")
            return redirect('/login')
        except Exception as e:
            flash("Signup failed. Please try again.", "error")
    return render_template('login_signup.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check if user is already logged in
    if 'user_id' in session:
        flash("You are already logged in.", "info")
        return redirect('/')  # Redirect to home if the user is already logged in

    if request.method == 'POST':
        email = sanitize_input(request.form['email'])
        password = sanitize_input(request.form['password'])

        # Check if the user exists
        user = users.get(email)
        if not user:
            flash("User does not exist. Please sign up first.", "error")
            return redirect('/signup')

        # Check if the password is correct
        if check_password_hash(user['password_hash'], password):
            session['user_id'] = email  # Store email as user_id
            flash("Login successful!", "success")
            return redirect('/')
        else:
            flash("Invalid credentials. Please try again.", "error")

    return render_template('login_signup.html')

# Form Filling Route
@app.route('/form', methods=['GET', 'POST'])
def form_filling():
    if request.method == 'POST':
        try:
            # Extracting form data
            form_data = {
                'first_name': request.form['firstName'],
                'last_name': request.form['lastName'],
                'father_name': request.form['fatherName'],
                'mother_name': request.form['motherName'],
                'dob': request.form['dob'],
                'gender': request.form['gender'],
                'branch': request.form['branch'],
                'section': request.form['section'],
                'roll_number': request.form['rollNumber'],
                'year_of_study': request.form['yearOfStudy'],
                'percentage': request.form['percentage'],
                'phone': request.form['phone'],
                'email': request.form['email'],
                'blood_group': request.form.get('bloodGroup', ''),
                'address': request.form['address']
            }

            # Store form submission data in the in-memory store
            submissions.append(form_data)

            flash("Student details submitted successfully!", "success")
            return redirect('/success')
        except Exception as err:
            flash("There was an error while submitting the form. Please try again.", "error")
            return redirect('/form')

    return render_template('forms.html')

# Success Page Route
@app.route('/success')
def success_page():
    return render_template('thnx.html')

# Second Page Route
@app.route('/secondpg')
def second_page():
    return render_template('login_signup.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)