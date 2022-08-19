from os import path


class CSVReader:

    def __init__(self, path):
        self.__file = open(path, "r")
        self.list_of_names = []
        lst = self.__file.readline()
        self.list_of_names = lst.split(",")

    def get_record(self):
        line = self.__file.readline()
        if line == "":
            self.__file.close()
            return
        else:
            values = line.split(",")
            zipped_tuples_to_dict = dict(zip(self.list_of_names, values))
            return zipped_tuples_to_dict




