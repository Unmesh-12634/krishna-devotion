from flask import Flask, render_template, request
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

db = mysql.connector.connect(
    host=os.environ.get("DB_HOST"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    database=os.environ.get("DB_NAME")
)
cursor = db.cursor(dictionary=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        rating = request.form['rating']

        cursor.execute("INSERT INTO Feedback (name, feedback, rating) VALUES (%s, %s, %s)",
                       (name, message, rating))
        db.commit()

    cursor.execute("SELECT name, feedback AS message, rating, date_submitted FROM Feedback ORDER BY date_submitted DESC")

    feedbacks = cursor.fetchall()
    return render_template('6thfeedback.html', feedbacks=feedbacks)

@app.route('/thanks')
def thanks():
    return "Thank you for your feedback!"

@app.route('/feedbacks')
def feedbacks():
    cursor.execute("SELECT name, feedback AS message, rating, date_submitted FROM Feedback")
    data = cursor.fetchall()
    return render_template('view_feedback.html', feedbacks=data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)  # Port 10000 is good for Render
