from wsgiref.simple_server import make_server
from cgi import parse_qs, escape
import Bot

def application(environ, start_response):

    d = parse_qs(environ['QUERY_STRING'])
    query = d.get('query', [''])[0]
    query = escape(query)
    reply = Bot.response(query)
    dc = {"reply": reply}
    response_body = str(dc)
    
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(response_body)))
    ]
    start_response(status, response_headers)
    return [response_body.encode("utf-8")]

httpd = make_server('localhost', 9090, application)
httpd.serve_forever()