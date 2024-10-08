from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import numpy as np
import joblib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Initialize the database
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Call init_db to ensure database is ready
init_db()

# Load pre-trained models and scalers
try:
    maternal_model = joblib.load("model/best_xgb_model.pkl")
    fetal_model = joblib.load("model/fetal_health_classifier_main.joblib")
    maternal_scaler = joblib.load("model/scaler21.joblib")
    fetal_scaler = joblib.load("model/scaler.joblib")
except FileNotFoundError as e:
    print(f"Model files not found: {e}. Please ensure that the models are located in the 'model' directory.")
    exit()

def query_db(query, args=(), one=False):
    conn = sqlite3.connect('users.db')
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash('Username and password are required.')
            return redirect(url_for('signup'))
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        existing_user = query_db('SELECT * FROM users WHERE username = ?', [username], one=True)
        if existing_user:
            flash('Username already exists')
            return redirect(url_for('signup'))
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()
        flash('Signup successful. You can now login.')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash('Username and password are required.')
            return redirect(url_for('login'))
        
        user = query_db('SELECT * FROM users WHERE username = ?', [username], one=True)
        if user and check_password_hash(user[2], password):
            session['username'] = username
            flash('Login successful')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/')
def index():
    if 'username' not in session:
        flash('You need to login first.')
        return redirect(url_for('login'))
    
    return render_template('index.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/predict_maternal', methods=['GET', 'POST'])
def predict_maternal():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            age = float(request.form['age'])
            systolicBP = float(request.form['systolicBP'])
            diastolicBP = float(request.form['diastolicBP'])
            BS = float(request.form['BS'])
            bodyTemp = float(request.form['bodyTemp'])
            heartRate = float(request.form['heartRate'])

            # Make prediction
            input_features = np.array([[age, systolicBP, diastolicBP, BS, bodyTemp, heartRate]])
            input_features_scaled = maternal_scaler.transform(input_features)
            predicted_risk = maternal_model.predict(input_features_scaled)
            
            if predicted_risk[0] == 0:
                result = "Low Risk"
                color = "green"
            elif predicted_risk[0] == 1:
                result = "Medium Risk"
                color = "orange"
            else:
                result = "High Risk"
                color = "red"

            return render_template('maternal.html', prediction=result, color=color)

        except ValueError:
            flash("Please enter valid numeric values.")
            return render_template('maternal.html', error="Please enter valid numeric values.")

    return render_template('maternal.html')

@app.route('/predict_fetal', methods=['GET', 'POST'])
def predict_fetal():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            input_values = [float(request.form[key]) for key in [
                'BaselineValue', 'Accelerations', 'FetalMovement', 'UterineContractions', 'LightDecelerations', 
                'SevereDecelerations', 'ProlonguedDecelerations', 'AbnormalShortTermVariability',
                'MeanValueOfShortTermVariability', 'PercentageOfTimeWithAbnormalLongTermVariability',
                'MeanValueOfLongTermVariability', 'HistogramWidth', 'HistogramMin', 'HistogramMax', 
                'HistogramNumberOfPeaks', 'HistogramNumberOfZeroes', 'HistogramMode', 'HistogramMean', 
                'HistogramMedian', 'HistogramVariance', 'HistogramTendency'
            ]]
            
            # Make prediction
            input_features = np.array([input_values])
            input_features_scaled = fetal_scaler.transform(input_features)
            predicted_health = fetal_model.predict(input_features_scaled)

            if predicted_health[0] == 1:
                result = "Normal : The Fetus is Normal and healthy"
                color = "green"
                
            elif predicted_health[0] == 2:
                result = "Suspect : The Fetus needs monitoring"
                color = "orange"
            else:
                result = "Pathological : The Fetus is at High Risk"
                color = "red"

            return render_template('fetal.html', prediction=result, color=color)

        except ValueError:
            flash("Please enter valid numeric values.")
            return render_template('fetal.html', error="Please enter valid numeric values.")

    return render_template('fetal.html')

if __name__ == '__main__':
    app.run(debug=True)
