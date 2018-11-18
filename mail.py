import sendgrid
import os
import json
import requests
from threading import Timer
from time import time
from email import utils

from flask import Flask, render_template ,request ,url_for ,redirect
app = Flask(__name__)

# Define the api keys you will use and the domain name for mail gun
sendgrid_apiKey= "Your Api Key"
mailGun_domain= "Your Domain name"
mailGun_apiKey= "Your Api Key"


# Function for using SendGrid api
def SendGridAPi(Sender,Reciever,Subject,Content,Send_after):

    if not Content:
        Content=" "

    sg = sendgrid.SendGridAPIClient(apikey=sendgrid_apiKey)
    
    data = {
    "personalizations": [
        {
        "to": [
            {
            "email": Reciever
            }
        ],
        "subject": Subject,

        "send_at": int(time())+Send_after,
        }
    ],
    "from": {
        "email": Sender
    },
    "content": [
        {
        "type": "text/plain",
        "value": Content
        }
    ]
    }
    sg.client.mail.send.post(request_body=data)


# Function using MailGun Api 
def MailGunApi(Sender,Reciever,Subject,Content,Send_after):

    if not Content:
        Content=" "

    return requests.post(
        "https://api.mailgun.net/v3/%s/messages" % mailGun_domain,
        auth=("api", mailGun_apiKey),
        data={"from": "<%s>" % Sender,
              "to": Reciever,
              "subject": Subject,
              "text": Content,
              "o:deliverytime": utils.formatdate( Send_after+int(time())) })


# Routing (Flask) function that connects html with backend code
@app.route('/send', methods=['GET','POST'])
def send():

    if request.method == 'POST': #if the coming request is post method

        # Get the input from the user
        SendAfter=0
        reciever=request.form['to_email']
        sender=request.form['email']
        content=request.form['body']
        subject=request.form['subject']
        hours=int(request.form['hours'])
        minutes=int(request.form['minutes'])


        # Default values for the inputs if the user didn't enter any values
        if not reciever:
            reciever="test@example.com"
        if not sender:
            sender="test@example.com"
        if not subject:
            subject=" "
        if not hours:
            hours=0
        if not minutes:
            minutes=0

        # changing hours and minutes to seconds format for the json file used for the api
        SendAfter=(hours*3600)+(minutes*60)

        # Try mail gun service if failed go to send grid service
        try:

            MailGunApi(sender,reciever,subject,content,SendAfter)

        except:

            SendGridAPi(sender,reciever,subject,content,SendAfter)
                


        return redirect(url_for('send'))

    else:
        return render_template('index.html')



if __name__ == '__main__':
   app.run(debug=True)