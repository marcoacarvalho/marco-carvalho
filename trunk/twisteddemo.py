import os.path as path
import pprint

import twisted.internet.reactor as reactor
import twisted.web.resource as resource
import twisted.web.server as server

class Info(resource.Resource):
    isLeaf = True
    def render(self, request):
        request.setHeader('Content-Type', 'text/plain; charset=utf-8')
        request.setHeader('Cache-Control', 'no-cache')
        request.setHeader('Pragma', 'no-cache')
        request.setHeader('Expires', '0')

        res = []

        res.append(('request', request))
        res.append(('request.site', request.site))
        res.append(('request.site.protocol', request.site.protocol))
        res.append(('request.getSession()', request.getSession()))
        res.append(('len(request.getSession().__dict__)', len(request.getSession().__dict__)))
        res.append(('request type', type(request)))
        res.append(('request class', request.__class__))
        res.append(('request.method', request.method))
        res.append(('request.uri', request.uri))
        res.append(('request.path', request.path))
        res.append(('request.prepath', request.prepath))
        res.append(('request.postpath', request.postpath))
        res.append(('request.getHost()', list(request.getHost())))
        res.append(('request.prePathURL()', request.prePathURL()))
        res.append(('request.args', request.args))
        res.append(('request.transport', request.transport))
        res.append(('request.transport.hostname', request.transport.hostname))
        res.append(('request.transport.protocol', request.transport.protocol))
        res.append(('request.transport.reactor', request.transport.reactor))
        res.append(('request.transport.getPeer()', list(request.transport.getPeer())))
        res.append(('request.transport.getHost()', list(request.transport.getHost())))
        res.append(('request.transport.getHandle()', request.transport.getHandle()))
        res.append(('request.transport.server', request.transport.server))
        res.append(('request.transport.server.socket', request.transport.server.socket))
        res.append(('request.transport.server.socketType', request.transport.server.socketType))
        res.append(('request.transport.server.port', request.transport.server.port))
        res.append(('request.getAllHeaders()', request.getAllHeaders()))
        res.append(('request.content.getvalue()', request.content.getvalue()))

        return '\n'.join(['---> ' + i[0] + ': ' + pprint.pformat(i[1]) for i in res])

class RootResource(resource.Resource):
        def render(self, request):
                request.redirect('/info')
                return ''
        def getChild(self, path, request):
                if not path:
                        return self
                return resource.Resource.getChild(self, path, request)

# unleash

site = server.Site(RootResource())
site.resource.putChild('info', Info())

port = 8090

if __name__ == '__main__':
    reactor.listenTCP(port, site)
    reactor.run()
