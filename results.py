import logging
import xlsxwriter


def form_csv(device, command_results):
    datetime = __import__('datetime')

    now = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    filename = f"{device['d__device_name']}_{now}.csv"
    with open(f"{filename}", 'a+', newline='') as file:
        csv = __import__("csv")
        writer = csv.writer(file)
        try:
            total_tests = command_results['tests']['total']

            passed_tests = str(command_results['tests']['passed'])
            failed_tests = str(command_results['tests']['failed'])
            writer.writerow(['No.', 'Test', 'Status'])
            for i in range(0, total_tests):
                number = i+1
                command = command_results[number]['command']
                status = command_results[number]['status']
                row = [number, command, status]
                writer.writerow(row)

            writer.writerow('')
            writer.writerow(['Total tests', total_tests])
            writer.writerow(['Passed tests', passed_tests])
            writer.writerow(['Failed tests', failed_tests])
            manufacturer = command_results['manufacturer']['manufacturer']
            model = command_results['manufacturer']['model']
            writer.writerow(['Manufacturer', 'Model'])
            writer.writerow([manufacturer, model])
        except:
            logging.error("Failed to print to csv file.")
            exit(1)
