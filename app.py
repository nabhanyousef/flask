from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import base64
import cv2
import numpy as np

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key'  # Change this to a secure key in production
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Dummy user database (replace with a real database in production)
users = {}

# Home route
@app.route('/')
def index():
    return redirect(url_for('login'))

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash('Username already exists. Please choose another.', 'error')
        else:
            users[username] = {'password': password}
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')

# Profile route
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Update user profile information
        users[session['username']].update({
            'full_name': request.form['full_name'],
            'age': request.form['age'],
            'weight': request.form['weight'],
            'height': request.form['height']
        })
        return redirect(url_for('camera'))
    
    return render_template('profile.html')

# Camera route
@app.route('/camera', methods=['GET', 'POST'])
def camera():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Get the base64 image data from the form
        image_data = request.form['image']
        image_data = image_data.split(',')[1]  # Remove the "data:image/png;base64," prefix
        
        # Decode the base64 image data
        image_bytes = base64.b64decode(image_data)
        image_array = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        # Save the image
        filename = f"{session['username']}_capture.png"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        cv2.imwrite(filepath, image)
        
        # Update the user's image in the database
        users[session['username']]['image'] = filename
        return redirect(url_for('report'))
    
    return render_template('camera.html')

# Report route
@app.route('/report')
def report():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user = users[session['username']]
    return render_template('report.html', user=user)

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
