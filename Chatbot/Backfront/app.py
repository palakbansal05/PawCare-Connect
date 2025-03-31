from flask import Flask,render_template,request
from flask_cors import CORS
app=Flask(__name__)
CORS(app)
@app.route("/")
def main():
    return "server running"
@app.route("/About_us")
def login():
    return render_template("About_us.html")
@app.route("/report")
def report():
    return render_template("Report.html")
@app.route("/submit-report",methods=["POST"])
def submit_report():
    description=request.form.get("description")
    location=request.form.get("location")
    image=request.form.get("image")
    message="Injured Animal Report"
    message+="\n Location:" + location
    if description:
        message+="The state of dog:" + description
    if image:
        message+="Image of the animal" + image
       
    return ("Hurrray! The report is sent to the NGO's and Shelter homes.\nThank you so much for your kindness and support.\nThe world needs more people like you.☻")
@app.route("/real-timechat")
def chat():
    return render_template("Chat.html")   
if __name__=="__main__":
    app.run(debug=True)