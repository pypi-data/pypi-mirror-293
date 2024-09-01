import smtplib
import socket


def smtp_verify_email(mx_record, email):
    """
    Performs SMTP verification for the given email address.
    
    Args:
        mx_record (str): The MX record of the domain.
        email (str): The email address to verify.
        
    Returns:
        dict: Contains 'status' and 'message' indicating the result of the verification.
    """

    try:
        with smtplib.SMTP(mx_record, timeout=5) as server:
            # server.set_debuglevel(1)
            server.helo()  # Greet the server
            server.mail('test@packagehandler.com')  # Specify the sender's email
            code, message = server.rcpt(email)  # Attempt to send to the recipient's email
        
        # Check SMTP response code
        if code == 250:
            return {"status": "200", "message": "Valid email"}
        elif code == 550:
            if "blocked using Spamhaus" in str(message):
                return {"status": "502", "message": "Your IP address is blocked by Spamhaus. Please check your IP and try again."}
            return {"status": "400", "message": "Invalid email: The mailbox is unavailable"}
        elif code == 450:
            return {"status": "400", "message": "Temporary failure: Mailbox is unavailable"}
        elif code == 421:
            return {"status": "500", "message": "Service not available: The server is down or overloaded"}
        elif code == 451:
            return {"status": "500", "message": "Server error: The action was aborted"}
        else:
            return {"status": "400", "message": f"Unexpected SMTP response code {code}"}
    except KeyboardInterrupt:
        return {"status": "500", "message": "Operation interrupted by user."}
    except smtplib.SMTPRecipientsRefused:
        return {"status": "400", "message": "Recipient refused. The email might be blocked or invalid."}
    except smtplib.SMTPDataError:
        return {"status": "400", "message": "SMTP Data Error. The email might be blocked or invalid."}
    except smtplib.SMTPConnectError:
        return {"status": "500", "message": "SMTP Connect Error. Could not connect to the mail server."}
    except smtplib.SMTPHeloError:
        return {"status": "500", "message": "SMTP HELO Error. The server did not respond properly."}
    except smtplib.SMTPException as e:
        return {"status": "500", "message": f"SMTP Error: {e}"}
    except socket.error as e:
        return {"status": "500", "message": f"Socket Error: {e}"}
