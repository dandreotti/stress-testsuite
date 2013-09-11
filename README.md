stress-testsuite
================


##Setup
================


Download [The Grinder](http://sourceforge.net/projects/grinder/) and unzip it wherever you prefer.
Scripts for environment settings are provided. Change file "setupEnv.sh" accordingly with your installation.  
For more information see [this documentation page](http://grinder.sourceforge.net/g3/getting-started.html#howtostart).

##VOMS script requirements
================

The file "grinder.properties" is set to use the script "vomstest.py", which requires the creation of a keystore to work properly.
Create a keystore to store your credentials (PKCS12 format is used in this example): 

    keytool -importkeystore -srckeystore &lt;cert.p12> -srcstoretype PKCS12 -destkeystore mykeystore.jks -srcstorepass &lt;password> -deststorepass &lt;password>


<b>Note:</b> for ease of use the same password should be set for both the keystore and the private key and it must be at least 6 characters long.


##VOMS Execution
================

In order to start the console and the agent run the following commands: 

    ./runConsole.sh
    ./runAgent.sh

Then execute the test from the console. Please see [this link](http://grinder.sourceforge.net/g3/console.html).
