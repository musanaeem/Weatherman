from os import path
import sys
from termcolor import colored
import zipfile


class Weatherman:  # Weatherman Application in one class

    file_pre = "Murree_weather_"  # The part of the file name that is same for all files

    # Dictionaries as class instances to store calculation results
    e_result = dict()
    a_result = dict()
    c_result = dict()

    # Report Number to print
    report_num = 1

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

        self.__curr_e = None
        self.__curr_a = None
        self.__curr_c = None

    # Method to extract weather files to specified path
    def Extract(self):
        # Extract the weatherman.zip file to path
        with zipfile.ZipFile("weatherfiles.zip", 'r') as zip_ref:
            zip_ref.extractall(self.__path)

    def getData(self, mode):
        if mode == "e":

            high_date = Weatherman.e_result['maxdate']
            low_date = Weatherman.e_result['mindate']
            high_temp = Weatherman.e_result['maxtemp']
            low_temp = abs(Weatherman.e_result['mintemp'])

            high_date = high_date.split("-")  # Separating date into day, month and year
            low_date = low_date.split("-")

            high_month = Weatherman.months[int(high_date[1])-1]
            high_year = high_date[2]
            low_month = Weatherman.months[int(low_date[1])-1]
            low_year = low_date[2]

            return high_temp, low_temp, high_month, low_month, high_year, low_year

        elif mode == "a":
            high_avg_temp = round(Weatherman.a_result['avgmaxtemp'])
            low_avg_temp = round(abs(Weatherman.a_result['avgmintemp']))
            mean_avg_hum = round(Weatherman.a_result['avghumid'])

            return high_avg_temp, low_avg_temp, mean_avg_hum

        elif mode == "c":
            max_pads = []
            min_pads = []
            max_pad = ""
            min_pad = ""

            max_temp = Weatherman.c_result["max_temp"]
            min_temp = Weatherman.c_result["min_temp"]

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

                max_pads.append(max_pad)
                min_pads.append(min_pad)

                max_pad = ""
                min_pad = ""

            return max_temp, min_temp, max_pads, min_pads

    # Method to Print report of calculated results
    def Print_report(self, mode):

        # Checking which argument is true to print accordingly
        if mode == "e":
            high_temp, low_temp, high_month, low_month, high_year, low_year = self.getData("e")

            # Making use of format strings to output results
            print(
            f"""Report Number {Weatherman.report_num}
                Highest: {high_temp}C on {high_month} {high_year}
                Lowest: {low_temp}C on {low_month} {low_year}
                    """)
            Weatherman.report_num += 1

        elif mode == "a":
            high_avg_temp, low_avg_temp, mean_avg_hum = self.getData("a")
            print(
            f"""Report Number {Weatherman.report_num}
                Highest Average: {high_avg_temp}C
                Lowest Average: {low_avg_temp}C
                Average Mean Humidity: {mean_avg_hum}%
                    """)
            Weatherman.report_num += 1

        elif mode == "c":

            max_temp, min_temp, max_pads, min_pads = self.getData("c")

            print(f'''Report Number {Weatherman.report_num}''')

            # Run loop for all the days logged
            for i in range(len(max_temp)):

                # If !b, Print according to c argument, else print according to bonus task
                if self.__b == 0:
                    print(
                f"""        
                {i+1} {max_pads[i]} {max_temp[i]}C
                {i+1} {min_pads[i]} {min_temp[i]}C""")

                else:
                    print(
                f"""
                {i + 1} {min_pads[i]}{max_pads[i]} {min_temp[i]}C - {max_temp[i]}C""")

            Weatherman.report_num += 1

    # Method to read lines from the file and return
    def Reader(self, mode):

        # path to file till the common part of all files
        pth = self.__path + "/weatherfiles/" + Weatherman.file_pre
        exist = False
        date = ""

        mult_lines = []

        if mode == "e":
            date = self.__curr_e.split('/')

        elif mode == "a":
            date = self.__curr_a.split('/')

        elif mode == "c":
            date = self.__curr_c.split('/')
            if len(date) < 2:
                raise Exception("Please Enter the correct year and month for -c")

        if len(date[0]) != 4:
            raise Exception("Wrong date Format entered")

        if len(date) < 2:
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
            mon = int(date[1])
            if 0 < mon < 13:
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
            for e in self.__e:
                self.__curr_e = e
                self.Calculate_Results("e")
        if self.__a is not None:
            for a in self.__a:
                self.__curr_a = a
                self.Calculate_Results("a")
        if self.__c is not None:
            for c in self.__c:
                self.__curr_c = c
                self.Calculate_Results("c")
