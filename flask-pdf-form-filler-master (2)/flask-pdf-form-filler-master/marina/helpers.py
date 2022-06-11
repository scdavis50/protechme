import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders


def send_email(email, message_type, file):
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.ehlo()
    smtpObj.login('marinathechatbot38@gmail.com', "MarinaIsOurChatbot")

    Applicant_Name = "Marina Chatbot"

    message = MIMEMultipart()
    message['Subject'] = "Protective Order Application: " + Applicant_Name
    message['From'] = 'marinathechatbot38@gmail.com'
    message['Reply-to'] = 'marinathechatbot38@gmail.com'
    message['To'] = email

    text = MIMEText("Here is the completed PO application for: " + Applicant_Name)
    message.attach(text)

    with open(file, "rb") as opened:
        openedfile = opened.read()
    attachedfile = MIMEApplication(openedfile, _subtype = "pdf")
    attachedfile.add_header('content-disposition', 'attachment', filename = "poapplication" + Applicant_Name + ".pdf")
    message.attach(attachedfile)
    smtpObj.sendmail(message['From'], message['To'], message.as_string())

