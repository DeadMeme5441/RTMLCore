#!/usr/bin/env python3

from . import Subtag


class tag:
    def __init__(self, tag_name="", subtags_list=[]):
        self.tag_name = tag_name
        self.subtags_list = subtags_list

    @property
    def asdict(self):
        subtags_dict_list = []
        for subtag in self.subtags_list:
            subtags_dict_list.append(subtag.asdict)

        return {"tag_name": self.tag_name, "subtags_list": subtags_dict_list}
