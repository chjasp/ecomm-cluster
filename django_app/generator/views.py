
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.files.storage import default_storage
from django.conf import settings
from django.core.files.base import ContentFile

from rest_framework.decorators import api_view, permission_classes
# Userinput- & Databaserelated imports
from .models import Token
# Topic-model-related imports
from .scripts.topicmodel import Modelbuilder
# Imports general gpt-3-settings (ENGINE, TEMP, ...)
from .scripts.prompt_settings import * 
# General Python imports
import concurrent.futures
import json
import re
import openai
import time

import numpy as np
from numpy.linalg import norm
import pickle
from tqdm import tqdm, tqdm_notebook
import os
import time
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input

openai.api_key = KEY

new_shape = (136, 102, 3)
model = VGG16(weights='imagenet', input_shape=new_shape, include_top=False)

def extract_features(img_path, model):
	input_shape = (136, 102, 3)
	img = image.load_img(img_path,
	                     target_size=(input_shape[0], input_shape[1]))
	img_array = image.img_to_array(img)
	expanded_img_array = np.expand_dims(img_array, axis=0)
	preprocessed_img = preprocess_input(expanded_img_array)
	features = model.predict(preprocessed_img)
	flattened_features = features.flatten()
	normalized_features = flattened_features / norm(flattened_features)
	return normalized_features

# Pure render-functions
def home(request):
	return render(request, 'generator/home.html', {'title': 'home'})

def table_create(request):

	users = User.objects.all()[5:]
	for i in range(len(users)):
		print("###")
		Token.objects.create(user_id=users[i].id, remaining_tokens=400)
		print(users[i])
		print(users[i].id)
   

	# users = []
	# print(User.objects.all())

	# users.append(User.objects.get(id=7))
	# users.append(User.objects.get(id=2))
	# users.append(User.objects.get(id=3))
	# users.append(User.objects.get(id=4))
	# users.append(User.objects.get(id=5))

	# for i in range(len(users)):
	# 	print(users[i])

	# beta1 = User.objects.get(id=1)
	# beta2 = User.objects.get(id=2)
	# beta3 = User.objects.get(id=3)
	# beta4 = User.objects.get(id=4)
	# beta5 = User.objects.get(id=5)

	# Token.objects.create(user_id=beta1.id)
	# Token.objects.create(user_id=beta2.id)
	# Token.objects.create(user_id=beta3.id)
	# Token.objects.create(user_id=beta4.id)
	# Token.objects.create(user_id=beta5.id)

	print("users created")
	return render(request, 'generator/about.html', {'title': 'about'})

@login_required
def direct(request):
	return render(request, 'generator/generate.html', {'title': 'generate'})


# Auxiliary-functions
def gpt3_call(prompt, settings, user_id):
	# Make API-call
	json_output = openai.Completion.create(engine=ENGINE,
                 						   prompt=prompt,
										   max_tokens=settings["max_tokens"],
										   temperature=settings["temp"],
										   stop=settings["stop"],
										   top_p=settings["top_p"],
										   presence_penalty=settings["pres_penalty"],
										   frequency_penalty=settings["freq_penalty"],
										   n=settings["n"],
										   user=user_id)

	print(json_output)

	result_array = []
	for i in range(settings["n"]):
		# Check for sensitive content
		response_check = "<|endoftext|>" + json_output["choices"][i]["text"] + "\n--\nLabel:"
		safeInt = openai.Completion.create(engine='content-filter-alpha-c4',
										prompt=response_check,
										max_tokens=1,
										temperature=0.0,
										top_p=0,
										user="admin_Christoph")
		if safeInt["choices"][0]["text"] == '0':
			result_array.append(json_output["choices"][i]["text"])
		else: result_array.append("1. Warning: Inappropriate output generated AI: Warning: Inappropriate output generated")

	return result_array

def split_check(arr, mode):
	if (mode=="initQuestions" or mode=="Google Ad"):
		split = re.split('1. |2. ', arr)
		print("SPLIT")
		print(split)
		if (len(split) > 1):
			return split[1]
		else:
			return "--"
	else:
		if (mode == "answer"):
			split = arr.split("Answer: ")
			if (len(split) == 2):
				return split[1]
			else:
				return "--"
		else:
			split = arr.split("AI: ")
			if (len(split) == 2):
				return split[1]
			else:
				return "--"

