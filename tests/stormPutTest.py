import subprocess
import os
import tempfile
import re

from net.grinder.script import Test
from net.grinder.script.Grinder import grinder


### custom properties settings  ###

props=grinder.properties

storm_endpoint=props.get('grinder.storm.endpoint')
storm_SA=props.get('grinder.storm.sa')


### Prepare to Put and Put Done commands  ###

base_command=" -e " + storm_endpoint + " -s srm://" + storm_endpoint + "/srm/managerv2?SFN=/" + storm_SA + "/"

PTP_COMMAND="clientSRM ptp -p" + base_command
PD_COMMAND="clientSRM pd" + base_command


### patterns for token and failure matching

pattern_token = r'(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})'
pattern_error = r'(SRM_FAILURE)'


### pre-compiled regular expression objects

regex_token = re.compile(pattern_token, flags=re.MULTILINE)
regex_error = re.compile(pattern_error, flags=re.MULTILINE)


test = Test(1, "Put request")


class srmRequest:

### Return stdout and stderr for the executed command ###

    def runSrmRequest(self,cmd):
       p = subprocess.Popen([cmd, ''], shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
       (out,err)=p.communicate()

       return (out,err)


### Return the matched expression or None otherwise  ###

class TestRunner:

    def findMatch(self,regex,data):

	res=None
        m = regex.search(data)
	if(m):
		res=m.group()

	return res


### Execute a ptp and in case of success a pd  ###

    def __call__(self):

	file_name = os.path.basename(tempfile.mkstemp()[1])

 	cmd=PTP_COMMAND + file_name
	
	obj=srmRequest()
	test.record(obj)

	grinder.statistics.delayReports = 1

	out,err = obj.runSrmRequest(cmd)
	
	grinder.logger.info(out)

	result=self.findMatch(regex_error,out)

	if result == "SRM_FAILURE":		
		grinder.statistics.forLastTest.success = 0
		grinder.statistics.report()
	else:
		token=self.findMatch(regex_token,out)
		cmd=PD_COMMAND + file_name + " -t " + token

		out,err = obj.runSrmRequest(cmd)
		grinder.logger.info(out)
		result=self.findMatch(regex_error,out)

		if result == "SRM_FAILURE":
			grinder.statistics.forLastTest.success = 0
                	grinder.statistics.report()


	grinder.statistics.delayReports = 0
