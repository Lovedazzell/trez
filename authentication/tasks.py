from celery import shared_task
from django.conf import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


    
@shared_task(bind=True)
def email_token_send(self,email , token):        

        msg = MIMEMultipart()
        msg.set_unixfrom('author')
        msg['From'] = 'Trezunt '+ settings.EMAIL_HOST_USER
        msg['To'] = email
        msg['Subject'] = 'Welcome to Trezent'
      
        html_text = f'<div style="margin-bottom: 13px;background-color: white;padding: 7px 13px;border-radius: 5px;"><h1 style="width: 230px; height: 40px;" >TREZUNT</h1></div> <div style="background-color: white;padding: 7px 20px;border-radius: 5px;"><p> Click on the  below link to verify your account and start your journey to make money. </p><b>  <a href="{settings.HOST}auth/verify/{token}/">{settings.HOST}auth/verify/{token}/</a>   <b> <p>if not received check your span</p></div>'

        simple_msg = MIMEText(html_text, 'html')


        msg.attach(simple_msg)

        mailserver = smtplib.SMTP_SSL('smtpout.secureserver.net', 465)
        mailserver.ehlo()
        mailserver.login(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)

        mailserver.sendmail(settings.EMAIL_HOST_USER,email,msg.as_string())

        mailserver.quit()
       

@shared_task(bind=True)
def email_to_user(self,email,title,html_message):
        msg = MIMEMultipart()
        msg.set_unixfrom('author')
        msg['From'] = 'Trezunt '+ settings.EMAIL_HOST_USER
        msg['To'] = email
        msg['Subject'] = title
      
       
        simple_msg = MIMEText(html_message, 'html')


        msg.attach(simple_msg)

        mailserver = smtplib.SMTP_SSL('smtpout.secureserver.net', 465)
        mailserver.ehlo()
        mailserver.login(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)

        mailserver.sendmail(settings.EMAIL_HOST_USER,email,msg.as_string())

        mailserver.quit() 
        
       