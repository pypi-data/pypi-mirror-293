from enum import Enum

from ffclip.FFClipParam import FFClipParam

# 默认持续时长
default_duration = 1


class AnimationType(Enum):
    """
    定义动画类型
    """
    animation_in = "in"  # 进场动画
    animation_out = "out"  # 出场动画
    animation_loop = "loop"  # 循环


class AnimationInName(Enum):
    """
    定义动画效果
    """
    fade_in = "fade_in"  # 淡入淡出
    fade_resize_in = "fade_resize_in"  # 淡入放大
    slide_up = "slide_up"  # 向上滑动
    slide_down = "slide_down"  # 向下滑动
    slide_left = "slide_left"  # 向左滑动
    slide_right = "slide_right"  # 向右滑动
    slide = "slide"  # 自动判断滑动到指定位置


class AnimationOutName(Enum):
    """
    定义动画效果
    """
    fade_out = "fade_out"
    fade_resize_out = "fade_resize_out"
    slide_up = "slide_up"  # 向上滑动
    slide_down = "slide_down"  # 向下滑动
    slide_left = "slide_left"  # 向左滑动
    slide_right = "slide_right"  # 向右滑动
    slide = "slide"  # 自动判断滑动到指定位置


class AnimationSlide:
    name: str = None
    duration: float = 0
    start_pos: tuple = None
    target_pos: tuple = None
    t_start: float = 0
    t_end: float = 0

    def __init__(self, slide_type: str, animation_map: dict, clip_param: FFClipParam):
        animation = animation_map.get(slide_type)
        if animation is None:
            return
        video_size = clip_param.main_size
        main_duration = clip_param.main_duration
        clip_size = clip_param.size
        if clip_size is None:
            clip_size = clip_param.original_size
        clip_pos = clip_param.position
        self.slide_type = slide_type
        self.name = animation.get('name')
        self.duration = animation.get('duration')
        if self.duration is None:
            self.duration = default_duration
        self.t_start = clip_param.start
        self.t_end = clip_param.end
        if self.t_start is None:
            self.t_start = 0
        if self.t_end is None:
            self.t_end = main_duration
        # 通过主视频和元素位置，计算start_pos 和 target_pos
        if self.slide_type == AnimationType.animation_in.value:
            # 计算进入动画的开始位置和结束位置
            if self.name == AnimationInName.slide.slide_right.value:
                # 向右滑动，y坐标不变，初始在屏幕最外侧左边
                self.start_pos = (0 - clip_size[0], clip_pos[1])
                self.target_pos = clip_pos

            if self.name == AnimationInName.slide.slide_left.value:
                # 向左滑动，y坐标不变，初始在屏幕最外侧右边
                self.start_pos = (video_size[0], clip_pos[1])
                self.target_pos = clip_pos

            if self.name == AnimationInName.slide.slide_up.value:
                # 向上滑动，x坐标不变，初始在屏幕最外侧下边
                self.start_pos = (clip_pos[0], video_size[1])
                self.target_pos = clip_pos

            if self.name == AnimationInName.slide.slide_down.value:
                # 向下滑动，x坐标不变，初始在屏幕最外侧上边
                self.start_pos = (clip_pos[0], 0 - clip_size[1])
                self.target_pos = clip_pos

        if self.slide_type == AnimationType.animation_out.value:
            self.t_end = self.t_end - self.duration
            # 出场动画，start_pos = clip_pos, target_pos = 出场位置
            if self.name == AnimationOutName.slide.slide_right.value:
                # 向右滑动，y坐标不变，初始在元素设定位置，结束在屏幕右侧
                self.start_pos = clip_pos
                self.target_pos = (video_size[0], clip_pos[1])

            if self.name == AnimationOutName.slide.slide_left.value:
                # 向左滑动，y坐标不变，初始在元素设定位置，结束在屏幕左侧
                self.start_pos = clip_pos
                self.target_pos = (0 - clip_size[0], clip_pos[1])

            if self.name == AnimationOutName.slide.slide_up.value:
                # 向上滑动，x坐标不变，初始在元素设定位置，结束在屏幕上侧
                self.start_pos = clip_pos
                self.target_pos = (clip_pos[0], 0 - clip_size[1])

            if self.name == AnimationOutName.slide.slide_down.value:
                # 向下滑动，x坐标不变，初始在元素设定位置，结束在屏幕下侧
                self.start_pos = clip_pos
                self.target_pos = (clip_pos[0], video_size[1])

    def check(self):
        return self.start_pos is not None and self.target_pos is not None and self.t_end > self.t_start
