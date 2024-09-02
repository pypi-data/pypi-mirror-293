import os


# 使用 ffmpeg zoompan滤镜，实现镜头聚焦效果，： 镜头在图片上下左右移动，实现聚焦效果


def movie_zoompan(file_name: str, duration: float, action: str, size: str):
    """
    :param file_name: 文件名称
    :param duration: 持续时长
    :param action: 运镜方案
    :return:
    ffmpeg -y -i ./out/windows_people_resize.jpg -vf "scale=19200x12800,
    zoompan=x='(1489+(on/100)*(-1022))*10*(1-1/zoom):y='(278+(on/100)*(93))*10*(1-1/zoom)':z='2.8':d=100:s=1920x1280"
    -pix_fmt yuv420p -c:v libx264 ./out/windows_people_move1.mp4
    """
    command = f"ffmpeg -i {file_name} -vf \"zoompan=z='min(zoom+0.0015,1.5)':d={duration}:x='if(gte(zoom,1.5),x,x+1/a)':y='y+mod(d,{duration}/2)*2':s={size}\" -y {file_name}_zoompan.mp4"
    os.system(command)
