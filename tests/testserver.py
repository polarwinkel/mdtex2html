#!/usr/bin/python3
#coding: utf-8
'''
Testserver for mdtex2html
'''

from http.server import BaseHTTPRequestHandler, HTTPServer
from cgi import parse_header, parse_multipart
from multiprocessing import Process

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import mdtex2html

# global settings:

webServerPort = 8001

# Testing-Page:
page = '''
<!doctype html>
<html>
    <head>
        <title>Testserver for mdtex2html</title>
        <style>
            .tooltip .tooltiptext {
                display: none;
            }
            .tooltip:hover .tooltiptext {
                display: inline;
                border-radius: 0.3em;
                background-color: #777;
                position: fixed;
            }
        </style>
    </head>
    <body>
        <h1>Testserver for <code>mdtex2html</code></h1>
        <h2><code>mdtex</code>-Code</h2>
        <textarea oninput="render()" id="mdtexCode" rows="5" cols="72"></textarea><br />
        <button onclick="render()">type or click to render the code</button>
        <h2>Rendering</h2>
        <div id="mathmlView" style="border:1px solid silver;"></div>
        <h2>Rendered Code</h2>
        <textarea id="renderedCode" rows="5" cols="72">
        </textarea><br />
        <script>
            function mdtex2html(mdtex) {
                var xhr = new XMLHttpRequest();
                xhr.open("POST", "mdtex2html", false);
                xhr.setRequestHeader("Content-Type", "application/mdtex");
                xhr.send(mdtex);
                return xhr.responseText;
            }
            function render() {
                mdtex = document.getElementById("mdtexCode").value;
                html = mdtex2html(mdtex);
                document.getElementById("mathmlView").innerHTML = html;
                document.getElementById("renderedCode").value = html;
            }
        </script>
    </body>
</html>
'''

# WebServer stuff:

class HTTPServer_RequestHandler(BaseHTTPRequestHandler):
    ''' HTTPRequestHandler class '''
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
    def do_HEAD(s):
        self._set_headers;
    
    def do_GET(self):
        ''' The GET-Handler returns the testing-page '''
        self._set_headers()
        self.wfile.write(bytes(page, 'utf8'))
        return
    
    def parse_POST(self):
        ''' get the post data from the request '''
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'application/mdtex':
            length = int(self.headers['content-length'])
            postvars = self.rfile.read(length).decode('utf-8')
        else:
            postvars = {}
        return postvars
    
    def do_POST(self):
        ''' the rendering request is expected as POST-request '''
        self._set_headers()
        postvars = self.parse_POST()
        if self.path == '/mdtex2html':
            try:
                result = mdtex2html.convert(postvars, extensions=['tables', 'def_list', 'fenced_code', 'tables', 'admonition', 'nl2br', 'sane_lists', 'toc'])
            except Exception as e:
                result = 'ERROR: Could not convert the mdTeX to HTML:' + str(e)
        self.wfile.write(bytes(result, "utf8"))
        return

def runWebServer():
    ''' start the webserver '''
    print('starting server')
    server_address = ('127.0.0.1', webServerPort)
    httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
    print('server is running on port ' + str(webServerPort))
    httpd.serve_forever()

# get it started:

webServer = Process(target=runWebServer, args=())
webServer.start()
