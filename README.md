Apvideor: A music-driven system for generating apparel display video
====

Introduction
----
Video plays a great important role in online apparel sales, which is a vital tool for publicity and to provide consumers with space of imagination. However, as the apparel market rapidly updates in large amounts every day, creating videos for fast increasing clothes can be challenging and labor-consuming. Considering this, we present ApVideor, a musicdriven video generation system customized for displaying clothes. This system consists of two main modules: music recommendation module and audio-visual synthesis module. The former assists users in searching background music that matches the apparel style, while the latter combines the audio and visuals into a video by music-driven approaches. Our user study suggests that this system makes the video creation process significantly easier and faster than manual creation. Meanwhile, the viewer test suggests that apparel-displaying videos created using our system are of comparable quality to those created manually by people who have worked with video editing.

How to Use
----
1. Ensure that the operating environment memory is larger than 8G (since the process of cliping video images by moviepy need to consume a lot of memory).
2. Download the project package and extract it.
3. Programming Environment：
>Python3.6
4. Install dependency package：<br>
>* make use of the requirements.txt to install the dependency(Django,Librosa,.etc): <br>
```
pip install -r requirements.txt
```
>* install ffmpeg<br>
5. Run：<br>
```
python manage.py runserver 8000
```
6. Visit the website：
>http://localhost:8000/musicGo

Result
----
You can go [here](https://deryy.github.io/Apvideor_demo/page.html) to see the videos created by Apvideor and some other detail informations.

