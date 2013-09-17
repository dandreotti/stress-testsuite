 
import random

from net.grinder.script import Test
from net.grinder.script.Grinder import grinder
from net.grinder.plugin.http import HTTPRequest

from lib import variables

 
list_vo=variables.vo_map;
vo_keys=sorted(list_vo.keys())
host=variables.voms_host

resource="/generate-ac"

#request = HTTPRequest()

class TestRunner:
    def __call__(self):

	grinder.SSLControl.setKeyStoreFile("mykeystore.jks", "123456")


	for index in range(len(vo_keys)):
		#vo = random.choice(list_vo.keys())
		vo = vo_keys[index]
		test = Test(index, "VOMS AC for VO "+vo)
	        request = HTTPRequest()
		test.record(request)
		port=list_vo[vo]
		url="https://"+host+":"+str(port)+resource
		
		grinder.statistics.delayReports = 1

        	result = str(request.GET(url))

		if not '200 OK' in result:		
			grinder.statistics.forLastTest.success = 0
			grinder.statistics.report()

		grinder.statistics.delayReports = 0
