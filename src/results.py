def create_csv_filename(device_name):
    datetime = __import__('datetime')
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    filename = f"{device_name}_{now}.csv"
    return filename


def open_csv_file(filename):
    csv_file = open(f"results/{filename}", 'a+', newline='')
    return csv_file


def write_to_csv_file(csv_file, command_results):
    try:
        csv = __import__("csv")
        writer = csv.writer(csv_file)

        manufacturer = command_results['manufacturer']['manufacturer']
        model = command_results['manufacturer']['model']
        total_tests = command_results['tests']['total']
        passed_tests = command_results['tests']['passed']
        failed_tests = command_results['tests']['failed']

        writer.writerow(['Manufacturer', 'Model'])
        writer.writerow([manufacturer, model])
        writer.writerow('')
        writer.writerow(
            ['Number', 'Test', 'Expected output', 'Actual output', 'Status'])

        for i in range(0, total_tests):
            number = i+1
            command = command_results[number]['command']
            expected = command_results[number]['expected']
            actual = command_results[number]['actual']
            status = command_results[number]['status']
            row = [number, command, expected, actual, status]
            writer.writerow(row)
        writer.writerow('')
        writer.writerow(['Passed tests', passed_tests])
        writer.writerow(['Failed tests', failed_tests])
        writer.writerow(['Total tests', total_tests])
    except:
        print("Failed to write to csv file.")
        exit(1)


def form_csv(device, command_results):
    filename = create_csv_filename(device['d__device_name'])
    csv_file = open_csv_file(filename)
    write_to_csv_file(csv_file, command_results)
    csv_file.close()
