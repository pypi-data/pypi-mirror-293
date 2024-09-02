from ffclip import FFHelper
from ffclip.FFAudioClip import FFAudioClip
from ffclip.FFClip import FFClip
from ffclip.FFSubtitlesClip import FFSubtitlesClip


class FFVideoClip(FFClip):

    def __init__(self, file_path: str, has_mask=True, audio: FFAudioClip = None, subtitles: FFSubtitlesClip = None):
        self.has_mask = has_mask
        super().__init__(file_path, audio=audio, subtitles=subtitles)

    def video_size(self):
        if self.size is not None:
            return self.size
        else:
            return self.original_size

    def export_audio(self, audio_path: str = None):
        if audio_path and self.has_audio():
            # ffmpeg -i C0439.MP4 -vn -acodec pcm_s16le -ar 44100 -ac 1 audio01.wav
            # ffmpeg -i input.mp4 -vn -b:a 128k -ar 44k -c:a mp3 output.mp3
            if audio_path.endswith(".wav"):
                command = ["ffmpeg", "-i", self.file_path, "-vn", "-acodec",
                           "44100", "-ar", "pcm_s16le",  "-y", audio_path]
            elif audio_path.endswith(".aac"):
                command = ["ffmpeg", "-i", self.file_path, "-vn", "-c:a", "copy", "-y", audio_path]
            elif audio_path.endswith(".mp3"):
                command = ["ffmpeg", "-i", self.file_path, "-vn", "-b:a", "128k",
                           "-ar", "44100", "-c:a", "mp3", "-y", audio_path]
            else:
                raise ValueError("Unsupported audio format.")
            FFHelper.call_cmd(command, comment='音频提取')
        else:
            raise ValueError("No audio in the video clip.")