# @csrf_exempt
@api_view(["POST"]) 
@permission_classes([IsAuthenticated])
def query_json_copypress(request):
	data = request.data 
	u_id = data["id"]
	name = data["name"]
	text = data["text"]
	mode = data["response_mode"]

	u_token = Token.objects.get(user_id=u_id)
	if u_token.remaining_tokens <= 0:
		resp = {"status":"success",
		"result": ["Token Supply Used Up"]}
		return HttpResponse(json.dumps(resp), content_type="json")
	
	u_token.remaining_tokens -= 3
	u_token.save()

	if (mode=="Facebook Ad"):
		prompt = FACEBOOK_PRIMER + name + "// " + text + "]"
		settings = {
			"max_tokens": FB_MAX_TOKENS,
			"temp": FB_TEMP,
			"stop": FB_STOP,
			"top_p": FB_TOP_P,
			"pres_penalty": FB_PRES_PEN,
			"freq_penalty": FB_FREQ_PEN,
			"n": FB_N
		}
	elif (mode=="Google Ad"):
		prompt = GOOGLE_AD_PRIMER + name + "// " + text + "]"
		settings = {
			"max_tokens": GGL_MAX_TOKENS,
			"temp": GGL_TEMP,
			"stop": GGL_STOP,
			"top_p": GGL_TOP_P,
			"pres_penalty": GGL_PRES_PEN,
			"freq_penalty": GGL_FREQ_PEN,
			"n": GGL_N
		}
	elif (mode=="Blog Idea"):
		prompt = BLOG_IDEA_PRIMER + text + "]"
		settings = {
			"max_tokens": BIDEA_MAX_TOKENS,
			"temp": BIDEA_TEMP,
			"stop": BIDEA_STOP,
			"top_p": BIDEA_TOP_P,
			"pres_penalty": BIDEA_PRES_PEN,
			"freq_penalty": BIDEA_FREQ_PEN,
			"n": BIDEA_N
		}
	elif (mode=="Blog Intro"):
		prompt = BLOG_INTRO_PRIMER + text + "]"
		settings = {
			"max_tokens": BINTR_MAX_TOKENS,
			"temp": BINTR_TEMP,
			"stop": BINTR_STOP,
			"top_p": BINTR_TOP_P,
			"pres_penalty": BINTR_PRES_PEN,
			"freq_penalty": BINTR_FREQ_PEN,
			"n": BINTR_N
		}
	else:
		prompt = DESCRIPTION_PRIMER + name + " // " + text + "]"
		settings = {
			"max_tokens": DESCR_MAX_TOKENS,
			"temp": DESCR_TEMP,
			"stop": DESCR_STOP,
			"top_p": DESCR_TOP_P,
			"pres_penalty": DESCR_PRES_PEN,
			"freq_penalty": DESCR_FREQ_PEN,
			"n": DESCR_N
		}

	print(f"prompt in BACKEND:\n" + prompt)

	gpt3_results = gpt3_call(prompt, settings, u_id)

	result_array = []
	for i in range(len(gpt3_results)):
		tmp_arr = gpt3_results[i].split("\n")
		result_array = result_array + tmp_arr

	# 1st checks for emptiness then removes "1.", "2.", "AI: "
	print(result_array)
	final_array = list(filter(lambda x: len(x) > 3, result_array))
	print(final_array)
	final_array = list(map(lambda y: split_check(y, mode), final_array))
	print(final_array)

	final_array = list(filter(lambda  x: x != "--", final_array))
	if (gpt3_results == []):
		resp = {"status":"failure",
	"result": gpt3_results}
	else:
		resp = {"status":"success",
	"result": final_array}
	return HttpResponse(json.dumps(resp), content_type="json")

