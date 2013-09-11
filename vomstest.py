 
from net.grinder.script import Test
from net.grinder.script.Grinder import grinder
from net.grinder.plugin.http import HTTPRequest
 
test = Test(1, "Request VOMS AC")
request = HTTPRequest()
test.record(request)

class TestRunner:
    def __call__(self):
        grinder.SSLControl.setKeyStoreFile("mykeystore.jks", "123456")        
        test.record(request)
        result = request.GET("https://emitestbed07.cnaf.infn.it:15002/generate-ac")



