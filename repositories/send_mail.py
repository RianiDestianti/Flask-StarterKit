import os
import threading
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(email, name, subject, html):
    """Kirim email di background thread (tidak menahan response, seperti di Bun)."""
    threading.Thread(target=_send, args=(email, subject, html), daemon=True).start()


def _send(email, subject, html):
    try:
        if not os.getenv('SENDGRID_API_KEY'):
            raise ValueError('SENDGRID_API_KEY belum diisi')

        message = Mail(
            from_email   = os.getenv('MAIL_FROM', ''),
            to_emails    = email,
            subject      = subject,
            html_content = html,
        )

        SendGridAPIClient(os.getenv('SENDGRID_API_KEY')).send(message)
        print('[mail] Email berhasil dikirim!')
    except Exception as error:
        print('[mail] Gagal kirim email:', getattr(error, 'body', None) or error)


def template_mail(greeting, content, button, url, closing):
    button_html = f"""
                                    <tr>
                                        <td style="padding: 40px 35px; text-align: center;">
                                            <a href="{url}" style="border-radius: 4px; color: #fff; padding: 8px 18px; text-decoration: none; background-color: #2d3748;"
                                            target="_blank" rel="noopener">{button}</a>
                                        </td>
                                    </tr>""" if button else ''

    message = f"""
        <table cellspacing="0" border="0" cellpadding="0" width="100%" bgcolor="#f2f3f8" style="font-family: Open Sans, sans-serif;">
            <tr>
                <td>
                    <table style="background-color: #f2f3f8; max-width:670px; margin:0 auto;" width="100%" border="0"
                        align="center" cellpadding="0" cellspacing="0">
                        <tr>
                            <td style="height:50px;">&nbsp;</td>
                        </tr>
                        <tr>
                            <td>
                                <table width="95%" border="0" cellpadding="0" cellspacing="0"
                                    style="max-width:670px; background:#fff; border-radius:3px; box-shadow:0 6px 18px 0 rgba(0,0,0,.06);">
                                    <tr>
                                        <td style="height:40px;">&nbsp;</td>
                                    </tr>
                                    <tr>
                                        <td style="padding:0 35px;">
                                            <p style="font-size:15px; color:#455056; margin:8px 0 0; line-height:24px;"><b>{greeting}</b></p>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding:0 35px;">
                                            <p style="font-size:15px; color:#455056; margin:8px 0 0; line-height:24px;">{content}</p>
                                        </td>
                                    </tr>{button_html}
                                    <tr>
                                        <td style="padding:0 35px;">
                                            <p style="font-size:15px; color:#455056; margin:8px 0 0; line-height:24px;">{closing}</p>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="height:40px;">&nbsp;</td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td style="height:80px;">&nbsp;</td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>"""

    return message
