
import smtplib
import socket


def check_catch_all(mx_record, domain):
    """
    Check if the domain is a catch-all by attempting to verify multiple random emails.
    """
    test_emails = [
        f"random1@{domain}",
        f"random2@{domain}",
        f"random3@{domain}",
    ]
    
    try:
        with smtplib.SMTP(mx_record, timeout=5) as server:
            server.helo()
            server.mail('test@packagehandler.com')
            results = []
            for email in test_emails:
                code, message = server.rcpt(email)
                results.append(code == 250)
            if all(results):
                return True
            else:
                return False
    except (smtplib.SMTPException, socket.error) as e:
        return False
