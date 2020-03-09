from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.context_processors import csrf
# Create your views here.
from django.http import HttpResponse
from django.views.generic import TemplateView
import speech_recognition as sr
import wikipedia
import codecs
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from gtts import gTTS
from playsound import playsound
from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from nltk.corpus import words
import nltk
import re
from QuestionAnswering.QA_Model.interact import GetEvidence
from QuestionAnswering.prepare_content import prepare_content_QA
import time
from django_ajax.decorators import ajax
import os
nltk.download('words')
r=sr.Recognizer()
imp_words=""
answer=""
wh_q_list=['when','where','whose','which','who','whom','why','how','in','on','is','was','are','will','can']
def contact(request):
    return render(request,'contact.html',context=None)
def documentation(request):
    return render(request,'Documentation.html',context=None)
def about(request):
    return render(request,'About.html',context=None)
def details(request):
    one_paragraph=""
    c={}
    c.update(csrf(request))
    source=request.POST.get('Que')
    source=source.lower()
    print(source)
    corpus=[]
    #stopWords = set(stopwords.words("english"))
    refrences=[]#list of referenced links
    start_timer=time.time()
    try:
        sq = wikipedia.search(source,results=3)
        c.update({'title':source})
        corpus.append(source)
        for i,j in enumerate(sq):
            print(i,wikipedia.page(j).url)
            tokenize_page_words = (wikipedia.page(j).content).replace('=','') 
            imp_words=' '.join([word for word in tokenize_page_words.split()])
            #corpus.append(wikipedia.summary(j))
            corpus.append(imp_words)
            refrences.append(wikipedia.page(j).url) 
        refrences= list(dict.fromkeys(refrences))
        c.update({'refrences':refrences})
        one_paragraph=prepare_content_QA(corpus)
        first_word=source.split()[0]
        first_word=first_word.lower()
        if(first_word not in wh_q_list):
            answer=wikipedia.summary(source,sentences=1)
        else:
            answer = GetEvidence(one_paragraph,source)
        c.update({'data1':answer})
        myobj = gTTS(text=answer, lang='en', slow=False)
        myobj.save("answer.mp3")
        print("Answer:",answer)
        end_timer=time.time()
        c.update({'ti':format(round(end_timer - start_timer,2))})
        print('Total Time: {:.4f}s'.format(end_timer - start_timer)) 
        return render(request,'details.html',c)    
    except:# (ValueError,TypeError,ConnectionError,ConnectionAbortedError,Exception)
        print('in exception block')
        c.update({'exceptions':'Error'})
        return render(request,"details.html",c)
class HomePageView(TemplateView):
    def get(self,request,**kwargs):  
        return render(request,'index.html',context=None)
@ajax
def getwords(request):
    word_list = words.words()
    return {'result':word_list}
   
@ajax
def playsnd(request):
    playsound('answer.mp3')
    flag="ok"
    return {'result':flag}
@ajax
def openmic(request):
    with sr.Microphone() as source:
        print("Listening...")
        audio=r.listen(source)  
    try:
        print("Asked:"+r.recognize_google(audio))
    except (sr.WaitTimeoutError,sr.UnknownValueError,sr.RequestError):
        er='NO'
        return {'result':er}
    que=r.recognize_google(audio)
    return {'result': que}

