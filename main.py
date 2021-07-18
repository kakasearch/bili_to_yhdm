#查询数据库拿到bv
#用bv拿到视频截图
#调用番剧搜索

import requests
from pymongo import MongoClient
import re,os
import queryAni
from Mp4info import Mp4info

def handle_fiddle(fidder_headers):
	headers = {}
	for item in fidder_headers.split("\n"):
		if ': ' in item:
			[k,v] = item.split(': ')
			if k !=  "Content-Length: ":  #去除Content-Length
				headers[k] = v

# ffmpeg -i http://cdnvideo.chengjiao.stdu.edu.cn/cemsvideo/wl224/ziyuan/0407.mp4 -f image2 -ss 60 -vframes 1 shoutcut.png
def get_img(bv:str):
#获取视频链接
#获取截图、
	parse_url = "https://api.leduotv.com/wp-api/ifr.php?vid=https://www.bilibili.com/video/"+bv
	headers = handle_fiddle("""
		Host: api.leduotv.com
		Connection: keep-alive
		Cache-Control: max-age=0
		sec-ch-ua: "Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"
		sec-ch-ua-mobile: ?0
		Upgrade-Insecure-Requests: 1
		User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36
		Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
		Sec-Fetch-Site: none
		Sec-Fetch-Mode: navigate
		Sec-Fetch-User: ?1
		Sec-Fetch-Dest: document
		Accept-Encoding: gzip, deflate, br
		Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
		If-Modified-Since: Sun, 18 Jul 2021 05:00:00 GMT
		""")
	r = requests.get(parse_url,headers=headers)
	url = "https://api.leduotv.com" +re.findall(r"url='(.*)'",r.text)[0]
	r = requests.get(url,headers=headers)
	url = re.findall(r'"url": "(.*)"',r.text)[0] #真正的地址
		# Mp4info(video_url).get_duration()
	for i in range(3):
		name = "out%s.jpg"%i
	if os.path.exists(name): 
		os.remove(name) 
		os.system("ffmpeg -i \"%s\" -f image2 -ss %s -vframes 1 name"%(url,i*10+10,name))

conn = MongoClient("localhost",27017)
db = conn.bili2yh
notfound =db.notfound
done = db.done
while True:
	data = notfound.find_one()
	if data:
		#查询
		bv = data["bv"]
		yname = data["yname"]
		img = get_img(bv)
		names = []
		for i in range(3):
			name = "out%s.jpg"%i
			if os.path.exists(name): 
				names.append(queryAni.get_ani_name_by_img(open(name,'br')))
		if len(set([i[0] for i in names])) == 1:
			#多张图查到的结果相同
			#存入
			notfound.delete_one(data)
			if not done.find_one({"yname":yname}):
				done.insert_one({"yname":yname,"name":names[0][0]})
	else:
		print('查询完毕')
		break



