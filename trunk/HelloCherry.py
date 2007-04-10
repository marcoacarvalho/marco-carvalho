import cherrypy

class HelloWorld:
    def index(self):
        return "Hello world!"
    index.exposed = True

cherrypy.root = HelloWorld()
cherrypy.server.start()

