from django.core.mail import EmailMessage


import threading
import random
import string


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        EmailThread(email).start()

    def random_number():
        return random.randint(100000, 999999)
        
    def random_string(length):
        return ''.join((random.choice(string.ascii_uppercase) for x in range(length)))
