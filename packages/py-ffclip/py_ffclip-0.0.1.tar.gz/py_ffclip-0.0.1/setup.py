from setuptools import setup, find_packages

setup(
    name='py-ffclip',
    version='0.0.1',
    author='kangkang',
    author_email='chenwk.top@foxmail.com',
    description='基于python封装的ffmpeg视频处理工具，依赖ffmpeg命令行',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        "pydub>=0.25.1"
    ],
)
