#截图查询番剧
#用于B站到樱花查询

import requests
import opencc

def handle_fiddle(fidder_headers):
	headers = {}
	for item in fidder_headers.split("\n"):
		if ': ' in item:
			[k,v] = item.split(': ')
			if k !=  "Content-Length: ":  #去除Content-Length
				headers[k] = v
	return headers
def get_zh_name(ani_id):
	"""
	通过截图搜索结果查询对应的番剧名字，返回中文简体的名字
	"""
	headers= handle_fiddle("""
	POST https://trace.moe/anilist HTTP/1.1
	Host: trace.moe
	Connection: keep-alive
	Content-Length: 1395
	sec-ch-ua: "Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"
	sec-ch-ua-mobile: ?0
	User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36
	Content-Type: application/json
	Accept: */*
	Origin: https://trace.moe
	Sec-Fetch-Site: same-origin
	Sec-Fetch-Mode: cors
	Sec-Fetch-Dest: empty
	Referer: https://trace.moe/
	Accept-Encoding: gzip, deflate, br
	Accept-Language: zh-CN,zh;q=0.9,en;q=0.8""")

	data = {"query":"query ($ids: [Int]) {\n Page(page: 1, perPage: 50) {\n media(id_in: $ids, type: ANIME) {\n id\n title {\n native\n romaji\n english\n }\n }\n }\n }\n ",
	"variables":{"ids":[ani_id]}}
	r=requests.post("https://trace.moe/anilist",headers=headers, json=data,verify=False)
	name = r.json()["data"]["Page"]["media"][0]["title"]["chinese"]
	cc = opencc.OpenCC('t2s')
	return cc.convert(name.split(' ')[0])




def get_ani_name_by_img(img_b):
	"""
	img 为二进制对象 open(,'rb')或者其他
	"""
	fidder_headers = """
	POST https://api.trace.moe/search?cutBorders& HTTP/1.1
	Host: api.trace.moe
	Connection: keep-alive
	Content-Length: 66864
	sec-ch-ua: "Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"
	sec-ch-ua-mobile: ?0
	User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36
	Accept: */*
	Origin: https://trace.moe
	Sec-Fetch-Site: same-site
	Sec-Fetch-Mode: cors
	Sec-Fetch-Dest: empty
	Referer: https://trace.moe/
	Accept-Encoding: gzip, deflate, br
	Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
	"""
	headers = handle_fiddle(fidder_headers)
	files = {'image': ("blob", img_b,"image/jpeg")}
	r=requests.post("https://api.trace.moe/search?cutBorders&",headers=headers, files=files,verify=False)
	result = r.json()["result"][0]
	if result:
		ani_id = result["anilist"]
		similarity = result["similarity"]
		print(ani_id)
		name = get_zh_name(ani_id)
		return (name,similarity)
	else:
		print(r.json()["error"])
		return False


if __name__ == "__main__":
	result =  get_ani_name_by_img(open('d:/desktop/out.jpg','br'))
	if result:
		print('查询的结果为： ',result[0])
		print("相似度: ",result[1])