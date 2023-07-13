import smtplib
import configparser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load the configuration file
config = configparser.ConfigParser()
config.read('credentials.ini')

def send_email_notification(subject, body, to_address):
    """
    Function to send an email notification.
    """
    from_address = config.get('credentials', 'email')
    from_password = config.get('credentials', 'password')

    # Setup the email
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_address, from_password)
        text = msg.as_string()
        server.sendmail(from_address, to_address, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Error occurred while sending email: {str(e)}")

