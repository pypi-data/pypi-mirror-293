import xlsxwriter

def write_results_to_file(file_path, results_by_status):
    """Write results to a text file."""
    with open(file_path, 'w') as file:
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
            
            file.write(f"\n{title}\n")
            file.write("-" * (len(title) + 2) + "\n")
            for email, message in results:
                file.write(f"{email}: {message}\n")

def write_results_to_excel(output_file, results_by_status):
    """Write results to an Excel file."""
    workbook = xlsxwriter.Workbook(output_file)
    worksheet = workbook.add_worksheet()

    # Write the headers
    worksheet.write('A1', 'Mail ID')
    worksheet.write('B1', 'Status')
    worksheet.write('C1', 'Message')

    row = 1
    for status, results in results_by_status.items():
        for email, message in results:
            worksheet.write(row, 0, email)
            worksheet.write(row, 1, status)
            worksheet.write(row, 2, message)
            row += 1

    workbook.close()
