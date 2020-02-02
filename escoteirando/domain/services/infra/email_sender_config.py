from escoteirando.ext.logging import get_logger


class EmailSenderConfig:
    LOG = get_logger()

    def __init__(self, fromStr: str = None):

        self.SenderName: str = None
        self.SenderEmail: str = None
        self.SMTPHost: str = None
        self.SMTPPort: int = 0
        self.UserName: str = None
        self.Password: str = None
        self.UseSSL: bool = False
        self.UseTLS: bool = False

    def to_dict(self):
        json = {
            "sn": self.SenderName,
            "se": self.SenderEmail,
            "sh": self.SMTPHost,
            "sp": self.SMTPPort,
            "un": self.UserName,
            "pw": self.Password,
            "us": self.UseSSL,
            "ut": self.UseTLS
        }
        return json

    def from_dict(self, d: dict):
        try:
            sn = d['sn']
            se = d['se']
            sh = d['sh']
            sp = d['sp']
            un = d['un']
            pw = d['pw']
            us = d['us']
            ut = d['ut']
            self.SenderName = sn
            self.SenderEmail = se
            self.SMTPHost = sh
            self.SMTPPort = sp
            self.UserName = un
            self.Password = pw
            self.UseSSL = us
            self.UseTLS = ut
            return True
        except Exception as exc:
            self.LOG.exception("EmailSenderConfig invalid data: %s", exc)
            return False
