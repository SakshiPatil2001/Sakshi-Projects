# Import necessary libraries
# Flask: for building the web application
# joblib: to load the trained model
# pandas: for handling data in DataFrame format
# mysql.connector: to connect to the MySQL database
from flask import Flask, render_template, request
import joblib
import pandas as pd
import mysql.connector

# Initialize the Flask app
app = Flask(__name__)

# Load the trained Zomato price prediction model
model = joblib.load(r'C:\Users\saksh\OneDrive\Desktop\zomato-price-prediction\models\zomato_price_predictor.pkl')

# Configure MySQL database connection
# Connecting to the 'zomato_db' MySQL database hosted locally
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sakshi@01",
    database="zomato_db"
)

# Define the index route, which handles both GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve form data: rating, votes, and whether the restaurant is vegetarian
        rating = float(request.form['rating'])
        votes = int(request.form['votes'])
        is_veg = 1 if request.form['is_veg'] == 'Yes' else 0

        # Prepare the input data for the model prediction
        # The data is structured into a DataFrame with columns 'rating', 'votes', and 'is_veg'
        data = pd.DataFrame([[rating, votes, is_veg]], columns=['rating', 'votes', 'is_veg'])

        # Use the trained model to predict the price based on the input data
        predicted_price = model.predict(data)[0]

        # Insert the prediction result into the MySQL database
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO predictions (rating, votes, is_veg, predicted_price) VALUES (%s, %s, %s, %s)",
            (rating, votes, is_veg, predicted_price)
        )
        db.commit()  # Commit the transaction to save the data
        cursor.close()  # Close the database cursor

        # Render the index.html template and pass the predicted price for display
        return render_template('index.html', prediction=predicted_price)

    # For GET requests, simply render the index.html template
    return render_template('index.html')

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)

 


