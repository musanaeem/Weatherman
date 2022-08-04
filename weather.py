from os import path
import zipfile
import sys
from termcolor import colored


class Weatherman:  # Weatherman Application in one class

    file_pre = "Murree_weather_"  # The part of the file name that is same for all files

    # Dictionaries as class instances to store calculation results
    e_result = dict()
    a_result = dict()
    c_result = dict()

    # Initialize Lists in these indexes of dictionary
    c_result["max_temp"] = []
    c_result["min_temp"] = []

    # List with months to access by numerical form
    months = ["Jan", "Feb", "Mar",
              "Apr", "May", "Jun",
              "Jul", "Aug", "Sep",
              "Oct", "Nov", "Dec"
              ]

    # Class Constructor
    def __init__(self, path, e, a, c, b):
        self.__path = path
        self.__e = e
        self.__a = a
        self.__c = c
        self.__b = b

    # Method to extract weather files to specified path
    def Extract(self):
        # Extract the weatherman.zip file to path
        with zipfile.ZipFile("weatherfiles.zip", 'r') as zip_ref:
            zip_ref.extractall(self.__path)

    # Method to Print report of calculated results
    def Print_report(self, mode):

        # Checking which argument is true to print accordingly
        if mode == "e":

            high_date = Weatherman.e_result['maxdate']
            low_date = Weatherman.e_result['mindate']

            high_date = high_date.split("-")  # Separating date into day, month and year
            low_date = low_date.split("-")

            # Making use of format strings to output results
            print(f"""
                Highest: {Weatherman.e_result['maxtemp']}C on {Weatherman.months[int(high_date[1])-1]} {high_date[2]}
                Lowest: {Weatherman.e_result['mintemp']}C on {Weatherman.months[int(low_date[1])-1]} {low_date[2]}
                    """)

        elif mode == "a":

            print(f"""
                Highest Average: {round(Weatherman.a_result['avgmaxtemp'])}C
                Lowest Average: {round(Weatherman.a_result['avgmintemp'])}C
                Average Mean Humidity: {round(Weatherman.a_result['avghumid'])}%
                    """)

        elif mode == "c":

            max_pad = ""
            min_pad = ""

            # Run loop for all the days logged
            for i in range(len(Weatherman.c_result["max_temp"])):
                if i > 30:  # Break if days somehow exceed 31 days
                    break

                # Making '+' Strings to pad to output
                for j in range(Weatherman.c_result["max_temp"][i]):
                    max_pad += "+"

                for j in range(Weatherman.c_result["min_temp"][i]):
                    min_pad += "+"

                # Adding color to strings
                max_pad = colored(max_pad, 'red')
                min_pad = colored(min_pad, 'blue')

                # If !b, Print according to c argument, else print according to bonus task
                if self.__b == 0:
                    print(f"""
                    {i+1} {max_pad} {Weatherman.c_result["max_temp"][i]}C
                    {i+1} {min_pad} {Weatherman.c_result["min_temp"][i]}C""")

                    max_pad = ""
                    min_pad = ""
                else:
                    print(f"""
                    {i + 1} {min_pad}{max_pad} {Weatherman.c_result["min_temp"][i]}C - {Weatherman.c_result["max_temp"][i]}C""")

                    max_pad = ""
                    min_pad = ""

    # Method to read lines from the file and return
    def Reader(self, mode):

        # path to file till the common part of all files
        pth = self.__path + "/weatherfiles/" + Weatherman.file_pre
        exist = False
        date = ""

        mult_lines = []

        if mode == "e":
            if self.__e is None:
                raise Exception("Enter an argument for -e")
            else:
                date = self.__e.split('/')

        elif mode == "a":
            if self.__a is None:
                raise Exception("Enter an argument for -a")
            else:
                date = self.__a.split('/')

        elif mode == "c":
            if self.__c is None:
                raise Exception("Enter an argument for -c")
            else:
                date = self.__c.split('/')

            if len(date)<2:
                raise Exception("Please Enter the correct year and month for -c")

        if date == "":
            raise Exception("Date not Entered")

        elif len(date) < 2:
            for month in Weatherman.months:
                file = pth + date[0] + "_" + month + ".txt"

                if path.exists(file):
                    exist = True
                    f = open(file, 'r')
                    lines = f.readlines()
                    mult_lines.append(lines)
            if not exist:
                raise Exception("Files for this year are not in the system.")
        else:
            file = pth + date[0] + "_" + Weatherman.months[int(date[1])-1] + ".txt"

            if path.exists(file):
                f = open(file, 'r')
                lines = f.readlines()
                mult_lines.append(lines)
            else:
                raise Exception("No such file exists. Please enter file that is in the system")

        return mult_lines

    # Method that calculates the read data
    def Calculate_Results(self, mode):

        if mode == "e":
            high_temp = 0
            low_temp = sys.maxsize

            mult_lines = self.Reader("e")

            for lines in mult_lines:
                for line in lines[1:]:
                    lst = line.split(',')

                    if lst[1] != "":
                        if int(lst[1]) > high_temp:
                            high_temp = int(lst[1])
                            high_date = lst[0]

                    if lst[3] != "":
                        if int(lst[3]) < low_temp:
                            low_temp = int(lst[3])
                            low_date = lst[0]

            Weatherman.e_result['maxtemp'] = high_temp
            Weatherman.e_result['mintemp'] = low_temp
            Weatherman.e_result['maxdate'] = high_date
            Weatherman.e_result['mindate'] = low_date

            self.Print_report("e")

        elif mode == "a":
            avg_max_t = 0
            avg_min_t = 0
            avg_humid = 0

            count_max_t = 0
            count_min_t = 0
            count_hum = 0

            mult_lines = self.Reader("a")

            for lines in mult_lines:
                for line in lines[1:]:
                    lst = line.split(',')

                    if lst[1] != "":
                        avg_max_t += int(lst[1])
                        count_max_t += 1

                    if lst[3] != "":
                        avg_min_t += int(lst[3])
                        count_min_t += 1

                    if lst[9] != "":
                        avg_humid += int(lst[9])
                        count_hum += 1

            Weatherman.a_result['avgmaxtemp'] = avg_max_t / count_max_t
            Weatherman.a_result['avgmintemp'] = avg_min_t / count_min_t
            Weatherman.a_result['avghumid'] = avg_humid / count_hum

            self.Print_report("a")

        elif mode == "c":

            mult_lines = self.Reader("c")

            for lines in mult_lines:
                for line in lines[1:]:
                    lst = line.split(',')

                    if lst[1] != "":
                        Weatherman.c_result["max_temp"].append(int(lst[1]))

                    if lst[3] != "":
                        Weatherman.c_result['min_temp'].append(int(lst[3]))
            self.Print_report("c")

    # The method main calls to start the code
    def run(self):
        self.Extract()

        if self.__e is not None:
            self.Calculate_Results("e")
        if self.__a is not None:
            self.Calculate_Results("a")
        if self.__c is not None:
            self.Calculate_Results("c")
