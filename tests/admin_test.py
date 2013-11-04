import random
import glob
import socket

from net.grinder.script import Test
from net.grinder.script.Grinder import grinder
from net.grinder.plugin.http import HTTPRequest
from string import Template

from javax.net.ssl import SSLSocketFactory
from javax.net.ssl import SSLSocket
from java.net import InetSocketAddress

from lib import variables

cert_dir="/Users/andreaceccanti/git/test-ca/igi-test-ca/certs"

# A shorter alias for the grinder.logger.info() method.
log = grinder.logger.info

HOST="wilco.cnaf.infn.it"
PORT=15000
RESOURCE="/generate-ac"

KEYSTORE_PASSWORD="pass123"
KEY_PASSWORD="pass"

KEYSTORE_FILENAME_PATTERN="%s/load*.ks" % cert_dir
CERT_FILENAME_PATTERN="%s/load*.cert.pem" % cert_dir
KEY_FILENAME_PATTERN="%s/load*.key.pem" % cert_dir

KEYSTORES=glob.glob(KEYSTORE_FILENAME_PATTERN)
CERTS=glob.glob(CERT_FILENAME_PATTERN)
KEYS=glob.glob(KEY_FILENAME_PATTERN)

VOMS_REQUEST_TEMPLATE= Template('''0<?xml version="1.0" encoding="US-ASCII"?><voms><command>G/${vo}</command><base64>1</base64><version>4</version><lifetime>43200</lifetime></voms>''')


def get_random_certificate():
    index=random.randrange(len(CERTS))
    return (KEYSTORES[index], CERTS[index], KEYS[index])
        
class TestRunner:
    
    def __call__(self):    
        
        (ks,cert,key) = get_random_certificate()
        log("Cert: %s" % ks)
        grinder.SSLControl.setKeyStoreFile(ks,KEYSTORE_PASSWORD)
        
        test  = Test(1, "Admin legacy connector request")
        req = HTTPRequest()
        test.record(req)
                         
        url="https://"+HOST+":"+str(PORT)+"/generate-ac"
         
        req.GET(url)
         
        req2= HTTPRequest()
        test2 = Test(2, "Admin 8443 connector request")
        test2.record(req2)
         
        url2="https://"+HOST+":8443/voms/mysql/generate-ac"
        req2.GET(url2)
        
        legacy = LegacyVOMSRequestResponse(HOST,PORT,"mysql")
        test3 = Test(3, "Admin legacy request")
        test3.record(legacy)
        
        output = legacy()
        log("legacy response: %s" % output)


class LegacyVOMSRequestResponse:
    def __init__(self, host, port, vo):
        self._host = host
        self._port = port
        self._vo = vo
            
            
    def _parse_response(self, sock):
        
        full_msg = ''
        while True:
            c = sock.getInputStream().read()
            if c == -1:
                break
            full_msg += unichr(c)
        
        return full_msg
        
    def __call__(self):
        xml_msg = VOMS_REQUEST_TEMPLATE.substitute({'vo': self._vo})
        f = grinder.SSLControl.getSSLContext().getSocketFactory()
        s = f.createSocket()
        
        log("socket: %s" % s)
        address = InetSocketAddress(self._host, self._port)
        s.connect(address)
        
        s.getOutputStream().write(xml_msg)
        s.getOutputStream().flush()
        
        response = self._parse_response(s)
        return response
        
        
            
        log("out: %s" % full_msg)
        s.close()
        
         
        