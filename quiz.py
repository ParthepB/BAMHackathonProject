from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Store answers in memory (for demo; use a database for production)
user_answers = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/career-quiz', methods=['POST'])
def career_quiz():
    career_type = request.form.get('career_type')
    # Store or process the answer as needed
    user_answers['career_type'] = career_type
    # Redirect to a follow-up question or results page
    return render_template('quiz_result.html', career_type=career_type)

if __name__ == "__main__":
    app.run(debug=True)