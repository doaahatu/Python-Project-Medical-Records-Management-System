# Malak Ammar - 1211470                 # Doaa Hatu - 1211088

import re
import csv
from datetime import datetime


# Patient class that represents a single test
class Patient:

    def __init__(self, patientId):
        self.patientId = patientId
        self.tests = []

    def add_test(self, test_name, test_date, test_time, result, unit, status, c_test_data=None):
        test_record = {
            'test_name': test_name,
            'test_date': test_date,
            'test_time': test_time,
            'result': result,
            'unit': unit,
            'status': status,
            'c_test_data': c_test_data,
        }
        self.tests.append(test_record)

    def getId(self):
        return self.patientId

    def update_test(self, test_name, test_date, test_time, result, unit, status, c_test_data=None):
        test_record = {
            'test_name': test_name,
            'test_date': test_date,
            'test_time': test_time,
            'result': result,
            'unit': unit,
            'status': status,
            'c_test_data': c_test_data,
        }
        self.tests.append(test_record)

    def display_tests(self):
        if not self.tests:
            return "NO TESTS FOUND FOR THIS PATIENT."
        display_str = f"Patient ID: {self.patientId}\n"
        display_str += "Test Records:\n"
        for test in self.tests:
            status = test['status'].capitalize()

            if test['c_test_date'] and test['c_test_time']:
                completionInfo = f", Completed on {test['c_test_date']} {test['c_test_time']}"
            else:
                completionInfo = ""
            display_str += (f"Test Name: {test['test_name']}, Date: {test['test_date']} {test['test_time']}, "
                            f"Result: {test['result']} {test['unit']}, Status: {status}{completionInfo}\n")
        print(display_str)



filename = "medicalRecord.txt"
ids = []


