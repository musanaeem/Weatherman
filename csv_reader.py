from os import path


class CSVReader:

    def __init__(self, path):
        self.__file = open(path, "r")
        self.dictionary = dict()

        self.get_line_in_dict()

    def get_line(self):
        line = self.__file.readline()
        if line == "":
            self.__file.close()
            return
        else:
            lst = line.split(",")
            count = 0
            for dic in self.dictionary:
                self.dictionary[dic] = lst[count]

                count += 1
            #return line
            return self.dictionary
    def get_line_in_dict(self):
        line = self.__file.readline()
        lst = line.split(",")

        for elem in lst:
            self.dictionary[elem] = ""

