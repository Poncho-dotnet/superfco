from urllib import request, parse
import ssl

# url = "https://si3.bcentral.cl/Siete/ES/Siete/Cuadro/CAP_TIPO_CAMBIO/MN_TIPO_CAMBIO4/TCB_510_PARIDADES/TCB_510?cbFechaDiaria=2020&cbFrecuencia=DAILY&cbCalculo=NONE&cbFechaBase="
# contents = urllib.request.urlopen(url).read()

# https://stackoverflow.com/questions/36484184/python-make-a-post-request-using-python-3-urllib
# https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
# url = "https://www.bolsadesantiago.com/api/RV_ResumenMercado/getAccionesPrecios"

context = ssl._create_unverified_context()
# data = parse.urlencode({}).encode()
# req =  request.Request(url, data=data) # this will make the method "POST"
# contents = request.urlopen(req, context=context).read()

# url = "https://www.bolsadesantiago.com/acciones_precios"
# contents = request.urlopen(url, context=context).read()

url = "https://www.bolsadesantiago.com/api/Securities/csrfToken"
contents = request.urlopen(url, context=context).read()

text_file = open("test.html", "wb")
text_file.write(contents)
text_file.close()
