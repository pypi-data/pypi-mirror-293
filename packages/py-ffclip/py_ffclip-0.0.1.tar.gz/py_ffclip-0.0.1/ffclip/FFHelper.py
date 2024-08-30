import json
import os.path
import subprocess
import time

from ffclip.FFClipParam import FFClipParam
from ffclip.FFMetaInfo import FFMetaInfo

PIPE = -1
STDOUT = -2
DEVNULL = -3


def call_cmd(cmd, comment: str = '', print_error=True):
    cmd_line = " ".join(cmd)
    start = time.time()
    print(f"执行命令行-开始[{comment}]: {cmd_line}")
    popen_params = {"stdout": DEVNULL,
                    "stderr": PIPE,
                    "stdin": DEVNULL}
    if os.name == "nt":
        popen_params["creationflags"] = 0x08000000
    proc = subprocess.Popen(cmd, **popen_params)
    out, err = proc.communicate()  # proc.wait()
    proc.stderr.close()
    if proc.returncode:
        if print_error:
            logger.error(f'执行命令行-异常[{comment}]: {proc}')
        raise IOError(err.decode('utf8'))
    else:
        cost = time.time() - start
        print(f'执行命令行-成功[{comment}]: cost = {round(cost, 2)} s')
    del proc


def read_meta_info(file_path: str) -> FFMetaInfo:
    cmds = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", file_path]
    cmd_line = " ".join(cmds)
    print(f"获取视频元信息: {cmd_line}")
    proc = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    proc.stderr.close()
    if proc.returncode:
        raise IOError(err.decode('utf8'))
    else:
        meta = json.loads(out.decode('utf8'))
        return FFMetaInfo(meta)


def write_video(clips, output_path: str, fps: int = None,
                codec: str = "libx264", bitrate: str = None,
                preset: str = None, audio: bool = True, audio_codec: str = None,
                audio_bitrate: str = "128k", threads: int = None,
                crf: str = None, resize: tuple = None) -> bool:
    if clips is None or len(clips) == 0:
        raise Exception("请先设置视频剪辑")

    if len(clips) == 1:
        clips[0].write_video(output_path, fps=fps, codec=codec, bitrate=bitrate, preset=preset, audio=audio,
                             audio_codec=audio_codec, audio_bitrate=audio_bitrate, threads=threads,
                             crf=crf, resize=resize)
        return True
    return False


def build_common_cmds(filter_complex, clip_param: FFClipParam, output_path: str, fps: int = 24,
                      codec: str = "copy", bitrate: str = None, preset: str = None,
                      audio: bool = True, audio_codec: str = None,
                      audio_bitrate: str = None, threads: int = None,
                      crf: str = None, resize: tuple = None):
    command = []
    if len(filter_complex.filter_cmd) > 0:
        command.extend(["-filter_complex", ";".join(filter_complex.filter_cmd)])
    if fps is not None:
        command.extend(["-r", str(fps)])
    if codec is not None:
        command.extend(["-c:v", codec])
    if audio_codec is not None:
        command.extend(["-c:a", audio_codec])
    if audio_bitrate is not None:
        command.extend(["-b:a", audio_bitrate])
    if preset is not None:
        command.extend(["-preset", preset])
    if resize and len(resize) == 2:
        command.extend(["-s", f"{resize[0]}x{resize[1]}"])
    else:
        if clip_param.size is not None:
            command.extend(["-s", f"{clip_param.size[0]}x{clip_param.size[1]}"])
    if clip_param.start is not None and clip_param.end is not None:
        command.extend(["-ss", str(clip_param.start)])
        command.extend(["-to", str(clip_param.end)])
    if crf:
        command.extend(["-crf", crf])
    else:
        if bitrate is not None:
            command.extend(["-b", bitrate])
        else:
            command.extend(["-crf", "22"])
    if threads is not None:
        command.extend(["-threads", str(threads)])
    if filter_complex.filter_a == '[0:a]':
        filter_complex.filter_a = '0:a'
    if filter_complex.filter_v == '[0:v]':
        filter_complex.filter_v = '0:v'
    if audio and filter_complex.filter_a is not None:
        command.extend(["-map", filter_complex.filter_a])
        # "-shortest",
    command.extend(["-map", filter_complex.filter_v, output_path])
    return command
