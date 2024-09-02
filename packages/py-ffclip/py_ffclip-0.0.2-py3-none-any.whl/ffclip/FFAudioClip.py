from pydub import AudioSegment


class FFAudioClip:
    file_path: str = None
    aloop: int = -1
    volume: float = 1.0
    duration: float = None
    audio: AudioSegment = None

    def __init__(self, file_path: str = None, volume: float = 1.0, duration: float = 0, format_type=None):
        self.file_path = file_path
        self.duration = duration
        self.volume = volume
        if file_path is not None:
            if format_type is None:
                format_type = file_path.split(".")[-1]
            audio = AudioSegment.from_file(file_path, format=format_type)
            self.audio = audio
            self.duration = audio.duration_seconds
        pass

    def get_path(self):
        return self.file_path

    def set_duration(self, duration: float):
        self.duration = duration
        return self

    def set_volume(self, volume: float):
        self.volume = volume
        return self

    def volumex(self, volume: float):
        self.volume = volume
        return self