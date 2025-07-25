from flask import Flask, render_template, redirect, url_for, request, jsonify, send_file
from quiz import process_career_quiz
from rmaker import generate_full_resume, generate_resume_pdf
import io

app = Flask(__name__)

@app.route('/')
def index():
    """Redirect to form.html when website is first accessed"""
    return redirect(url_for('form'))

@app.route('/form')
def form():
    """Display login/signup form"""
    return render_template('form.html')

@app.route('/home')
def home():
    """Display home page"""
    return render_template('home.html')

@app.route('/features')
def features():
    """Display features page"""
    return render_template('features.html')

@app.route('/about')
def about():
    """Display about page"""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """Display contact page"""
    return render_template('contact.html')

@app.route('/settings')
def settings():
    """Display settings page"""
    return render_template('settings.html')

@app.route('/rmaker')
def rmaker():
    """Display resume maker page"""
    return render_template('rmaker.html')

@app.route('/rgrader')
def rgrader():
    """Display resume grader page"""
    return render_template('rgrader.html')

@app.route('/mock')
def mock():
    """Display mock interview bot page"""
    return render_template('mock.html')

@app.route('/career-quiz', methods=['GET', 'POST'])
def career_quiz():
    """Display career quiz page"""
    return render_template('career-quiz.html')

@app.route('/submit-quiz', methods=['POST'])
def submit_quiz():
    """Handle career quiz submission and return recommendations"""
    try:
        data = request.get_json()
        career_type = data.get('career_type')
        answers = data.get('answers', {})
        
        # Process the quiz using our backend logic
        recommendations = process_career_quiz(career_type, answers)
        
        return jsonify(recommendations)
    
    except Exception as e:
        # Return error response
        return jsonify({
            'error': 'Failed to process quiz',
            'message': str(e)
        }), 500

@app.route('/api/generate-resume', methods=['POST'])
def generate_resume_api():
    """Handle resume generation and return JSON response"""
    try:
        user_data = request.get_json()
        print(f"Received user data: {user_data}")
        
        # Generate the resume
        resume = generate_full_resume(user_data)
        print(f"Generated resume: {resume}")
        
        return jsonify({
            'success': True,
            'resume': resume
        })
        
    except Exception as e:
        print(f"Error in generate_resume_api: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/download-resume-pdf', methods=['POST'])
def download_resume_pdf():
    """Generate and download resume as PDF"""
    try:
        user_data = request.get_json()
        print(f"Generating PDF for user data: {user_data}")
        
        # Generate the resume data
        resume = generate_full_resume(user_data)
        
        # Generate PDF
        pdf_content = generate_resume_pdf(resume)
        
        # Create a file-like object
        pdf_buffer = io.BytesIO(pdf_content)
        pdf_buffer.seek(0)
        
        # Get the user's name for filename, or use default
        filename = f"{resume['personal_info'].get('name', 'Resume').replace(' ', '_')}_Resume.pdf"
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/quiz-result')
def quiz_result():
    """Display quiz result page"""
    return render_template('quiz-result.html')

@app.route('/logout')
def logout():
    """Handle logout by redirecting to form with JavaScript to clear localStorage"""
    return '''
    <script>
        localStorage.removeItem("currentUser");
        window.location.href = "/form";
    </script>
    '''

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
