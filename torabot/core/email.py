import smtplib
import time
from uuid import uuid4
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


COMMASPACE = ', '


def send(username, password, targets, head, body, attachments=[]):
    attachments = list(attachments)
    if not attachments:
        m = MIMEText(body)
    else:
        m = MIMEMultipart()
        m.attach(MIMEText(body))
        for child in format_attachments(attachments):
            m.attach(child)

    m['Subject'] = head
    m['From'] = username
    m['To'] = COMMASPACE.join(targets)
    m['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(username, targets, m.as_string())
    smtp.quit()


def get_attachment_data(a):
    data = a.get('data')
    if data is None:
        with open(a.path, 'rb') as f:
            data = f.read()
    return data


def get_attachment_name(a):
    name = a.get('name')
    if name is None:
        if 'path' in a:
            name = os.path.basename(a.path)
        else:
            name = str(uuid4())
    return name


def format_attachments(attachments):
    for a in attachments:
        maintype, subtype = a.get('mime', 'application/octet-stream').split('/', 1)
        data = get_attachment_data(a)
        if maintype == 'text':
            # Note: we should handle calculating the charset
            msg = MIMEText(data.decode('utf-8'), _subtype=subtype)
        elif maintype == 'image':
            msg = MIMEImage(data, _subtype=subtype)
        elif maintype == 'audio':
            msg = MIMEAudio(data, _subtype=subtype)
        else:
            msg = MIMEBase(maintype, subtype)
            msg.set_payload(data)
            # Encode the payload using Base64
            encoders.encode_base64(msg)
        # Set the filename parameter
        msg.add_header(
            'Content-Disposition',
            'attachment',
            filename=get_attachment_name(a)
        )
        yield msg


if __name__ == '__main__':
    import os
    from ..ut.bunch import Bunch
    from .. import make
    app = make()
    conf = app.config
    send(
        conf['TORABOT_EMAIL_USERNAME'],
        conf['TORABOT_EMAIL_PASSWORD'],
        ['answeror@gmail.com'],
        conf['TORABOT_EMAIL_HEAD'],
        'test torabot email',
        [Bunch(
            path=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'nerv.png'),
            mime='application/image'
        )],
    )
