from core.messages import Messages
from core.utils import Util


class RegistrationEmail():
    def send(self):
        email = self.get('email')
        otp = self.get('plain_otp')
        subject = Messages.messages(1)
        email_body = f"Hi ,\n\nGreetings! \n\n \
            You are just a step away from accessing your account \n \n \
            We are sharing a verification code to access your account. The code is valid for 10 minutes and usable only once.\n \
            \n \
            Your OTP   :  {otp} \n \
            Expires in   :  10 minutes \n\n \
            Best Regards,"

        data = {'email_body': email_body, 'to_email': email,
                'email_subject': subject}
        Util.send_email(data)
