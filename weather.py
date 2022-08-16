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
        self.files_path_prefix = self.__path + "/weatherfiles/" + Weatherman.file_name_prefix  # path common in all files

        # Report Number to print
        self.report_num = 1

    def file_exists(self, date):

        if len(date) < 2:  # To check if month is inputted or only year
            for month in self.months:  # Running code for all 12 months and opening files that exist
                file = self.files_path_prefix + date[0] + "_" + month + ".txt"

                if path.exists(file):
                    return True

            raise Exception("Files for this year are not in the system.")

        else:
            mon = int(date[1])
            if 0 < mon < 13:  # Validate month is in between 1-12
                file = self.files_path_prefix + date[0] + "_" + self.months[mon - 1] + ".txt"
                if path.exists(file):
                    return True
            else:
                raise Exception("Invalid month entered")

            raise Exception("Files for this year are not in the system.")

    def check_input_validity(self, date, mode):

        if len(date[0]) != 4:  # To check if year is entered correctly
            raise Exception("Wrong year Format entered")
        if mode == "c":
            if len(date) < 2:
                raise Exception("Please Enter the correct year and month for -c")

        return self.file_exists(date)

    # Method to extract weather files to specified path
    def extract_files(self):
        # Extract the weatherman.zip file to path
        with zipfile.ZipFile("weatherfiles.zip", "r") as zip_ref:
            zip_ref.extractall(self.__path)

    def get_highest_argument_data(self, result):
        high_date = result["maxdate"]
        low_date = result["mindate"]
        humid_date = result["humiddate"]

        high_temp = result["maxtemp"]
        low_temp = abs(result["mintemp"])
        humid_percent = result["humid"]

        high_date = high_date.split("-")  # Separating date into day, month and year
        low_date = low_date.split("-")
        humid_date = humid_date.split("-")

        high_month = Weatherman.months[int(high_date[1]) - 1]
        high_year = high_date[2]
        low_month = Weatherman.months[int(low_date[1]) - 1]
        low_year = low_date[2]
        humid_month = Weatherman.months[int(humid_date[1]) - 1]
        humid_year = humid_date[2]

        return high_temp, low_temp, high_month, low_month, high_year, low_year, humid_percent, humid_month, humid_year

    def get_average_argument_data(self, result):
        high_avg_temp = round(int(result["avgmaxtemp"]))
        low_avg_temp = round(abs(result["avgmintemp"]))  # abs used to counteract negative results
        mean_avg_hum = round(result["avghumid"])

        return high_avg_temp, low_avg_temp, mean_avg_hum

    def get_chart_argument_data(self, result):
        max_pads = []
        min_pads = []
        max_pad = ""
        min_pad = ""

        max_temp = result["max_temp"]
        min_temp = result["min_temp"]

        # Run loop for all the days logged
        for i in range(len(max_temp)):

            # Making '+' Strings to pad to output
            for j in range(max_temp[i]):
                max_pad += "+"

            for j in range(abs(min_temp[i])):
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

        return max_temp, min_temp, max_pads, min_pads

    def generate_report_highest(self, result):
        high_temp, low_temp, high_month, low_month, high_year, low_year,\
            humid_percent, humid_month, humid_year = self.get_highest_argument_data(result)  # Data to print

        # Making use of format strings to output results
        print(
            f"""Report Number {self.report_num}
                        Highest: {high_temp}C on {high_month} {high_year}
                        Lowest: {low_temp}C on {low_month} {low_year}
                        Humidity: {humid_percent}% on {humid_month} {humid_year}
                            """)
        self.report_num += 1  # Recording report number to display multiple reports

    def generate_report_average(self, result):
        high_avg_temp, low_avg_temp, mean_avg_hum = self.get_average_argument_data(result)
        print(
            f"""Report Number {self.report_num}
                        Highest Average: {high_avg_temp}C
                        Lowest Average: {low_avg_temp}C
                        Average Mean Humidity: {mean_avg_hum}%
                            """)
        self.report_num += 1

    def generate_report_chart_form(self, result):
        max_temp, min_temp, max_pads, min_pads = self.get_chart_argument_data(result)

        print(f"""Report Number {self.report_num}""")

        # Run loop for all the days logged
        for i in range(len(max_temp)):

            # If !b, Print according to c argument, else print according to bonus task
            if self.__chart_form_combined == 0:
                print(
                    f"""        
                        {i + 1} {max_pads[i]} {max_temp[i]}C
                        {i + 1} {min_pads[i]} {min_temp[i]}C""")

            else:
                print(
                    f"""
                        {i + 1} {min_pads[i]}{max_pads[i]} {min_temp[i]}C - {max_temp[i]}C""")

        self.report_num += 1

    # Method to Print report of calculated results
    def print_report(self, mode, result):

        # Checking which argument is true to print accordingly
        if mode == "e":
            self.generate_report_highest(result)

        elif mode == "a":
            self.generate_report_average(result)

        elif mode == "c":
            self.generate_report_chart_form(result)

    # Method to read lines from the file and return

    def calculate_highest_helper(self, dic, high_temp, low_temp, high_humidity, high_date, low_date, humid_date):

        #lst = line.split(",")  # Split line into list with elements separated with by ','

        if dic["Max TemperatureC"] != "":  # lst[1] contains high temp results in a line
            if int(dic["Max TemperatureC"]) > high_temp:  # code to check highest
                high_temp = int(dic["Max TemperatureC"])
                high_date = dic["PKT"]

        if dic["Min TemperatureC"] != "":  # lst[3] contains low temp results in a line
            if int(dic["Min TemperatureC"]) < low_temp:  # code to check lowest
                low_temp = int(dic["Min TemperatureC"])
                low_date = dic["PKT"]

        if dic["Max Humidity"] != "":
            if int(dic["Max Humidity"]) > high_humidity:
                high_humidity = int(dic["Max Humidity"])
                humid_date = dic["PKT"]

        return high_temp, high_date, low_temp, low_date, high_humidity, humid_date

    def highest_per_month(self, year, month, high_temp, low_temp,
                          high_humidity, high_date,
                          low_date, humid_date):

        file = self.files_path_prefix + year + "_" + month + ".txt"

        if path.exists(file):
            reader = CSVReader(file)

            dictionary = reader.get_line()
            while dictionary:
                high_temp, high_date, low_temp, low_date, high_humidity, humid_date \
                    = self.calculate_highest_helper(dictionary, high_temp, low_temp,
                                                    high_humidity, high_date,
                                                    low_date, humid_date)
                dictionary = reader.get_line()

            return True, high_temp, high_date, low_temp, low_date, high_humidity, humid_date
        return False, high_temp, high_date, low_temp, low_date, high_humidity, humid_date

    def calculate_highest(self, date):
        high_temp = 0
        high_humidity = 0
        low_temp = sys.maxsize
        high_date, low_date, humid_date = "", "", ""
        exists = False

        if len(date) < 2:  # To check if month is inputted or only year
            for month in self.months:  # Running code for all 12 months and opening files that exist
                if not exists:  # If no files found, keep checking
                    exists, high_temp, high_date, low_temp, low_date, high_humidity,\
                     humid_date = self.highest_per_month(date[0], month, high_temp,
                                                         low_temp, high_humidity, high_date,
                                                         low_date, humid_date)

                else:  # If even one file found, set exist as True and ignore that tuple value
                    _, high_temp, high_date, low_temp, low_date, high_humidity,\
                     humid_date = self.highest_per_month(date[0], month, high_temp,
                                                         low_temp, high_humidity, high_date,
                                                         low_date, humid_date)
            if not exists:
                raise Exception("Files for this year are not in the system.")

        else:
            mon = int(date[1])  # Getting month in word form
            if 0 < mon < 13:  # Validate month is in between 1-12
                month = self.months[mon - 1]

                _, high_temp, high_date, low_temp, low_date, high_humidity, \
                humid_date = self.highest_per_month(date[0], month, high_temp,
                                                    low_temp, high_humidity, high_date,
                                                    low_date, humid_date)

        results = dict()
        # Storing the results obtained into a data structure defined in class level dictionaries
        results["maxtemp"] = high_temp
        results["mintemp"] = low_temp
        results["maxdate"] = high_date
        results["mindate"] = low_date
        results["humid"] = high_humidity
        results["humiddate"] = humid_date

        return results

    def calculate_average_helper(self, dic, avg_max_temp, count_max_temp,
                                 avg_min_temp, count_min_temp, avg_humidity, count_humidity):

        if dic["Max TemperatureC"] != "":
            avg_max_temp += int(dic["Max TemperatureC"])  # adding up all the temperature occurrences
            count_max_temp += 1

        if dic["Min TemperatureC"] != "":
            avg_min_temp += int(dic["Min TemperatureC"])
            count_min_temp += 1

        if dic[" Mean Humidity"] != "":  # lst[3] contains mean humidity results in a line
            avg_humidity += int(dic[" Mean Humidity"])
            count_humidity += 1

        return avg_max_temp, count_max_temp, avg_min_temp, count_min_temp, avg_humidity, count_humidity

    def average_per_month(self, year, month, avg_max_temp, count_max_temp,
                          avg_min_temp, count_min_temp, avg_humidity, count_humidity):

        file = self.files_path_prefix + year + "_" + month + ".txt"

        if path.exists(file):
            reader = CSVReader(file)

            dictionary = reader.get_line()
            while dictionary:
                avg_max_temp, count_max_temp, avg_min_temp, \
                    count_min_temp, avg_humidity, count_humidity \
                    = self.calculate_average_helper(dictionary, avg_max_temp, count_max_temp,
                                                    avg_min_temp, count_min_temp, avg_humidity, count_humidity)
                dictionary = reader.get_line()

            return True, avg_max_temp, count_max_temp, avg_min_temp, count_min_temp, avg_humidity, count_humidity
        return False, avg_max_temp, count_max_temp, avg_min_temp, count_min_temp, avg_humidity, count_humidity

    def calculate_average(self, date):
        avg_max_temp = 0
        avg_min_temp = 0
        avg_humidity = 0

        count_max_temp = 0  # variables to count number of occurrences to calculate avg
        count_min_temp = 0
        count_humidity = 0

        exists = False

        if len(date) < 2:  # To check if month is inputted or only year

            for month in Weatherman.months:  # Running code for all 12 months and opening files that exist

                if not exists:  # If no files found, keep checking
                    exists, avg_max_temp, count_max_temp, avg_min_temp,\
                     count_min_temp, avg_humidity, count_humidity\
                     = self.average_per_month(date[0], month, avg_max_temp,
                                              count_max_temp, avg_min_temp,
                                              count_min_temp, avg_humidity, count_humidity)

                else:  # If even one file found, set exist as True and ignore that tuple value
                    _, avg_max_temp, count_max_temp, avg_min_temp, \
                     count_min_temp, avg_humidity, count_humidity \
                     = self.average_per_month(date[0], month, avg_max_temp,
                                              count_max_temp, avg_min_temp,
                                              count_min_temp, avg_humidity, count_humidity)

            if not exists:
                raise Exception("Files for this year are not in the system.")

        else:
            mon = int(date[1])  # Getting month in word form
            if 0 < mon < 13:  # Validate month is in between 1-12
                month = self.months[mon - 1]

                _, avg_max_temp, count_max_temp, avg_min_temp, \
                    count_min_temp, avg_humidity, count_humidity \
                    = self.average_per_month(date[0], month, avg_max_temp,
                                             count_max_temp, avg_min_temp,
                                             count_min_temp, avg_humidity, count_humidity)

        results = dict()

        # Storing average of results obtained in class level dictionaries
        results["avgmaxtemp"] = avg_max_temp / count_max_temp
        results["avgmintemp"] = avg_min_temp / count_min_temp
        results["avghumid"] = avg_humidity / count_humidity

        return results

    def calculate_chart_form_data_helper(self, dic, results):

        if dic["Max TemperatureC"] != "":
            results["max_temp"].append(
                int(dic["Max TemperatureC"]))  # adding to list in dictionary to print them all

        if dic["Min TemperatureC"] != "":
            results["min_temp"].append(
                int(dic["Min TemperatureC"]))

        return results

    def calculate_chart_form_data(self, date):
        results = dict()
        results["max_temp"] = []
        results["min_temp"] = []

        mon = int(date[1])  # Getting month in word form
        if 0 < mon < 13:  # Validate month is in between 1-12
            file = self.files_path_prefix + date[0] + "_" + self.months[mon - 1] + ".txt"
            reader = CSVReader(file)

            dictionary = reader.get_line()
            while dictionary:
                results = self.calculate_chart_form_data_helper(dictionary, results)
                dictionary = reader.get_line()

            return results

    # Method that calculates the read data
    def argument_handler(self, curr, argument_type):
        date = curr.split('/')
        is_valid = self.check_input_validity(date, argument_type)

        result = dict()

        if is_valid:
            if argument_type == "e":
                result = self.calculate_highest(date)
            elif argument_type == "a":
                result = self.calculate_average(date)
            else:
                result = self.calculate_chart_form_data(date)

        # Function that prints report according to the mode provided
        self.print_report(argument_type, result)
        result.clear()

    # The method main calls to start the code
    def run(self):
        self.extract_files()  # call function to extract weatherman zip to path

        # All arguments will be checked to ensure multiple arguments accepted
        if self.__highest_arguments is not None:  # check if -e argument was set
            for highest_argument in self.__highest_arguments:  # catering multiple inputs argument for multiple reports
                self.argument_handler(highest_argument, "e")  # Calculating results one input at a time

        if self.__average_arguments is not None:  # check if -a argument was set
            for average_argument in self.__average_arguments:
                self.argument_handler(average_argument, "a")

        if self.__chart_form_arguments is not None:  # check if -c argument was set
            for chart_form_argument in self.__chart_form_arguments:
                self.argument_handler(chart_form_argument, "c")
