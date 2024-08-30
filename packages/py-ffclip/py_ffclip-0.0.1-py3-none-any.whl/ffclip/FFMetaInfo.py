
class FFformat:
    """
    视频格式信息
    """
    filename: str = None
    nb_streams: int = None
    nb_programs: int = None
    format_name: str = None
    format_long_name: str = None
    size: str = None
    start_time: float = None
    duration: float = 1
    bit_rate: str = None

    def __init__(self, format: dict):
        self.filename = format.get('filename')
        self.nb_streams = format.get('nb_streams')
        self.nb_programs = format.get('nb_programs')
        self.format_name = format.get('format_name')
        self.format_long_name = format.get('format_long_name')
        self.size = format.get('size')
        self.start_time = format.get('start_time')
        if format.get('duration') is not None:
            self.duration = float(format.get('duration'))
        self.bit_rate = format.get('bit_rate')


class FFStream:
    """
    视频流信息
    """
    index: int = None
    codec_name: str = None
    codec_long_name: str = None
    codec_type: str = None
    codec_tag_string: str = None
    codec_tag: str = None
    width: int = None
    height: int = None
    coded_width: int = None
    coded_height: int = None
    closed_captions: int = None
    film_grain: int = None
    has_b_frames: int = None
    pix_fmt: str = None
    level: int = None
    color_range: str = None
    color_space: str = None
    color_transfer: str = None
    color_primaries: str = None
    refs: int = None
    r_frame_rate: str = None
    avg_frame_rate: str = None
    time_base: str = None
    disposition: dict = None
    duration: float = 1
    duration_ts: int = None
    bit_rate: str = None
    nb_frames: str = None
    extradata_size: int = None


    def __init__(self, stream: dict):
        self.index = stream.get('index')
        self.codec_name = stream.get('codec_name')
        self.codec_long_name = stream.get('codec_long_name')
        self.codec_type = stream.get('codec_type')
        self.codec_tag_string = stream.get('codec_tag_string')
        self.codec_tag = stream.get('codec_tag')
        self.width = stream.get('width')
        self.height = stream.get('height')
        self.coded_width = stream.get('coded_width')
        self.coded_height = stream.get('coded_height')
        self.closed_captions = stream.get('closed_captions')
        self.film_grain = stream.get('film_grain')
        self.has_b_frames = stream.get('has_b_frames')
        self.pix_fmt = stream.get('pix_fmt')
        self.level = stream.get('level')
        self.color_range = stream.get('color_range')
        self.color_space = stream.get('color_space')
        self.color_transfer = stream.get('color_transfer')
        self.color_primaries = stream.get('color_primaries')
        self.refs = stream.get('refs')
        self.r_frame_rate = stream.get('r_frame_rate')
        self.avg_frame_rate = stream.get('avg_frame_rate')
        self.time_base = stream.get('time_base')
        self.disposition = stream.get('disposition')
        if stream.get('duration') is not None:
            self.duration = float(stream.get('duration'))
        self.duration_ts = stream.get('duration_ts')
        self.bit_rate = stream.get('bit_rate')
        self.nb_frames = stream.get('nb_frames')
        self.extradata_size = stream.get('extradata_size')


class FFMetaInfo:
    """
    视频元信息
    """
    streams: list[FFStream] = None
    format: FFformat = None
    meta_info: dict = None

    def __init__(self, meta_info: dict):
        self.streams = [FFStream(stream) for stream in meta_info.get('streams')]
        self.format = FFformat(meta_info.get('format'))
        self.meta_info = meta_info

    def has_audio(self):
        """
        是否有音频
        :return:
        """
        for stream in self.streams:
            if stream.codec_type == 'audio':
                return True
        return False

    def to_string(self):
        return f"streams: {self.streams}, format: {self.format}"