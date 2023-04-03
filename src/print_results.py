from datetime import datetime
import csv


class PrintResults:
    def __init__(self, device_name, command_results, *args, **kwargs):
        self.device_name = device_name
        self.command_results = command_results
        self.filename = None
        self.csv_file = None

    def create_csv_filename(self):
        now = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        self.filename = f"{self.device_name}_{now}.csv"

    def open_csv_file(self):

        self.csv_file = open(f"results/{self.filename}", 'w+', newline='')

    def write_to_csv_file(self):
        try:
            writer = csv.writer(self.csv_file)

            manufacturer = self.command_results['manufacturer']['manufacturer']
            model = self.command_results['manufacturer']['model']
            total_tests = self.command_results['tests']['total']
            passed_tests = self.command_results['tests']['passed']
            failed_tests = self.command_results['tests']['failed']

            writer.writerow(['Manufacturer', 'Model'])
            writer.writerow([manufacturer, model])
            writer.writerow('')
            writer.writerow(
                ['Number', 'Test', 'Expected output', 'Actual output', 'Status'])

            for i in range(0, total_tests):
                number = i+1
                command = self.command_results[number]['command']
                expected = self.command_results[number]['expected']
                actual = self.command_results[number]['actual']
                status = self.command_results[number]['status']
                row = [number, command, expected, actual, status]
                writer.writerow(row)
            writer.writerow('')
            writer.writerow(['Passed tests', passed_tests])
            writer.writerow(['Failed tests', failed_tests])
            writer.writerow(['Total tests', total_tests])
        except:
            print("Failed to write to csv file")
            exit(1)
