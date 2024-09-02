import os
import tempfile

from ffclip.FFAudioClip import FFAudioClip
from ffclip.FFClip import FFClip
from ffclip.FFSubtitlesClip import FFSubtitlesClip


class FFImageClip(FFClip):

    def __init__(self, img, audio: FFAudioClip = None, subtitles: FFSubtitlesClip = None):
        if type(img) is str:
            file_path = img
        else:
            # np.array(img) 转换为图片
            temp_file_fd, file_path = tempfile.mkstemp(suffix='.png')
            os.close(temp_file_fd)
            img.save(file_path)
        super().__init__(file_path, audio, subtitles)
        if audio is None:
            self.set_duration(1)
