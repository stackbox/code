import web

urls=('/.*',"hello")


class hello:
    def GET(self):
		return 'hello world'


app = web.application(urls,globals())