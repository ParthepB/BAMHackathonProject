from flask import Flask, render_template, redirect, url_for

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

@app.route('/quiz-result')
def quiz_result():
    """Display quiz results page"""
    return render_template('quiz_result.html')

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
