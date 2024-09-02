import os.path

from ffclip import FilterComplexHelper, FFHelper
from ffclip.FFAudioClip import FFAudioClip
from ffclip.FFClipParam import FFClipParam
from ffclip.FFClipXfade import FFClipXfade
from ffclip.FFMetaInfo import FFMetaInfo
from ffclip.FilterComplexResult import FilterComplexResult
from ffclip.FFSubtitlesClip import FFSubtitlesClip


class FFClip:
    PIPE = -1
    STDOUT = -2
    DEVNULL = -3
    # 原始尺寸
    original_size: tuple = None
    file_path: str = None
    duration: float = None
    start: float = 0
    end: float = None
    position: tuple = None
    size: tuple = None
    loop: int = None
    stream_loop: int = None
    filter_cmd: str
    volume: float = None
    fps: int = None
    # 扩展其他的滤镜
    v_filter_map: dict = None
    a_filter_map: dict = None

    animation_map: dict = None

    bgm: FFAudioClip = None
    audio: FFAudioClip = None
    subtitles: FFSubtitlesClip = None
    clip_xfade: FFClipXfade = None
    meta_info: FFMetaInfo = None

    def __init__(self, file_path: str, audio: FFAudioClip = None, subtitles: FFSubtitlesClip = None):
        if not file_path:
            raise Exception("剪辑文件不能为空")
        if file_path.startswith("http") or file_path.startswith("https"):
            pass
        else:
            if not os.path.exists(file_path):
                raise Exception(f"剪辑文件不存在: {file_path}")
        self.file_path = file_path
        self.position = (0, 0)
        # 必须初始化 ，否则所有的 clip 都会共享这个对象
        self.v_filter_map = {}
        self.a_filter_map = {}
        self.animation_map = {}
        self.meta_info = FFHelper.read_meta_info(file_path)
        self.duration = self.meta_info.streams[0].duration
        self.original_size = (self.meta_info.streams[0].width, self.meta_info.streams[0].height)
        self.audio = audio
        self.subtitles = subtitles
        if self.audio is None and self.meta_info.has_audio():
            self.audio = FFAudioClip(duration=self.duration)
        if self.audio is not None and self.is_img_type():
            self.set_duration(audio.duration)

    def add_animation(self, animation_map: dict):
        self.animation_map = animation_map
        if animation_map is not None and "in" in animation_map:
            name = animation_map["in"]['name']
            duration = animation_map["in"]['duration']
            if name == 'fade_in' and duration is not None:
                self.fade_in(duration)
        if animation_map is not None and "out" in animation_map:
            name = animation_map["out"]['name']
            duration = animation_map["out"]['duration']
            if name == 'fade_out' and duration is not None:
                self.fade_out(duration)
        return self

    def set_v_filter(self, filter_v: dict):
        self.v_filter_map = filter_v
        return self

    def set_a_filter(self, filter_a: dict):
        self.a_filter_map = filter_a
        return self

    def __add_animation_in(self, name, duration):
        self.animation_map['in'] = {
            "name": name,
            "duration": duration
        }

    def __add_animation_out(self, name, duration):
        self.animation_map['out'] = {
            "name": name,
            "duration": duration
        }

    def set_audio(self, audio: FFAudioClip = None):
        # 重置音频
        self.audio = audio
        if audio is not None:
            self.set_duration(audio.duration)
        return self

    def set_bgm(self, bgm: FFAudioClip):
        # 添加背景音乐
        self.bgm = bgm
        return self

    def resize(self, size: tuple):
        self.size = size
        return self

    def set_duration(self, duration: float):
        self.duration = duration
        self.end = self.start + duration
        return self

    def set_start(self, start: float):
        self.start = start
        return self

    def set_end(self, end: float):
        self.end = end
        self.duration = self.end + self.start
        return self

    def set_position(self, position: tuple):
        self.position = position
        return self

    def rotate(self, rotate: int):
        self.v_filter_map["rotate"] = rotate
        return self

    def hflip(self):
        self.v_filter_map["hflip"] = True
        if self.is_img_type():
            self.set_loop()
        return self

    def vflip(self):
        self.v_filter_map["vflip"] = True
        # 需要转换为循环，否则无法显示
        if self.is_img_type():
            self.set_loop()
        return self

    def alpha(self, alpha: float = 1):
        if alpha < 0 or alpha > 1:
            raise Exception("参数异常：透明度取值范围为 0-1")
        self.v_filter_map["alpha"] = alpha
        return self

    def set_fps(self, fps: int):
        self.fps = fps
        return self

    def set_pos(self, position: tuple):
        self.position = position
        return self

    def set_loop(self, loop: int = -1):
        """
        设置循环次数，gif循环播放需要设置次参数，图片滑动+淡入淡出也需要加此参数
        :param loop:
        :return:
        """
        self.loop = loop
        return self

    def set_stream_loop(self, stream_loop: int = -1):
        """
        控制音频、视频循环播放次数
        :param stream_loop:
        :return:
        """
        self.stream_loop = stream_loop
        return self

    def get_path(self):
        return self.file_path

    def set_volume(self, volume: float):
        if self.is_video_type():
            self.volume = volume
        return self

    def side_in(self, name: str = 'left', duration: float = 1.0):
        """
        添加滑动进场动画 left/right/up/down
        :param name:
        :param duration:
        :return:
        """
        self.__add_animation_in("slide_" + name, duration)
        return self

    def side_out(self, name: str = 'right', duration: float = 1.0):
        """
        添加滑动出场动画 left/right/up/down
        :param name:
        :param duration:
        :return:
        """
        self.__add_animation_out("slide_" + name, duration)
        return self

    def has_audio(self):
        # 获取视频的音频
        try:
            return self.is_video_type() and self.meta_info.has_audio()
        except Exception as e:
            return False

    def has_subtitles(self):
        return self.subtitles is not None

    def is_gif_type(self):
        return self.get_path().lower().endswith(".gif")

    def is_video_type(self):
        # 是否视频格式
        if (self.get_path().lower().endswith(".mp4") or
                self.get_path().lower().endswith(".mkv") or
                self.get_path().lower().endswith(".flv") or
                self.get_path().lower().endswith(".mpeg") or
                self.get_path().lower().endswith(".avi") or
                self.get_path().lower().endswith(".mov")):
            return True
        return False

    def is_img_type(self):
        # 是否图片格式
        if (self.get_path().lower().endswith(".jpg") or
                self.get_path().lower().endswith(".png") or
                self.get_path().lower().endswith(".jpeg")):
            return True
        return False

    def fadein(self, duration: int):
        return self.fade_in(duration)

    def fade_in(self, duration: int):
        self.v_filter_map["fadein"] = duration
        if self.is_img_type():
            self.set_loop()
        return self

    def fadeout(self, duration: int):
        return self.fade_out(duration)

    def fade_out(self, duration: int):
        self.v_filter_map["fadeout"] = duration
        if self.is_img_type():
            self.set_loop()
        return self

    def xfade(self, transition: str = "fade", duration: float = 1):
        self.clip_xfade = FFClipXfade(transition, duration)
        return self

    def set_subtitles(self, subtitle: FFSubtitlesClip):
        self.subtitles = subtitle
        return self

    def build_clip_param(self):
        clip_param = FFClipParam(self.file_path, original_size=self.original_size, fps=self.fps,
                                 start=self.start, end=self.end, position=self.position,
                                 size=self.size, volume=self.volume, loop=self.loop, xfade=self.clip_xfade,
                                 animation=self.animation_map)
        clip_param.set_filter_map(self.v_filter_map, self.a_filter_map)
        return clip_param

    def filter_complex(self, index: int, ff_clip_param=None, filter_complex: FilterComplexResult = None):
        """
        将参数转换为 ffmpeg 的 filter_complex 参数
        :return:
        """
        if ff_clip_param is None:
            ff_clip_param = self.build_clip_param()

        # 设定初始视频流
        filter_name = f"{index}:v"

        filter_content, filter_name = FilterComplexHelper.filter_single(filter_name, index,
                                                                        filter_complex.increment_and_get(),
                                                                        ff_clip_param)
        if index > 0:
            filter_content, filter_name = FilterComplexHelper.overlay(filter_name,
                                                                      filter_complex.filter_v, index,
                                                                      filter_complex.increment_and_get(),
                                                                      ff_clip_param)
        if len(ff_clip_param.cmds) > 0:
            filter_complex.update_filter_v(index, filter_name)
            filter_complex.add_complex_filter("; ".join(ff_clip_param.cmds))
        return self

    def write_video(self, output_path: str, fps: int = 24, codec: str = "libx264", bitrate: str = None,
                    preset: str = None, audio: bool = True, audio_codec: str = None,
                    audio_bitrate: str = None, threads: int = None, crf: str = None, resize: tuple = None):
        command = [
            "ffmpeg", "-y"
        ]
        if self.is_img_type():
            command.extend(["-loop", "1"])
            if self.duration is None:
                self.set_duration(1)
        command.extend(["-i", self.file_path])
        filter_complex = FilterComplexResult()
        audio_idx = 0
        if audio and self.audio is not None and self.audio.file_path is not None:
            command.extend(["-i", self.audio.get_path()])
            audio_idx += 1
            filter_complex.filter_a = f'{audio_idx}:a'
        if audio and self.audio is not None:
            filter_content, filter_name_a = FilterComplexHelper.filter_single_a(filter_complex.filter_a,
                                                                                1, filter_complex.increment_and_get(),
                                                                                self.audio)
            filter_complex.filter_a = filter_name_a
            filter_complex.add_complex_filter(filter_content)
            if self.bgm is not None and self.bgm.file_path is not None:
                if self.audio.aloop is not None:
                    command.extend(["-stream_loop", str(self.audio.aloop)])
                command.extend(["-i", self.bgm.get_path()])
                audio_idx += 1
                filter_content, filter_name_a = FilterComplexHelper.amix_bgm(filter_complex.filter_a,
                                                                             f'{audio_idx}:a', self.bgm)
                filter_complex.filter_a = filter_name_a
                filter_complex.add_complex_filter(filter_content)

        if self.has_subtitles():
            # 加入字幕滤镜
            out_filter = "[v_end]"
            filter_complex.filter_cmd.append(self.subtitles.get_vf(filter_complex.filter_v, out_filter))
            filter_complex.update_filter_v(1, out_filter)

        if not audio or self.audio is None:
            filter_complex.filter_a = None

        command.extend(
            FFHelper.build_common_cmds(filter_complex, self.build_clip_param(), output_path, fps=fps, codec=codec,
                                       bitrate=bitrate, preset=preset, audio=audio, audio_codec=audio_codec,
                                       audio_bitrate=audio_bitrate, threads=threads, crf=crf, resize=resize))
        FFHelper.call_cmd(command, comment="导出视频")
