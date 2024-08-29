from ._mailer import Lmi

class TmpMail():
    def __init__(self, email: str = None,  password: str = None):
        self.email = email
        self.password = password
    def domainsAvl(self):
        return Lmi().domains()
    def create(self):
        return Lmi().register(email=self.email, password=self.password)
    def login(self):
        return Lmi().get_token(self.email, self.password)
    def check_sms(self, auth, page):
        return Lmi().get_sms(auth, page)

obj = TmpMail(email='caroleeaquamarine@filmla.org', password='80qQsb>D|Q')
token = obj.login()
print(token)
sms = obj.check_sms(token, 1)
print(sms)