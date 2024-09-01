from threading import Thread
from mailValidator.terminalScript.argument_parser import parse_arguments
from mailValidator.terminalScript.progress import animate_progress
from mailValidator.terminalScript.file_writer import write_results_to_file, write_results_to_excel
from mailValidator.email_utils import verify_email
from mailValidator.utils.logging_utils import setup_logging





def read_emails_from_file(file_path):
    """Read email addresses from a text file, ensuring the file is not empty."""
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if not lines:
                print("The file is empty.")
                return []
            return [line.strip() for line in lines if line.strip()]
    except FileNotFoundError:
        print("The file was not found.")
        return []
    except IOError:
        print("An error occurred while reading the file.")
        return []


def print_results_to_terminal(results_by_status):
    """Print results to the terminal."""
    for status, results in results_by_status.items():
        title = {
            "200": "Success (200)",
            "201": "Domain is a catch-all (201)",
            "400": "Client Errors (400)",
            "500": "Server Errors (500)",
            "403": "Forbidden (403)",
            "404": "Not Found (404)",
            "503": "Service Unavailable (503)"
        }.get(status, "Unknown Status")
        
        if results:
            print(f"\n{title}\n")
            print("-" * (len(title) + 2))
            for email, message in results:
                print(f"{email}: {message}")


def validate_email(args):
    # Start the logging setup
    setup_logging()
    
    # Validate output format if provided
    if args.output and not (args.output.endswith('.txt') or args.output.endswith('.xlsx')):
        print(f"Unsupported output format: {args.output}. Please use .txt or .xlsx.")
        return False

    # Load emails from file if specified, otherwise split the input string
    if args.emails.endswith('.txt'):
        emails = read_emails_from_file(args.emails)
        if len(emails) == 0:
            print("The file contains no data.")
            return False
    else:
        emails = [email.strip() for email in args.emails.split(',')]
    
    # Start the progress thread
    progress_thread = Thread(target=animate_progress)
    progress_thread.daemon = True
    progress_thread.start()
    
    results_by_status = {
        "200": [],
        "201": [],
        "400": [],
        "500": [],
        "403": [],
        "404": [],
        "503": [],
    }

    try:
        for email in emails:
            result = verify_email(email)
            status_code = result.get('status', '500')
            message = result.get('message', 'Unknown error')

            if status_code in results_by_status:
                results_by_status[status_code].append((email, message))
            else:
                results_by_status["500"].append((email, "Unexpected status code"))
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting...")
    finally:
        print("\rEmail validation completed.\n")
        
        # Output results based on the provided arguments
        if args.output is None:
            print_results_to_terminal(results_by_status)
        elif args.output.endswith('.txt'):
            write_results_to_file(args.output, results_by_status)
        elif args.output.endswith('.xlsx'):
            write_results_to_excel(args.output, results_by_status)
        
        if args.output:
            print(f"Results written to {args.output}")

def main():
    args = parse_arguments()
    validate_email(args)

if __name__ == "__main__":
    main()
