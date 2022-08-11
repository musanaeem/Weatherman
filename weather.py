# Imports written in alphabetical order
from os import path
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
        self.__highest_argument = highest_argument
        self.__average_argument = average_argument
        self.__chart_form_argument = chart_form_argument
        self.__chart_form_combined = chart_form_combined

        # Variables used to cater multiple inputs of a specific argument
        self.__curr_e = None
        self.__curr_a = None
        self.__curr_c = None

        # Dictionaries as class instances to store calculation results
        self.highest_argument_result = dict()
        self.average_argument_result = dict()
        self.chart_form_argument_results = dict()

        # Initialize Lists in these indexes of dictionary
        self.chart_form_argument_results["max_temp"] = []
        self.chart_form_argument_results["min_temp"] = []

        # Report Number to print
        self.report_num = 1

    # Method to extract weather files to specified path
    def extract_files(self):
        # Extract the weatherman.zip file to path
        with zipfile.ZipFile("weatherfiles.zip", 'r') as zip_ref:
            zip_ref.extractall(self.__path)

    # Method to get data to print from class level data structures according to mode passed
    def get_data(self, mode):
        if mode == "e":

            high_date = self.highest_argument_result['maxdate']
            low_date = self.highest_argument_result['mindate']
            high_temp = self.highest_argument_result['maxtemp']
            low_temp = abs(self.highest_argument_result['mintemp'])

            high_date = high_date.split("-")  # Separating date into day, month and year
            low_date = low_date.split("-")

            high_month = Weatherman.months[int(high_date[1])-1]
            high_year = high_date[2]
            low_month = Weatherman.months[int(low_date[1])-1]
            low_year = low_date[2]

            return high_temp, low_temp, high_month, low_month, high_year, low_year

        elif mode == "a":
            high_avg_temp = round(self.average_argument_result['avgmaxtemp'])
            low_avg_temp = round(abs(self.average_argument_result['avgmintemp']))  # abs used to counteract negative results
            mean_avg_hum = round(self.average_argument_result['avghumid'])

            return high_avg_temp, low_avg_temp, mean_avg_hum

        elif mode == "c":
            max_pads = []
            min_pads = []
            max_pad = ""
            min_pad = ""

            max_temp = self.chart_form_argument_results["max_temp"]
            min_temp = self.chart_form_argument_results["min_temp"]

            # Run loop for all the days logged
            for i in range(len(max_temp)):

                # Making '+' Strings to pad to output
                for j in range(max_temp[i]):
                    max_pad += "+"

                for j in range(abs(min_temp[i])):
                    min_pad += "+"

                # Adding color to strings
                max_pad = colored(max_pad, 'red')
                min_pad = colored(min_pad, 'blue')

                # Adding results to a list to return to print
                max_pads.append(max_pad)
                min_pads.append(min_pad)

                # Resetting values for next iteration
                max_pad = ""
                min_pad = ""

            return max_temp, min_temp, max_pads, min_pads

    def generate_report_highest(self):
        high_temp, low_temp, high_month, low_month, high_year, low_year = self.get_data("e")  # Data to print

        # Making use of format strings to output results
        print(
            f"""Report Number {self.report_num}
                        Highest: {high_temp}C on {high_month} {high_year}
                        Lowest: {low_temp}C on {low_month} {low_year}
                            """)
        self.report_num += 1  # Recording report number to display multiple reports

    def generate_report_average(self):
        high_avg_temp, low_avg_temp, mean_avg_hum = self.get_data("a")
        print(
            f"""Report Number {self.report_num}
                        Highest Average: {high_avg_temp}C
                        Lowest Average: {low_avg_temp}C
                        Average Mean Humidity: {mean_avg_hum}%
                            """)
        self.report_num += 1

    def generate_report_chart_form(self):
        max_temp, min_temp, max_pads, min_pads = self.get_data("c")

        print(f'''Report Number {self.report_num}''')

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
    def print_report(self, mode):

        # Checking which argument is true to print accordingly
        if mode == "e":
            self.generate_report_highest()

        elif mode == "a":
            self.generate_report_average()

        elif mode == "c":
            self.generate_report_chart_form()

    # Method to read lines from the file and return
    def reader(self, mode):

        pth = self.__path + "/weatherfiles/" + Weatherman.file_name_prefix  # path common in all files
        exist = False
        date = ""

        mult_lines = []

        if mode == "e":
            date = self.__curr_e.split('/')  # split date into year and month

        elif mode == "a":
            date = self.__curr_a.split('/')

        elif mode == "c":
            date = self.__curr_c.split('/')
            if len(date) < 2:
                raise Exception("Please Enter the correct year and month for -c")

        if len(date[0]) != 4:  # To check if year is entered correctly
            raise Exception("Wrong year Format entered")

        if len(date) < 2:  # To check if month is inputted or only year
            for month in Weatherman.months:  # Running code for all 12 months and opening files that exist
                file = pth + date[0] + "_" + month + ".txt"

                if path.exists(file):  # if file for that month exists
                    exist = True  # To check if even on file exists in a year
                    f = open(file, 'r')
                    lines = f.readlines()  # Reading all the lines in a file
                    mult_lines.append(lines)  # Adding lines to a list of file lines
            if not exist:
                raise Exception("Files for this year are not in the system.")
        else:
            mon = int(date[1])  # Getting month in word form
            if 0 < mon < 13:  # Validate month is in between 1-12
                file = pth + date[0] + "_" + Weatherman.months[mon-1] + ".txt"

                if path.exists(file):
                    f = open(file, 'r')
                    lines = f.readlines()
                    mult_lines.append(lines)
                else:
                    raise Exception("No such file exists. Please enter file that is in the system")

            else:
                raise Exception("Wrong format of month entered")

        return mult_lines

    def calculate_highest(self):
        high_temp = 0
        low_temp = sys.maxsize

        mult_lines = self.reader("e")  # Reader gives all the lines in file(s)

        for lines in mult_lines:
            for line in lines[1:]:  # Ignore first line as that is entirely string
                lst = line.split(',')  # Split line into list with elements separated with by ','

                if lst[1] != "":  # lst[1] contains high temp results in a line
                    if int(lst[1]) > high_temp:  # code to check highest
                        high_temp = int(lst[1])
                        high_date = lst[0]

                if lst[3] != "":  # lst[3] contains low temp results in a line
                    if int(lst[3]) < low_temp:  # code to check lowest
                        low_temp = int(lst[3])
                        low_date = lst[0]

        # Storing the results obtained into a data structure defined in class level dictionaries
        self.highest_argument_result['maxtemp'] = high_temp
        self.highest_argument_result['mintemp'] = low_temp
        self.highest_argument_result['maxdate'] = high_date
        self.highest_argument_result['mindate'] = low_date

        # Function that prints report according to the mode provided
        self.print_report("e")

    def calculate_average(self):
        avg_max_temp = 0
        avg_min_temp = 0
        avg_humidity = 0

        count_max_temp = 0  # variables to count number of occurrences to calculate avg
        count_min_temp = 0
        count_humidity = 0

        mult_lines = self.reader("a")

        for lines in mult_lines:
            for line in lines[1:]:
                lst = line.split(',')

                if lst[1] != "":
                    avg_max_temp += int(lst[1])  # adding up all the temperature occurrences
                    count_max_temp += 1

                if lst[3] != "":
                    avg_min_temp += int(lst[3])
                    count_min_temp += 1

                if lst[9] != "":  # lst[3] contains mean humidity results in a line
                    avg_humidity += int(lst[9])
                    count_humidity += 1

        # Storing average of results obtained in class level dictionaries
        self.average_argument_result['avgmaxtemp'] = avg_max_temp / count_max_temp
        self.average_argument_result['avgmintemp'] = avg_min_temp / count_min_temp
        self.average_argument_result['avghumid'] = avg_humidity / count_humidity

        self.print_report("a")

    def calculate_chart_form_data(self):
        mult_lines = self.reader("c")

        for lines in mult_lines:
            for line in lines[1:]:
                lst = line.split(',')

                if lst[1] != "":
                    self.chart_form_argument_results["max_temp"].append(int(lst[1]))  # adding to list in dictionary to print them all

                if lst[3] != "":
                    self.chart_form_argument_results['min_temp'].append(int(lst[3]))
        self.print_report("c")

    # Method that calculates the read data
    def calculate_results(self, mode):

        # Calculate according to argument provided
        if mode == "e":
            self.calculate_highest()

        elif mode == "a":
            self.calculate_average()

        elif mode == "c":
            self.calculate_chart_form_data()

    # The method main calls to start the code
    def run(self):
        self.extract_files()  # call function to extract weatherman zip to path

        # All arguments will be checked to ensure multiple arguments accepted
        if self.__highest_argument is not None:  # check if -e argument was set
            for e in self.__highest_argument:  # code that caters to multiple inputs to one argument to generate multiple reports
                self.__curr_e = e
                self.calculate_results("e")  # Calculating results one input at a time
        if self.__average_argument is not None:
            for a in self.__average_argument:
                self.__curr_a = a
                self.calculate_results("a")
        if self.__chart_form_argument is not None:
            for c in self.__chart_form_argument:
                self.__curr_c = c
                self.calculate_results("c")
