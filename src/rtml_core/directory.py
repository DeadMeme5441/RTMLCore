#!/usr/bin/env python3

from os import listdir
from os.path import isfile, join
from . import document


class directory:
    def __init__(self, directory_path):
        self.directory_path = directory_path
        super().__init__()

    @property
    def file_paths_list(self):
        return [
            f
            for f in listdir(self.directory_path)
            if isfile(join(self.directory_path, f))
        ]

    @property
    def documents(self):

        document_obj_list = []
        for f_path in self.file_paths_list:
            document_obj_list.append(document(file_path=f_path))

        return document_obj_list
