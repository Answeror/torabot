from email.mime.text import MIMEText
import smtplib
import time


def send(username, password, targets, head, body):
    m = MIMEText(body)
    m['Subject'] = head
    m['From'] = username
    m['To'] = ';'.join(targets)
    m['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(username, targets, m.as_string())
    smtp.quit()


def send_notice(conf, target, body):
    send(
        conf['TORABOT_EMAIL_USERNAME'],
        conf['TORABOT_EMAIL_PASSWORD'],
        [target],
        conf['TORABOT_EMAIL_HEAD'],
        body,
    )
