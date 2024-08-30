class FilterComplexResult:
    filter_v: str
    filter_a: str
    filter_cmd: list[str]
    filter_a_list: list
    filter_v_list: list
    filter_index = 0

    def __init__(self):
        self.filter_v = "0:v"
        self.filter_a = "0:a"
        self.filter_cmd = []
        self.filter_a_list = []
        self.filter_v_list = []
        self.filter_index = 0

    def increment_and_get(self):
        self.filter_index += 1
        return self.filter_index

    def add_filter_a(self, filter_a: str):
        self.filter_a_list.append(filter_a)
        return self

    def add_filter_v(self, filter_v: str):
        self.filter_v_list.append(filter_v)
        return self

    def update_filter_v(self, index: int, filter_v: str):
        self.filter_v = filter_v
        if index < len(self.filter_v_list):
            self.filter_v_list[index] = self.filter_v
        else:
            self.filter_v_list.append(self.filter_v)
        return self

    def update_filter_a(self, index: int, filter_a: str):
        self.filter_a = filter_a
        if index < len(self.filter_a_list):
            self.filter_a_list[index] = self.filter_a
        else:
            self.filter_a_list.append(self.filter_a)
        return self

    def add_complex_filter(self, filter_cmd: str):
        self.filter_cmd.append(filter_cmd)
        return self

    def get_filter_a(self, index: int):
        return self.filter_a_list[index]

    def get_filter_v(self, index: int):
        return self.filter_v_list[index]
