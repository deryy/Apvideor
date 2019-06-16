Apvideor: A music-driven system for generating apparel display video
====

Introduction
----
Video plays a great important role in online apparel sales, which is a vital tool for publicity and to provide consumers with space of imagination. However, as the apparel market rapidly updates in large amounts every day, creating videos for fast increasing clothes can be challenging and labor-consuming. Considering this, we present ApVideor, a musicdriven video generation system customized for displaying clothes. This system consists of two main modules: music recommendation module and audio-visual synthesis module. The former assists users in searching background music that matches the apparel style, while the latter combines the audio and visuals into a video by music-driven approaches. Our user study suggests that this system makes the video creation process significantly easier and faster than manual creation. Meanwhile, the viewer test suggests that apparel-displaying videos created using our system are of comparable quality to those created manually by people who have worked with video editing.

How to Use
----
1. 首先要保证运行环境内存大于等于`8G`（moviepy剪辑视频图片需要消耗大量内存）；
2. 下载ApVideor工程文件包(zip, scp, scp, unzip)并解压
3. 基础环境配置：Python3.6
4. 安装依赖包：<br>
>>用requirements.txt安装pip包（包括Django、Librosa等）；<br>
>>安装ffmpeg环境<br>
5. 在主目录文件夹下运行：
  python manage.py runserver 8000

Result
----
You can go [here](https://deryy.github.io/Apvideor_demo/page.html) to see the videos created by Apvideor and some other detail informations.

