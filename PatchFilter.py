import os
from fnmatch import fnmatch
import io


def __get_validator(cut_patterns, besides_patterns):

    def should_save(filename):
        return any(fnmatch(filename, pattern) for pattern in besides_patterns) \
               or not all(fnmatch(filename, pattern) for pattern in cut_patterns)

    return should_save


class __FileDiff:

    def __init__(self, name):
        self.__name = name
        self.__lines = []

    def append_line(self, line):
        self.__lines.append(line)

    def write_to_file(self, file):
        for line in self.__lines:
            file.write(line)

    @property
    def name(self):
        return self.__name

    def __str__(self):
        return self.__name


def __diff_files(filename, encoding="UTF-8"):

    with io.open(file=filename, encoding=encoding) as file:
        file_diff = __FileDiff("Temp")

        for line in file:

            if line.startswith("Index"):
                yield file_diff

                file_diff = __FileDiff(line.replace("Index: ", '').replace("\n", ''))

            if file_diff:
                file_diff.append_line(line)


def do_filter(filename, new_filename, cut_patterns, besides_patterns, encoding):

    print("Original file: ", filename)
    print("New file: ", new_filename)

    print("Cut file, using patterns: ", cut_patterns)

    print("Besides: ", besides_patterns)

    print("Using encoding: ", encoding)

    should_save = __get_validator(cut_patterns, besides_patterns)

    try:

        with io.open(new_filename, mode="w", encoding=encoding) as new_file:

            for diff_file in __diff_files(filename, encoding):
                if should_save(diff_file.name):
                    diff_file.write_to_file(new_file)

            print("Done")

    except (UnicodeDecodeError, FileNotFoundError, ValueError) as e:
        print(e)
        if os.path.isfile(new_filename):
            os.remove(new_filename)
