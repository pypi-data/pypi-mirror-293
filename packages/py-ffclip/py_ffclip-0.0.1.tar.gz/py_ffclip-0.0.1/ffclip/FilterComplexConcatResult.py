import json


class FilterComplexConcatResult:

    filter_v: str
    filter_a: str
    filter_cmd: list[str]
    xfade_offset: int
    xfade_duration: int
    filter_a_list: list
    filter_v_list: list
    xfade_concat_list: list
    clip_list: list
    filter_index = 0

    def __init__(self):
        # 初始化参数
        self.filter_v = "0:v"
        self.filter_a = "0:a"
        self.filter_cmd = []
        self.xfade_offset = 0
        self.xfade_duration = 0
        self.filter_a_list = []
        self.filter_v_list = []
        self.xfade_concat_list = []
        self.clip_list = []
        self.filter_index = 0

    def add_clip_param(self, clip):
        self.clip_list.append(clip)
        return self

    def increment_and_get(self):
        self.filter_index += 1
        return self.filter_index

    def add_concat(self, concat: dict):
        self.xfade_concat_list.append(json.dumps(concat))
        self.xfade_concat_list.append("concat")
        return self

    def add_xfade(self, xfade: dict):
        # 格式为 { 'name':'[0:v]','duration':1, 'offset': 1, 'transition': 'fade' }
        self.xfade_concat_list.append(json.dumps(xfade))
        self.xfade_concat_list.append("xfade")
        return self

    def add_filter_a(self, filter_a: str):
        self.filter_a_list.append(filter_a)
        return self

    def add_filter_v(self, filter_v: str):
        self.filter_v_list.append(filter_v)
        return self

    def update_filter_v(self, filter_v: str):
        self.filter_v = filter_v
        return self

    def update_filter_a(self, filter_a: str):
        self.filter_a = filter_a
        return self

    def add_complex_filter(self, filter_cmd: str):
        self.filter_cmd.append(filter_cmd)
        return self

    def get_filter_a(self, index: int):
        return self.filter_a_list[index]

    def get_filter_v(self, index: int):
        return self.filter_v_list[index]

