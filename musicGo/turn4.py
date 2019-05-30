# -- coding: utf-8 --
# Track beats using time series input
import librosa
import matplotlib.pyplot as plt
import librosa.display
import numpy as np
import random

np.set_printoptions(threshold=np.inf)



def music_result(music_path):
	#保留两位小数
	def trans2deci(a):
		b=[]
		for x in a:
			tmp = round(x,2)
			b.append(tmp)
		return b

	#强弱二值化
	def trans2di(a):
		it_max = np.max(a)
		a_left = list(filter(lambda x: x < it_max, a))
		it_second_max = np.max(a_left)

		b=[]
		for x in a:
			if x >= (it_second_max*0.5):
				x=1
			else:
				x=0
			b.append(x)
		return b


	#识别突出音符(max,=1,比前一音符强度大2倍)匹配的时间点(模式一)
	def peaks_turn_detect(note_strengths):
		index_list = []
		similarity = []
		imax = np.max(note_strengths)
		max_index = note_strengths.index(imax)
		# index_list.append(max_index)
		for index,note_strength in enumerate(note_strengths):
			if index!=max_index:
				if index>=1 and note_strength >= 2*note_strengths[index-1]:
					outer = note_strength - note_strengths[index-1]
					index_list.append(index)
					similarity.append(outer)
		# index_list.sort()
		# print(index_list, similarity)
		index_list = np.array(index_list)[np.argsort(similarity)][::-1]
		# print("模式一识别：",index_list)
		return index_list

	#识别空音段前后音符匹配的起点和终点对(模式二)
	def rests_turn_detect(onset_times,tempo):
		all_couple=[]
		for i in range(0,len(onset_times)):
			couple=[]
			if(i<len(onset_times)-1):
				space = onset_times[i+1]-onset_times[i]
				if(space>=1.8*60/tempo):
					couple.append(i)
					couple.append(i+1)
					all_couple.append(couple)
		return all_couple

	#识别旋律时间段(模式三)
	def rhythm_detect(note_strengths):
		index_list = []
		for i in range(0,len(note_strengths)-20):
			for j in range(i+10,len(note_strengths)-10):
				if note_strengths[i]>=note_strengths[j]*0.8 and note_strengths[i]<=note_strengths[j]*1.2:
					sum = 0
					for k in range(1,10):
						if note_strengths[i+k]>=note_strengths[j+k]*0.8 and note_strengths[i+k]<=note_strengths[j+k]*1.2:
							sum += 1
							if sum==9:
								index_list.append([i,i+10])
							else:
								continue
						else:
							break
				else:
					continue

		similarity = []
		for a in index_list:
			s1 = np.array(note_strengths[a[0]: a[0]+10])
			s2 = np.array(note_strengths[a[1]: a[1]+10])
			similarity.append(np.sqrt(np.mean(s1-s2)**2))
		# print(similarity)
		index_list = np.array(index_list)[np.argsort(similarity)]

		return index_list

	#强弱差值段(模式四)
	def difference_value_detect(note_strengths):
		index_list = []
		k = 0
		sum = 0

		for i in range(k,len(note_strengths)-2):
			if note_strengths[i]<note_strengths[i+1]:
				if note_strengths[i+2]<note_strengths[i+1]:
					sum += 1
					k += 2
					continue
				else:
					if sum >= 4:
						index_list.append([i,i+sum])
					sum = 0
					k += 2
					continue
			elif note_strengths[i]>note_strengths[i+1]:
				if note_strengths[i+2]>note_strengths[i+1]:
					sum += 1
					k += 2
					continue
				else:
					if sum >= 4:
						index_list.append([i,i+sum])
					sum = 0
					k += 2
					continue

		similarity = [np.std(note_strengths[a[0]:a[1]]) for a in index_list]
		index_list = np.array(index_list)[np.argsort(similarity)][::-1]

		return index_list


