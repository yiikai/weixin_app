#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, request, url_for,render_template
import hashlib
app = Flask(__name__)
app.debug = True 
app.config['SECRET_KEY'] = 'This is a screat, who konws I want fuck her'
#weixin verify arg which set by user self
token = 'healthggg_2017'
weixin_appid = "wx518a4fbd804999aa"
weixin_secret = "aDYOKllNkmYnNbZkCEBCezcBw4V1okHCSJ0zrkXLH8U"
import threading
import urllib
import urllib2
import json
access_token = ''
use_time = 0
def get_accesstoken(appid,secret):
	url = 'https://api.weixin.qq.com/cgi-bin/token?' + 'grant_type=client_credential' + '&appid=' + appid + '&secret=' + secret
	req = urllib2.urlopen(url).read()
	text = json.loads(req)		
	global access_token 
	access_token = text['access_token']
	global use_time 
	use_time = text['expires_in']
	print access_token,use_time	

#get_accesstoken(weixin_appid,weixin_secret)

import xml.etree.ElementTree as ET
import weixininterface.weixinInterface as wf
from DBhandler.mysqlhandler import *
import sys
import json
#reload(sys)
#sys.setdefaultencoding('utf-8')

@app.route('/menu')
def caipu():
	titlename = request.args.get('titlename')
	dbhandler = mysqlhandler("Menu","127.0.0.1","root")
	data = dbhandler.execute("select title_img,ingredient,steps from Shipu where title like '%s'" % (titlename)).first()
	dbhandler.disconnect()
	picurl = "resource/"+data[0]
	ingredient = json.loads(data[1])
	steps = json.loads(data[2])
	return render_template('index.html',title=titlename,pic=picurl,ingred=ingredient,step=steps)


weixinObj = wf.wxIF() 
@app.route('/',methods=["GET","POST"])
def weixin_verify():
	if request.method == "GET":
		signature = request.args.get('signature', '')
		timestamp = request.args.get('timestamp', '')
	        nonce = request.args.get('nonce', '')
		echostr = request.args.get('echostr', '')
		s = ''.join(sorted([timestamp, nonce, token]))
		sha1 = hashlib.sha1()
		sha1.update(s)
		if sha1.hexdigest() == signature:
	            return echostr
	elif request.method == "POST":
		root = ET.fromstring(request.data)
		for event in root.iter('Event'):
			if event.text == "subscribe":
				return weixinObj.wx_describe(root)
			else:
				return ""
		for content in root.iter('Content'):
			inputText = content.text
			dbhandler = mysqlhandler("Menu","127.0.0.1","root")
			#data = dbhandler.execute("select title,title_img,ingredient,steps from Shipu where title like '%%%s%%'" % (inputText)).first()
			data = dbhandler.execute("select title,title_img,ingredient,steps from Shipu where title like '%%%s%%' limit 0,4" % (inputText)).fetchall()
			if len(data) == 0:
				print "XXXXXXXXXXXXXXXXXXXXXXXX",len(data)
				dbhandler.disconnect()
				return weixinObj.wx_text_response(root,"没有想要的菜谱哟！！！！")
			#获取成分信息和标题组织成文字信息
			#titlepicurl = "http://106.14.199.53/resource/" + data[1]
			#titlename = data[0]
			#ingrd = data[2]
			#dataurl = "http://106.14.199.53"+ url_for('caipu',titlename=titlename)#titlename=titlename,picurl=titlepicurl,ingredient="dji")
			#dbhandler.disconnect()
			#return weixinObj.wx_pictext_response(root,titlename,titlepicurl,dataurl)
			datainfo = []
			for i in data:
				titlepicurl = "http://106.14.199.53/resource/" + i[1]
				titlename = i[0]
				ingrd = i[2]
				dataurl = "http://106.14.199.53"+ url_for('caipu',titlename=titlename)
				d = {"titlename":titlename,"titlepicurl":titlepicurl,"dataurl":dataurl}
				datainfo.append(d)
			dbhandler.disconnect()
			return weixinObj.wx_pictext_nums_response(root,datainfo)

									
				
if __name__ == '__main__':
	app.run()
