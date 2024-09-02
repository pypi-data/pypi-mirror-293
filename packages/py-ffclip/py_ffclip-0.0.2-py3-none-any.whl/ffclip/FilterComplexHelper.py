from ffclip.FFAudioClip import FFAudioClip
from ffclip.FFClipParam import FFClipParam
from ffclip.animation.FFAnimation import AnimationSlide, AnimationType

METHOD_CONCAT = "concat"
METHOD_COMPOSE = "compose"


def to_input_filter(filter_name: str):
    if not filter_name.startswith("["):
        filter_name = f"[{filter_name}]"
    return filter_name


def filter_single_a(filter_input: str, clip_index: int, filter_index: int, aduio_clip: FFAudioClip):
    """
    只有一个输入输出的音频操作滤镜
    :param aduio_clip:
    :param filter_input:
    :param filter_index:
    :param clip_index:
    :param clip:
    :return:
    """
    filter_list = []
    filter_input = to_input_filter(filter_input)
    filter_out = f"[a{clip_index}{filter_index}]"
    if aduio_clip.volume is not None:
        filter_list.append(f"volume={aduio_clip.volume}")
    if len(filter_list) > 0:
        filter_content = filter_input + ",".join(filter_list)
        filter_content += f"{filter_out}"
        return filter_content, filter_out
    else:
        return '', filter_input


def amix_bgm(lat_audio: str, bgm_filter: str, audo_clip: FFAudioClip):
    """
    混合背景音乐
    :param lat_audio:
    :param bgm_filter:
    :return:
    """
    filter_out = f"[amix_out]"
    filter_content = None
    bgm = '[bgm]'
    bgm_filter = to_input_filter(bgm_filter)
    lat_audio = to_input_filter(lat_audio)
    if audo_clip.volume is not None:
        filter_content = f"{bgm_filter}volume={audo_clip.volume}"
        if audo_clip.aloop > 0:
            filter_content += f",aloop=loop={audo_clip.aloop}"
        filter_content += f"{bgm};"
    if filter_content is not None:
        filter_content = filter_content + f"{lat_audio}{bgm}amix=inputs=2:duration=first:dropout_transition=2{filter_out}"
    else:
        filter_content = f"{lat_audio}{bgm_filter}amix=inputs=2:duration=first{filter_out}"
    return filter_content, filter_out


def filter_single(filter_input: str, clip_index: int, filter_index: int, clip: FFClipParam):
    """
    只有一个输入输出的滤镜
    :param filter_input:
    :param clip_index: 当前剪辑的第几个视频
    :param filter_index: 当前剪辑的第几个滤镜
    :param clip:
    :return:
    """
    v_filter_map = clip.v_filter_map
    filter_list = []
    filter_input = to_input_filter(filter_input)
    filter_out = f"[v{clip_index}{filter_index}]"
    if clip.fps is not None:
        fps = f"fps={clip.fps}"
        filter_list.append(fps)

    if clip.loop is not None and not (clip.loop == -1 and clip.is_gif()):
        total_frames = 1
        loop = f"loop=loop={clip.loop}:size={total_frames}:start=0"
        filter_list.append(loop)

    # 透明度
    alpha = v_filter_map.get('alpha')
    if alpha is not None:
        alpha_filter = f"colorchannelmixer=aa={alpha}"
        filter_list.append(alpha_filter)

    if clip_index > 0:
        duration_in = v_filter_map.get('fadein')
        if duration_in is not None:
            st = clip.start
            fade_in = f"fade=in:st={st}:d={duration_in}:alpha=1"
            filter_list.append(fade_in)

        duration_out = v_filter_map.get('fadeout')
        if duration_out is not None:
            st = clip.end
            if clip.end > duration_out:
                st = clip.end - duration_out
            fade_out = f"fade=out:st={st}:d={duration_out}:alpha=1"
            filter_list.append(fade_out)

    if clip.size is not None:
        # 统一ASR参数，否则影响后续视频连接操作
        scale = f"scale={clip.size[0]}:{clip.size[1]},setsar=1"
        filter_list.append(scale)

    if 'rotate' in v_filter_map:
        rotate_val = v_filter_map['rotate']
        if rotate_val != 0:
            rotate = f"rotate={rotate_val}*PI/180::ow='rotw(PI/4)':oh='roth(PI/4)':fillcolor='none'"
            filter_list.append(rotate)

    if 'hflip' in v_filter_map:
        filter_list.append('hflip')

    if 'vflip' in v_filter_map:
        filter_list.append('vflip')

    if len(filter_list) > 0:
        filter_content = filter_input + ",".join(filter_list)
        filter_content += f"{filter_out}"
        clip.append_cmd(filter_content)
        return filter_content, filter_out
    else:
        return "", filter_input


