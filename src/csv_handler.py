from datetime import datetime
import csv


class CSVHandler:
    def __init__(self,  *args, **kwargs):

        self.filename = None
        self.csv_file = None
        self.writer = None

    def create_csv_filename(self, device_name):
        now = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        self.filename = f"{device_name}_{now}.csv"

    def open_csv_file(self):

        self.csv_file = open(f"results/{self.filename}", 'w+', newline='')
        self.writer = csv.writer(self.csv_file)

    def write_manufacturer_data(self, manufacturer_data):
        try:
            manufacturer = manufacturer_data['manufacturer']
            model = manufacturer_data['model']
            self.writer.writerow(['Manufacturer', 'Model'])
            self.writer.writerow([manufacturer, model])
        except:
            print("Failed to write to csv file")
            exit(1)

    def write_command_title(self):
        self.writer.writerow('')
        self.writer.writerow(
            ['Number', 'Test', 'Expected output', 'Actual output', 'Status'])

    def write_command_data(self, command_results):
        try:
            number = command_results['number']
            command = command_results['command']
            expected = command_results['expected_response']
            actual = command_results['actual_response']
            status = command_results['status']
            row = [number, command, expected, actual, status]
            self.writer.writerow(row)

        except:
            exit("Failed to write command data to csv file")

    def write_test_results(self, test_data):
        try:
            total_tests = test_data['total_commands']
            passed_tests = test_data['passed']
            failed_tests = test_data['failed']
            self.writer.writerow('')
            self.writer.writerow(['Passed tests', passed_tests])
            self.writer.writerow(['Failed tests', failed_tests])
            self.writer.writerow(['Total tests', total_tests])
        except:
            exit("Failed to write tests results to csv file")

    def close_csv_file(self):
        self.csv_file.close()
