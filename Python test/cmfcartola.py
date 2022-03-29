from urllib import request, parse
import ssl

# # https://stackoverflow.com/questions/4476373/simple-url-get-post-function-in-python
# url = "http://www.cmfchile.cl/institucional/estadisticas/cfm_download.php"
# payload = {"txt_inicio": "31/07/2020", "txt_termino": "31/07/2020", "ffmm": "%", "captcha": "v1vxlr"}

# # POST with form-encoded data
# #req = request.Request(url, data=payload)
# data = parse.urlencode(payload).encode()
# contents = request.urlopen(url, data=data).read()

# # Response, status etc
# text_file = open("test.html", "wb")
# text_file.write(contents)
# text_file.close()


url = "http://www.cmfchile.cl/institucional/estadisticas/fondos_cartola_diaria.php"
contents = request.urlopen(url).read()

# Response, status etc
text_file = open("test.html", "wb")
text_file.write(contents)
text_file.close()

# url = "http://www.cmfchile.cl/sitio/biblioteca/captcha2/captcha.php"
# url = "http://www.cmfchile.cl//sitio/biblioteca/captcha/newsession.php"
# payload = {"accion": "valida", "valor": "v1vxlr"}

# # # POST with form-encoded data
# # #req = request.Request(url, data=payload)
# data = parse.urlencode({}).encode()
# contents = request.urlopen(url, data=data).read()

# # Response, status etc
# text_file = open("test.html", "wb")
# text_file.write(contents)
# text_file.close()

# url = "https://postman-echo.com/post"
# payload = {"accion": "valida", "valor": "v1vxlr"}

# # POST with form-encoded data
# #req = request.Request(url, data=payload)
# data = parse.urlencode(payload).encode()
# contents = request.urlopen(url, data=data).read()

# # Response, status etc
# text_file = open("test.html", "wb")
# text_file.write(contents)
# text_file.close()

