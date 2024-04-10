import os
import smtplib 
from email.message import EmailMessage

EMAIL_ADDRESS = "gjkkunwar07@gmail.com"
EMAIL_PASSWORD = "slgr nstm wrwv rsxb"

def send_email(email):
    msg = EmailMessage()
    msg['Subject'] = 'Welcome to Library Management System  '
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email 

    # HTML content
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f2f2f2;
                text-align: center;
                padding: 50px;
            }
            h1 {
                color: #4CAF50;
                font-size: 24px;
            }
            p {
                font-size: 18px;
                margin-top: 20px;
                color: #333;
            }
            .emoji {
                font-size: 36px;
            }
        </style>
    </head>
    <body>
        <h1>Congratulations ! 🎉</h1>
        <p>You are successfully registered !</p>
    </body>
    </html>
    """

    
    msg.add_alternative(html_content, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
    