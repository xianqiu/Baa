import socket
import json
import time
import sys
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from baa.template import fill_template


def send_mail(sender_conf, receivers, title, content, attachment_paths=None):
    """ 发送邮件.
    :param sender_conf: 发件人以及服务器信息
    :param receivers: 收件人列表(list)
    :param title: 标题
    :param content: 文本内容
    :param attachment_paths: 附件路径(list)
    """
    try:
        server = smtplib.SMTP_SSL(sender_conf['server'], sender_conf['port'])
        server.login(sender_conf['sender'], sender_conf['password'])
        mail = format_mail(sender_conf['sender'], receivers, title, content, attachment_paths)
        server.sendmail(sender_conf['sender'], receivers, mail.as_string())
        server.quit()
    except smtplib.SMTPException as e:
        print('fail', e.args)


def format_mail(sender, receivers, title, content, attachment_paths=None):
    """ 返回邮件对象.

    :param sender: 发件人
    :param receivers: 收件人(list)
    :param title: 标题
    :param content: 文本内容
    :param attachment_paths: 附件路径(list)
    :return: 返回MIMEMultipart对象
    """
    mail = MIMEMultipart()
    mail['From'] = sender
    mail['To'] = ','.join(receivers)
    mail['Subject'] = title
    mail.attach(MIMEText(content, 'plain', 'utf-8'))
    if attachment_paths:
        for path in attachment_paths:
            att = MIMEText(open(path, 'rb').read(), 'base64', 'utf-8')
            att['Content-Type'] = 'application/octet-stream'
            att['Content-Disposition'] = "attachment; filename=%s" % path
            mail.attach(att)
    return mail


def get_host():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def get_script():
    return sys.argv[0]


def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


class Baa(object):

    def __init__(self):
        self.__receivers = []
        self.__title_prefix = '[Baa~ Baa~]'
        self.__title = ""
        self.__sender_conf = None
        default_path = Path(get_script()).parent / 'sender.json'
        if Path(default_path).exists():
            self.set_sender(default_path)

    def add_receiver(self, receiver):
        self.__receivers.append(receiver)

    def set_sender(self, sender_conf_path):
        if not Path(sender_conf_path).exists():
            raise FileNotFoundError("%s does not exist!")
        with open(sender_conf_path, encoding='UTF-8') as f:
            s = f.read()
        self.__sender_conf = json.loads(s, encoding='UTF-8')

    def set_title(self, title):
        self.__title = title

    def send(self, message=""):
        """ 发送提醒.
        """
        if not self.__sender_conf:
            print("[Error] Fail to initialize sender!")
            return
        value_dict = {
            'host': get_host(),
            'script': get_script(),
            'time': get_time()
        }
        content = message + fill_template(value_dict)
        title = self.__title_prefix + self.__title
        send_mail(self.__sender_conf, self.__receivers, title, content)
