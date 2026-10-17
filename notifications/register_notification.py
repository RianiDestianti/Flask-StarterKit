import os
from urllib.parse import quote
from repositories.send_mail import send_email, template_mail


class RegistrationNotification:
    def send(self, email, name, token):
        url      = self._url(name, email, token)
        button   = self._button()
        greeting = self._greeting(name)
        content  = self._content(token)
        closing  = self._closing()

        subject  = 'Kode Verifikasi Pendaftaran Anda!'
        html     = template_mail(greeting, content, button, url, closing)

        send_email(email, name, subject, html)

    def _url(self, name, email, token):
        return f"{os.getenv('FRONTEND_URL', '')}/verification?name={quote(name)}&email={quote(email)}&token={quote(token)}"

    def _button(self):
        return ''

    def _greeting(self, firstname):
        return f"Halo {firstname}!"

    def _content(self, otp):
        return f"""Terima kasih telah mendaftar. <br><br>
        Untuk menyelesaikan proses registrasi, silakan masukkan kode verifikasi (OTP) berikut:<br><br>
        <center><strong style="font-size: 22px; letter-spacing: 2px;text-align: center;">{otp}</strong></center><br><br>
        Kode ini hanya berlaku selama 5 menit. Jangan bagikan kode ini kepada siapa pun."""

    def _closing(self):
        return "Harap jangan ragu untuk menghubungi kami jika Anda memiliki pertanyaan.<br>"


registration_notification = RegistrationNotification()
