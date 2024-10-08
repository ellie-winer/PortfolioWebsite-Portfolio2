from datetime import date
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
ckeditor = CKEditor(app)
Bootstrap5(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///posts.db")

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_USER')

mail = Mail(app)


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template('about.html')

# Contact route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message_content = request.form.get('message')

        # Create an email message
        msg = Message('New Contact Form Submission',
                      recipients=['your-email@example.com'])  # Your email address
        msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message_content}"

        try:
            mail.send(msg)  # Send the email
            flash('Message sent successfully!', 'success')
        except Exception as e:
            print(f"Failed to send email: {e}")
            flash('Failed to send message. Please try again later.', 'danger')

        return redirect(url_for('home'))

    return render_template('contact.html')




if __name__ == "__main__":
    app.run(debug=True)