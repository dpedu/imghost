import cherrypy
import logging
import os
import cgi
import tempfile
import subprocess
from shutil import copyfile

class Mountable(object):
    """
    Macro for encapsulating a component's config and methods into one object.
    :param conf: cherrypy config dict for use when mounting this component
    """
    def __init__(self, conf=None):
        self.conf = conf if conf else {'/': {}}

    def mount(self, path):
        """
        Mount this component into the cherrypy tree
        :param path: where to mount it e.g. /v1
        :return: self
        """
        cherrypy.tree.mount(self, path, self.conf)
        return self


class tempFileStorage(cgi.FieldStorage):
    def make_file(self, binary=None):
        return tempfile.NamedTemporaryFile()


def noBodyProcess():
    cherrypy.request.process_request_body = False

cherrypy.tools.noBodyProcess = cherrypy.Tool('before_request_body', noBodyProcess)


type2ext = {
    "image/png": "png",
    "image/jpg": "jpg",
    "image/gif": "gif"
}


class ImgHostApiV1(Mountable):

    @cherrypy.expose
    @cherrypy.tools.noBodyProcess()
    def upload(self, theFile=None):

        # convert the header keys to lower case
        lcHDRS = {}
        for key, val in cherrypy.request.headers.items():
            lcHDRS[key.lower()] = val

        if int(lcHDRS['content-length']) > 10**7:
            raise Exception("File size max of 10MB exceeded")

        formFields = tempFileStorage(fp=cherrypy.request.rfile,
                                     headers=lcHDRS,
                                     environ={'REQUEST_METHOD': 'POST'},
                                     keep_blank_values=True)

        theFile = formFields['theFile']

        # os.link(theFile.file.name, '/tmp/' + theFile.filename)
        try:
            ext = type2ext[str(theFile.type)]
        except KeyError:
            raise Exception("File type not allowed")

        sha = subprocess.check_output(["sha512sum", theFile.file.name])
        sha = sha.decode("UTF-8").split(" ")[0]
        imgpath = os.path.join("i", "{}.{}".format(sha[0:8], ext))
        copyfile(theFile.file.name, os.path.join("ui", imgpath))
        cherrypy.response.headers['Location'] = "/" + imgpath
        cherrypy.response.status = 302


class ImgHostApi(object):
    def __init__(self):

        ui_path = os.path.join(os.getcwd(), 'ui')
        self.ui = Mountable(conf={'/': {
                                  'tools.staticdir.on': True,
                                  'tools.staticdir.dir': ui_path,
                                  'tools.staticdir.index': 'index.html'
                                  }}).mount('/')

        self.app_v1 = ImgHostApiV1(conf={'/': {'tools.proxy.on': True,
                                               }}).mount('/api/v1')

        cherrypy.config.update({
            'sessionFilter.on': False,
            'tools.sessions.on': False,
            'tools.sessions.locking': 'explicit',
            # 'tools.sessions.timeout': 525600,
            'request.show_tracebacks': True,
            'server.socket_port': 3000,  # TODO configurable port
            'server.thread_pool': 25,
            'server.socket_host': '0.0.0.0',
            'server.socket_timeout': 5,
            'log.screen': False,
            'engine.autoreload.on': False,

        })

    def run(self):
        cherrypy.engine.start()
        cherrypy.engine.block()
        logging.info("API has shut down")

    def stop(self):
        cherrypy.engine.exit()
        logging.info("API shutting down...")


def main():
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)-15s %(levelname)-8s %(name)s %(filename)s:%(lineno)d %(message)s")

    api = ImgHostApi()
    api.run()
