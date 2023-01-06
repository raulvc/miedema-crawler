import csv
import os
from os.path import exists


class Writer:

    def __init__(self, out_file):
        self._file = self._open_file(out_file)
        self._writer = self._load_writer()

    def _open_file(self, filename):
        """ truncates and opens a file for writing """
        file = os.path.abspath(os.path.expanduser(filename))

        if exists(file):
            os.truncate(file, 0)

        return open(file, "a+")

    def _load_writer(self):
        writer = csv.DictWriter(self._file, self._get_header())
        writer.writeheader()
        self.flush()

        return writer

    def _get_header(self):
        ticks = [str(i/10) for i in range(1, 10)]
        return ['pair'] + ticks

    def write(self, pair, values):
        row = dict(values)
        pretty_pair = ''.join(pair)
        row['pair'] = pretty_pair

        self._writer.writerow(row)

    def flush(self):
        self._file.flush()

    def close(self):
        self._file.close()

