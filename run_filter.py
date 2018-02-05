import argparse
import datetime
import textwrap
from PatchFilter import do_filter


description = """
---------------------------------------------------
     Filtering the patch file using parameters.
---------------------------------------------------
Example:
   python3 run_filter.py diff.patch '*xml' '*exe' -b '* /scripts/*'
"""


def generate_new_filename_if_need(filename, new_filename=None):
    if new_filename is None:
        filename, extension = filename.split(".")
        return ".".join([
            "_".join([filename, datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")]),
            extension
        ])
    else:
        return new_filename


parser = argparse.ArgumentParser(
    prog='patch files filter',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(description)
)

parser.add_argument('file', metavar='filename', type=str, nargs=1, help='file to parse')

parser.add_argument('remove', type=str, nargs='+', help='list of patterns to cut')

parser.add_argument('-n', '--new', type=str, nargs=1, help='file to save (default "d_m_Y_H_M_filename"))',
                    default=[None])

parser.add_argument('-b', '--beside', type=str, nargs='+', help='cut besides that',
                    default=[])

parser.add_argument('-e', '--encoding', type=str, nargs=1, help='file encoding (default ISO-8859-1)',
                    default=['ISO-8859-1'])

args = parser.parse_args()

do_filter(
    filename=args.file[0],
    new_filename=generate_new_filename_if_need(args.file[0], args.new[0]),
    cut_patterns=args.remove,
    besides_patterns=args.beside,
    encoding=args.encoding[0]
)


