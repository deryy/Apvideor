# -*- coding: utf-8 -*-
import os
import sys
import shutil
import math
import random
import numpy as np
from PIL import Image
from moviepy.editor import *
from moviepy.audio.fx import all
from moviepy.video.tools.cuts import find_video_period
from moviepy.audio.tools.cuts import find_audio_period
from . import turn4
from moviepy.video.tools.drawing import circle

APVIDEOR_HEIGHT = 720

def trans2deci(a):
	b=[]
	for x in a:
		tmp = round(x,2)
		b.append(tmp)
	return b

# 获取文件大小
def get_file_size(path):
    file_byte = os.path.getsize(path)
    return sizeConvert(file_byte)

# 获得视频时长
def get_file_times(path):
    clip = VideoFileClip(path)
    # file_time = timeConvert(clip.duration)
    file_time = clip.duration
    return file_time

# 时间转换 seconds-->小时分钟秒
def timeConvert(size):
    M, H = 60, 60 ** 2
    if size < M:
        return str(size) + u'秒'
    if size < H:
        return u'%s分钟%s秒' % (int(size / M), int(size % M))
    else:
        hour = int(size / H)
        mine = int(size % H / M)
        second = int(size % H % M)
        tim_srt = u'%s小时%s分钟%s秒' % (hour, mine, second)
        return tim_srt

#缩小特效
def narrow(clip, duration, left, top, ratio):
    return clip.set_duration(duration).resize(lambda t : 1 - ratio*t/duration).set_pos((left, top))
#放大特效
def enlarge(clip, duration, left, top, ratio):  
    return clip.set_duration(duration).resize(lambda t : 1 + ratio*t/duration).set_pos((left, top))

def scroll(get_frame, t):
    """
    This function returns a 'region' of the current frame.
    The position of this region depends on the time.
    """
    frame = get_frame(t)
    speed = 50
    h = 720
    frame_region = frame[int(speed*t):int(speed*t)+h,:]
    return frame_region

# def _get_size(t, du):
# 	max_enlarge = 1.15
# 	new_size = 1 + t*((max_enlarge - 1)/du)
# 	return new_size

