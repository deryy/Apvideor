#-*- coding:utf-8 -*-
from django.http import HttpResponseNotFound,HttpResponse,HttpResponseForbidden,HttpResponseRedirect
from django.shortcuts import render,render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
import json
import string
import random
import time
import json
import os
import csv
from django.conf import settings

from . import picv2v

savepath = os.path.join(os.path.dirname(__file__),'..','images_data')
# Create your views here.
def index(request):
	return render(request,'index.html')
	
def material(request):
	return render(request,'material.html')

def music(request):
	return render(request,'music.html')

def result(request):
	return render(request,'result.html')

def tutorial(request):
	return render(request,'tutorial.html')

@csrf_exempt
def imageSave(request):
	f_list = request.FILES.getlist('file')
	print(f_list)
	result=[]
	#图片文件夹名命名以用户随机id_绝对时间戳
	random_user_id = ''.join([random.choice(string.digits) for i in range(8)])
	time_stamp = int(round(time.time() * 1000))
	dirname = random_user_id+'_'+str(time_stamp)
	dir_url = os.path.join(savepath,dirname)

	if not os.path.exists(dir_url):
		os.makedirs(dir_url)
	for f in f_list:

		if not os.path.exists(savepath):
			os.makedirs(savepath)
		
		#文件夹内图片命名以自增序号.jpg
		inc_id = len(os.listdir(dir_url))+1
		filename = str(inc_id)
		origin_format = f.name.split('.')[-1]
		
		if origin_format == 'mp4':
			format = '.mp4'
			print(origin_format,' -> ',format)	
		else:
			format = '.jpg'
			print(origin_format,' -> ',format)
		save_url = os.path.join(dir_url,filename + format)
		print(save_url)
		dest = open(save_url,'wb+')
		for chunk in f.chunks():
			dest.write(chunk)
		dest.flush()
		dest.close()

	result.append(dirname)
	return HttpResponse(json.dumps(result),content_type='application/json')

@csrf_exempt
def getVideo(request):
	material_dirname = request.POST.get("material_path")
	material_path = os.path.join(savepath, material_dirname)
	music_id = request.POST.get("music_path")
	music_path = os.path.join(settings.STATIC_ROOT, 'apvideor', music_id+'.mp3')
	result_video_path = os.path.join(settings.STATIC_ROOT, material_dirname+'_result.mp4')
	convert_effect_path = os.path.join(settings.STATIC_ROOT, 'convert_effect')
	print("music_path",music_path)
	print("result_video_path",result_video_path)
	picv2v.picv2v_generate(music_path,material_path,result_video_path,convert_effect_path)

	return HttpResponse("success")

@csrf_exempt
def getMusicStyle(request):
	dress_style = request.POST.get("dress_style")
	match_file_path = os.path.join(os.path.dirname(__file__),'apparel_style_to_music.csv')
	fma_file_path = os.path.join(os.path.dirname(__file__),'fma_meta_for_recommendation.csv')

	with open(match_file_path,'r',encoding='utf-8') as f1:
		with open(fma_file_path,'r',encoding='utf-8') as f2:
			match_reader = csv.reader(f1)
			fma_reader = csv.reader(f2)
			music_style = ''
			valence = ''
			i = 1
			genre_valence_pairs = []
			for row in match_reader:
				if i==1:
					i=i+1
					continue
				if dress_style == row[0]:
					g, v = row[1], float(row[2])
					genre_valence_pairs.append((g, v))

			random.shuffle(genre_valence_pairs)
			music_style, valence = genre_valence_pairs[0]
			total_list=[]
			for row in fma_reader:
				if row[4] == music_style and abs(float(row[3])-valence)<0.5:
					total_list.append(row)
			
			total_list.sort(key=lambda x:int(x[6]))
			total_list.reverse()
			
			id_list = []
			if len(total_list) < 5:
				id_list = [x[0].zfill(6) for x in total_list]
			else:
				id_list = [x[0].zfill(6) for x in total_list[0:5]]
			print(id_list)
	random.shuffle(id_list)
	result = []
	result.append(id_list)


	return HttpResponse(json.dumps(result),content_type='application/json')

@csrf_exempt
def getMusicName(request):
	music_id = request.POST.get("music_id")
	music_name=''

	fma_file_path = os.path.join(os.path.dirname(__file__),'fma_meta_for_recommendation.csv')
	with open(fma_file_path,'r',encoding='utf-8') as f:
		fma_reader = csv.reader(f)
		i = 1
		for row in fma_reader:
			if i==1:
				i=i+1
				continue
			if int(music_id) == int(row[0]):
				music_name = row[1]
				print("music_name:",music_name)
				break
	
	result = []
	result.append(music_name)

	return HttpResponse(json.dumps(result),content_type='application/json')


@csrf_exempt
def ajax(request):
	return HttpResponse("ajax")




