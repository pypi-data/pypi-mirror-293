from ffclip.FFAudioClip import FFAudioClip
from ffclip.FFClipXfade import FFClipXfade


class FFClipParam:
    file_path: str = None
    original_size: tuple = None
    start: float = 0
    end: float = None
    position: tuple = (0, 0)
    size: tuple = None
    volume: float = None
    loop: int = None
    fps: int = None
    xfade: FFClipXfade
    cmds: list = None
    animation: dict = None
    # 扩展其他的滤镜
    v_filter_map: dict = {}
    a_filter_map: dict = {}

    audio: FFAudioClip = None
    bgm: FFAudioClip = None

    # 主视频参数，composite_video_clip 时使用
    main_duration = 1
    main_size = tuple

    def __init__(self, file_path=None, original_size: tuple = None, fps: int = None, start: float = 0,
                 end: float = None,
                 position: tuple = (0, 0), size: tuple = None,
                 volume: float = None, loop: int = None,
                 xfade: FFClipXfade = None, animation: dict = None):
        self.original_size = original_size
        self.fps = fps
        self.file_path = file_path
        self.start = start
        self.end = end
        self.position = position
        self.size = size
        self.volume = volume
        self.loop = loop
        self.xfade = xfade
        self.cmds = []
        self.animation = animation

    def has_animation(self, key):
        return self.animation is not None and key in self.animation

    def get_animation(self, name):
        return name in self.animation

    def set_main_duration(self, main_duration):
        self.main_duration = main_duration
        return self

    def set_main_size(self, main_size):
        self.main_size = main_size
        return self

    def set_filter_map(self, v_filter_map, a_filter_map):
        self.v_filter_map = v_filter_map
        self.a_filter_map = a_filter_map
        return self

    def set_animation_map(self, animation_map):
        self.animation = animation_map
        return self

    def set_audio(self, audio: FFAudioClip):
        # 重置音频
        self.audio = audio
        return self

    def set_bgm(self, bgm: FFAudioClip):
        # 添加背景音乐
        self.bgm = bgm
        return self

    def append_cmd(self, cmd: str):
        if cmd is not None and len(cmd) > 0:
            self.cmds.append(cmd)
        return self

    def is_image(self):
        return (self.file_path.lower().endswith(".jpg") or
                self.file_path.lower().endswith(".jpeg") or
                self.file_path.lower().endswith(".png") or
                self.file_path.lower().endswith(".bmp") or
                self.file_path.lower().endswith(".tiff")
                )

    def is_gif(self):
        return self.file_path.lower().endswith(".gif")

    def is_video(self):
        return (self.file_path.lower().endswith(".mp4") or
                self.file_path.lower().endswith(".mov") or
                self.file_path.lower().endswith(".webm") or
                self.file_path.lower().endswith(".mkv")
                )
