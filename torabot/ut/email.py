import smtplib
from uuid import uuid4
from email import encoders
from email.header import Header
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, formatdate, COMMASPACE
from logbook import Logger
import mimetypes


ENCODING = 'utf-8'
log = Logger(__name__)


class EmailLoginError(Exception):
    pass


def pack(
    sender_addr,
    recipient_addrs,
    subject,
    text=None,
    attachments=[],
    sender_name=None,
    html=None
):
    if sender_name is None:
        sender_name = sender_addr
    sender_name = Header(sender_name, ENCODING).encode()

    msg_root = MIMEMultipart('mixed')
    msg_root['date'] = formatdate()
    msg_root['From'] = formataddr((sender_name, sender_addr))
    msg_root['To'] = COMMASPACE.join(recipient_addrs)
    msg_root['Subject'] = Header(subject, ENCODING)
    msg_root.preamble = 'This is a multi-part message in MIME format.'

    msg_related = MIMEMultipart('related')
    msg_root.attach(msg_related)

    msg_alternative = MIMEMultipart('alternative')
    msg_related.attach(msg_alternative)

    if text:
        msg_text = MIMEText(text, 'plain', ENCODING)
        msg_alternative.attach(msg_text)

    if html:
        msg_html = MIMEText(html, 'html', ENCODING)
        msg_alternative.attach(msg_html)

    for child in format_attachments(attachments):
        msg_related.attach(child)

    return msg_root


def _send(
    sender_addr,
    password,
    recipient_addrs,
    subject,
    text=None,
    attachments=[],
    sender_name=None,
    html=None,
    save=False,
    host='smtp.gmail.com',
    port=587
):
    msg_root = pack(
        sender_addr=sender_addr,
        recipient_addrs=recipient_addrs,
        subject=subject,
        text=text,
        attachments=attachments,
        sender_name=sender_name,
        html=html,
    )

    if port is None:
        smtp = smtplib.SMTP(host)
    else:
        smtp = smtplib.SMTP(host, port)

    smtp.ehlo()

    try:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(sender_addr, password)
    except smtplib.SMTPException as e:
        if 'SMTP AUTH extension not supported by server.' in str(e):
            # not auth required
            pass
        else:
            raise EmailLoginError('email login failed') from e

    smtp.send_message(msg_root)
    smtp.quit()

    if save:
        return msg_root.as_string()


def get_attachment_data(a):
    data = a.get('data')
    if data is None:
        with open(a.path, 'rb') as f:
            data = f.read()
    return data


def guess_extension(mime):
    ext = mimetypes.guess_extension(mime)
    # 163 mail not recognize .jpe
    # for why jpe:
    # http://stackoverflow.com/a/11396288/238472
    return '.jpeg' if ext == '.jpe' else ext


def get_attachment_name(a):
    name = a.get('name')
    if name is None:
        if 'path' in a:
            name = os.path.basename(a.path)
        else:
            name = str(uuid4())
    ext = guess_extension(get_mime(a)) or ''
    return name + ext


def get_mime(a):
    return a.get('mime', 'application/octet-stream')


def format_attachments(attachments):
    for a in attachments:
        maintype, subtype = get_mime(a).split('/', 1)
        data = get_attachment_data(a)
        if maintype == 'text':
            # Note: we should handle calculating the charset
            msg = MIMEText(data.decode(ENCODING), subtype, ENCODING)
        elif maintype == 'image':
            msg = MIMEImage(data, subtype)
        elif maintype == 'audio':
            msg = MIMEAudio(data, subtype)
        else:
            msg = MIMEBase(maintype, subtype)
            msg.set_payload(data)
            # Encode the payload using Base64
            encoders.encode_base64(msg)
        # Set the filename parameter
        msg.add_header(
            'Content-Disposition',
            'attachment',
            filename=Header(get_attachment_name(a), ENCODING).encode()
        )
        yield msg


def _send_conf(
    conf,
    recipient_addrs,
    subject,
    text=None,
    attachments=[],
    sender_name=None,
    html=None,
    save=False
):
    if conf['TORABOT_DEBUG']:
        log.debug('send email {} to {}', subject, recipient_addrs)
        return
    return _send(
        sender_addr=conf['TORABOT_EMAIL_USERNAME'],
        password=conf['TORABOT_EMAIL_PASSWORD'],
        recipient_addrs=recipient_addrs,
        subject=subject,
        text=text,
        attachments=attachments,
        sender_name=sender_name,
        html=html,
        save=save,
        host=conf['TORABOT_EMAIL_HOST'],
        port=conf['TORABOT_EMAIL_PORT'],
    )


def send(
    recipient_addrs,
    subject,
    text=None,
    attachments=[],
    sender_name=None,
    html=None,
    save=False
):
    from .local import local
    return _send_conf(
        local.conf,
        recipient_addrs=recipient_addrs,
        subject=subject,
        text=text,
        attachments=attachments,
        sender_name=sender_name,
        html=html,
        save=save
    )


def async_send(
    recipient_addrs,
    subject,
    text=None,
    attachments=[],
    sender_name=None,
    html=None,
    save=False
):
    from .async_local import local
    return _send_conf(
        local.conf,
        recipient_addrs=recipient_addrs,
        subject=subject,
        text=text,
        attachments=attachments,
        sender_name=sender_name,
        html=html,
        save=save
    )


if __name__ == '__main__':
    import os
    from .bunch import Bunch
    from .local import local
    _send(
        recipient_addrs=['answeror@gmail.com'],
        subject=local.conf['TORABOT_EMAIL_HEAD'],
        text='测试中文',
        attachments=[Bunch(
            path=os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                'nerv.png'
            ),
            mime='image/png',
            name='例大祭11カット'
        )]
    )
