import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Email Validator CLI.')
    
    parser.add_argument(
        '--emails',
        type=str,
        required=True,
        help='Comma-separated list of email addresses to verify.'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        # required=True,
        help='Output file name to store the results (supports .txt and .xlsx formats).'
    )
    
    return parser.parse_args()
