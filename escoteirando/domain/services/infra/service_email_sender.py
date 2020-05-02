import smtplib

from escoteirando.ext.configs import Configs
from ..base_service import BaseService


class ServiceEmailSender(BaseService):
    LOG_INFO = 'ServiceEmailSender'

    def __init__(self, db):
        super().__init__(db)
        self.config: Configs = Configs.Instance()
        self.log.info('INIT %s', self.LOG_INFO)

    def is_valid_config(self):
        return bool(self.config.MAIL_SERVER and
                    self.config.MAIL_PORT and
                    self.config.MAIL_USERNAME and
                    self.config.MAIL_PASSWORD)

    def send_mail(self, to: str, subject: str, body: str, **kwargs) -> bool:
        # TODO: https://docs.python.org/3/library/email.examples.html
        if not self.is_valid_config():
            self.log.error('%s: INVALID SETUP', self.LOG_INFO)
            return False
        try:
            FROM = self.config.MAIL_USER_FROM
            TO = to if isinstance(to, list) else [to]
            SUBJECT = subject
            TEXT = body
            CCO = '' if 'CCO' not in kwargs else f'Cco: {kwargs["CCO"]}\n'
            # Prepare actual message
            message = "From: {0}\nTo: {1}\n{2}Subject: {3}\n\n{4}".format(
                FROM,
                CCO,
                ", ".join(TO),
                SUBJECT,
                TEXT
            )
            if self.config.MAIL_USE_SSL:
                # SMTP_SSL Example
                server = smtplib.SMTP_SSL(
                    self.config.MAIL_SERVER,
                    self.config.MAIL_PORT)
            else:
                server = smtplib.SMTP('{0}:{1}'.format(
                    self.config.MAIL_SERVER,
                    self.config.MAIL_PORT))
                if self.config.MAIL_USE_TLS:
                    server.ehlo()
                    server.starttls()
            server.login(self.config.MAIL_USERNAME, self.config.MAIL_PASSWORD)
            server.sendmail(FROM, TO, message)
            if self.config.MAIL_USE_SSL:
                server.quit()
            server.close()
            self.log.info('%s: Email [%s] sent to [%s]',
                          self.LOG_INFO, subject, to)
            return True
        except Exception as exc:
            self.log.exception(
                '%s: ERROR ON SENDING EMAIL %s', self.LOG_INFO, exc)
        return False