def picv2v_generate(musicpath,material_path,save_path,convert_effect_path):

	# audio = AudioFileClip(musicpath).subclip(0, 30)
	# audio_period = find_audio_period(audio)

	#获取所有转场点
	convertpoints = turn4.music_result(musicpath)
	list0 = [0]
	# listnum = [15,16,17,18]

	path = material_path #文件夹目录
	files= os.listdir(path) #得到文件夹下的所有文件名称
	video = [] 
	points = 0
	numpoints = 0

	# #遍历文件夹
	# files = [f for f in files if f[0] !='.']
	# points = len(files)
	# print(points)


	# #随机选取转场素材加入文件夹
	# convertfiles = os.listdir(convert_effect_path)
	# newconvertfiles = []
	# for i in range(0,3):
	# 	print('k')
	# 	x = random.randint(0, len(convertfiles)-1)
	# 	shutil.copyfile(os.path.join(convert_effect_path,convertfiles[x]),os.path.join(path,convertfiles[x]))

	# files= os.listdir(path)
	#再一次遍历更新后的文件夹

	files = [f for f in files if f[0] !='.']
	numpoints = len(files)

	print(files)
	print(numpoints)

	#根据文件数量减少转场点
	if len(convertpoints) >= numpoints:
		convertpoints = random.sample(convertpoints, numpoints)
	elif len(convertpoints) < numpoints:
		num = numpoints - len(convertpoints)
		listnum = []
		for i in range(0,num):
			listnum.append(random.uniform(0, 30))
		convertpoints += listnum

	convertpoints += list0
	convertpoints.sort()
	print(convertpoints)

	i = 0
	for file in files: #遍历文件夹
		# print(os.path.join(path, file))

		if os.path.splitext(file)[1] == ".mp4": #判断视频文件格式是否为.mp4
			
			print(os.path.splitext(file)[1])
			file_path = os.path.join(path, file) #粘合完整视频路径

			#判断视频时长
			file_time = get_file_times(file_path)

			if file_time >= 10:
				videoClip = VideoFileClip(file_path).resize(height=APVIDEOR_HEIGHT).set_position('center') \
					                                 .set_start(convertpoints[i]) \
					                                 .set_end(convertpoints[i]+10)
				video.append(videoClip)
				print(os.path.join(path, file))
				print("i=",i)
				print("file_time is:",file_time)
				print(convertpoints[i],convertpoints[i]+10)

				i += 1

				#重新设置转场点
				transitionpoint = convertpoints[i-1]+10
				reconvertpoints = turn4.music_result(musicpath)

				convertpoints = []
				for j in range(0,len(reconvertpoints)):
					if reconvertpoints[j] > transitionpoint:
						convertpoints.append(reconvertpoints[j])

				print("i=",i)
				print(len(convertpoints))
				print(convertpoints)

				numpoints -= i
				print("numpoints=",numpoints)
				list0 = [transitionpoint]
				#根据文件数量减少转场点
				if len(convertpoints) >= numpoints:
					convertpoints = random.sample(convertpoints, numpoints)
				elif len(convertpoints) < numpoints:
					num = numpoints - len(convertpoints)
					listnum = []
					for i in range(0,num):
						listnum.append(random.uniform(transitionpoint,30))
					convertpoints += listnum

				convertpoints += list0
				convertpoints.sort()
				print(convertpoints)

				i = 0

			elif file_time < 10:

				# videoClip = VideoFileClip(file_path).set_position('center') \
				#                                      .set_start(convertpoints[i]) \
				#                                      .set_end(convertpoints[i+1]) #加载视频
				# video.append(videoClip) #将加载完后的视频加入列表
				# print(os.path.join(path, file))
				# print("file_time is:",file_time)
				# print(convertpoints[i],convertpoints[i+1])

				# i += 1
				videoClip = VideoFileClip(file_path).resize(height=APVIDEOR_HEIGHT).set_position('center') \
					                                 .set_start(convertpoints[i]) \
					                                 .set_end(convertpoints[i]+file_time)
				video.append(videoClip)
				print(os.path.join(path, file))
				print("i=",i)
				print("file_time is:",file_time)
				print(convertpoints[i],convertpoints[i]+file_time)

				i += 1

				#重新设置转场点
				transitionpoint = convertpoints[i-1]+file_time
				reconvertpoints = turn4.music_result(musicpath)

				convertpoints = []
				for j in range(0,len(reconvertpoints)):
					if reconvertpoints[j] > transitionpoint:
						convertpoints.append(reconvertpoints[j])

				print("i=",i)
				print(len(convertpoints))
				print(convertpoints)

				numpoints -= i
				print("numpoints=",numpoints)
				list0 = [transitionpoint]
				#根据文件数量减少转场点
				if len(convertpoints) >= numpoints:
					convertpoints = random.sample(convertpoints, numpoints)
				elif len(convertpoints) < numpoints:
					num = numpoints - len(convertpoints)
					listnum = []
					for i in range(0,num):
						listnum.append(random.uniform(transitionpoint,30))
					convertpoints += listnum

				convertpoints += list0
				convertpoints.sort()
				print(convertpoints)

				i = 0

		elif os.path.splitext(file)[1] == ".jpg":

			print(os.path.splitext(file)[1])
			
			# ratio = 1

			tempimg = Image.open(os.path.join(path, file))
			try:
				data = np.asarray(tempimg)
			except SystemError:
				data = np.asarray(tempimg.getdata())

			print(i)
			print(os.path.join(path, file))
			du = convertpoints[i+1]-convertpoints[i]

			#淡入淡出
			if du<=1:
				tempimgClip = ImageClip(data).resize(height=APVIDEOR_HEIGHT) \
					                          .set_pos('center') \
					                          .set_start(convertpoints[i]) \
					                          .set_end(convertpoints[i+1]) \
					                          .fadein(0.1).fadeout(0.1)
											  # .resize(lambda t : 1+math.sin(t))
			#缩小
			elif (du>1 and du<=2):
				tempimgClip = ImageClip(data).resize(height=APVIDEOR_HEIGHT) \
					                          .set_pos('center') \
					                          .set_start(convertpoints[i]) \
					                          .set_end(convertpoints[i+1]) \
					                          .resize(lambda t : 1-0.02*t) \
					                          .fadein(0.5).fadeout(0.5)
				# tempimgClip = enlarge(tempimgClip, 2, 'center', 'center', 1)

			#放大
			elif (du>2 and du<=3):
				tempimgClip = ImageClip(data).resize(height=APVIDEOR_HEIGHT) \
				                          .set_pos('center') \
				                          .set_start(convertpoints[i]) \
				                          .set_end(convertpoints[i+1]) \
										  .resize(lambda t : 1+0.03*t) \
										  .fadein(1).fadeout(1)
										  # .set_position(lambda t: ('center', -10*t)) \
										  # .set_pos('center',lambda t:-20*t) \
										  # .resize(lambda t : _get_size(t, du)) \


			#左到右
			elif (du>3 and du<=4):
				tempimgClip = ImageClip(data).resize(height=APVIDEOR_HEIGHT) \
					                          .set_pos('left') \
					                          # .set_start(convertpoints[i]) \
					                          # .set_end(convertpoints[i+1]) \
					                          # .set_position(lambda t:(20*t,'center'))
					                          # .set_pos(lambda t:20*t,'center')
											  # .resize(lambda t : 1+math.sin(t)))
				edited_right = tempimgClip.fx(vfx.mirror_x)
				tempimgClip = clips_array([[tempimgClip, edited_right]]).set_position(lambda t:(60*t-200,'center')).set_start(convertpoints[i]).set_end(convertpoints[i+1])

			else:
				tempimgClip = ImageClip(data).resize(height=APVIDEOR_HEIGHT) \
					                          .set_pos('center') \
					                          .set_start(convertpoints[i]) \
					                          .set_end(convertpoints[i+1]) \
					                          .fadein(2).fadeout(2)

			video.append(tempimgClip)
			# print(i, os.path.join(path, file), convertpoints[i],convertpoints[i+1], type(convertpoints))
			print(convertpoints[i],convertpoints[i+1])
			i += 1


	final_time = convertpoints[-1]

	if final_time < 29:
		print('final_time', final_time)
		jpgs = [f for f in files if f[-4:]==".jpg"]
		idx_random = random.randint(0, len(jpgs)-1)
		final_file = os.path.join(path, jpgs[idx_random])

		Ftempimg = Image.open(os.path.join(path, final_file))
		try:
			data = np.asarray(Ftempimg)
		except SystemError:
			data = np.asarray(Ftempimg.getdata())

		r = random.random()#0-1之间抽样随机数
		w,h = [720,720]
				
		if r > 0.5:
			FtempimgClip = ImageClip(data).resize(height=APVIDEOR_HEIGHT) \
						                 .set_pos('center') \
						                 .set_start(final_time) \
						                 .set_end(30) \
						                 .add_mask()
						                 # .fadein(1).fadeout(1)
			FtempimgClip.mask.get_frame = lambda t: circle(screensize=(FtempimgClip.w,FtempimgClip.h),
	                                       center=(FtempimgClip.w/2,FtempimgClip.h/4),
	                                       radius=max(0,int(360-t*360/(30-final_time))),
	                                       col1=1, col2=0, blur=4)
			video.append(FtempimgClip)

		else:
			FtempimgClip = ImageClip(data).resize(height=APVIDEOR_HEIGHT) \
						                 .set_pos('center') \
						                 .set_start(final_time) \
						                 .set_end(30) \
						                 .resize(lambda t : 1-0.02*t) \
						                 .fadein(1).fadeout(1)
			video.append(FtempimgClip)

	# musicpath = music_path()
	audioClip = AudioFileClip(musicpath)


	# video = video.speedx(final_duration=30*audio_period).fx(vfx.loop, duration=audio.duration)
	video = np.array(video)
	# print(audioClip, video)
	# video = video.set_audio(audioClip)

	final_clips = CompositeVideoClip(video, size=(720,720), bg_color=(0,0,0)).set_audio(audioClip).fadein(0.5).fadeout(0.5)

	final_clips.write_videofile(save_path, fps=24, codec='libx264', audio_bitrate='1000k', bitrate='4000k')
	# fps=videoClip.fps
	# set_duration(convertpoints[numpoints])

if __name__ == "__main__":
	convertpath = "/Users/admin/Desktop/convert/" #转场素材文件夹目录
	material_path = "/Users/admin/Desktop/材料/时尚/视觉素材" #文件夹目录
	save_path = './newvideo.mp4'
	musicpath = '/Users/admin/Desktop/023371.mp3'
	picv2v_generate(musicpath, material_path, save_path, convertpath)


