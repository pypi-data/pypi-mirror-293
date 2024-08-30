class FFClipXfade:
    duration: float = None
    transition: str = "fade"
    offset: float = 0

    def __init__(self, transition: str = "fade", duration: float = None):
        self.duration = duration
        self.transition = transition

    def get_transition(self):
        return self.transition

    def set_offset(self, offset: float):
        self.offset = offset
        return self