class MAIN:

    def __init__(self):
        self.main()

    # Main Function
    def main(self):
        while True:
            patients = {}
            # store patients
            patients, patientsObj = MAIN.loadPatient(self, "medicalRecord.txt", patients)
            #for p in patientsObj:
                #print(p.getId())
            choice = MAIN.displayMenu(self)

            if choice == '1':
                MAIN.addNewMedicalTest(self)
            elif choice == '2':
                patients, patientsObj = MAIN.addNewMedicalRecord(self, patients, patientsObj)
            elif choice == '3':
                MAIN.updateMedicalRecord(self)
            elif choice == '4':
                MAIN.updateMedicalTest(self)
            elif choice == '5':
                MAIN.filter_medical_tests(self, patients, patientsObj)
            elif choice == '6':
                MAIN.filter_medical_tests(self, patients, patientsObj)
            elif choice == '7':
                MAIN.exportToCSV(self)
            elif choice == '8':
                MAIN.import_records(self)
            elif choice == '9':
                print("Exiting The System...")
                break
            else:
                print("INVALID CHOICE! PLEASE SELECT A VALID OPTION.")

    def loadPatient(self, filename, patients):
        try:
            patientsObj = []
            with open(filename, 'r') as file:
                for line in file:
                    #print(line)
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.strip().split(',')

                    patient_id = parts[0].split(':')[0].strip()
                    test_name = parts[0].split(':')[1].strip()
                    test_date, test_time = parts[1].split()
                    result = parts[2]
                    unit = parts[3]
                    status = parts[4].capitalize()
                    c_test_data = parts[5] if len(parts) > 5 else None
                    # Create test record
                    test_record = [
                        test_name, test_date, test_time, result, unit, status, c_test_data
                    ]
                    if patient_id not in patients:
                        #print("no")
                        # Create a new Patient object and add it to the dictionary and list
                        new_patient = Patient(patient_id)
                        new_patient.add_test(test_name, test_date, test_time, result, unit, status, c_test_data)
                        #print(new_patient.getId())
                        #print(new_patient.tests)
                        patients[patient_id] = []
                        patients[patient_id].append(test_record)
                        #print(patients)
                        # append object
                        patientsObj.append(new_patient)
                        #print("obj list")
                        #print(patientsObj)
                    # If the patient does exist
                    else:
                        #print("yes")
                        patients[patient_id].append(test_record)
                        #print(patients)
                        for object in patientsObj:
                            if patient_id == object.getId():
                                #print(object.getId())
                                object.add_test(test_name, test_date, test_time, result, unit, status,
                                                      c_test_data)
                        #print(patientsObj)

                return patients, patientsObj

        except FileNotFoundError:
            print(f"FILE {filename} NOT FOUND.")

    # Function to display main menu
    def displayMenu(self):
        print("=================================================================")
        print("                MEDICAL TEST MANAGEMENT MENU")
        print("=================================================================")
        print("1. ADD NEW MEDICAL TEST")
        print("2. ADD NEW MEDICAL TEST RECORD")
        print("3. UPDATE PATIENT RECORDS")
        print("4. UPDATE MEDICAL TESTS")
        print("5. FILTER MEDICAL TESTS")
        print("6. GENERATE SUMMARY REPORTS")
        print("7. EXPORT MEDICAL RECORDS")
        print("8. IMPORT MEDICAL RECORDS")
        print("9. EXIT")
        print("=================================================================")
        choice = input("PLEASE SELECT AN OPTION (1-9): ")
        print("=================================================================")
        return choice

    # Function to check if the entered value is integer or -
    def isInt(self, value):
        try:
            # Check if the value is an integer or '-'
            if value == '-':
                return True
            float(value)
            return True
        except ValueError:
            return False

    # Function to check if the entered value has integer or not
    def containsInt(self, value):
        # Check if the value contains any numeric digits
        return bool(re.search(r'\d', value))

    # Function to check if id exists
    def isExist(self, id):
        try:
            with open(filename, 'r') as file:
                # Store id's
                for record in file:
                    idPart = record.strip().split(':')[0]
                    # print(idPart)
                    ids.append(idPart)
        except FileNotFoundError:
            print(f"FILE {filename} NOT FOUND.")

        try:
            if MAIN.isInt(self, ids.index(id)):
                return 1
        except ValueError:
            return 0

    # Function to retrieve test names and units data from medicalTest.txt file
    def retrieveMedicalTestNamesAndUnits(self):
        filename = "medicalTest.txt"
        # Extracting the test names from the file and store them in dictionary
        tests = []
        testDict = {}
        try:
            with open(filename, 'r') as file:
                for record in file:
                    recordParts = record.strip().split(';')
                    # print(recordParts)
                    if len(recordParts) > 0:
                        firstPart = recordParts[0].strip()
                        unitPart = recordParts[2].strip()
                        # print(unitPart)
                        longName = firstPart.split(':')[1].strip()
                        # print(longName)
                        # Extracting the test name from the name part
                        testName = firstPart.split('(')[-1].split(')')[0].strip()
                        testUnit = unitPart.split(':')[-1].split(',')[0].strip()
                        # print(testUnit)
                        tests.append(testName)
                        testDict[testName] = testUnit
                return tests, testDict

        except FileNotFoundError:
            print(f"FILE {filename} NOT FOUND.")

    def validateId(self, id):
        while 1:
            if id == '':
                print("INVALID PATIENT ID! ID CAN NOT BE EMPTY.")
                print("=================================================================")
                id = input("PLEASE ENTER THE PATIENT ID: ")
                print("=================================================================")
                continue
            elif len(id) != 7 and MAIN.isInt(self, id):
                print("INVALID PATIENT ID! ID MUST BE 7-DIGITS LONG.")
                print("=================================================================")
                id = input("PLEASE ENTER THE PATIENT ID: ")
                print("=================================================================")
                continue
            elif not MAIN.isInt(self, id):
                print("INVALID PATIENT ID! ID CAN NOT CONTAIN CHARACTERS.")
                print("=================================================================")
                id = input("PLEASE ENTER THE PATIENT ID: ")
                print("=================================================================")
                continue

            # If input is valid, then break
            return id

    def validateOption(self, tests, testDict, testNum):
        while 1:
            if testNum == '':
                print("INVALID TEST NUMBER! TEST NUMBER CAN NOT BE EMPTY.")
                print("=================================================================")
                print("PLEASE CHOOSE A TEST BY ENTERING THE NUMBER:")
                for i, test in enumerate(tests):
                    print(f"{i + 1}: {test}")
                print("=================================================================")
                testNum = input("TEST NUM.")
                print("=================================================================")
                continue
            elif not MAIN.isInt(self, testNum):
                print("INVALID TEST NUMBER! TEST NUMBER CAN NOT CONTAIN CHARACTERS.")
                print("=================================================================")
                print("PLEASE CHOOSE A TEST BY ENTERING THE NUMBER:")
                for i, test in enumerate(tests):
                    print(f"{i + 1}: {test}")
                print("=================================================================")
                testNum = input("TEST NUM.")
                print("=================================================================")
                continue
            elif int(testNum) > len(tests) or int(testNum) < 1:
                print(f"INVALID TEST NUMBER! TEST NUMBER MUST BE BETWEEN 1 & {len(tests)}.")
                print("=================================================================")
                print("PLEASE CHOOSE A TEST BY ENTERING THE NUMBER:")
                for i, test in enumerate(tests):
                    print(f"{i + 1}: {test}")
                print("=================================================================")
                testNum = input("TEST NUM.")
                print("=================================================================")
                continue

            # If input is valid, then break
            testNum = int(testNum)
            # Assign the value of test name
            testName = tests[testNum - 1]
            testunit = testDict[testName]
            # print(testunit)
            return testName, testunit, testNum

    def validateDate(self, testDate):
        while 1:
            if testDate == '':
                print("INVALID TEST DATE! TEST DATE CAN NOT BE EMPTY.")
                print("=================================================================")
                testDate = input("PLEASE ENTER THE TEST DATE YOU WANT TO UPDATE FOR THIS RECORD: ")
                print("=================================================================")
                continue
            # Validate test date format
            try:
                # Check if the date format is YYYY-MM-DD
                if len(testDate) != 10 or testDate[4] != '-' or testDate[7] != '-':
                    raise ValueError

                year = testDate[:4]
                month = testDate[5:7]
                day = testDate[8:10]

                # Validate length of year, month, and day
                if len(year) != 4 or len(month) != 2 or len(day) != 2:
                    raise ValueError

                year = int(year)
                month = int(month)
                day = int(day)

                # Validate month and day ranges
                if not (1 <= month and month <= 12):
                    raise ValueError
                if not (1 <= day and day <= 31):
                    raise ValueError

            except (ValueError, IndexError):
                print("INVALID TEST DATE! TEST DATE MUST BE IN YY-MM-DD FORMAT WITH VALID VALUES.")
                print("=================================================================")
                testDate = input("PLEASE ENTER THE TEST DATE YOU WANT TO UPDATE FOR THIS RECORD: ")
                print("=================================================================")
            else:
                return testDate

    def validateTime(self, testTime):
        while 1:
            if testTime == '':
                print("INVALID TEST TIME! TEST TIME CAN NOT BE EMPTY.")
                print("=================================================================")
                testTime = input("PLEASE ENTER THE TEST TIME YOU WANT TO ADD TO THIS RECORD: ")
                print("=================================================================")
                continue
            # Validate test time format
            try:
                # Check if the time format is hh:mm
                if len(testTime) != 5 or testTime[2] != ':':
                    raise ValueError

                hour = testTime[0:2]
                minute = testTime[3:5]
                # print(hour)
                # print(minute)

                # Validate length of hour, and minute
                if len(hour) != 2 or len(minute) != 2:
                    raise ValueError

                hour = int(hour)
                minute = int(minute)

                # Validate hour and minute ranges
                if not (1 <= hour and hour <= 12):
                    raise ValueError
                if not (1 <= minute and minute <= 60):
                    raise ValueError

            except (ValueError, IndexError):
                print("INVALID TEST TIME! TEST TIME MUST BE IN hh:mm FORMAT WITH VALID VALUES.")
                print("=================================================================")
                testTime = input("PLEASE ENTER THE TEST TIME YOU WANT TO ADD TO THIS RECORD: ")
                print("=================================================================")
            else:
                return testTime

    def validateResult(self, result):
        while 1:
            if result == '':
                print("INVALID RESULT FOR THIS TEST! RESULT CAN NOT BE EMPTY.")
                print("=================================================================")
                result = input(f"PLEASE ENTER THE RESULT FOR THIS TEST: ")
                print("=================================================================")
                continue

            if not MAIN.isInt(self, result):
                print("INVALID RESULT FOR THIS TEST! RESULT CAN NOT CONTAIN CHARACTERS.")
                print("=================================================================")
                result = input(f"PLEASE ENTER THE RESULT FOR THIS TEST: ")
                print("=================================================================")
                continue

            # If input is valid, then break
            return result

    def validateStatus(self, tests, testNum, statusNum):
        while 1:
            if statusNum == '':
                print("INVALID TEST STATUS NUMBER! TEST STATUS NUMBER CAN NOT BE EMPTY.")
                print("=================================================================")
                print("PLEASE CHOOSE A TEST STATUS BY ENTERING THE NUMBER:")
                for i, test in enumerate(tests):
                    print(f"{i + 1}: {test}")
                print("=================================================================")
                statusNum = input("TEST STATUS NUM.")
                print("=================================================================")
                continue
            elif not MAIN.isInt(self, testNum):
                print("INVALID TEST STATUS NUMBER! TEST STATUS NUMBER CAN NOT CONTAIN CHARACTERS.")
                print("=================================================================")
                print("PLEASE CHOOSE A TEST BY ENTERING THE NUMBER:")
                print("1. COMPLETED.")
                print("2. PENDING.")
                print("3. REVIEWED.")
                print("=================================================================")
                statusNum = input("TEST STATUS NUM.")
                print("=================================================================")
                continue
            elif int(statusNum) > 3 or int(statusNum) < 1:
                print(f"INVALID TEST NUMBER! TEST NUMBER MUST BE BETWEEN 1 & 3.")
                print("=================================================================")
                print("PLEASE CHOOSE A TEST BY ENTERING THE NUMBER:")
                print("1. COMPLETED.")
                print("2. PENDING.")
                print("3. REVIEWED.")
                print("=================================================================")
                statusNum = input("TEST STATUS NUM.")
                print("=================================================================")
                continue

            # Mapping
            if int(statusNum) == 1:
                status = "Completed"

                # If it is completed, then insert the date
                cTestDate = input("PLEASE ENTER THE TEST DATE RESULTS YOU WANT TO ADD TO THIS RECORD: ")
                print("=================================================================")

                while 1:
                    if cTestDate == '':
                        print("INVALID TEST DATE! TEST DATE CAN NOT BE EMPTY.")
                        print("=================================================================")
                        cTestDate = input("PLEASE ENTER THE TEST DATE RESULTS YOU WANT TO ADD TO THIS RECORD: ")
                        print("=================================================================")
                        continue
                    # Validate test date format
                    try:
                        # Check if the date format is YYYY-MM-DD
                        if len(cTestDate) != 10 or cTestDate[4] != '-' or cTestDate[7] != '-':
                            raise ValueError

                        year = cTestDate[:4]
                        month = cTestDate[5:7]
                        day = cTestDate[8:10]

                        # Validate length of year, month, and day
                        if len(year) != 4 or len(month) != 2 or len(day) != 2:
                            raise ValueError

                        year = int(year)
                        month = int(month)
                        day = int(day)

                        # Validate month and day ranges
                        if not (1 <= month and month <= 12):
                            raise ValueError
                        if not (1 <= day and day <= 31):
                            raise ValueError

                    except (ValueError, IndexError):
                        print("INVALID TEST DATE! TEST DATE MUST BE IN YY-MM-DD FORMAT WITH VALID VALUES.")
                        print("=================================================================")
                        cTestDate = input("PLEASE ENTER THE TEST DATE RESULTS YOU WANT TO ADD TO THIS RECORD: ")
                        print("=================================================================")
                    else:
                        break

                cTestTime = input("PLEASE ENTER THE TEST TIME RESULTS YOU WANT TO ADD TO THIS RECORD: ")
                print("=================================================================")

                while 1:
                    if cTestTime == '':
                        print("INVALID TEST TIME! TEST TIME CAN NOT BE EMPTY.")
                        print("=================================================================")
                        cTestTime = input("PLEASE ENTER THE TEST TIME RESULTS YOU WANT TO ADD TO THIS RECORD: ")
                        print("=================================================================")
                        continue
                    # Validate test time format
                    try:
                        # Check if the time format is hh:mm
                        if len(cTestTime) != 5 or cTestTime[2] != ':':
                            raise ValueError

                        hour = cTestTime[0:2]
                        minute = cTestTime[3:5]
                        # print(hour)
                        # print(minute)

                        # Validate length of hour, and minute
                        if len(hour) != 2 or len(minute) != 2:
                            raise ValueError

                        hour = int(hour)
                        minute = int(minute)

                        # Validate hour and minute ranges
                        if not (1 <= hour and hour <= 12):
                            raise ValueError
                        if not (1 <= minute and minute <= 60):
                            raise ValueError

                    except (ValueError, IndexError):
                        print("INVALID TEST TIME! TEST TIME MUST BE IN hh:mm FORMAT WITH VALID VALUES.")
                        print("=================================================================")
                        cTestTime = input("PLEASE ENTER THE TEST TIME RESULTS YOU WANT TO ADD TO THIS RECORD: ")
                        print("=================================================================")
                    else:
                        break

            elif int(statusNum) == 2:
                status = "Pending"
                return status, None, None
            else:
                status = "Reviewed"
                return status, None, None

            # If input is valid, then break
            return status, cTestDate, cTestTime

    def validateRecordNum(self, recordNum, i):
        while 1:
            if recordNum == '':
                print("INVALID OPTION NUMBER! OPTION NUMBER CAN NOT BE EMPTY.")
                print("=================================================================")
                recordNum = input("PLEASE CHOOSE THE RECORD YOU WANT TO UPDATE: ")
                print("=================================================================")
                continue
            elif not MAIN.isInt(self, recordNum):
                print("INVALID OPTION NUMBER! OPTION NUMBER CAN NOT CONTAIN CHARACTERS.")
                print("=================================================================")
                recordNum = input("PLEASE CHOOSE THE RECORD YOU WANT TO UPDATE: ")
                print("=================================================================")
                continue
            elif int(recordNum) > i - 1 or int(recordNum) < 1:
                print(f"INVALID OPTION NUMBER! OPTION NUMBER MUST BE BETWEEN 1 & {i - 1}.")
                print("=================================================================")
                recordNum = input("PLEASE CHOOSE THE RECORD YOU WANT TO UPDATE: ")
                print("=================================================================")
                continue

            # If input is valid, then break
            return recordNum

    # Function to add new medical test
    def addNewMedicalTest(self):
        flag1 = 0
        flag2 = 0

        print("                ADDING A NEW MEDICAL TEST")
        print("=================================================================")

        testName = input("PLEASE ENTER THE NEW MEDICAL TEST NAME YOU WANT TO ADD: ")
        print("=================================================================")

        while 1:
            if testName == '':
                print("INVALID TEST NAME! TEST NAME CAN NOT BE EMPTY.")
                print("=================================================================")
                testName = input("PLEASE ENTER THE NEW MEDICAL TEST NAME YOU WANT TO ADD: ")
                print("=================================================================")
                continue
            else:
                break

        abrTestName = input("PLEASE ENTER THE ABBREVIATION NEW MEDICAL TEST NAME YOU WANT TO ADD: ")
        print("=================================================================")

        while 1:
            if abrTestName == '':
                print("INVALID TEST NAME ABBREVIATION! ABBREVIATION CAN NOT BE EMPTY.")
                print("=================================================================")
                abrTestName = input("PLEASE ENTER THE ABBREVIATION NEW MEDICAL TEST NAME YOU WANT TO ADD: ")
                print("=================================================================")
                continue
            else:
                break

        minRange = input(f"PLEASE ENTER THE MINIMUM RANGE FOR TEST {abrTestName}, ENTER '-' IF NO MIN. RANGE: ")
        print("=================================================================")

        if minRange == '-':
            flag1 = 0
        else:
            flag1 = 1

        while 1:
            if minRange == '':
                print("INVALID MINIMUM RANGE FOR TEST NAME! RANGE CAN NOT BE EMPTY.")
                print("=================================================================")
                minRange = input(f"PLEASE ENTER THE MINIMUM RANGE FOR TEST {abrTestName}, ENTER '-' IF NO MIN. RANGE: ")
                print("=================================================================")
                continue

            if not MAIN.isInt(self, minRange):
                print("INVALID MINIMUM RANGE FOR TEST NAME! RANGE CAN NOT CONTAIN CHARACTERS.")
                print("=================================================================")
                minRange = input(f"PLEASE ENTER THE MINIMUM RANGE FOR TEST {abrTestName}, ENTER '-' IF NO MIN. RANGE: ")
                print("=================================================================")
                continue

            # If input is valid, then break
            break

        maxRange = input(f"PLEASE ENTER THE MAXIMUM RANGE FOR TEST {abrTestName}, ENTER '-' IF NO MAX. RANGE: ")
        print("=================================================================")

        if maxRange == '-':
            flag2 = 0
        else:
            flag2 = 1

        while 1:
            if maxRange == '':
                print("INVALID MAXIMUM RANGE FOR TEST NAME! RANGE CAN NOT BE EMPTY.")
                print("=================================================================")
                maxRange = input(f"PLEASE ENTER THE MINIMUM RANGE FOR TEST {abrTestName}, ENTER '-' IF NO MAX. RANGE: ")
                print("=================================================================")
                continue

            if not MAIN.isInt(self, maxRange):
                print("INVALID MAXIMUM RANGE FOR TEST NAME! RANGE CAN NOT CONTAIN CHARACTERS.")
                print("=================================================================")
                maxRange = input(f"PLEASE ENTER THE MINIMUM RANGE FOR TEST {abrTestName}, ENTER '-' IF NO MAX. RANGE: ")
                print("=================================================================")
                continue

            if minRange >= maxRange:
                print("INVALID MAXIMUM RANGE FOR TEST NAME! MAX. RANGE CAN NOT BE LESS THEN MIN. RANGE.")
                print("=================================================================")
                maxRange = input(f"PLEASE ENTER THE MINIMUM RANGE FOR TEST {abrTestName}, ENTER '-' IF NO MAX. RANGE: ")
                print("=================================================================")
                continue

            # If input is valid, then break
            break

        unit = input(f"PLEASE ENTER THE UNIT FOR TEST {abrTestName}: ")
        print("=================================================================")

        while 1:
            if unit == '':
                print("INVALID UNIT FOR TEST NAME! UNIT CAN NOT BE EMPTY.")
                print("=================================================================")
                unit = input(f"PLEASE ENTER THE UNIT FOR TEST {abrTestName}: ")
                print("=================================================================")
                continue

            if MAIN.containsInt(self, unit):
                print("INVALID UNIT FOR TEST NAME! UNIT CAN NOT CONTAIN DIGITS.")
                print("=================================================================")
                unit = input(f"PLEASE ENTER THE UNIT FOR TEST {abrTestName}: ")
                print("=================================================================")
                continue

            # If input is valid, then break
            break

        turnaroundTime = input(f"PLEASE ENTER THE TURNAROUND TIME (DD-hh-mm) FOR TEST {abrTestName}: ")
        print("=================================================================")

        while 1:
            if turnaroundTime == '':
                print("INVALID TURNAROUND TIME FOR TEST NAME! TURNAROUND TIME CAN NOT BE EMPTY.")
                print("=================================================================")
                turnaroundTime = input(f"PLEASE ENTER THE TURNAROUND TIME (DD-hh-mm) FOR TEST {abrTestName}: ")
                print("=================================================================")
                continue

            # Validate turnaround time format
            try:
                days, hours, minutes = map(int, turnaroundTime.split('-'))
                if days < 0 or hours < 0 or minutes < 0:
                    raise ValueError
            except (ValueError, IndexError):
                print("INVALID TURNAROUND TIME FORMAT. USE DD-HH-MM FORMAT.")
                print("=================================================================")
                turnaroundTime = input(f"PLEASE ENTER THE TURNAROUND TIME (DD-hh-mm) FOR TEST {abrTestName}: ")
                print("=================================================================")
            else:
                break

        filename = "medicalTest.txt"

        try:
            # Append to the file
            with open(filename, "a") as file:
                # Min & Max
                if flag1 and flag2:
                    file.write(
                        f"\nName: {testName} ({abrTestName}); Range: > {minRange}, < {maxRange}; Unit: {unit}; {turnaroundTime}")
                # Min Only
                elif flag1 and not flag2:
                    file.write(
                        f"\nName: {testName} ({abrTestName}); Range: > {minRange}; Unit: {unit}; {turnaroundTime}")
                # Max Only
                elif flag2 and not flag1:
                    file.write(
                        f"\nName: {testName} ({abrTestName}); Range: < {maxRange}; Unit: {unit}; {turnaroundTime}")
                else:
                    file.close()
                    print("INVALID RANGE, YOU NEED TO SPECIFY AT LEAST ONE OF THE MIN. OR MAX. RANGES.")
                    return

        # If file not found
        except FileNotFoundError:
            print(f"FILE {filename} NOT FOUND.")
            return

        print(f"                TEST \"{testName} ({abrTestName})\" ADDED SUCCESSFULLY.")
        return

    # Function to add new medical record
    def addNewMedicalRecord(self, patients, patientsObj):
        flag1 = 0
        flag2 = 0

        print("                ADDING A NEW MEDICAL RECORD")
        print("=================================================================")

        id = input("PLEASE ENTER THE PATIENT ID YOU WANT TO ADD: ")
        print("=================================================================")

        # Validate entered id
        id = MAIN.validateId(self, id)

        # Create the new patient
        patient = Patient(id)

        # Extracting the test names from the file and store them in dictionary
        tests = []
        testDict = {}
        tests, testDict = MAIN.retrieveMedicalTestNamesAndUnits(self)

        print("PLEASE CHOOSE A TEST BY ENTERING THE NUMBER:")
        for i, test in enumerate(tests):
            print(f"{i + 1}: {test}")

        print("=================================================================")
        testNum = input("TEST NUM.")
        print("=================================================================")

        # validate testNumber
        testName, testunit, testNum = MAIN.validateOption(self, tests, testDict, testNum)

        testDate = input("PLEASE ENTER THE TEST DATE YOU WANT TO ADD TO THIS RECORD: ")
        print("=================================================================")

        testDate = MAIN.validateDate(self, testDate)

        testTime = input("PLEASE ENTER THE TEST TIME YOU WANT TO ADD TO THIS RECORD: ")
        print("=================================================================")

        testTime = MAIN.validateTime(self, testTime)

        result = input(f"PLEASE ENTER THE RESULT FOR THIS TEST: ")
        print("=================================================================")

        result = MAIN.validateResult(self, result)

        print("PLEASE CHOOSE A TEST BY ENTERING THE NUMBER:")
        print("1. COMPLETED.")
        print("2. PENDING.")
        print("3. REVIEWED.")
        print("=================================================================")

        statusNum = input("TEST STATUS NUM.")
        print("=================================================================")

        status, cTestDate, cTestTime = MAIN.validateStatus(self, tests, testNum, statusNum)
        c_test_data = f"{cTestDate} {cTestTime}"
        test_record = [
            testName, testDate, testTime, result, testunit, status, c_test_data
        ]

        if id not in patients:
            # print("no")
            # Create a new Patient object and add it to the dictionary and list
            new_patient = Patient(id)
            new_patient.add_test(testName, testDate, testTime, result, testunit, status, c_test_data)
            # print(new_patient.getId())
            # print(new_patient.tests)
            patients[id] = []
            patients[id].append(test_record)
            # print(patients)
            # append object
            patientsObj.append(new_patient)

        # If the patient does exist
        else:
            # print("yes")
            patients[id].append(test_record)
            # print(patients)
            for object in patientsObj:
                if id == object.getId():
                    # print(object.getId())
                    object.add_test(testName, testDate, testTime, result, testunit, status, c_test_data)
            # print(patientsObj)

        filename = "medicalRecord.txt"

        try:
            # Append to the file
            with open(filename, "a") as file:
                if status == 'Completed':
                    # patient.display_tests()
                    file.write(
                        f"\n{id}: {testName}, {testDate} {testTime}, {result}, {testunit}, {status}, {cTestDate} {cTestTime}")
                else:
                    # patient.display_tests()
                    file.write(f"\n{id}: {testName}, {testDate} {testTime}, {result}, {testunit}, {status}")
        # If file not found
        except FileNotFoundError:
            print(f"FILE {filename} NOT FOUND.")
            return

        print(f"            PATIENT WITH ID: \"{id}\" ADDED SUCCESSFULLY.")
        return patients, patientsObj

    # Function to update medical record
    def updateMedicalRecord(self):

        # flag to check if id exists
        isIdExist = 0
        flag2 = 0

        print("                UPDATING A MEDICAL RECORD")
        print("=================================================================")

        id = input("PLEASE ENTER THE PATIENT ID YOU WANT TO UPDATE: ")
        print("=================================================================")

        id = MAIN.validateId(self, id)


        # Store Patient Records
        patientRecords = []
        i = 1
        filename = "medicalRecord.txt"
        try:
            with open(filename, 'r') as file:
                for record in file:
                    idPart = record.strip().split(':')[0]
                    if idPart == id:
                        patientRecords.append(record)
                        print(f"{i}- {record}")
                        i += 1
                        continue
        except FileNotFoundError:
            print(f"FILE {filename} NOT FOUND.")
        # print(patientRecords)

        while 1:
            # check if the id does not exist
            if not patientRecords:
                print("ID DOES NOT EXIST! NOTHING TO UPDATE.")
                print("=================================================================")
                id = input("PLEASE ENTER THE PATIENT ID YOU WANT TO UPDATE: ")
                print("=================================================================")

                id = MAIN.validateId(self, id)

                # Store Patient Records
                patientRecords = []
                i = 1
                filename = "medicalRecord.txt"
                try:
                    with open(filename, 'r') as file:
                        for record in file:
                            idPart = record.strip().split(':')[0]
                            if idPart == id:
                                patientRecords.append(record)
                                print(f"{i}- {record}")
                                i += 1
                                continue
                except FileNotFoundError:
                    print(f"FILE {filename} NOT FOUND.")

            else:
                break

        print("=================================================================")
        recordNum = input("PLEASE CHOOSE THE RECORD YOU WANT TO UPDATE: ")
        print("=================================================================")

        recordNum = MAIN.validateRecordNum(self, recordNum, i)

        newid = input("PLEASE ENTER THE PATIENT ID YOU WANT TO UPDATE: ")
        print("=================================================================")

        newid = MAIN.validateId(self, newid)

        # Extracting the test names from the file and store them in dictionary
        tests = []
        testDict = {}

        tests, testDict = MAIN.retrieveMedicalTestNamesAndUnits(self)

        print("PLEASE CHOOSE A TEST BY ENTERING THE NUMBER:")
        for i, test in enumerate(tests):
            print(f"{i + 1}: {test}")

        print("=================================================================")
        testNum = input("TEST NUM.")
        print("=================================================================")

        testName, testunit, testNum = MAIN.validateOption(self, tests, testDict, testNum)

        testDate = input("PLEASE ENTER THE TEST DATE YOU WANT TO UPDATE FOR THIS RECORD: ")
        print("=================================================================")

        testDate = MAIN.validateDate(self, testDate)

        testTime = input("PLEASE ENTER THE TEST TIME YOU WANT TO UPDATE FOR THIS RECORD: ")
        print("=================================================================")

        testTime = MAIN.validateTime(self, testTime)

        result = input(f"PLEASE ENTER THE RESULT FOR THIS TEST: ")
        print("=================================================================")

        result = MAIN.validateResult(self, result)

        print("PLEASE CHOOSE A TEST BY ENTERING THE NUMBER:")
        print("1. COMPLETED.")
        print("2. PENDING.")
        print("3. REVIEWED.")
        print("=================================================================")

        statusNum = input("TEST STATUS NUM.")
        print("=================================================================")

        status, cTestDate, cTestTime = MAIN.validateStatus(self, tests, testNum, statusNum)

        filename = "medicalRecord.txt"
        recordNum = int(recordNum)
        i = 1
        if status == 'Completed':
            updatedRecord = f"{newid}: {testName}, {testDate} {testTime}, {result}, {testunit}, {status}, {cTestDate} {cTestTime}\n"
        else:
            updatedRecord = f"{newid}: {testName}, {testDate} {testTime}, {result}, {testunit}, {status}\n"
        updatedRecords = []

        try:
            # Update the file
            with open(filename, "r") as file:
                for line in file:
                    # print(line)
                    idPart = line.strip().split(':')[0]
                    if idPart == id:
                        if i == recordNum:
                            updatedRecords.append(updatedRecord)
                        else:
                            i += 1
                            updatedRecords.append(line)
                            continue
                    else:
                        updatedRecords.append(line)

        # If file not found
        except FileNotFoundError:
            print(f"FILE {filename} NOT FOUND.")
            return
        try:
            # Update the file
            with open(filename, "w") as file:
                file.writelines(updatedRecords)
                print("PATIENT FIELDS UPDATED SUCCESSFULLY.")

        # If file not found
        except FileNotFoundError:
            print(f"FILE {filename} NOT FOUND.")

        return

    # Function to update a medical test
    def updateMedicalTest(self):
        flag1 = 0
        flag2 = 0

        print("                UPDATING A MEDICAL TEST")
        print("=================================================================")

        # Store medical test Records
        medicalRecords = []
        i = 1
        filename = "medicalTest.txt"
        try:
            with open(filename, 'r') as file:
                for record in file:
                    medicalRecords.append(record)
                    print(f"{i}- {record}")
                    i += 1
        except FileNotFoundError:
            print(f"FILE {filename} NOT FOUND.")

        print("=================================================================")
        recordNum = input("PLEASE CHOOSE THE MEDICAL TEST YOU WANT TO UPDATE: ")
        print("=================================================================")

        recordNum = MAIN.validateRecordNum(self, recordNum, i)



        testName = input("PLEASE ENTER THE NEW MEDICAL TEST NAME YOU WANT TO UPDATE: ")
        print("=================================================================")

        while 1:
            if testName == '':
                print("INVALID TEST NAME! TEST NAME CAN NOT BE EMPTY.")
                print("=================================================================")
                testName = input("PLEASE ENTER THE NEW MEDICAL TEST NAME YOU WANT TO UPDATE: ")
                print("=================================================================")
                continue
            else:
                break

        abrTestName = input("PLEASE ENTER THE ABBREVIATION NEW MEDICAL TEST NAME YOU WANT TO UPDATE: ")
        print("=================================================================")

        while 1:
            if abrTestName == '':
                print("INVALID TEST NAME ABBREVIATION! ABBREVIATION CAN NOT BE EMPTY.")
                print("=================================================================")
                abrTestName = input("PLEASE ENTER THE ABBREVIATION NEW MEDICAL TEST NAME YOU WANT TO UPDATE: ")
                print("=================================================================")
                continue
            else:
                break

        minRange = input(f"PLEASE ENTER THE MINIMUM RANGE FOR TEST {abrTestName}, ENTER '-' IF NO MIN. RANGE: ")
        print("=================================================================")

        if minRange == '-':
            flag1 = 0
        else:
            flag1 = 1

        while 1:
            if minRange == '':
                print("INVALID MINIMUM RANGE FOR TEST NAME! RANGE CAN NOT BE EMPTY.")
                print("=================================================================")
                minRange = input(f"PLEASE ENTER THE MINIMUM RANGE FOR TEST {abrTestName}, ENTER '-' IF NO MIN. RANGE: ")
                print("=================================================================")
                continue

            if not MAIN.isInt(self, minRange):
                print("INVALID MINIMUM RANGE FOR TEST NAME! RANGE CAN NOT CONTAIN CHARACTERS.")
                print("=================================================================")
                minRange = input(f"PLEASE ENTER THE MINIMUM RANGE FOR TEST {abrTestName}, ENTER '-' IF NO MIN. RANGE: ")
                print("=================================================================")
                continue

            # If input is valid, then break
            break

        maxRange = input(f"PLEASE ENTER THE MAXIMUM RANGE FOR TEST {abrTestName}, ENTER '-' IF NO MAX. RANGE: ")
        print("=================================================================")

        if maxRange == '-':
            flag2 = 0
        else:
            flag2 = 1

        while 1:
            if maxRange == '':
                print("INVALID MAXIMUM RANGE FOR TEST NAME! RANGE CAN NOT BE EMPTY.")
                print("=================================================================")
                maxRange = input(f"PLEASE ENTER THE MINIMUM RANGE FOR TEST {abrTestName}, ENTER '-' IF NO MAX. RANGE: ")
                print("=================================================================")
                continue

            if not MAIN.isInt(self, maxRange):
                print("INVALID MAXIMUM RANGE FOR TEST NAME! RANGE CAN NOT CONTAIN CHARACTERS.")
                print("=================================================================")
                maxRange = input(f"PLEASE ENTER THE MINIMUM RANGE FOR TEST {abrTestName}, ENTER '-' IF NO MAX. RANGE: ")
                print("=================================================================")
                continue

            if minRange >= maxRange:
                print("INVALID MAXIMUM RANGE FOR TEST NAME! MAX. RANGE CAN NOT BE LESS THEN MIN. RANGE.")
                print("=================================================================")
                maxRange = input(f"PLEASE ENTER THE MINIMUM RANGE FOR TEST {abrTestName}, ENTER '-' IF NO MAX. RANGE: ")
                print("=================================================================")
                continue

            # If input is valid, then break
            break

        unit = input(f"PLEASE ENTER THE UNIT FOR TEST {abrTestName}: ")
        print("=================================================================")

        while 1:
            if unit == '':
                print("INVALID UNIT FOR TEST NAME! UNIT CAN NOT BE EMPTY.")
                print("=================================================================")
                unit = input(f"PLEASE ENTER THE UNIT FOR TEST {abrTestName}: ")
                print("=================================================================")
                continue

            if MAIN.containsInt(self, unit):
                print("INVALID UNIT FOR TEST NAME! UNIT CAN NOT CONTAIN DIGITS.")
                print("=================================================================")
                unit = input(f"PLEASE ENTER THE UNIT FOR TEST {abrTestName}: ")
                print("=================================================================")
                continue

            # If input is valid, then break
            break

        turnaroundTime = input(f"PLEASE ENTER THE TURNAROUND TIME (DD-hh-mm) FOR TEST {abrTestName}: ")
        print("=================================================================")

        while 1:
            if turnaroundTime == '':
                print("INVALID TURNAROUND TIME FOR TEST NAME! TURNAROUND TIME CAN NOT BE EMPTY.")
                print("=================================================================")
                turnaroundTime = input(f"PLEASE ENTER THE TURNAROUND TIME (DD-hh-mm) FOR TEST {abrTestName}: ")
                print("=================================================================")
                continue

            # Validate turnaround time format
            try:
                days, hours, minutes = map(int, turnaroundTime.split('-'))
                if days < 0 or hours < 0 or minutes < 0:
                    raise ValueError
            except (ValueError, IndexError):
                print("INVALID TURNAROUND TIME FORMAT. USE DD-HH-MM FORMAT.")
                print("=================================================================")
                turnaroundTime = input(f"PLEASE ENTER THE TURNAROUND TIME (DD-hh-mm) FOR TEST {abrTestName}: ")
                print("=================================================================")
            else:
                break

        # Min & Max
        if flag1 and flag2:
            up = f"Name: {testName} ({abrTestName}); Range: > {minRange}, < {maxRange}; Unit: {unit}; {turnaroundTime}"
        # Min Only
        elif flag1 and not flag2:
            up = f"Name: {testName} ({abrTestName}); Range: > {minRange}; Unit: {unit}; {turnaroundTime}"
        # Max Only
        elif flag2 and not flag1:
            up = f"Name: {testName} ({abrTestName}); Range: < {maxRange}; Unit: {unit}; {turnaroundTime}"
        else:
            print("INVALID RANGE, YOU NEED TO SPECIFY AT LEAST ONE OF THE MIN. OR MAX. RANGES.")
            return

        updatedMedicalRecords = []
        i = 1
        recordNum = int(recordNum)
        oldRecord = medicalRecords[recordNum - 1]
        #print(oldRecord)
        #print(up)
        try:
            with open(filename, 'r') as file:
                for record in file:
                    if oldRecord == record:
                        updatedMedicalRecords.append(up)
                        continue
                    updatedMedicalRecords.append(record)
                    i += 1
        except FileNotFoundError:
            print(f"FILE {filename} NOT FOUND.")

        filename = "medicalTest.txt"

        try:
            # Append to the file
            with open(filename, "w") as file:
                file.writelines(updatedMedicalRecords)

        # If file not found
        except FileNotFoundError:
            print(f"FILE {filename} NOT FOUND.")
            return

        print(f"                TEST \"{testName} ({abrTestName})\" UPDATED SUCCESSFULLY.")
        return

    def load_test_ranges(self, filename):
        test_ranges = {}
        try:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    # Extract information
                    name_part, range_part = line.split(';', 1)
                    #print(name_part)
                    #print(range_part)
                    parts = line.split(';')
                    test_name_part = parts[0].split(':')[1].strip()
                    abbreviation = test_name_part.split('(')[1].replace(')', '').strip()
                    #print(abbreviation)

                    min_value = None
                    max_value = None

                    # Extract the min and max values from range_part
                    if '> ' in range_part:
                        #print(">")
                        min_value_str = range_part.split('> ')[1].split(',')[0].strip()
                        #print(min_value_str)
                        if min_value_str != '-':
                            min_value = float(min_value_str)

                    if '< ' in range_part:
                        #print("<")
                        max_value_str = range_part.split('< ')[1].split(';')[0].strip()
                        #print(max_value_str)
                        if max_value_str != '-':
                            max_value = float(max_value_str)


                    # Store the parsed data in the test_ranges dictionary
                    test_ranges[abbreviation] = {'min': min_value, 'max': max_value}

        except FileNotFoundError:
                print(f"FILE {filename} NOT FOUND.")

        return test_ranges

    def retrieve_abnormal_tests_from_file(self, medical_record_file, test_ranges):
        import statistics
        results = []
        records_set = set()
        abnormal_tests = []
        try:
            with open(medical_record_file, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split(',')
                    test_name = parts[0].split(':')[1].strip()
                    result = float(parts[2])

                    # Check for abnormal test results
                    test_abbreviation = test_name  # Assuming test_name is the abbreviation
                    if test_abbreviation in test_ranges:
                        test_info = test_ranges[test_abbreviation]
                        min_range = test_info['min']
                        max_range = test_info['max']

                        is_abnormal = False
                        if (min_range is not None and result <= min_range) or (
                                max_range is not None and result >= max_range):
                            is_abnormal = True

                        if is_abnormal:
                            #print(line)
                            parts = line.split(',')
                            result = parts[2].strip()
                            #print(result)
                            result = float(result)
                            # print(result)
                            results.append(result)
                            record_str = str(line)
                            records_set.add(record_str)

        except FileNotFoundError:
            print(f"FILE {medical_record_file} NOT FOUND.")
        print("-----------------------------REPORT------------------------------")
        print(f"MIN. VALUE: {min(results)}")
        print(f"MAX. VALUE: {max(results)}")
        print(f"AVG. VALUE: {statistics.mean(results)}")
        print("=================================================================")
        return records_set


    def retrieve_tests_by_status(self, medical_record_file, status_filter):
        import statistics
        results = []
        records_set = set()
        try:
            with open(medical_record_file, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split(',')
                    status = parts[4].capitalize().strip()
                    #print(status)

                    # Check for the desired status
                    if status == status_filter.lower().strip():
                        #print(line)
                        parts = line.split(',')
                        result = parts[2].strip()
                        #print(result)
                        result = float(result)
                        # print(result)
                        results.append(result)

                        record_str = str(line)
                        records_set.add(record_str)
                print("=================================================================")

        except FileNotFoundError:
            print(f"FILE {medical_record_file} NOT FOUND.")
        print("-----------------------------REPORT------------------------------")
        print(f"MIN. VALUE: {min(results)}")
        print(f"MAX. VALUE: {max(results)}")
        print(f"AVG. VALUE: {statistics.mean(results)}")
        print("=================================================================")
        return records_set

    def idFilter(self, patients):
        import statistics
        records_set = set()
        results = []
        id = input("Please enter the patient id: ")
        if id not in patients:
            print(f"No records found for patient ID: {id}")
            return
        else:
            for record in patients[id]:
                #print(record)
                result = float(record[3])
                #print(result)
                results.append(result)
                record_str = str(record)
                records_set.add(record_str)
            print("=================================================================")
            print("-----------------------------REPORT------------------------------")
            print(f"MIN. VALUE: {min(results)}")
            print(f"MAX. VALUE: {max(results)}")
            print(f"AVG. VALUE: {statistics.mean(results)}")
            print("=================================================================")

            return records_set

    def testNameFilter(self, patients):
        import statistics
        results = []
        records_set = set()
        filename = "medicalTest.txt"
        # Extracting the test names from the file and store them in dictionary
        tests = []
        testDict = {}
        try:
            with open(filename, 'r') as file:
                for record in file:
                    recordParts = record.strip().split(';')
                    # print(recordParts)
                    if len(recordParts) > 0:
                        firstPart = recordParts[0].strip()
                        unitPart = recordParts[2].strip()
                        # print(unitPart)
                        longName = firstPart.split(':')[1].strip()
                        # print(longName)
                        # Extracting the test name from the name part
                        testName = firstPart.split('(')[-1].split(')')[0].strip()
                        testUnit = unitPart.split(':')[-1].split(',')[0].strip()
                        # print(testUnit)
                        tests.append(testName)
                        testDict[testName] = testUnit
        except FileNotFoundError:
            print(f"FILE {filename} NOT FOUND.")
        i = 1
        print("Please enter the number of test name you want to filter:")
        for test in tests:
            print(f"{i}- {test}")
            i += 1
        print("=================================================================")
        testNum = input("Test num.")
        testNum = int(testNum)
        print("=================================================================")
        selected_test_name = tests[testNum - 1]
        # Iterate through all patient records and filter by the selected test name
        matching_records = []

        try:
            filename = "medicalRecord.txt"
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    # Extract test name from the line
                    patient_id = line.split(':')[0].strip()
                    test_name = line.split(':')[1].split(',')[0].strip()
                    # print(test_name)

                    if test_name.lower() == selected_test_name.lower():
                        matching_records.append(line)

            # Display the matching records
            if matching_records:
                #print(f"Found {len(matching_records)} records with the test name '{selected_test_name}':\n")
                for record in matching_records:
                    parts = record.split(',')
                    result = parts[2].strip()
                    #print(result)
                    result = float(result)
                    # print(result)
                    results.append(result)
                    record_str = str(record)
                    records_set.add(record_str)
            else:
                print(f"No records found with the test name '{selected_test_name}'.")

        except FileNotFoundError:
            print(f"FILE {filename} NOT FOUND.")
        #print(results)
        print("-----------------------------REPORT------------------------------")
        print(f"MIN. VALUE: {min(results)}")
        print(f"MAX. VALUE: {max(results)}")
        print(f"AVG. VALUE: {statistics.mean(results)}")
        print("=================================================================")
        return records_set


    def singleFilter(self, patients, patienstObj):
        print("Select the field you want to filter based on:")
        print("1- Patient Id.")
        print("2- Test name.")
        print("3- Abnormal Tests.")
        print("4- Test Status.")
        print("=================================================================")
        selection = input("Selection Num.")
        selection = int(selection)
        print("=================================================================")
        if selection == 1:
            records_set = set()
            records_set = MAIN.idFilter(self, patients)
            MAIN.printSet(self, records_set)
        elif selection == 2:
            records_set = set()
            records_set = MAIN.testNameFilter(self, patients)
            MAIN.printSet(self, records_set)
        elif selection == 3:
            records_set = set()
            testRanges = {}
            testRanges = MAIN.load_test_ranges(self, "medicalTest.txt")
            # print(testRanges)
            records_set = MAIN.retrieve_abnormal_tests_from_file(self, "medicalRecord.txt", testRanges)
            MAIN.printSet(self, records_set)

        elif selection == 4:
            records_set = set()

            print("Please select the number of status you want to filter:")
            print("1- Completed.")
            print("2- Pending.")
            print("3- Reviewed.")
            print("=================================================================")
            op=input("Status Num.")
            print("=================================================================")
            status = ""
            op = int(op)
            if op == 1:
                status = "completed"
            elif op == 2:
                status = "Pending"
            elif op == 3:
                status = "Reviewed"
            else:
                print("Invalid option!")
                return
            records_set = MAIN.retrieve_tests_by_status(self, "medicalRecord.txt", status)
            MAIN.printSet(self, records_set)

    def printSet(self, records_set):
        for record in records_set:
            print(record)


    def twoFilter(self, patients, patienstObj):
        print("Enter the first number of field you want to filter:")
        print("1- Patient Id.")
        print("2- Test name.")
        print("3- Abnormal Tests.")
        print("4- Test Status.")
        print("=================================================================")
        selection1 = input("Selection Num.")
        selection1 = int(selection1)
        print("=================================================================")
        print("Enter the second number of field you want to filter:")
        print("1- Patient Id.")
        print("2- Test name.")
        print("3- Abnormal Tests.")
        print("4- Test Status.")
        print("=================================================================")
        selection2 = input("Selection Num.")
        selection2 = int(selection2)
        print("=================================================================")
        records_set1 = set()
        records_set2 = set()

        # Filter based on the first selection
        if selection1 == 1:
            records_set1 = MAIN.idFilter(self, patients)
        elif selection1 == 2:
            records_set1 = MAIN.testNameFilter(self, patients)
        elif selection1 == 3:
            testRanges = {}
            testRanges = MAIN.load_test_ranges(self, "medicalTest.txt")
            records_set1 = MAIN.retrieve_abnormal_tests_from_file(self, "medicalRecord.txt", testRanges)
        elif selection1 == 4:
            print("Please select the number of status you want to filter:")
            print("1- Completed.")
            print("2- Pending.")
            print("3- Reviewed.")
            print("=================================================================")
            op = input("Status Num.")
            print("=================================================================")
            status = ""
            op = int(op)
            if op == 1:
                status = "completed"
            elif op == 2:
                status = "Pending"
            elif op == 3:
                status = "Reviewed"
            else:
                print("Invalid option!")
                return
            records_set1 = MAIN.retrieve_tests_by_status(self, "medicalRecord.txt", status)
        else:
            print("Invalid selection for the first filter.")
            return

        # Filter based on the second selection
        if selection2 == 1:
            records_set2 = MAIN.idFilter(self, patients)
        elif selection2 == 2:
            records_set2 = MAIN.testNameFilter(self, patients)
        elif selection2 == 3:
            testRanges = {}
            testRanges = MAIN.load_test_ranges(self, "medicalTest.txt")
            records_set2 = MAIN.retrieve_abnormal_tests_from_file(self, "medicalRecord.txt", testRanges)
        elif selection2 == 4:
            print("Please select the number of status you want to filter:")
            print("1- Completed.")
            print("2- Pending.")
            print("3- Reviewed.")
            print("=================================================================")
            op = input("Status Num.")
            print("=================================================================")
            status = ""
            op = int(op)
            if op == 1:
                status = "completed"
            elif op == 2:
                status = "Pending"
            elif op == 3:
                status = "Reviewed"
            else:
                print("Invalid option!")
                return
            records_set2 = MAIN.retrieve_tests_by_status(self, "medicalRecord.txt", status)
        else:
            print("Invalid selection for the second filter.")
            return

        # Intersection of the two sets
        combined_records = records_set1.intersection(records_set2)

        import statistics
        results = []
        # Print the combined records
        if combined_records:
            for record in combined_records:
                result = MAIN.extract_between_occurrences(self, record, "'", 7, 8)
                #print(result)
                result = float(result)
                # print(result)
                results.append(result)
                #print(result)
        else:
            print("No records found matching both criteria.")
            return
        print("-----------------------------REPORT------------------------------")
        print(f"MIN. VALUE: {min(results)}")
        print(f"MAX. VALUE: {max(results)}")
        print(f"AVG. VALUE: {statistics.mean(results)}")
        print("=================================================================")

    def extract_between_occurrences(self, s, char, nth_start, nth_end):
        # Find the start and end positions of the nth occurrences
        start_pos = -1
        end_pos = -1
        count = 0

        for i, c in enumerate(s):
            if c == char:
                count += 1
                if count == nth_start:
                    start_pos = i
                elif count == nth_end:
                    end_pos = i
                    break

        # Extract substring between the nth occurrences
        if start_pos != -1 and end_pos != -1 and end_pos > start_pos:
            return s[start_pos + 1:end_pos]
        else:
            return None

    def periodFilter(self, patients):
        import statistics
        results = []

        # Get the start and end dates for filtering
        start_date_str = input("Enter the start date (YYYY-MM-DD): ")
        end_date_str = input("Enter the end date (YYYY-MM-DD): ")
        print("=================================================================")

        try:
            # Convert the input strings to datetime objects
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        records_set = set()

        try:
            with open(filename, 'r') as file:
                filtered_records = []

                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    # Split the line into parts
                    parts = line.split(',')

                    if len(parts) < 5:
                        print(f"Skipping malformed record: {line}")
                        continue

                    # Extract relevant parts
                    patient_id = parts[0].split(':')[0].strip()
                    test_date_str = parts[1].strip()

                    try:
                        # Convert test_date_str to datetime
                        test_date = datetime.strptime(test_date_str.split()[0], "%Y-%m-%d")
                    except ValueError:
                        print(f"Invalid date format for record: {line}. Skipping this record.")
                        continue

                    # Check if the test date is within the specified period
                    if start_date <= test_date <= end_date:
                        filtered_records.append(line)

                # Print the filtered records
                if filtered_records:
                    for record in filtered_records:
                        print(record)
                        record_str = str(record)
                        records_set.add(record_str)
                        parts = record.split(',')
                        result = parts[2].strip()
                        #print(result)
                        result = float(result)
                        # print(result)
                        results.append(result)
                else:
                    print("No records found within the specified date range.")
                print("=================================================================")

        except FileNotFoundError:
            print(f"FILE {filename} NOT FOUND.")
        print("-----------------------------REPORT------------------------------")
        print(f"MIN. VALUE: {min(results)}")
        print(f"MAX. VALUE: {max(results)}")
        print(f"AVG. VALUE: {statistics.mean(results)}")
        print("=================================================================")
        return records_set

    def calculate_turnaround(self, start_time_str, end_time_str):
        start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M')
        end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M')
        turnaround_time = (end_time - start_time).total_seconds() / 60.0  # Convert to minutes
        return turnaround_time

    def filter_by_turnaround(self, filename, min_period, max_period):
        import statistics
        results = []
        try:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split(',')
                    patient_id = parts[0].split(':')[0].strip()
                    test_name = parts[0].split(':')[1].strip()
                    test_date_time = parts[1].strip()
                    result = parts[2].strip()
                    #print(result)
                    unit = parts[3].strip()
                    status = parts[4].strip()
                    completion_date_time = parts[5].strip() if len(parts) > 5 else None

                    if status.lower() == 'completed' and completion_date_time:
                        # Extract the start and completion times
                        start_time = test_date_time
                        end_time = completion_date_time

                        # Calculate turnaround time
                        turnaround_time = MAIN.calculate_turnaround(self, start_time, end_time)

                        # Check if turnaround time is within the specified range
                        if min_period <= turnaround_time <= max_period:
                            print(line)
                            print(
                                f'Patient ID: {patient_id}, Test Name: {test_name}, Turnaround Time: {turnaround_time} minutes')
                            print("=================================================================")

                            result = float(result)
                            results.append(result)


        except FileNotFoundError:
            print(f"File {filename} not found.")
        print("-----------------------------REPORT------------------------------")
        print(f"MIN. VALUE: {min(results)}")
        print(f"MAX. VALUE: {max(results)}")
        print(f"AVG. VALUE: {statistics.mean(results)}")
        print("=================================================================")


    def filter_medical_tests(self, patients, patienstObj):
        """Read from user the filtering criteria."""
        print("Please enter the criteria you want to filter based on:")
        print("1- Single criterion.")
        print("2- Two criterion.")
        print("3- Test Period Filter.")
        print("4- Turnaround period Filter.")
        print("=================================================================")
        selection = input("Criteria Num.")
        selection = int(selection)
        print("=================================================================")
        if selection == 1:
            MAIN.singleFilter(self, patients, patienstObj)
        elif selection == 2:
            MAIN.twoFilter(self, patients, patienstObj)
        elif selection == 3:
            records_set = set()
            records_set = MAIN.periodFilter(self, patients)
        elif selection == 4:
            while 1:

                min_period = float(input("Enter minimum turnaround time (in minutes): "))
                max_period = float(input("Enter maximum turnaround time (in minutes): "))
                print("=================================================================")
                if min_period >= max_period:
                    print("Invalid! Min. must be less than Max.")
                    print("=================================================================")

                else:
                    break
            MAIN.filter_by_turnaround(self, 'medicalRecord.txt', min_period, max_period)

        else:
            print("Invalid selection.")
            return

    def exportToCSV(self):
        try:
            f1o = open("medicalRecord.txt", 'r')
            f2o = open("medicalRecord.csv", 'w', newline='')
            # Initialize CSV writer
            writer = csv.writer(f2o)

            # write header
            writer.writerow(['Record ID', 'Test Type', 'Date and Time', 'Value', 'Unit', 'Status', 'Completion Time'])

            for line in f1o:
                # Strip any whitespace and split the line by commas
                records = [record.strip() for record in line.strip().split(',')]

                # Split the first part by colon to separate PatientID and TestName
                PID, testType = records[0].split(':', 1)
                PID = PID.strip()
                testT = testType.strip()

                # Handle cases where time completion does not exist
                if len(records) == 6:
                    # If completion time does not exist, append an empty string for it
                    records.append('')

                # Ensure that we have 7 elements
                row = [PID, testType] + records[1:]

                # Write row to CSV file
                writer.writerow(row)
        except Exception as e:
            print(f"An error occurred: {e}")
        print("\nRECORDS EXPORTED SUCCESSFULLY TO A COMMA SEPARATED FILE.\n")

    # function to import records from a comma separated file
    def import_records(self):
        fileName = "medical_records.csv"

        new_records = []

        with open(fileName, 'r') as comma_file:
            file_read = csv.reader(comma_file)

            # skip the header
            next(file_read)

            # main proccess
            for line in file_read:
                if len(line) == 6:
                    id, test_name, test_date, result, unit, status = line[:6]
                    record = f"{id}: {test_name}, {test_date}, {result}, {unit}, {status}"
                    new_records.append(record)
                elif len(line) > 6:
                    id, test_name, test_date, result, unit, status = line[:6]
                    comp_date = line[6]
                    record = f"{id}: {test_name}, {test_date}, {result}, {unit}, {status}, {comp_date}"
                    new_records.append(record)

            # save the records to medical records file
        with open("medicalRecord.txt", 'a') as dest_file:
            for rec in new_records:
                dest_file.write(rec + '\n')

        print("\nRECORDS IMPORTED SUCCESSFULLY FROM THE COMMA SEPARATED FILE.\n")


main = MAIN()