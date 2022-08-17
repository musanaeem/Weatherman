# Imports written in alphabetical order
from os import path
from csv_reader import CSVReader
import sys
from termcolor import colored
import zipfile


class Weatherman:  # Weatherman Application in one class

    file_name_prefix = "Murree_weather_"  # The part of the file name that is same for all files

    # List with months to access by numerical form
    months = ["Jan", "Feb", "Mar",
              "Apr", "May", "Jun",
              "Jul", "Aug", "Sep",
              "Oct", "Nov", "Dec"
              ]

    # Class Constructor
    def __init__(self, path, highest_argument, average_argument, chart_form_argument, chart_form_combined):
        self.__path = path
        self.__highest_arguments = highest_argument
        self.__average_arguments = average_argument
        self.__chart_form_arguments = chart_form_argument
        self.__chart_form_combined = chart_form_combined

        # path common in all files
        self.files_path_prefix = self.__path + "/weatherfiles/" + Weatherman.file_name_prefix

        # Report Number to print
        self.report_num = 1

    # The method main calls to start the code
    def run(self):
        self.extract_files()  # call function to extract weatherman zip to path

        # All arguments will be checked to ensure multiple arguments accepted
        if self.__highest_arguments is not None:  # check if -e argument was set
            for highest_argument in self.__highest_arguments:  # catering multiple inputs argument for multiple reports
                self.highest_argument_handler(highest_argument)  # Calculating results one input at a time

        if self.__average_arguments is not None:  # check if -a argument was set
            for average_argument in self.__average_arguments:
                self.average_argument_handler(average_argument)

        if self.__chart_form_arguments is not None:  # check if -c argument was set
            for chart_form_argument in self.__chart_form_arguments:
                self.chart_argument_handler(chart_form_argument)

    # Method to extract weather files to specified path
    def extract_files(self):
        # Extract the weatherman.zip file to path
        with zipfile.ZipFile("weatherfiles.zip", "r") as zip_ref:
            zip_ref.extractall(self.__path)

    # Method that calculates the read data
    def highest_argument_handler(self, current_argument):

        is_valid = self.validate_year(current_argument)

        if is_valid:
            is_file = self.files_exists_in_year(current_argument)

            if is_file:
                result = self.calculate_highest(current_argument)

                # Function that prints report according to the mode provided
                self.generate_report_highest(result)
            else:
                print(f"Files for the year {current_argument} are not in the system.")

    def validate_year(self, date):

        if len(date) != 4:  # To check if year is entered correctly
            print("Wrong year Format entered")
            return False
        return True

    def files_exists_in_year(self, date):
        for month in self.months:  # Running code for all 12 months and opening files that exist
            file = self.get_file_path(date, month)

            if path.exists(file):
                return True
        return False

    def get_file_path(self, year, month):
        if month.isdigit():
            mon = int(month)
            if 0 < mon < 12:
                mon = self.months[mon - 1]
                return self.files_path_prefix + year + "_" + mon + ".txt"
        else:
            return self.files_path_prefix + year + "_" + month + ".txt"

    def calculate_highest(self, date):
        highest_temp = 0
        highest_humidity = 0
        lowest_temp = sys.maxsize
        highest_date, lowest_date, humid_date = "", "", ""
        exists = False

        for month in self.months:  # Running code for all 12 months and opening files that exist
            year = date

            file = self.files_path_prefix + year + "_" + month + ".txt"

            if path.exists(file):  # If file exists
                highest_temp, highest_date, lowest_temp, lowest_date, highest_humidity,\
                 humid_date = self.highest_per_month(file, highest_temp,
                                                     lowest_temp, highest_humidity, highest_date,
                                                     lowest_date, humid_date)
                exists = True

        if not exists:
            print("Files for this year are not in the system.")

        results = dict()
        # Storing the results obtained into a data structure defined in class level dictionaries
        results["highest_temperature"] = highest_temp
        results["lowest_temperature"] = lowest_temp
        results["highest_date"] = highest_date
        results["lowest_date"] = lowest_date
        results["humid"] = highest_humidity
        results["humidity_date"] = humid_date

        return results

    def highest_per_month(self, file, highest_temp, lowest_temp,
                          highest_humidity, highest_date,
                          lowest_date, humid_date):

        reader = CSVReader(file)

        dictionary = reader.get_record()
        while dictionary:
            highest_temp, highest_date, lowest_temp, lowest_date, highest_humidity, humid_date \
                = self.calculate_highest_helper(dictionary, highest_temp, lowest_temp,
                                                highest_humidity, highest_date,
                                                lowest_date, humid_date)
            dictionary = reader.get_record()

        return highest_temp, highest_date, lowest_temp, lowest_date, highest_humidity, humid_date

    def calculate_highest_helper(self, dic, highest_temp, lowest_temp, highest_humidity, highest_date, lowest_date, humid_date):

        if dic["Max TemperatureC"] != "":  # lst[1] contains highest temp results in a line
            if int(dic["Max TemperatureC"]) > highest_temp:  # code to check highest
                highest_temp = int(dic["Max TemperatureC"])
                highest_date = dic["PKT"]

        if dic["Min TemperatureC"] != "":  # lst[3] contains lowest temp results in a line
            if int(dic["Min TemperatureC"]) < lowest_temp:  # code to check lowest
                lowest_temp = int(dic["Min TemperatureC"])
                lowest_date = dic["PKT"]

        if dic["Max Humidity"] != "":
            if int(dic["Max Humidity"]) > highest_humidity:
                highest_humidity = int(dic["Max Humidity"])
                humid_date = dic["PKT"]

        return highest_temp, highest_date, lowest_temp, lowest_date, highest_humidity, humid_date

    def generate_report_highest(self, result):
        highest_temp, lowest_temp, highest_month, lowest_month, highest_year, lowest_year,\
            humid_percent, humid_month, humid_year = self.get_highest_argument_data(result)  # Data to print

        # Making use of format strings to output results
        print(
            f"""Report Number {self.report_num}
                        highest: {highest_temp}C on {highest_month} {highest_year}
                        lowest: {lowest_temp}C on {lowest_month} {lowest_year}
                        Humidity: {humid_percent}% on {humid_month} {humid_year}
                            """)
        self.report_num += 1  # Recording report number to display multiple reports

    def get_highest_argument_data(self, result):
        highest_date = result["highest_date"]
        lowest_date = result["lowest_date"]
        humid_date = result["humidity_date"]

        highest_temp = result["highest_temperature"]
        lowest_temp = abs(result["lowest_temperature"])
        humid_percent = result["humid"]

        highest_date = highest_date.split("-")  # Separating date into day, month and year
        lowest_date = lowest_date.split("-")
        humid_date = humid_date.split("-")
        highest_month = Weatherman.months[int(highest_date[1]) - 1]
        highest_year = highest_date[2]
        lowest_month = Weatherman.months[int(lowest_date[1]) - 1]
        lowest_year = lowest_date[2]
        humid_month = Weatherman.months[int(humid_date[1]) - 1]
        humid_year = humid_date[2]

        return highest_temp, lowest_temp, highest_month, lowest_month, highest_year, lowest_year, humid_percent, humid_month, humid_year

    def average_argument_handler(self, current_argument):
        date = current_argument.split("/")
        is_valid = self.validate_month_and_year(date)

        file = self.get_file_path(date[0], date[1])

        if is_valid:
            is_file = self.file_exists(file)

            if is_file:
                result = self.calculate_average(file)

                # Function that prints report according to the mode provided
                self.generate_report_average(result)
            else:
                print(f"Files for the date {current_argument} are not in the system.")

    def validate_month_and_year(self, date):
        if len(date) < 2:
            print("Please Enter the correct year and month for -c")
            return False
        if len(date[0]) != 4:  # To check if year is entered correctly
            print("Wrong year Format entered")
            return False
        if 0 > int(date[1]) < 13:  # Validate month is in between 1-12
            print("Wrong month Format entered")
            return False
        return True

    def file_exists(self, file):
        if path.exists(file):
            return True
        else:
            return False

    def calculate_average(self, file):
        avg_highest_temperature = 0
        avg_lowest_temperature = 0
        avg_humidity = 0

        count_highest_temperature = 0  # variables to count number of occurrences to calculate avg
        count_lowest_temperature = 0
        count_humidity = 0

        if path.exists(file):
            reader = CSVReader(file)

            record = reader.get_record()
            while record:
                avg_highest_temperature, count_highest_temperature, avg_lowest_temperature, \
                 count_lowest_temperature, avg_humidity, count_humidity \
                 = self.calculate_average_helper(record, avg_highest_temperature, count_highest_temperature,
                                                 avg_lowest_temperature, count_lowest_temperature, avg_humidity, count_humidity)
                record = reader.get_record()

        results = dict()

        # Storing average of results obtained in class level dictionaries
        results["avghighest_temperature"] = avg_highest_temperature / count_highest_temperature
        results["avglowest_temperature"] = avg_lowest_temperature / count_lowest_temperature
        results["avghumid"] = avg_humidity / count_humidity

        return results

    def calculate_average_helper(self, dic, avg_highest_temperature, count_highest_temperature,
                                 avg_lowest_temperature, count_lowest_temperature, avg_humidity, count_humidity):

        if dic["Max TemperatureC"] != "":
            avg_highest_temperature += int(dic["Max TemperatureC"])  # adding up all the temperature occurrences
            count_highest_temperature += 1

        if dic["Min TemperatureC"] != "":
            avg_lowest_temperature += int(dic["Min TemperatureC"])
            count_lowest_temperature += 1

        if dic[" Mean Humidity"] != "":  # lst[3] contains mean humidity results in a line
            avg_humidity += int(dic[" Mean Humidity"])
            count_humidity += 1

        return avg_highest_temperature, count_highest_temperature, avg_lowest_temperature, count_lowest_temperature, avg_humidity, count_humidity

    def generate_report_average(self, result):
        highest_avg_temp, lowest_avg_temp, mean_avg_hum = self.get_average_argument_data(result)
        print(
            f"""Report Number {self.report_num}
                        highest Average: {highest_avg_temp}C
                        lowest Average: {lowest_avg_temp}C
                        Average Mean Humidity: {mean_avg_hum}%
                            """)
        self.report_num += 1

    def get_average_argument_data(self, result):
        highest_avg_temp = round(int(result["avghighest_temperature"]))
        lowest_avg_temp = round(abs(result["avglowest_temperature"]))  # abs used to counteract negative results
        mean_avg_hum = round(result["avghumid"])

        return highest_avg_temp, lowest_avg_temp, mean_avg_hum

    def chart_argument_handler(self, current_argument):
        date = current_argument.split("/")
        is_valid = self.validate_month_and_year(date)

        file = self.get_file_path(date[0], date[1])

        if is_valid:
            is_file = self.file_exists(file)

            if is_file:
                result = self.calculate_chart_form_data(file)

                # Function that prints report according to the mode provided
                self.generate_report_chart_form(result)
            else:
                print(f"Files for the date {current_argument} are not in the system.")

    def calculate_chart_form_data(self, file):
        results = dict()
        results["highest_temperature"] = []
        results["lowest_temperature"] = []

        reader = CSVReader(file)

        dictionary = reader.get_record()
        while dictionary:
            results = self.calculate_chart_form_data_helper(dictionary, results)
            dictionary = reader.get_record()

        return results

    def calculate_chart_form_data_helper(self, dic, results):

        if dic["Max TemperatureC"] != "":
            results["highest_temperature"].append(
                int(dic["Max TemperatureC"]))  # adding to list in dictionary to print them all

        if dic["Min TemperatureC"] != "":
            results["lowest_temperature"].append(
                int(dic["Min TemperatureC"]))

        return results

    def generate_report_chart_form(self, result):
        highest_temperature, lowest_temperature, max_pads, min_pads = self.get_chart_argument_data(result)

        print(f"""Report Number {self.report_num}""")

        # Run loop for all the days logged
        for i in range(len(highest_temperature)):

            # If !b, Print according to c argument, else print according to bonus task
            if self.__chart_form_combined == 0:
                print(
                    f"""        
                        {i + 1} {max_pads[i]} {highest_temperature[i]}C
                        {i + 1} {min_pads[i]} {lowest_temperature[i]}C""")

            else:
                print(
                    f"""
                        {i + 1} {min_pads[i]}{max_pads[i]} {lowest_temperature[i]}C - {highest_temperature[i]}C""")

        self.report_num += 1

    def get_chart_argument_data(self, result):
        max_pads = []
        min_pads = []
        max_pad = ""
        min_pad = ""

        highest_temperature = result["highest_temperature"]
        lowest_temperature = result["lowest_temperature"]

        # Run loop for all the days logged
        for i in range(len(highest_temperature)):

            # Making '+' Strings to pad to output
            for j in range(highest_temperature[i]):
                max_pad += "+"

            for j in range(abs(lowest_temperature[i])):
                min_pad += "+"

            # Adding color to strings
            max_pad = colored(max_pad, "red")
            min_pad = colored(min_pad, "blue")

            # Adding results to a list to return to print
            max_pads.append(max_pad)
            min_pads.append(min_pad)

            # Resetting values for next iteration
            max_pad = ""
            min_pad = ""

        return highest_temperature, lowest_temperature, max_pads, min_pads





















