import json

from ffclip import FFHelper, FilterComplexHelper
from ffclip.FFAudioClip import FFAudioClip
from ffclip.FFClip import FFClip
from ffclip.FFClipParam import FFClipParam
from ffclip.FFSubtitlesClip import FFSubtitlesClip
from ffclip.FFVideoClip import FFVideoClip
from ffclip.FilterComplexConcatResult import FilterComplexConcatResult


class FFConcatVideoClip:
    """
    连接多个视频
    """
    volume: float = None
    start: float = 0
    end: float = None
    duration: float = None
    size: tuple = None
    final_v: str = None
    final_a: str = None
    has_audio: bool = False
    bgm: FFAudioClip = None
    subtitles: FFSubtitlesClip = None
    clips: list[FFClip] = None

    def __init__(self, clips: list[FFClip], subtitles: FFSubtitlesClip = None):
        if clips is None or len(clips) == 0:
            raise Exception("FFConcatVideoClip clips is empty")
        self.clips = clips
        self.subtitles = subtitles
        d = 0
        for clip in clips:
            d += clip.duration
        self.set_duration(d)

    def __build_audio(self):
        """
        构建音频
        :return:
        """
        return FFAudioClip(volume=self.volume)

    def append_clip(self, clip: FFClip):
        self.clips.append(clip)
        self.duration += clip.duration
        return self

    def set_bgm(self, bgm: FFAudioClip):
        self.bgm = bgm
        return self

    def set_volume(self, volume: float):
        self.volume = volume
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

    def set_subtitles(self, subtitles: FFSubtitlesClip, has_audio: bool = True):
        self.subtitles = subtitles
        self.has_audio = has_audio
        return self

    def build_clip_param(self):
        return FFClipParam(size=self.size, start=self.start, end=self.end, volume=self.volume)

    def write_video(self, output_path: str, fps: int = None, codec: str = "libx264", bitrate: str = None,
                    preset: str = None, audio: bool = True, audio_codec: str = "aac",
                    audio_bitrate: str = "128k", threads: int = None):

        if len(self.clips) == 1:
            # 只有一个片段，调用元素本身的剪辑
            if self.bgm is not None:
                self.clips[0].set_bgm(self.bgm)
            if self.subtitles is not None:
                self.clips[0].set_subtitles(self.subtitles)
            return FFHelper.write_video(self.clips, output_path, fps=fps, codec=codec, bitrate=bitrate, preset=preset,
                                        audio=audio,
                                        audio_codec=audio_codec, audio_bitrate=audio_bitrate, threads=threads)

        command = ["ffmpeg", "-y"]

        for video in self.clips:
            if video.is_video_type():
                command.extend(["-i", video.get_path()])

        filter_complex = FilterComplexConcatResult()
        # 初始化视频流
        for index, clip in enumerate(self.clips):
            filter_v = f"{index}:v"
            filter_a = f"{index}:a"
            if clip.audio is not None:
                filter_complex.add_filter_a(filter_a)
            else:
                filter_complex.add_filter_a("")
            filter_complex.add_filter_v(filter_v)
            filter_complex.add_clip_param(clip.build_clip_param())
            if clip.clip_xfade is not None:
                # 格式为 { 'name':'[0:v]','duration':1, 'offset': 1, 'transition': 'fade' }
                xfade_node = {
                    'name': filter_v,
                    'name_a': filter_a,
                    'duration': clip.clip_xfade.duration,
                    'offset': clip.duration,
                    'transition': clip.clip_xfade.transition
                }
                filter_complex.add_xfade(xfade_node)
            else:
                concat_node = {
                    'name': filter_v,
                    'name_a': filter_a
                }
                filter_complex.add_concat(concat_node)

        if self.bgm is not None:
            if self.bgm.aloop is not None:
                command.extend(["-stream_loop", str(self.bgm.aloop)])
            command.extend(["-i", self.bgm.get_path()])
            filter_a = f"[{len(self.clips)}:a]"
            filter_complex.add_filter_a(filter_a)

        for index, clip in enumerate(self.clips):
            # 音频单独剪辑 输入1个filter 输出1个filter
            if clip.audio is not None:
                filter_name_a = filter_complex.get_filter_a(index)
                ff_param = clip.build_clip_param()
                filter_content, filter_name_a = FilterComplexHelper.filter_single_a(filter_name_a, index,
                                                                                    filter_complex.increment_and_get(),
                                                                                    ff_param)
                filter_complex.update_filter_a(filter_name_a)
                if len(ff_param.cmds) > 0:
                    filter_complex.add_complex_filter("; ".join(ff_param.cmds))

        # 连接音频
        # filter_content, filter_name_a = FilterComplexHelper.concat_a_list(filter_complex.filter_a_list)
        # filter_complex.filter_a = filter_name_a
        # filter_complex.add_complex_filter(filter_content)

        self.xfade_concat_expression(filter_complex)

        # 当前音频剪辑
        ff_param = self.build_clip_param()
        filter_content, filter_name_a = FilterComplexHelper.filter_single_a(filter_complex.filter_a,
                                                                            len(self.clips), 0,
                                                                            self.__build_audio())
        if len(ff_param.cmds) > 0:
            filter_complex.update_filter_a(filter_name_a)
            filter_complex.add_complex_filter("; ".join(ff_param.cmds))

        # 加入背景音乐
        if self.bgm is not None:
            bgm_filter_name_a = filter_complex.get_filter_a(len(self.clips))
            filter_name_a = filter_complex.filter_a
            filter_content, filter_name_a = FilterComplexHelper.amix_bgm(filter_name_a, bgm_filter_name_a, self.bgm)
            filter_complex.filter_a = filter_name_a
            filter_complex.add_complex_filter(filter_content)

        if self.subtitles is not None:
            # 加入字幕滤镜
            out_filter = "[v_end]"
            filter_complex.filter_cmd.append(self.subtitles.get_vf(filter_complex.filter_v, out_filter))
            filter_complex.update_filter_v(out_filter)

        ff_param = self.build_clip_param()
        ff_param.end = None
        command.extend(
            FFHelper.build_common_cmds(filter_complex, ff_param, output_path, fps=fps, codec=codec,
                                       bitrate=bitrate, preset=preset, audio=audio, audio_codec=audio_codec,
                                       audio_bitrate=audio_bitrate, threads=threads))
        FFHelper.call_cmd(command, comment="连接视频")

    def xfade_concat_expression(self, filter_complex: FilterComplexConcatResult):
        step = 0
        # 移除最后一个元素
        filter_list = filter_complex.xfade_concat_list[:-1]
        while 'xfade' in filter_list:
            index = filter_list.index('xfade')
            result = self.xfade(filter_list, index - 1, index + 1, step, filter_complex)
            filter_list = filter_list[:index - 1] + [result] + filter_list[index + 2:]
            step += 1
        while 'concat' in filter_list:
            index = filter_list.index('concat')
            result = self.concat(filter_list, index - 1, index + 1, step, filter_complex)
            filter_list = filter_list[:index - 1] + [result] + filter_list[index + 2:]
            step += 1
        final_filter = eval(filter_list[0])['name']
        final_filter_a = eval(filter_list[0])['name_a']
        filter_complex.update_filter_v(final_filter)
        filter_complex.update_filter_a(final_filter_a)
        return filter_list[0]

    def concat(self, filter_list, current_idx, next_idx, step: int, filter_complex: FilterComplexConcatResult):
        input_a = eval(filter_list[current_idx])
        input_b = eval(filter_list[next_idx])
        filter_a = FilterComplexHelper.to_input_filter(input_a['name'])
        filter_b = FilterComplexHelper.to_input_filter(input_b['name'])
        filter_a_a = FilterComplexHelper.to_input_filter(input_a['name_a'])
        filter_b_a = FilterComplexHelper.to_input_filter(input_b['name_a'])
        content = f"{filter_a}{filter_a_a}{filter_b}{filter_b_a}concat=n=2:v=1:a=1:[concat_v{step}][concat_a{step}]"
        filter_complex.add_complex_filter(content)
        res = {
            'name': f"[concat_v{step}]",
            'name_a': f"[concat_a{step}]",
        }
        return json.dumps(res)

    def xfade(self, filter_list, current_idx, next_idx, step: int,
              filter_complex: FilterComplexConcatResult):
        input_a = eval(filter_list[current_idx])
        input_b = eval(filter_list[next_idx])
        offset = input_a['offset']
        a_duration = input_a['duration']
        transition = input_a['transition']
        filter_a = FilterComplexHelper.to_input_filter(input_a['name'])
        filter_b = FilterComplexHelper.to_input_filter(input_b['name'])
        filter_a_a = FilterComplexHelper.to_input_filter(input_a['name_a'])
        filter_b_a = FilterComplexHelper.to_input_filter(input_b['name_a'])
        content = f"{filter_a}{filter_b}xfade={transition}:duration={a_duration}:offset={offset - a_duration}:[xfade_{step}]"
        content += f";{filter_a_a}{filter_b_a}concat=n=2:v=0:a=1:[xfade_a{step}]"
        filter_complex.add_complex_filter(content)
        next_duration = 0
        if 'offset' in input_b:
            offset = offset + input_b['offset']
            transition = input_b['transition']
            next_duration = input_b['duration']
        res = {
            'name': f"[xfade_{step}]",
            'name_a': f"[xfade_a{step}]",
            'duration': next_duration,
            'offset': offset - a_duration,
            'transition': transition
        }
        return json.dumps(res)


