#!/usr/bin/python
#-*- coding:latin-1 -*-
import sys,os
try:
    import pygtk
    pygtk.require('2.0')
    import gtk, gobject
    import gtk.glade
    import urllib2
    import threading
except:
    print "Não foram encontrados os módulos necessários"
    sys.exit(1)
        
class appWindow:
    def __init__(self):
        gtk.gdk.threads_init()
        appPath=os.path.dirname(os.path.abspath(__file__))+ "/"
        self.widgetTree = gtk.glade.XML(appPath+'job_down.glade')
        self.window = self.widgetTree.get_widget('form')
        self.fileUrl="http://www.nacaolivre.org/disco/enviados/trabalho.pdf"
        self.localFilename="Trabalho_pacotes_baixado.pdf"
        self.fim=0
        
        if (self.window):
            self.window.connect('destroy', gtk.main_quit)

        self.txtaddr = self.widgetTree.get_widget('txtaddr')
        self.txtport = self.widgetTree.get_widget('txtport')
        self.txtuser = self.widgetTree.get_widget('txtuser')
        self.txtpass = self.widgetTree.get_widget('txtpass')
        self.status = self.widgetTree.get_widget('label10')
        self.file1 = self.widgetTree.get_widget('filechooser')
        self.pb1 = self.widgetTree.get_widget('pb1')
        self.widgetTree.signal_autoconnect(self)
        
        self.window.show_all()
        gtk.gdk.threads_leave()
        self.downloader=clsDownload()
        self.file1.set_filename(os.environ['HOME'])
        self.destPath=os.environ['HOME']
        self.pb1.hide()
        if self.destPath[-1:]!="/":
            self.destPath+="/"
    def set_status(self,text,ttw=5):
        time_to_wait=ttw
        self.status.set_label(text)
        idTimeout = gobject.timeout_add(time_to_wait*1000, lambda: self.status.set_label(""))
            
    def pulsar(self):
        idTimeout = gobject.timeout_add(100, lambda: self.pb1.pulse())
        if(self.fim==0):
            idTimeout = gobject.timeout_add(100, lambda: self.pulsar())
        else:
            self.pb1.set_fraction(1.0)
            self.pb1.set_fraction(0.0)
    def threaded(f):
        def wrapper(*args):
            t = threading.Thread(target=f, args=args)
            t.start()
        return wrapper
    @threaded
    def baixarUrl(self):
        self.status.set_label("<b><span foreground=\"#016600\">Baixando trabalho...</span></b>")
        gtk.gdk.threads_init()
        self.pulsar()
        gtk.gdk.threads_leave()
        try:
            pagina = self.downloader.download(self.fileUrl)
        except:
            self.status.set_label("<b><span foreground=\"red\">Erro ao baixar. Verifique proxy ou conexão</span></b>")
        self.codigo = pagina.read()
        pagina.close()
        self.set_status("<b><span foreground=\"#016600\">O arquivo foi baixado com sucesso!</span></b>")
        self.fim=1
        gtk.gdk.threads_init()
        self.set_status("<b><span foreground=\"#016600\">Salvando...</span></b>",10)
        hwnd=open(self.destPath+self.localFilename,"w")
        hwnd.write(self.codigo)
        hwnd.close()
        self.pb1.hide()
        self.status.set_label("<b><span foreground=\"#016600\">Salvo com sucesso em \"%s\"</span></b>"%(self.destPath))
        gtk.gdk.threads_leave()
        self.status.set_label("<b><span foreground=\"#016600\">Salvo com sucesso em \"%s\"</span></b>"%(self.destPath))
    def checkProxyFields(self):
        a1=self.txtaddr.get_text()
        a2=self.txtport.get_text()
        a3=self.txtuser.get_text()
        a4=self.txtpass.get_text()
        if (len(a1) > 0 ) and (len(a2) > 0):
            if (len(a3) > 0 ) and (len(a4) > 0):
                self.set_status("<b><span foreground=\"blue\">Preenchimento de autenticação OK!</span></b>")
                self.downloader.setProxy(a1,a2,a3,a4)
            elif (len(a3) > 0 ) or (len(a4) > 0):
                self.set_status("<b><span foreground=\"red\">Preencha usuario e senha!</span></b>")
            elif (len(a3) == 0 ) and (len(a4) == 0):
                self.set_status("<b><span foreground=\"#016600\">OK, proxy sem autenticação!</span></b>")
                self.downloader.setProxy(a1,a2)
        elif (len(a1) > 0 ) or (len(a2) > 0):
            self.set_status("<b><span foreground=\"red\">Preencha IP do host e porta!</span></b>")
        elif (len(a1) == 0 ) and (len(a2) == 0):
            self.set_status("<b><span foreground=\"#016600\">OK, sem proxy !</span></b>")
            self.downloader.unsetProxy()
            
    # Callbacks ---------------------------------------------------------------
    def on_form_destroy(self, widget):
        print "Tchau!"

    def on_txtaddr_changed(self, widget):
        self.checkProxyFields()

    def on_txtport_changed(self, widget):
        self.checkProxyFields()

    def on_txtuser_changed(self, widget):
        self.checkProxyFields()

    def on_txtpass_changed(self, widget):
        self.checkProxyFields()

    def on_filechooser_selection_changed(self, widget):
        self.destPath=widget.get_filename()
        if self.destPath[-1:]!="/":
            self.destPath+="/"

    def on_cmd1_clicked(self, widget):
        self.pb1.show_all()
        self.baixarUrl()
    # Auxiliary Methods -------------------------------------------------------

class clsDownload:
    def __init__(self):
        self.proxyed=0
        pass
    def setProxy(self,addr,port,user=None,passwd=None):
        if (user==None) and (passwd==None):
            proxy_support = urllib2.ProxyHandler({"http" : "http://"+addr+":"+port})
        elif  (user!=None) and (passwd!=None):
            proxy_support = urllib2.ProxyHandler({"http" : "http://"+user+":"+passwd+"@"+addr+":"+port})
                
        opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        self.proxyed=1
    def unsetProxy(self):
        opener = urllib2.build_opener()
        urllib2.install_opener(opener)
        self.proxyed=0
    def download(self,url):
        self.downloader=urllib2.urlopen(url)
        return self.downloader
        
if __name__ == '__main__':
    app = appWindow()
    gtk.main()
