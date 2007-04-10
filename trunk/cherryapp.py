import webbrowser
import threading
import cherrypy

MainPage = """\
<html>
<head>
<title>An example application</title>
</head>
<body>
<h1>This is my sample application</h1>
Put the content here...
<hr>
<a href="/exit">Quit</a>
</body>
</html>
"""

FinishPage = """\
<html>
<head>
<title>System Terminated</title>
</head>
<body>
<H1 align="center">System Terminated</h1>
</body>
</html>
"""

class MyApp:
    """ Sample request handler class. """

    def index(self):
        return MainPage

    index.exposed = True

    def exit(self):
        threading.Timer(1, cherrypy.server.stop).start()
        return FinishPage

    exit.exposed = True

cherrypy.root = MyApp()
threading.Timer(1, webbrowser.open, ("http://127.0.0.1:8080",)).start()
cherrypy.server.start()
