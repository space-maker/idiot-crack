#!/usr/bin/python
# *-* coding: utf8 *-*

import pycurl
from StringIO import StringIO
from urllib import urlencode

class Sendform:
    """
    Senform:
    Classe qui gère l'envoie et la réception de données en utilisant la
    librairie Pycurl via des requêtes HTTP de type POST seulement
    """
    def __init__(self, url):
        self._buffer = StringIO()
        
        self._c = pycurl.Curl()
        self._c.setopt(self._c.URL, url)
        self._c.setopt(self._c.WRITEDATA, self._buffer)
        

    def send_data(self, data_list, is_encode = False):
        self._c.setopt(self._c.POSTFIELDS, urlencode(data_list) if not is_encode else data_list)
        self._c.perform()
    
    def get_response(self):
        return self._buffer.getvalue()


if __name__ == '__main__':
    print("Set of test\n")

    send = Sendform("http://192.168.0.3/ms.dev-mohamed/index.php5?fuseaction=secure.act_form_login&lang=fr")
    send.send_data({'frm_login': 'admin', 'frm_password': 'admin'})
    print(send.get_response())
