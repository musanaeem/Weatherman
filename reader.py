from os import path


class Reader:

    file_name_prefix = "Murree_weather_"  # The part of the file name that is same for all files

    def __init__(self, path, months):
        self.line = ""
        self.lines = []
        self.mult_lines = []
        self.__path = path
        self.line_number = 0
        self.months = months

        self.__mode = ""
        self.__argument = ""

        self.files_path_prefix = self.__path + "/weatherfiles/" + Reader.file_name_prefix  # path common in all files

    def set_mode(self, mode):
        self.__mode = mode

    def set_argument(self, argument):
        self.__argument = argument

    def file_exists(self, date):
        exists = False

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

    def check_input_validity(self, date):
        if self.__mode == "c":
            if len(date) < 2:
                raise Exception("Please Enter the correct year and month for -c")
        if len(date[0]) != 4:  # To check if year is entered correctly
            raise Exception("Wrong year Format entered")

        return self.file_exists(date)

    def get_all_lines(self):
        mult_lines = []

        date = self.__argument.split('/')

        is_valid = self.check_input_validity(date)

        if is_valid:
            if len(date) < 2:  # To check if month is inputted or only year
                for month in self.months:  # Running code for all 12 months and opening files that exist
                    file = self.files_path_prefix + date[0] + "_" + month + ".txt"

                    if path.exists(file):
                        f = open(file, 'r')
                        lines = f.readlines()  # Reading all the lines in a file
                        mult_lines.append(lines)  # Adding lines to a list of file lines

            else:
                mon = int(date[1])  # Getting month in word form
                if 0 < mon < 13:  # Validate month is in between 1-12
                    file = self.files_path_prefix + date[0] + "_" + self.months[mon - 1] + ".txt"

                    f = open(file, 'r')
                    lines = f.readlines()
                    mult_lines.append(lines)

            return mult_lines
        else:
            raise Exception("Input was not Valid. Please try again")

    def get_next_line(self):
        pass

    def update_path(self, path):
        self.__path = path
        self.line_number = 0

    def read(self):
        pass
