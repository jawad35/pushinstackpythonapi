from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import re

from .models import Task
# Python program to check the
# loading time of the website

# Importing the libraries
from urllib.request import urlopen
from time import time

from urllib.parse import urljoin
import requests
import whois
# For internet speed
import speedtest
# getting keywords
# from googlesearch import search
import pandas as pd
# from Utilities.Services.GetTopWebsites import *
from django.http import HttpResponse

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/task-list/',
        'Detail View': '/task-detail/<str:pk>/',
        'Create': '/task-create/',
        'Update': '/task-update/<str:pk>/',
        'Delete': '/task-delete/<str:pk>/',
    }

    return Response(api_urls)
@api_view(['POST'])
def GetWebPageSourceCode(request):
    try:
        url = request.data['url']
        page = requests.get(url)
        soup = bs(page.content, "html.parser")
        sourceCode = soup.prettify()
        HtmlData = {
            "Success": True,
            "Data": {
                "SourceCode": sourceCode
            },
        }
        return Response(HtmlData)
    except Exception as e:
        HtmlData = {
            "Success": False,
        }
        return Response(HtmlData)


@api_view(['POST'])
def GetExtractedEmails(request):
    try:
        text = request.data['text']
        emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text)
        myemaillist = list(dict.fromkeys(emails))  # Remove duplicates
        InternetData = {
            "Success": True,
            "Data": {
                "ExtractedEmails": myemaillist
            },
        }
        return Response(InternetData)
    except Exception as e:
        InternetData = {
            "Success": False,
        }
        return Response(InternetData)


@api_view(['POST'])
def GetTopKeywords(request):
    try:
        text = request.data['text']
        df = get_links_from_google(text, 1)
        df["text"] = df["url"].apply(lambda x: get_page_content(x))
        df["text"] = df["text"].apply(text_cleaning)
        text = "".join(df["text"].to_list())
        topics_rank = get_top_n_keyphrases(text=text, top_n=29)
        print(topics_rank)
        InternetData = {
            "Success": True,
            "Data": {
                "TopWebsites": df["url"],
                "TopKeywords": topics_rank
            },
        }
        return Response(InternetData)
    except Exception as e:
        InternetData = {
            "Success": False,
        }
        return Response(InternetData)


@api_view(['GET'])
def TestMyInternetSpeed(request):
    try:
        wifi = speedtest.Speedtest()
        wifi.get_best_server()
        ping = wifi.results.ping
        downloadspeed = round(wifi.download() / 1000 / 1000, 1)
        uploadspeed = round(wifi.upload() / 1000 / 1000, 1)
        InternetData = {
            "Success": True,
            "Download": downloadspeed,
            "Upload": uploadspeed,
            "Ping": ping
        }
        return Response(InternetData)
    except Exception as e:
        InternetData = {
            "Success": False,
        }
        return Response(InternetData)


@api_view(['GET'])
def taskList(request):
    tasks = Task.objects.all().order_by('-id')
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def taskDetail(request, pk):
    tasks = Task.objects.get(id=pk)
    serializer = TaskSerializer(tasks, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def getTextCount(request):
    try:
        text = request.data['text']
        text_without_spaces = "".join(text.split())
        spaces = 0
        for i in text:
            if (i.isspace()):
                spaces += 1
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            print(serializer.data)
        letters = str(len(text_without_spaces))
        words = len(text.split())
        WebPagedata = {
            "Success": True,
            "Letters": letters,
            "Words": words,
            "Spaces": spaces
        }
        return Response({"TextCountData": WebPagedata})
    except Exception as e:
        WebPagedata = {
            "Success": False,
            "ErrorMsg": "You are not allowed to test this website"
        }
        return Response({"TextCountData": WebPagedata})


@api_view(['POST'])
def getAllWebPageImages(request):
    try:
        url = request.data['url']
        session = requests.Session()
        # set the User-agent as a regular browser
        session.headers[
            "User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
        # get the HTML content
        html = session.get(url).content
        soup = bs(html, "html.parser")
        images_files = []
        for css in soup.find_all("img"):
            if css.attrs.get("src"):
                css_url = urljoin(url, css.attrs.get("src"))
                images_files.append(css_url)
                serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            print(serializer.data)
        WebPagedata = {"Success": True, "AllImages": images_files}
        return Response({"WabPageData": WebPagedata})
    except Exception as e:
        WebPagedata = {
            "Success": False,
            "ErrorMsg": "You are not allowed to test this website"
        }
        return Response({"WabPageData": WebPagedata})


@api_view(['POST'])
def getDomainInfo(request):
    try:
        url = request.data['url']
        res = whois.whois(url)
        WebPagedata = {"Access": True, "domain": res}
        return Response({"WebPageData": WebPagedata})
    except Exception as e:
        print(e, 'err23')
        WebPagedata = {
            "Access": False,
            "ErrorMsg": "You are not allowed to test this website"
        }
        return Response({"WebPageData": WebPagedata})


@api_view(['POST'])
def getWebLoad(request):
    try:
        url = request.data['url']
        # initialize a session
        session = requests.Session()
        # set the User-agent as a regular browser
        session.headers[
            "User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
        # get the HTML content
        html = session.get(url).content
        soup = bs(html, "html.parser")
        # get the CSS files
        css_files = []

        for css in soup.find_all("link"):
            if css.attrs.get("href"):
                css_url = urljoin(url, css.attrs.get("href"))
                css_files.append(css_url)

        #Get Javascript files
        script_files = []
        for script in soup.find_all("script"):
            if script.attrs.get("src"):
                script_url = urljoin(url, script.attrs.get("src"))
                script_files.append(script_url)

        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            print(serializer.data)
        website = urlopen(url)
        open_time = time()
        output = website.read()
        close_time = time()
        website.close()
        WebPagedata = {
            "LoadTime": round(close_time - open_time, 3),
            "ScriptFilesUrls": script_files,
            "CssFilesUrls": css_files,
            "SearchUrl": url,
            "Access": True
        }
        # print(output)
        # print('The loading time of website is',round(close_time-open_time,3),'seconds')
        return Response({"WebPageData": WebPagedata})
    except Exception as e:
        WebPagedata = {
            "Access": False,
            "ErrorMsg": "You are not allowed to test this website"
        }
        return Response({"WebPageData": WebPagedata})


session = HTMLSession()


@api_view(['POST'])
def getYoutubeTags(request):

    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        # serializer.save()
        print(serializer.data)

    tasks = {}
    res = session.get(request.data['url'])
    soup = bs(res.text, "html.parser")
    tasks["tags"] = ', '.join([
        meta.attrs.get("content")
        for meta in soup.find_all("meta", {"property": "og:video:tag"})
    ])
    return Response({"data": tasks})


@api_view(['POST'])
def taskCreate(request):
    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def taskUpdate(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(instance=task, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def taskDelete(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()

    return Response('Item succsesfully delete!')
