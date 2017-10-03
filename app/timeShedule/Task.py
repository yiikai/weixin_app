import time
from celery import Celery,platforms
import urllib
import urllib2
platforms.C_FORCE_ROOT = True

celery = Celery('Task',broker='redis://localhost:6379/0')

#weixin access token schedule timer
#https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140183 reference args
@celery.task
def get_Accesstoken(appid,secret):
	url = 'https://api.weixin.qq.com/cgi-bin/token?' + 'grant_type=client_credential' + '&appid=' + appid + '&secret=' + secret
	print 'url is ' , url
	req = urllib2.urlopen(url)
	return req.read()
	
	
