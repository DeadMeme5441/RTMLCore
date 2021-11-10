#!/usr/bin/env python3


import re
from .Subtag import subtag
from .Tag import tag


class document:
    def __init__(self, file_path):
        self.file_path = file_path
        # self.check_tags_count()

    @property
    def asdict(self):
        tags_dict_list = []

        for tag_item in self.tags_list:
            tags_dict_list.append(tag_item.asdict)

        return {
            "file_name": self.file_name,
            "file_path": self.file_path,
            "file_data": str(self.file_data),
            "tags_list": tags_dict_list,
            "errors": self.errors,
        }

    @property
    def file_name(self):
        return self.file_path.split("/")[-1].split(".")[0]

    @property
    def file_data(self):
        try:
            file_data = open(self.file_path, "r").read()
            return file_data.replace("\n", "\n")
        except FileNotFoundError:
            print("Invalid file path passed.")

    @property
    def cleaned_closing_tags(self):
        cleaned_closing_tags = list(
            map(
                lambda closing_tag: str.replace(closing_tag, "/", ""), self.closing_tags
            )
        )

        return cleaned_closing_tags

    @property
    def opening_tags(self):

        opening_tags_list = []
        if re.findall("(\<[^\/].*?>)", str(self.file_data)):  # type: ignore
            opening_tags_list = re.findall("(\<[^\/].*?\>)", str(self.file_data))  # type: ignore

        all_opening_tags_obj_list = list(
            map(self._generate_tag_object, opening_tags_list)
        )
        opening_tags_name_list = list(
            set(
                map(
                    lambda x: x.split(";")[0].replace("<", "").strip(),
                    opening_tags_list,
                )
            )
        )

        opening_tags_obj_list = []

        for this_tag_name in opening_tags_name_list:
            opening_tags_obj_list.append(tag(tag_name=this_tag_name))

        for tag_obj in opening_tags_obj_list:
            for all_tag_obj in all_opening_tags_obj_list:
                if tag_obj.tag_name == all_tag_obj.tag_name:
                    tag_obj.subtags_list = (
                        tag_obj.subtags_list + all_tag_obj.subtags_list
                    )

        return opening_tags_obj_list

    @property
    def closing_tags(self):

        closing_tags_list = []
        if re.findall("(\<[\/].*?>)", str(self.file_data)):  # type: ignore
            closing_tags_list = re.findall("(\<[\/].*?\>)", str(self.file_data))  # type: ignore

        all_closing_tags_obj_list = list(
            map(self._generate_tag_object, closing_tags_list)
        )
        closing_tags_name_list = list(
            set(
                map(
                    lambda x: x.split(";")[0].replace("<", "").replace("/", "").strip(),
                    closing_tags_list,
                )
            )
        )

        closing_tags_obj_list = []

        for this_tag_name in closing_tags_name_list:
            closing_tags_obj_list.append(tag(tag_name=this_tag_name))

        for all_tag_obj in all_closing_tags_obj_list:
            for tag_obj in closing_tags_obj_list:
                if tag_obj.tag_name == all_tag_obj.tag_name:
                    tag_obj.subtags_list = (
                        tag_obj.subtags_list + all_tag_obj.subtags_list
                    )

        return closing_tags_obj_list

    @property
    def tags_list(self):

        opening_tags_list = list(map(lambda x: x.tag_name, self.opening_tags))
        closing_tags_list = list(map(lambda x: x.tag_name, self.closing_tags))

        all_tags = []

        tag_names_list = set(opening_tags_list).intersection(set(closing_tags_list))
        tag_error_list = set(opening_tags_list).union(set(closing_tags_list)) - (
            set(opening_tags_list).intersection(set(closing_tags_list))
        )

        for this_tag_name in tag_names_list:

            opening_subtags = list(
                filter(lambda x: x.tag_name == this_tag_name, self.opening_tags)
            )[0].subtags_list
            closing_subtags = list(
                filter(lambda x: x.tag_name == this_tag_name, self.closing_tags)
            )[0].subtags_list

            final_subtags_list = list(
                self._update_subtags_locations(opening_subtags, closing_subtags)
            )

            all_tags.append(
                tag(tag_name=this_tag_name, subtags_list=final_subtags_list)
            )

        for this_tag_name in tag_error_list:

            if this_tag_name in opening_tags_list:
                subtags = list(
                    filter(lambda x: x.tag_name == this_tag_name, self.opening_tags)
                )[0].subtags_list
            if this_tag_name in closing_tags_list:
                subtags = list(
                    filter(lambda x: x.tag_name == this_tag_name, self.closing_tags)
                )[0].subtags_list

            final_subtags_list = list(self._update_subtags_locations(subtags, subtags))

            all_tags.append(
                tag(tag_name=this_tag_name, subtags_list=final_subtags_list)
            )

        return all_tags

    @property
    def errors(self):

        error_dict = {"value": False, "tag_errors": [], "subtag_errors": []}

        if self._tag_errors() != []:
            error_dict["value"] = True
            error_dict["tag_errors"] = self._tag_errors()

        if self._subtag_errors() != []:
            error_dict["value"] = True
            error_dict["subtag_errors"] = self._subtag_errors()

        return error_dict

    def _tag_errors(self):

        error_list = []

        opening_tags_list = list(map(lambda x: x.tag_name, self.opening_tags))
        closing_tags_list = list(map(lambda x: x.tag_name, self.closing_tags))

        if set(opening_tags_list) == set(closing_tags_list):
            return error_list

        else:
            if list(set(opening_tags_list) - set(closing_tags_list)) != []:
                temp_dict = {}
                temp_dict["tag_list"] = list(
                    set(opening_tags_list) - set(closing_tags_list)
                )
                temp_dict["description"] = "Tag(s) opened but not closed."
                error_list.append(temp_dict)
            if list(set(closing_tags_list) - set(opening_tags_list)) != []:
                temp_dict = {}
                temp_dict["tag_list"] = list(
                    set(closing_tags_list) - set(opening_tags_list)
                )
                temp_dict["description"] = "Tag(s) closed but not opened."
                error_list.append(temp_dict)

            return error_list

    def _subtag_errors(self):

        error_list = []

        for tag in self.tags_list:
            tag_dict = {"tag_name": tag.tag_name, "subtags_list": []}
            for subtag in tag.subtags_list:
                if subtag.subtag_start == -1:
                    temp_dict = {}
                    temp_dict["subtag"] = subtag.asdict
                    temp_dict["description"] = "Subtag closed but not opened."
                    tag_dict["subtags_list"].append(temp_dict)
                if subtag.subtag_end == -1:
                    temp_dict = {}
                    temp_dict["subtag"] = subtag.asdict
                    temp_dict["description"] = "Subtag opened but not closed."
                    tag_dict["subtags_list"].append(temp_dict)

            if tag_dict["subtags_list"] != []:
                error_list.append(tag_dict)

        return error_list

    def _generate_tag_object(self, tag_item):

        tag_item_name = tag_item.split(";")[0].replace("<", "").strip()
        subtag_list = tag_item.split(";")[1:]
        subtag_obj_list = []
        location = self.file_data.find(tag_item)  # type: ignore

        if "/" not in tag_item_name:
            location += len(tag_item)
            for subtag_item in subtag_list:
                subtag_obj_list.append(
                    subtag(
                        subtag_name=subtag_item.split("=")[0].strip(),
                        subtag_value=subtag_item.split("=")[1].strip().replace(">", ""),
                        subtag_start=location,
                        subtag_end=-1,
                    )
                )

        else:
            tag_item_name = tag_item_name.replace("/", "")
            for subtag_item in subtag_list:
                subtag_obj_list.append(
                    subtag(
                        subtag_name=subtag_item.split("=")[0].strip(),
                        subtag_value=subtag_item.split("=")[1].strip().replace(">", ""),
                        subtag_start=-1,
                        subtag_end=location,
                    )
                )

        return tag(tag_name=tag_item_name, subtags_list=subtag_obj_list)

    def _update_subtags_locations(self, opening_subtags_list, closing_subtags_list):

        final_subtags_list = []

        for subtag_start_item in opening_subtags_list:
            for subtag_end_item in closing_subtags_list:
                if subtag_start_item == subtag_end_item:
                    final_subtags_list.append(
                        subtag(
                            subtag_name=subtag_start_item.subtag_name,
                            subtag_value=subtag_start_item.subtag_value,
                            subtag_start=subtag_start_item.subtag_start,
                            subtag_end=subtag_end_item.subtag_end,
                        )
                    )

        for subtag_start_item in opening_subtags_list:
            if subtag_start_item not in final_subtags_list:
                final_subtags_list.append(subtag_start_item)

        for subtag_end_item in closing_subtags_list:
            if subtag_end_item not in final_subtags_list:
                final_subtags_list.append(subtag_end_item)

        return final_subtags_list

    def _search_text(self, this_search_term):

        matches = re.finditer(this_search_term, self.file_data)  # type: ignore
        matches_positions = [match.start() for match in matches]

        return matches_positions

    def _search_tag(self, this_search_term):

        results_list = []

        for tag in self.tags_list:
            if tag.tag_name == this_search_term:
                results_list.append(tag.asdict)

        return results_list

    def _search_subtag(self, this_search_term):

        results_list = []

        for tag in self.tags_list:
            temp_dict = {"tag_name": tag.tag_name, "subtags_list": []}
            for subtag in tag.subtags_list:
                if (
                    this_search_term in subtag.subtag_name
                    or this_search_term in subtag.subtag_value
                ):
                    temp_dict["subtags_list"].append(subtag.asdict)

            if len(temp_dict["subtags_list"]) != 0:
                results_list.append(temp_dict)

        return results_list

    def search_document(self, search_type, search_term):

        print(search_term)
        print(type(search_term))

        search_result = {
            "search_type": search_type,
            "search_term": search_term,
            "value": False,
            "results": [
                {"Text_Results": []},
                {"Tag_Results": []},
                {"Subtag_Results": []},
            ],
        }

        if "text" in search_type:

            result = self._search_text(search_term)
            if len(result) != 0:
                search_result["value"] = True
                search_result["results"][0]["Text_Results"] = result

        if "tag" in search_type:

            result = self._search_tag(search_term)
            if len(result) != 0:
                search_result["value"] = True
                search_result["results"][1]["Tag_Results"] = result

        if "subtag" in search_type:

            result = self._search_subtag(search_term)
            if len(result) != 0:
                search_result["value"] = True
                search_result["results"][2]["Subtag_Results"] = result

        return search_result
