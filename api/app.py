# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python
import re
import time
from flask import Flask, request, Response
from flask_cors import CORS
import json

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

app = Flask(__name__)
CORS(app)
request_methods = ["POST"]


api_key = os.getenv("YOUTUBE_API_KEY")

def search_video(request_data):
    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=api_key)

    request = youtube.search().list(
        part="snippet",
        maxResults=25,
        q=request_data['search']
    )
    data = request.execute()

    videos_data = []
    for video in data['items']:
        if video['id'] and 'videoId' in video['id']:
            video_url = 'https://www.youtube.com/watch?v=' + video['id']['videoId']
            video_title = video['snippet']['title']
            video_description = video['snippet']['description']
            video_thumbnails = video['snippet']['thumbnails']['medium']['url']
            
            video_info = {
                'video_title': video_title,
                'video_description': video_description,
                'video_url': video_url,
                'video_thumbnails': video_thumbnails
            }
    
            videos_data.append(video_info)

    result_list = {
        "status": 1, "result": videos_data
    }

    print(result_list)
            
    return result_list

@app.route('/searchvideo', methods=['POST'])
def getreport():
    try:
        request_data = request.json
        result = search_video(request_data)
        # request_data = request.json
        return Response(json.dumps(result), mimetype="application/json")
    except Exception as e:
        return Response(json.dumps({"status": 0, "error_msg": str(e)}), mimetype='application/json'), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3000,debug=True)