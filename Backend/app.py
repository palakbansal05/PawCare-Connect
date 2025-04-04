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
    # Start Chatbot.py
    subprocess.Popen(["streamlit","run",CHAT_PATH,"--server.port","8501"],cwd =CHATBOT_DIR,shell=True)
     # Redirect to the Streamlit UI
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

    # Start ex.py
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
    MAIL_PASSWORD="vzhpgykllzqnrysj",  #This password will be deleted after submisssion
    MAIL_DEFAULT_SENDER='pawcareconnect@gmail.com'
)
    mail = Mail(app)
    #Data of NGos(Third Party APIs will be used and more data will be constantly added to the database)
    NGOs ={
    "Noida" : ["info@corpbiz.io", "info@wti.org.in" ,"info@smileindiatrust.org"] ,
    "Lucknow" : ["jeevaashraya@gmail.com", "pyarepanje@gmail.com", "igss.codeaart.com"],
    "Delhi" : ["gandhim@nic.in" , "friendicoes.india@gmail.com" ,"wildlifesos@proton.me", "jeevashram@gmail.com"],
    "Kanpur" : ["kkwaknp@gmail.com", "sevaaurdaan@gmail.com" , "privishafoundation.com"],
    "Meerut" :["support@neemkarolibaba.org.in", "team@weforsociety.org","pawnisinghal.psl@gmail.com"],
    "Varanasi" : ["varanasiforanimals@gmail.com", "animotelcare20@gmail.com" , "grootguardiansociety@gmail.com"],
    "Agra" : ["suratprasad@pfa-agra.org", "kiransetia79@gmail.com", "ekkartavya.dmsc.in"],
    "Prayagraj" : ["gandhim@exmpls.sansad.in" , "raiarchana053@gmail.com", "halina.society@gmail.com"],
    "Jhansi" : ["armsociety0@gmail.com", "aasrasocietyjhansi@gmail.com", "lakshyawelfaresociety2012@gmail.com"]
    }

    # To send emails to the NGOs

    # if Cityname in NGOs:
    #     for ngo_email in NGOs[Cityname]:
    #         msg = Message(
    #             subject="Injured Animal Reported-Immediate Help Needed",
    #             recipients=[ngo_email],
    #             body=message,
    #         )
    #         mail.send(msg)  # This line was missing - actually send the email
            
    #     return("Hurray! The report is sent to the NGO's and Shelter homes.\nThank you so much for your kindness and support.\nThe world needs more people like you.☻")
    # else:
    #     return("This city is still not added to the database yet.Sorry for the inconvenience.")


   # Sending email to a sample mail id
    msg = Message(
        subject="Injured Animal Reported-Immediate Help Needed",
        recipients=["palakbansal5002@gmail.com"],
        body=message,
        )
    try:
        mail.send(msg)
        return ("✅ The report is sent to the NGO's and Shelter homes.\nThank you so much for your kindness and support.\nThe world needs more people like you.☻")
    except Exception as e:
        return ("❌ Error submitting the report")

if __name__=="__main__":
    app.run(debug=True)