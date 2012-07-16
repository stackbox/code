# coding: utf-8
import web

urls=('/.*',"hello")


class hello:
    def GET(self):
		web.header('Content-Type','text/html')
		return 'hello world 03091154 吕思佳'


app = web.application(urls,globals())