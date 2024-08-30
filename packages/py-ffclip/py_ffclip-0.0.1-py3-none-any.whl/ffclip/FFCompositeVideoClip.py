from ffclip import FFHelper, FilterComplexHelper
from ffclip.FFAudioClip import FFAudioClip
from ffclip.FFClip import FFClip
from ffclip.FFClipParam import FFClipParam
from ffclip.FFImageClip import FFImageClip
from ffclip.FFSubtitlesClip import FFSubtitlesClip
from ffclip.FFTextClip import FFTextClip
from ffclip.FFVideoClip import FFVideoClip
from ffclip.FilterComplexResult import FilterComplexResult


class FFCompositeVideoClip:
    """
    将多个剪辑元素合成一个视频
    """
    start: float = 0
    end: float = None
    duration: float = None
    size: tuple = None
    loop: int = False
    audio: FFAudioClip = None
    bgm: FFAudioClip = None
    subtitles: FFSubtitlesClip = None
    clips: list[FFClip] = None

    def __init__(self, clips: list[FFClip], subtitles: FFSubtitlesClip = None):
        if len(clips) == 0:
            raise Exception("剪辑元素不能为空!")
        self.clips = clips
        self.audio = clips[0].audio
        self.subtitles = subtitles
        self.set_duration(clips[0].duration)
        self.resize(clips[0].size)

    def resize(self, size: tuple):
        self.size = size
        return self

    def set_audio(self, audio: FFAudioClip = None):
        # 重置音频
        self.audio = audio
        return self

    def set_bgm(self, bgm: FFAudioClip):
        # 添加背景音乐
        self.bgm = bgm
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

    def build_clip_param(self):
        clip_param = FFClipParam(start=self.start, end=self.end, size=self.size)
        return clip_param

    def set_subtitles(self, subtitles: FFSubtitlesClip):
        self.subtitles = subtitles
        return self

    def write_video(self, output_path: str, fps: int = 24, codec: str = None, bitrate: str = None,
                    preset: str = None, audio: bool = True, audio_codec: str = None,
                    audio_bitrate: str = None, threads: int = None, crf: str = None, resize: tuple = None):

        if len(self.clips) == 1:
            # 只有一个片段，调用元素本身的剪辑
            if self.bgm is not None:
                self.clips[0].set_bgm(self.bgm)
            if self.subtitles is not None:
                self.clips[0].set_subtitles(self.subtitles)
            return FFHelper.write_video(self.clips, output_path=output_path, fps=fps, codec=codec, bitrate=bitrate,
                                        preset=preset, audio=audio, audio_codec=audio_codec,
                                        audio_bitrate=audio_bitrate, threads=threads, crf=crf, resize=resize)

        command = ["ffmpeg", "-y"]
        for index, clip in enumerate(self.clips):
            if clip.is_gif_type() and clip.loop == -1:
                command.extend(["-ignore_loop", "0"])
            if clip.stream_loop is not None:
                command.extend(["-stream_loop", str(clip.stream_loop)])
            command.extend(["-i", clip.get_path()])

        filter_complex = FilterComplexResult()

        for index, clip in enumerate(self.clips):
            filter_v = f"{index}:v"
            filter_a = f"{index}:a"
            if self.audio is None and clip.audio is not None:
                self.set_audio(clip.audio)
                filter_complex.filter_a = filter_a
            filter_complex.add_filter_a(filter_a)
            filter_complex.add_filter_v(filter_v)
            ff_clip_param = clip.build_clip_param()
            ff_clip_param.set_main_duration(self.duration)
            if self.size is not None:
                ff_clip_param.set_main_size(self.size)
            else:
                ff_clip_param.set_main_size(self.clips[0].original_size)
            clip.filter_complex(index, ff_clip_param, filter_complex)

        audio_index = len(self.clips)
        if self.audio is None:
            filter_complex.filter_a = None
        else:
            if self.audio.file_path is not None:
                # 使用自定义音频替换
                command.extend(["-i", self.audio.get_path()])
                filter_a = f"{audio_index}:a"
                filter_complex.add_filter_a(filter_a)
                filter_complex.filter_a = filter_a

                filter_name_a = filter_complex.get_filter_a(audio_index)
                filter_content, filter_name_a = FilterComplexHelper.filter_single_a(filter_name_a,
                                                                                    audio_index,
                                                                                    filter_complex.increment_and_get(),
                                                                                    self.audio)
                filter_complex.update_filter_a(audio_index, filter_name_a)
                if len(filter_content) > 0:
                    filter_complex.add_complex_filter(filter_content)
                audio_index += 1

        if self.audio is not None and self.bgm is not None:
            if self.bgm.aloop is not None:
                command.extend(["-stream_loop", str(self.bgm.aloop)])
            command.extend(["-i", self.bgm.get_path()])
            filter_a = f"{audio_index}:a"
            filter_complex.add_filter_a(filter_a)

            filter_name_a = filter_complex.filter_a
            filter_content, filter_name_a = FilterComplexHelper.amix_bgm(filter_name_a, filter_a, self.bgm)
            filter_complex.filter_a = filter_name_a
            filter_complex.add_complex_filter(filter_content)

        if self.subtitles is not None:
            # 加入字幕滤镜
            out_filter = "[v_end]"
            filter_complex.filter_cmd.append(self.subtitles.get_vf(filter_complex.filter_v, out_filter))
            filter_complex.update_filter_v(1, out_filter)

        if not audio or self.audio is None:
            filter_complex.filter_a = None

        command.extend(
            FFHelper.build_common_cmds(filter_complex, clip_param=self.build_clip_param(), output_path=output_path,
                                       fps=fps, codec=codec, bitrate=bitrate, preset=preset,
                                       audio=audio, audio_codec=audio_codec, audio_bitrate=audio_bitrate,
                                       threads=threads, crf=crf, resize=resize))

        FFHelper.call_cmd(command, comment="组合剪辑")

