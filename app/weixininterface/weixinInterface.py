# -*- coding: utf-8 -*-
import time
#importxml.etree.ElementTree as ET

guideline = "欢迎关注健康出味 \n\
	     输入关键字: \n\
	     1.输入任意关键字查看相关菜谱"


class wxIF(object):
	def __init__(self):
		pass
	
	def wx_describe(self,xmlroot):
		for username in xmlroot.iter('FromUserName'):
			self._userid = username.text
		for server in xmlroot.iter('ToUserName'):
			self._serverid = server.text
		global guideline
		rsp = self.__make_text_response(guideline)
		return rsp	

	def wx_text_response(self,xmlroot,text):
		for username in xmlroot.iter('FromUserName'):
			self._userid = username.text
		for server in xmlroot.iter('ToUserName'):
			self._serverid = server.text
 		rsp = self.__make_text_response(text)
		return rsp

	def wx_pictext_response(self,xmlroot,titletext,titlepicurl,dataurl):
		for username in xmlroot.iter('FromUserName'):
			self._userid = username.text
		for server in xmlroot.iter('ToUserName'):
			self._serverid = server.text
 		rsp = self.__make_pictext_response(titletext,titlepicurl,dataurl)
		return rsp

	#可以返回多条图文信息接口
	#datainfo数组成员:{titlename:,titlepicurl:,dataurl:}
	def wx_pictext_nums_response(self,xmlroot,datainfo):
		for username in xmlroot.iter('FromUserName'):
			self._userid = username.text
		for server in xmlroot.iter("ToUserName"):
			self._serverid = server.text
		rsp = self.__make_pictext_nums_response(datainfo)
		return rsp			

	def __make_pictext_nums_response(self,datainfo):
		count = len(datainfo)
		pictextdata = '<xml>\
                                <ToUserName><![CDATA[%s]]></ToUserName>\
                                <FromUserName><![CDATA[%s]]></FromUserName>\
                                <CreateTime>%d</CreateTime>\
                                <MsgType><![CDATA[news]]></MsgType>\
                                <ArticleCount>%d</ArticleCount>\
				<Articles>'%(self._userid,self._serverid,int(time.time()),count)
		for i in datainfo:
			article = '<item>\
                                <Title><![CDATA[%s]]></Title>\
                                <Description><![CDATA[%s]]></Description>\
                                <PicUrl><![CDATA[%s]]></PicUrl>\
                                <Url><![CDATA[%s]]></Url>\
                                </item>'%(i['titlename'],"推荐菜".decode('utf-8'),i['titlepicurl'],i['dataurl'])
			pictextdata = pictextdata + article
		pictextdata = pictextdata + '</xml>'
		print "--------------------------------------"
		print pictextdata.encode('utf-8')
		print "======================================"
		return pictextdata
	
	def __make_pictext_response(self,titletext,titlepicurl,dataurl):
		pictextdata = '<xml>\
				<ToUserName><![CDATA[%s]]></ToUserName>\
				<FromUserName><![CDATA[%s]]></FromUserName>\
				<CreateTime>%d</CreateTime>\
				<MsgType><![CDATA[news]]></MsgType>\
				<ArticleCount>1</ArticleCount>\
				<Articles>\
				<item>\
				<Title><![CDATA[%s]]></Title>\
				<Description><![CDATA[%s]]></Description>\
				<PicUrl><![CDATA[%s]]></PicUrl>\
				<Url><![CDATA[%s]]></Url>\
				</item>\
				</Articles>\
				</xml>' % (self._userid,self._serverid,int(time.time()),titletext,"推荐菜".decode('utf-8'),titlepicurl,dataurl)
		print "--------------------------------------"
		print pictextdata.encode('utf-8')
		print "======================================"
		return pictextdata
	
	def __make_text_response(self,text):
		textdata = '<xml>\
			<ToUserName><![CDATA[%s]]></ToUserName>\
			<FromUserName><![CDATA[%s]]></FromUserName>\
			<CreateTime>%d</CreateTime>\
			<MsgType><![CDATA[text]]></MsgType>\
			<Content><![CDATA[%s]]></Content>\
			</xml>' % (self._userid,self._serverid,int(time.time()),text)
		return textdata
	
	def __make_picture_response(self):
		pass
	
	def find_key_word(self,keyword):
		pass	
		
