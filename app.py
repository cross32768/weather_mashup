# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for
from requests_oauthlib import OAuth1Session
from datetime import datetime, timedelta
import requests
import json
import config
import re
import pytz

app = Flask(__name__)


# 与えられた都市についてlivedoor天気情報のapi, weatherhacksに問い合わせて天気予報とその発表時間の現在時刻からの差を出力する関数
# 入力は県名ではなく都市名のstringで、戻り値は予報発表時刻の現在時刻からの差を[h,m,s]という形式で表すリストとstringの端的な天気情報の2つ
def weatherhacksapi(cityname):
    tempf = open('cityid.json', 'r')
    cityid_dict = json.load(tempf)
    if cityname not in cityid_dict:
        return [0,0,0], False
    
    cityid = cityid_dict[cityname]

    baseURL_weatherhacks = 'http://weather.livedoor.com/forecast/webservice/json/v1'
    resp = requests.get(baseURL_weatherhacks + '?city=' + cityid)
    
    resp_json = resp.json()
    time = resp_json['description']['publicTime']
    forecast = resp_json['forecasts'][0]['telop']
    
    time_sp = list(map(int, re.split('[-T:+]', time)))
    time_datetime = datetime(time_sp[0], time_sp[1], time_sp[2], time_sp[3], time_sp[4], 0, tzinfo=pytz.timezone('Asia/Tokyo'))
    delta = datetime.now(pytz.timezone('Asia/Tokyo')) - time_datetime
    delta_list = [0,0,0]
    if 'day' not in str(delta):
        delta_list = list(map(float, str(delta).split(':')))
    else:
        forecast = False
    
    return delta_list, forecast


# 与えられた都市について天気に関連したツイートをtiwtterから検索してきてそのツイート時間の現在時刻からの差と本文を返す関数
# 入力は県名ではなく都市名のstring,　及び何時間何分前までのツイートを探してくるかをそれぞれintで指定、
# 戻り値は[[h,m,s], 'tweet本文']という形のリスト
def twitterapi(cityname, hours_for_since=5, minutes_for_since=0):
    CK = config.CONSUMER_KEY
    CS = config.CONSUMER_SECRET
    AT = config.ACCESS_TOKEN
    ATS = config.ACCESS_SECRET
    api_twitter = OAuth1Session(CK, CS, AT, ATS)
    
    if hours_for_since + minutes_for_since / 60 > 24:
        raise ValueError('時間指定は24時間以内にしてください')
    
    since = datetime.now(pytz.timezone('Asia/Tokyo')) - timedelta(hours = hours_for_since, minutes = minutes_for_since)
    since_list = re.split('[ :]', str(since))
    since_for_query = since_list[0] + '_' + since_list[1] + ':' + since_list[2] + ':' + '00_JST'
    
    search_url = "https://api.twitter.com/1.1/search/tweets.json"
    params = {'q' : cityname + ' AND 天気' + ' -rt -bot', 
              'count' : 20,
              'locate' : 'ja',
              'since' : since_for_query,
              'result_type' : 'recent'}

    req = api_twitter.get(search_url, params = params)
    if req.status_code == 200:
        result = []
        tweets = json.loads(req.text)['statuses']
        for tweet in tweets:
            text = tweet['text']
            
            created_at = tweet['created_at']
            c_at = re.split('[ :+]', created_at)
            c_at_datetime = datetime(int(c_at[8]), int(str(datetime.now()).split('-')[1]), 
                                     int(c_at[2]), int(c_at[3]), int(c_at[4]), int(c_at[5]), 0, tzinfo=pytz.timezone('Asia/Tokyo'))
            delta = datetime.now(pytz.timezone('Asia/Tokyo')) - c_at_datetime - timedelta(hours=9, minutes=20)
            if 'day' not in str(delta):
                delta_list = list(map(float, str(delta).split(':')))
                if not text.startswith('@'):
                    result.append([delta_list, text])
        return result
    else:
        raise NotImplementedError('結果の取得に失敗しました')

# [h,m,s]形式の時間をいい感じのstringに直す
def timetostring(time):
    result = ''
    if int(time[0]) !=0:
        result += (str(int(time[0]))) + '時間'
    result += (str(int(time[1]))) + '分前'
    return result

# Routing
@app.route('/')
def index():
    title = "Weather information cite"
    message = "都市名を入力してエンターを押してください"
    
    return render_template('index.html',
                           message=message, title=title)

@app.route('/post', methods=['POST', 'GET'])
def post():
    if request.method == 'POST':
        title = "Weather information cite"
        message = "都市名を入力してエンターを押してください"
        cityname = request.form.getlist('city')[0]
        delta_list, forecast = weatherhacksapi(cityname)
        delta_string = timetostring(delta_list)
        result_twitter = twitterapi(cityname)
        for i in range(len(result_twitter)):
            result_twitter[i][0] = timetostring(result_twitter[i][0])
        return render_template('index.html', title=title,
                               cityname=cityname, message=message, 
                               delta_string=delta_string, forecast=forecast,
                               result_twitter=result_twitter)
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
