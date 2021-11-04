# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 21:36:06 2021

@author: Admin (Andrés Felipe Escallón Portilla)
"""

from flask import Flask
import os
from twilio.rest import Client
from flask import request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

@app.route("/")
def inicio():
    test = os.environ.get("Test")
    return test

@app.route("/sms")
def sms():
    try:
        # Your Account Sid and Auth Token from twilio.com/console
        # and set the environment variables. See http://twil.io/secure
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        origen = os.environ['TELEFONO_ORIGEN']
        client = Client(account_sid, auth_token)
        contenido = request.args.get("mensaje")
        destino = request.args.get("telefono")
        message = client.messages \
                        .create(
                             body=contenido,
                             from_= origen,
                             to='+57' + destino
                         )
        
        print(message.sid)
        return "Enviado correctamente"
    except Exception as e:
        print(e)
        return "Error enviando el mensaje"
    

@app.route("/envio-correo")
def email():
    
    destino = request.args.get("correo_destino")
    asunto = request.args.get("asunto")
    mensaje = request.args.get("contenido")
    origen = os.environ['EMAIL_ORIGEN']
    
    message = Mail(
    
    from_email=origen,
    to_emails=destino,
    subject=asunto,
    html_content=mensaje)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return "Correo electrónico enviado"
    except Exception as e:
        print(e.message)
        return "Error enviando el mensaje"


if __name__ == '__main__':
    app.run()