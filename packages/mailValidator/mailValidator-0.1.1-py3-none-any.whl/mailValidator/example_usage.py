import time
from threading import Thread
from mailValidator.utils.logger import get_logger
from mailValidator.email_utils import verify_email, verify_emails_list


logger = get_logger(__name__)
# Example usage

# ================ START: 1 =============
# ========================================
# custom_config = {
#     "blacklisted_domains": ["example.com"],
#     "whitelisted_domains": ["trusted.com"],
#     "blacklisted_emails": ["blocked@example.com"],
#     "whitelisted_emails": ["allowed@example.com"]
# }

# emails = ["anu.t@mitsogo.com", "test@example.com"]
# start_time = time.time()
# # results = verify_emails_list(emails, custom_config)
# results = verify_email("anu.t@mitsogo.com")
results = verify_email("foxspido@bugcrowdninja.com")
# results= verify_email("test1@example.com")
# results= verify_email("woyog39314@acpeak.com")
# results= verify_email("anuinfo@jamf.com")
# results= verify_email("xigoy97969@albarulo.com")
# results= verify_email("anu.t@litmus7.com")
# results= verify_email("anand.pillai@litmus7.com")
# results= verify_email("mail2learnanu@gmail.com")
# end_time = time.time()
print(results)
# logger.debug(f"Time taken for DNS record fetching: {end_time - start_time:.2f} seconds")
# ================ END: 1 =============
# ========================================



# ================ START: 2 =============
# ========================================
# emails = "anu.t@mitsogo.com", "test@example.com"

# def animate_progress():
#     dots = ''
#     while True:
#         print(f'\rLoading{dots}', end='')
#         dots += '.'
#         if len(dots) > 3:
#             dots = ''
#         time.sleep(0.5)


# emails = emails.split(',')
# progress_thread = Thread(target=animate_progress)
# progress_thread.daemon = True
# progress_thread.start()
# try:
#     for email in emails:
#         email= email.strip()
#         result = verify_email(email)
#         status_code = result.get('status', '500')  # Default to 500 if status not found
#         message = result.get('message', 'Unknown error')  # Default message if not found
#         print(f"\r{email}: Status Code {status_code}, Message: {message}")
    
# finally:
#     print("\rEmail validation completed.")
# ================ END: 2 =============
# ========================================




# ================ START: 3 =============
# ========================================
# Example email list
# emails = ["anu.t@mitsogo.com", "test@examples.com"]

# def animate_progress():
#     dots = ''
#     while True:
#         print(f'\rLoading{dots}', end='')
#         dots += '.'
#         if len(dots) > 3:
#             dots = ''
#         time.sleep(0.5)

# # Start the progress animation in a separate thread
# progress_thread = Thread(target=animate_progress)
# progress_thread.daemon = True
# progress_thread.start()

# try:
#     results = verify_emails_list(emails)
#     print("\nVerification Results:")
#     for email in emails:
#         result = results.get(email, {'status': '500', 'message': 'Unknown error'})
#         status_code = result.get('status', '500')
#         message = result.get('message', 'Unknown error')
#         print(f"{email}: Status Code {status_code}, Message: {message}")
# except Exception as e:
#     logger.error(f"An error occurred: {str(e)}")
# finally:
#     print("\rEmail validation completed.")
# ================ END: 3 =============
# ========================================