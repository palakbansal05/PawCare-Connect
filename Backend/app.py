from flask import Flask,render_template,request,redirect
from flask_cors import CORS
import subprocess
import time
from flask_mail import Mail, Message
app=Flask(__name__)
CORS(app)
CHAT_PATH=r"C:\Users\Jpd\Desktop_New\CodeForge\Chatbot\Chatbot.py"
SERVER_PATH = r"C:\Users\Jpd\Desktop_New\CodeForge\ChatSystem\server.py"
EX_PATH = r"C:\Users\Jpd\Desktop_New\CodeForge\ChatSystem\ex.py"
CHATBOT_DIR=r"C:\Users\Jpd\Desktop_New\CodeForge\Chatbot"

@app.route("/")
def main():
    subprocess.Popen(["streamlit","run",CHAT_PATH,"--server.port","8501"],cwd =CHATBOT_DIR,shell=True)
    return redirect("http://localhost:8501")

@app.route("/About_us")
def login():
    return render_template("About_us.html")
@app.route("/report")
def report():
    return render_template("Report.html")
@app.route("/real-timechat")
def chat():
    # Start server.py
    subprocess.Popen(["python", SERVER_PATH], shell=True)
    time.sleep(2)  # Wait 2 seconds to ensure the server starts properly

    # Start x.py
    subprocess.Popen(["streamlit", "run", EX_PATH, "--server.port", "8502"], shell=True)

    # Redirect to the Streamlit UI
    return redirect("http://localhost:8502")

@app.route("/submit-report",methods=["POST"])
def submit_report():
    Cityname=request.form.get("Cityname")
    description=request.form.get("description")
    location=request.form.get("location")
    message="Injured Animal Report 📢 "
    message+="\n\nLocation: " + location
    message+="\n\n City: " + Cityname
    if description:
        message+="\n\nThe state of Animal: " + description
    app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='pawcareconnect@gmail.com',
    MAIL_PASSWORD="vzhpgykllzqnrysj",
    MAIL_DEFAULT_SENDER='pawcareconnect@gmail.com'
)
   # Sending email to a sample mail id
    mail = Mail(app)
    msg = Message(
        subject="Injured Animal Reported-Immediate Help Needed",
        recipients=["palakbansal5002@gmail.com"],
        body=message,
        )

    try:
        mail.send(msg)
        return ("Hurrray! The report is sent to the NGO's and Shelter homes.\nThank you so much for your kindness and support.\nThe world needs more people like you.☻")
    except Exception as e:
        return f"❌ Error submitting the report"

if __name__=="__main__":
    app.run(debug=True)