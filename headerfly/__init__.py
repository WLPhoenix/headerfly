#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
from sys import argv

from .import style


class HeaderFly(object):

    IGNORE_TYPES = [
        ".min.js"
    ]
    HANDLE_TYPES = {
        ".css": style.slash_star_bang,
        ".html": style.html,
        ".js": style.slash_star_bang,
        ".py": style.utf_8_scripting,
        ".py.template": style.utf_8_scripting,
        ".rb": style.utf_8_scripting,
    }
    IGNORE_LINES = [
        "#!",
        "<!DOCTYPE"
    ]

    def __init__(self, path_to_header, apply_dir=".", verbose=False):

        self.header = open(path_to_header).read()
        self.apply_dir = apply_dir
        self.verbose = verbose
        self.current_line = 0


    def _apply_language_style(self, header, fname):
        # Explicit Ignore
        for ftype in self.__class__.IGNORE_TYPES:
            if fname.endswith(ftype):
                return None

        # Handle
        for ftype in self.__class__.HANDLE_TYPES:
            if fname.endswith(ftype):
                return self.__class__.HANDLE_TYPES[ftype](header)

        # Default Ignore
        return None


    def _add_header_to_dir(self, header, dirname, fnames):
        for fname in fnames:
            lang_header = self._apply_language_style(header, fname)
            if lang_header:
                self._add_header_to_file(lang_header, os.path.join(dirname, fname))


    def __call__(self):
        os.path.walk(self.apply_dir, self._add_header_to_dir, self.header)


    def _handle_skip_lines(self, lines):
        upper_first_line = lines[0].upper()
        for ignore in self.__class__.IGNORE_LINES:
            if upper_first_line.startswith(ignore):
                return 1

        return 0


    def _add_header_to_file(self, header, fname):
        # Defines
        def insert(text):
            lines.insert(self.current_line, text)


        def insert_if_not(text):
            if not lines[self.current_line] == text:
                insert(text)

        # Read
        try:
            lines = open(fname).readlines()
        except IOError, e:
            print(e)
            return

        # Skip file if empty
        if len(lines) == 0:
            return

        # Skip over necessary first lines
        self.current_line = self._handle_skip_lines(lines)


        # Apply header
        header_lines = header.split("\n")
        for hline in header_lines:
            insert_if_not("%s\n" % hline)
            self.current_line += 1

        # Blank
        insert_if_not("\n")

        # Write file
        with open(fname, "w") as ff:
            ff.write("".join(lines))

        self.current_line = 0


def main():
    if len(argv) == 2:
        HeaderFly(argv[1])()
    else:
        HeaderFly(argv[1], argv[2])()


if __name__ == '__main__':
    main()
