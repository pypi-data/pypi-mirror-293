class FFSubtitlesClip:
    subtitle_path: str = None
    fontsize: int = None
    font: str = None
    color: str = None
    margin_v = None
    margin_l = None
    margin_r = None
    shadow = None
    border_style = None
    outline = None

    def __init__(self, subtitle_path, fontsize=10, font=None, color="#ffffff", margin_v=None, margin_r=None,
                 margin_l=None, border_style=None, shadow=0, outline=0):
        """
        -vf"subtitles=subtitles_file.mxf_Subtitle.srt:force_style='OutlineColour=&H80000000,
        BorderStyle=3,Outline=1,Shadow=0,MarginV=20
        01.Name             风格(Style)的名称. 区分大小写. 不能包含逗号.
        02.Fontname         使用的字体名称, 区分大小写.
        03.Fontsize         字体的字号
        04.PrimaryColour    设置主要颜色, 为蓝-绿-红三色的十六进制代码相排列, BBGGRR. 为字幕填充颜色
        05.SecondaryColour  设置次要颜色, 为蓝-绿-红三色的十六进制代码相排列, BBGGRR. 在卡拉OK效果中由次要颜色变为主要颜色.
        06.OutlineColour    设置轮廓颜色, 为蓝-绿-红三色的十六进制代码相排列, BBGGRR.
        07.BackColour       设置阴影颜色, 为蓝-绿-红三色的十六进制代码相排列, BBGGRR. ASS的这些字段还包含了alpha通道信息. (AABBGGRR),
                            注ASS的颜色代码要在前面加上&H
        08.Bold             -1为粗体, 0为常规
        09.Italic           -1为斜体, 0为常规
        10.Underline       [-1 或者 0] 下划线
        11.Strikeout       [-1 或者 0] 中划线/删除线
        12.ScaleX          修改文字的宽度. 为百分数
        13.ScaleY          修改文字的高度. 为百分数
        14.Spacing         文字间的额外间隙. 为像素数
        15.Angle           按Z轴进行旋转的度数, 原点由alignment进行了定义. 可以为小数
        16.BorderStyle     1=边框+阴影, 3=纯色背景. 当值为3时, 文字下方为轮廓颜色的背景, 最下方为阴影颜色背景.
        17.Outline         当BorderStyle为1时, 该值定义文字轮廓宽度, 为像素数, 常见有0, 1, 2, 3, 4.
        18.Shadow          当BorderStyle为1时, 该值定义阴影的深度, 为像素数, 常见有0, 1, 2, 3, 4.
        19.Alignment       定义字幕的位置. 字幕在下方时, 1=左对齐, 2=居中, 3=右对齐. 1, 2, 3加上4后字幕出现在屏幕上方. 1, 2, 3
                            加上8后字幕出现在屏幕中间. 例: 11=屏幕中间右对齐. Alignment对于ASS字幕而言, 字幕的位置与小键盘数字对应的位置相同.
        20.MarginL         字幕可出现区域与左边缘的距离, 为像素数
        21.MarginR         字幕可出现区域与右边缘的距离, 为像素数
        22.MarginV         垂直距离
        "
        :param subtitle_path:
        :param fontsize:
        :param font:
        :param color:
        """
        self.subtitle_path = subtitle_path
        self.fontsize = fontsize
        self.font = font
        self.color = color
        self.margin_v = margin_v
        self.margin_l = margin_l
        self.margin_r = margin_r
        self.shadow = shadow
        self.border_style = border_style
        self.outline = outline

        if self.color.startswith('#'):
            html_color = self.color[1:]
            rr = html_color[0:2]
            gg = html_color[2:4]
            bb = html_color[4:6]
            self.color = f'&H{bb}{gg}{rr}&'

    def get_vf(self, input_filter: str = '', output_filter: str = ''):
        # ffmpeg4.4版本 字幕滤镜 无法自动换行
        if not input_filter.startswith('['):
            input_filter = f'[{input_filter}]'

        vf = f"subtitles={self.subtitle_path}:force_style='"
        vf = input_filter + vf
        if self.fontsize is not None:
            vf += f"FontSize={self.fontsize},"
        if self.font is not None:
            # 字体命名方式，[名称][空格][样式] 如： 翩翩体-简 常规体
            vf += f"FontName={self.font},"
        if self.color is not None:
            vf += f"PrimaryColour={self.color}"
        if self.margin_v is not None:
            vf += f",MarginV={self.margin_v}"
        if self.margin_l is not None:
            vf += f",MarginL={self.margin_l}"
        if self.margin_r is not None:
            vf += f",MarginR={self.margin_r}"
        if self.shadow is not None:  # 新增阴影设置
            vf += f",Shadow={self.shadow}"
        if self.border_style is not None:  # 新增阴影设置
            vf += f",BorderStyle={self.border_style}"
        if self.outline is not None:  # 新增阴影设置
            vf += f",Outline={self.outline}"
        vf += "'" + output_filter
        return vf