def overlay(filter_input: str, target_input: str, clip_index: int, filter_index: int, clip: FFClipParam):
    """
    将视频叠加到指定位置
    :param target_input: str
    :param filter_input: str
    :param clip_index: 当前剪辑的第几个视频
    :param filter_index: 当前剪辑的第几个滤镜
    :param clip: 叠加的位置
    :return:
    """
    position = clip.position
    start = clip.start
    end = clip.end
    filter_input = to_input_filter(filter_input)
    target_input = to_input_filter(target_input)
    if position is None:
        return "", filter_input
    filter_out = f"[v{clip_index}{filter_index}]"

    filter_content = None
    if clip.has_animation(AnimationType.animation_in.value) or clip.has_animation(AnimationType.animation_out.value):
        slide_in = AnimationSlide(AnimationType.animation_in.value, clip.animation, clip)
        slide_out = AnimationSlide(AnimationType.animation_out.value, clip.animation, clip)
        if slide_in.check() and slide_out.check():
            # print("start_pos=", slide_in.start_pos, "target_pos=", slide_in.target_pos, "end_pos=",
            #     slide_out.target_pos)
            filter_content = slide_in_out(start, end, slide_in.duration, slide_out.duration, slide_in.start_pos,
                                          slide_in.target_pos, slide_out.target_pos)
        else:
            if slide_in.check():
                filter_content = slide(start, end, slide_in.duration, slide_in.start_pos, slide_in.target_pos)
            if slide_out.check():
                filter_content = slide(start, end, slide_out.duration, slide_out.start_pos, slide_out.target_pos)
        if filter_content is not None:
            filter_content = f"{target_input}{filter_input}{filter_content}{filter_out}"
    if filter_content is None:
        filter_content = f"{target_input}{filter_input}overlay={position[0]}:{position[1]}"
        if start is not None and end is not None:
            # 如果有淡出效果，就不需要设置 enable between
            filter_content = filter_content + f":enable='between(t,{start},{end})'{filter_out}"
        else:
            filter_content = f"{filter_content}{filter_out}"
    clip.append_cmd(filter_content)
    return filter_content, filter_out


def xfade(last_input: str, current_input: str, clip_index: int = 0, filter_index: int = 1,
          clip: FFClipParam = None):
    """
    淡入
    :param last_input:
    :param current_input: str
    :param clip_index: 当前剪辑的第几个视频
    :param filter_index: 当前剪辑的第几个滤镜
    :param clip: FFClip
    :return:
    """
    last_input = to_input_filter(last_input)
    current_input = to_input_filter(current_input)
    if clip.xfade is None:
        return filter_index, "", last_input
    filter_out = f"[v{clip_index}{filter_index}]"
    filter_content = (f"{last_input}{current_input}xfade=transition={clip.xfade.transition}:"
                      f"duration={clip.xfade.duration}:offset={clip.xfade.offset}{filter_out}")
    clip.append_cmd(filter_content)
    return filter_content, filter_out