# if __name__ == '__main__':
	# Get the file path to the included audio example
	# Load the audio as a waveform `y`
	# Store the sampling rate as `sr`

	#filename ='Crazy Bird.mp3'
	#y, sr = librosa.load(filename,sr=None,offset=0.0, duration=30.0)
	# filepath = '/Users/dogyy/Documents/alibaba/musicpro/实验视频/'
	# filename = filepath+'MyDownfall.mp3'
	
	y, sr = librosa.load(music_path,sr=None)

	# 采样数目，一般每秒几万个
	# print('sample ratio:',sr)
	# 总采样数
	# print('y num:',len(y))


	# get onset envelope
	onset_env = librosa.onset.onset_strength(y=y, sr=sr)
	# print('onset_env length:',len(onset_env))
	# 音频帧转时间点，根据onset_strength为依据提取出来的基础坐标时间点,一般有几千个
	times = librosa.frames_to_time(np.arange(len(onset_env)),sr=sr)


	# Track beats using a pre-computed onset envelope to plot the beat events against the onset strength envelope
	tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env,sr=sr)
	beat_times = librosa.frames_to_time(beats, sr=sr)
	# print('tempo: {:.2f} beats per minute'.format(tempo))
	#print('beat_times:',trans2deci(beat_times))


	#每个节拍点的强弱识别
	beat_strengths = []
	for beat_time in beat_times:
		index = [index for index,i in enumerate(times) if i==beat_time]
		beat_strength = onset_env[index]
		beat_strengths.append(beat_strength)
	beat_strength_2 = trans2di(beat_strengths)
	#print("beat strength bi_tran:",beat_strength_2)


	#音符起点识别
	onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
	#帧数组到时间数组
	onset_times = librosa.frames_to_time(onset_frames, sr=sr)
	#print('onset time:',trans2deci(onset_times))

	#每个音符的强弱识别
	note_strengths = []
	for onset_time in onset_times:
		scale_indexs = [index for index,time in enumerate(times) if time>(onset_time-0.05) and time<(onset_time+0.05)]
		note_strength = np.max([onset_env[index] for index in scale_indexs])
		note_strengths.append(note_strength)
	#print("note strength bi_tran:",trans2di(note_strengths))
	#print("note strength:",note_strengths)

	turn_times = {}
	# print("--------------------------")
		
	#模式一识别(峰值音符)
	peak_index_list = peaks_turn_detect(note_strengths)
	peak_turn_times=[]
	for index in peak_index_list:
			peak_turn_times.append(onset_times[index])
	# print(u"模式一转场时间点：",trans2deci(peak_turn_times))
	turn_times['peak'] = trans2deci(peak_turn_times)
	# print("--------------------------")


	#模式二识别（空音段）
	rest_couples = rests_turn_detect(onset_times,tempo)
	# print("模式二识别：",rest_couples)
	rest_turn_times=[]
	for rest_couple in rest_couples:
		rest_turn_times.append(onset_times[rest_couple[0]])
		rest_turn_times.append(onset_times[rest_couple[1]])
	# print(u"模式二转场时间点：",trans2deci(rest_turn_times))
	turn_times['rest'] = trans2deci(rest_turn_times)
	# print("--------------------------")

	#模式三识别（旋律相似段）
	rhythm_d = rhythm_detect(note_strengths)
	# print("模式三识别：",rhythm_d)
	rhythm_d_times = []
	for rhythm in rhythm_d:
	    rhythm_d_times.append(onset_times[rhythm[0]])
	    rhythm_d_times.append(onset_times[rhythm[1]])
	# print(u"模式三转场时间点：",trans2deci(rhythm_d_times))
	turn_times['rhythm_d'] = trans2deci(rhythm_d_times)
	# print("--------------------------")

	#模式四识别（节奏规律段）
	difference_value_d = difference_value_detect(note_strengths)
	# print("模式四识别：",difference_value_d)
	difference_value_d_times = []
	for difference_value in difference_value_d:
	    difference_value_d_times.append(onset_times[difference_value[0]])
	    # difference_value_d_times.append(onset_times[difference_value[1]])
	# print(u"模式四转场时间点：",trans2deci(difference_value_d_times))
	turn_times['difference_value_d'] = trans2deci(difference_value_d_times)
	# print("--------------------------")

	#最终转场

	if tempo <= 60:
		# print("*** 舒缓音乐 ***")
		index_list = []
		ratio = 1
		# index_list.append(peak_turn_times)
		# index_list.append(rest_turn_times)
		# index_list.append(rhythm_d_times)
		# index_list.append(ifference_value_d_times)

		index_list = peak_turn_times + rest_turn_times + rhythm_d_times + difference_value_d_times


	elif tempo <= 120:
		# print("*** 自然音乐 ***")
		index_list = []
		ratio = 2
		# index_list.append(rhythm_d_times)
		# index_list.append(difference_value_d_times)
		# index_list.append(rest_turn_times)
		# index_list.append(peak_turn_times)

		index_list = rhythm_d_times + difference_value_d_times + rest_turn_times + peak_turn_times


	elif tempo >120:
		# print("*** 动感音乐 ***")
		index_list = []
		ratio = 3
		# index_list.append(peak_turn_times)
		# index_list.append(difference_value_d_times)
		# index_list.append(rest_turn_times)
		# index_list.append(rhythm_d_times)

		index_list = peak_turn_times + difference_value_d_times + rest_turn_times + rhythm_d_times


	# result = random.sample(index_list, 10)
	result = []
	for j in range(0,len(index_list)):
		if index_list[j] < 30:
			result.append(index_list[j])
	result.sort()

	return result



