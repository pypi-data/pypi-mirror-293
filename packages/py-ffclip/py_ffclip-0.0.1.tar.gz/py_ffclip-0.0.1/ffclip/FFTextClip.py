import os
import tempfile

from ffclip import FFHelper
from ffclip.FFImageClip import FFImageClip


class FFTextClip(FFImageClip):
    cmd: list = []
    txt: str = None

    def __init__(self, txt=None, filename=None, size=None, color='black',
                 bg_color='transparent', fontsize=None, font='Courier',
                 stroke_color=None, stroke_width=1, method='label',
                 kerning=None, align='center', interline=None,
                 temp_path=None, temptxt=None, remove_temp=True):
        # 字体名称必须将空格替换为-连接
        # 使用 fc-list : family file 获取可用的字体名称
        font = font.replace(" ", "-")
        if method == 'caption':
            txt = txt.lstrip()
        if txt is not None:
            if temptxt is None:
                temptxt_fd, temptxt = tempfile.mkstemp(suffix='.txt')
                try:  # only in Python3 will this work
                    os.write(temptxt_fd, bytes(txt, 'UTF8'))
                except TypeError:  # oops, fall back to Python2
                    os.write(temptxt_fd, txt)
                os.close(temptxt_fd)
            txt = '@' + temptxt
        else:
            # use a file instead of a text.
            txt = "@%" + filename

        self.txt = txt
        if size is not None:
            size = ('' if size[0] is None else str(size[0]),
                    '' if size[1] is None else str(size[1]))
        # 查找系统字体按照 字体名称-Style 命名
        cmd = (["magick",
                "-background", bg_color,
                "-fill", color,
                "-font", font])

        if fontsize is not None:
            cmd += ["-pointsize", "%d" % fontsize]
        if kerning is not None:
            cmd += ["-kerning", "%0.1f" % kerning]
        if stroke_color is not None:
            cmd += ["-stroke", stroke_color, "-strokewidth",
                    "%.01f" % stroke_width]
        if size is not None:
            cmd += ["-size", "%sx%s" % (size[0], size[1])]
        if align is not None:
            cmd += ["-gravity", align]
        if interline is not None:
            cmd += ["-interline-spacing", "%d" % interline]
        self.cmd = cmd

        temp_file_fd, temp_filename = tempfile.mkstemp(suffix='.png', dir=temp_path)
        os.close(temp_file_fd)
        self.cmd += ["%s:%s" % (method, txt),
                     "-type", "truecolormatte", "PNG32:%s" % temp_filename]
        try:
            FFHelper.call_cmd(cmd, comment="创建字体图片")
        except (IOError, OSError) as err:
            error = ("FFTextClip Error: creation of %s failed because of the "
                     "following error:\n\n%s.\n\n." % (filename, str(err)))
            raise IOError(error)

        if remove_temp:
            if os.path.exists(temptxt):
                os.remove(temptxt)
        FFImageClip.__init__(self, temp_filename)
        self.set_duration(1)