@api_view(["POST"]) 
@permission_classes([IsAuthenticated])
def query_json_focusgroup(request):

	data = request.data 
	u_id = data["id"]
	name = data["name"]
	text = data["text"]
	question = data["question"]
	mode = data["response_mode"]

	u_token = Token.objects.get(user_id=u_id)
	if u_token.remaining_tokens <= 0:
		resp = {"status":"success",
		"result": ["Token Supply Used Up"]}
		return HttpResponse(json.dumps(resp), content_type="json")

	if (mode=="answer"):
		prompt = ANSWER_PRIMER + name + " // " + text + "]\n" + "Question: " + question
		settings = {
			"max_tokens": ANSWER_MAX_TOKENS,
			"temp": ANSWER_TEMP,
			"stop": ANSWER_STOP,
			"top_p": ANSWER_TOP_P,
			"pres_penalty": ANSWER_PRES_PEN,
			"freq_penalty": ANSWER_FREQ_PEN,
			"n": ANSWER_N
		}
		u_token.remaining_tokens -= 1
		u_token.save()
	elif (mode=="elaboration"):
		prompt = ELABORATE_PRIMER + name + " // " + text + "]\n" + "Question: " + question
		settings = {
			"max_tokens": ELABORATE_MAX_TOKENS,
			"temp": ELABORATE_TEMP,
			"stop": ELABORATE_STOP,
			"top_p": ELABORATE_TOP_P,
			"pres_penalty": ELABORATE_PRES_PEN,
			"freq_penalty": ELABORATE_FREQ_PEN,
			"n": ELABORATE_N
		}
		u_token.remaining_tokens -= 1
		u_token.save()
	else:
		prompt = QUESTION_PRIMER + name + " // " + text + "]"
		settings = {
			"max_tokens":  QUESTIONS_MAX_TOKENS,
			"temp": QUESTIONS_TEMP,
			"stop": QUESTIONS_STOP,
			"top_p": QUESTIONS_TOP_P,
			"pres_penalty": QUESTIONS_PRES_PEN,
			"freq_penalty": QUESTIONS_FREQ_PEN,
			"n": QUESTIONS_N
		}
		u_token.remaining_tokens -= 3
		u_token.save()

	print(f"prompt in BACKEND:\n" + prompt)

	gpt3_results = gpt3_call(prompt, settings, u_id)

	result_array = []
	for i in range(len(gpt3_results)):
		tmp_arr = gpt3_results[i].split("\n")
		result_array = result_array + tmp_arr

	# 1st checks for emptiness then removes "1.", "2.", "AI: "
	print(result_array)
	final_array = list(filter(lambda x: len(x) > 3, result_array))
	print(final_array)
	final_array = list(map(lambda y: split_check(y, mode), final_array))
	print(final_array)

	final_array = list(filter(lambda  x: x != "--", final_array))

	if (gpt3_results == []):
		resp = {"status":"failure",
	"result": gpt3_results}
	else:
		resp = {"status":"success",
	"result": final_array}
	return HttpResponse(json.dumps(resp), content_type="json")

@api_view(["POST"]) 
def img_filter(request):

	print("DONT CALL!")

	data = request.data

	print(data["mode"])
	print(data["mode"] == "default")
	if (data["mode"] == "default"):
		with open('/home/christoph/Desktop/scoords.json', "r") as f:
			kset = json.loads(f.read())
	else:
		with open('/home/christoph/Desktop/scoords_crazy.json', "r") as f:
			kset = json.loads(f.read())

	results = kset

	if (results == []):
		resp = {"status":"failure",
	"result": results}
	else:
		resp = {"status":"success",
	"result": results}
	return HttpResponse(json.dumps(resp), content_type="json")

@api_view(["POST"]) 
def img_similarity(request):

	data = request.data
	img = data["file"]

	print(data["file"])

	path = default_storage.save('xxx.jpg', ContentFile(img.read()))
	tmp_file = os.path.join(settings.MEDIA_ROOT, path)

	feats = extract_features(tmp_file, model)

	print(feats.shape)

	with open('/home/christoph/Desktop/86feats.npy', 'rb') as f:
		references = np.load(f, allow_pickle=True)

	d = dict(enumerate(references.flatten(), 1))

	with open('/home/christoph/Desktop/scoords.json', "r") as f:
		kset = json.loads(f.read())

	dis = []
	for i in range(55):
		distance = np.linalg.norm(feats - d[1][i])
		dis.append(distance)
		print(str(i) + ": " + str(distance))

	min_idx = {}
	for i in range(5):
		orig_mins = min(dis)
		new_idx = dis.index(orig_mins)
		min_idx[new_idx] = kset[str(new_idx)]
		dis[new_idx] = 99999

	print(min_idx)

	results = min_idx

	if (results == []):
		resp = {"status":"failure",
	"result": results}
	else:
		resp = {"status":"success",
	"result": results}
	return HttpResponse(json.dumps(resp), content_type="json")