def concat_v_list(filter_list: list[str]):
    filter_out = f"[v_concat]"
    # 使用to_input_filter转换滤镜名称
    filter_list = list(map(to_input_filter, filter_list))
    filter_content = f"{''.join(filter_list)}concat=n={len(filter_list)}:v=1:a=0:unsafe=1{filter_out}"
    return filter_content, filter_out


def concat_a_list(filter_list: list[str]):
    """
    连接音频
    :param filter_list:
    :return:
    """
    # 移除空白的滤镜
    filter_list = list(filter(lambda x: x != "", filter_list))
    filter_list = list(map(to_input_filter, filter_list))
    filter_out = f"[a_concat]"
    filter_content = f"{''.join(filter_list)}concat=n={len(filter_list)}:v=0:a=1:unsafe=1{filter_out}"
    return filter_content, filter_out


def slide_in_out(start: float, end: float, duration_in, duration_out, start_pos: tuple, target_pos: tuple,
                 end_pos: tuple):
    """
    滑动进入和滑动退出，带淡入淡出效果
    :param duration_out:
    :param duration_in:
    :param start: 视频中元素开始显示的时间（秒）
    :param end: 视频中元素结束显示的时间（秒）
    :param start_pos: 元素的初始位置 (x, y)
    :param target_pos: 入场动画结束时元素的位置 (x1, y1)
    :param end_pos: 出场动画结束时元素的位置 (x2, y2)
    :return: FFmpeg 命令字符串
    """
    start_out = end - duration_out
    x_start, y_start = start_pos
    x_target, y_target = target_pos
    x_end, y_end = end_pos
    # 计算 X 和 Y 轴上的动画表达式
    x_expr_in = f"if(gte(t,{start}), {'max' if x_start > x_target else 'min'}({x_target}, {x_start}+({x_target}-{x_start})*min(1,(t-{start})/{duration_in})), {x_start})"
    y_expr_in = f"if(gte(t,{start}), {'max' if y_start > y_target else 'min'}({y_target}, {y_start}+({y_target}-{y_start})*min(1,(t-{start})/{duration_in})), {y_start})"
    x_expr_out = f"{x_end}*min(1,max(0,(t-{start_out})/{duration_out}))+{x_target}*max(0,1-min(1,(t-{start_out})/{duration_out}))"
    y_expr_out = f"{y_end}*min(1,max(0,(t-{start_out})/{duration_out}))+{y_target}*max(0,1-min(1,(t-{start_out})/{duration_out}))"
    # 构建 FFmpeg 命令
    return (f"overlay=x='if(gte(t,{start_out}),{x_expr_out},{x_expr_in})':"
            f"y='if(gte(t,{start_out}),{y_expr_out},{y_expr_in})':"
            f"enable='between(t,{start},{end})'")


def slide(start: float, end: float, duration: float, start_pos: tuple, target_pos: tuple):
    """
    滑动进入
    :param duration: 动画时长
    :param start: 视频中元素开始显示的时间（秒）
    :param end: 视频中元素结束显示的时间（秒）
    :param start_pos: 元素的初始位置 (x, y)
    :param target_pos: 入场动画结束时元素的位置 (x1, y1)
    :return: FFmpeg 命令字符串
    """
    x_start, y_start = start_pos
    x_end, y_end = target_pos
    # 计算 X 和 Y 轴上的动画表达式
    x_expr = f"if(gte(t,{start}), {'max' if x_start > x_end else 'min'}({x_end}, {x_start}+({x_end}-{x_start})*(t-{start})/{duration}), {x_start})"
    y_expr = f"if(gte(t,{start}), {'max' if y_start > y_end else 'min'}({y_end}, {y_start}+({y_end}-{y_start})*(t-{start})/{duration}), {y_start})"
    # 构建 FFmpeg 命令
    return f"overlay=x='{x_expr}':y='{y_expr}':enable='between(t,{start},{end})'"
