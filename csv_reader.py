from os import path


class CSV_Reader:

    def __init__(self, path):
        self.__file = open(path, "r")

    def get_line(self):
        line = self.__file.readline()
        if line == "":
            self.__file.close()
            return
        else:
            return self.__file.readline()
