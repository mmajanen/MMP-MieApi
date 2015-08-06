import mieServerConfig as mConf
import os
from mupif import *
import logging
logger = logging.getLogger()

# required firewall settings (on ubuntu):
# for computer running daemon (this script)
# sudo iptables -A INPUT -p tcp -d 0/0 -s 0/0 --dport 44361 -j ACCEPT
# for computer running a nameserver
# sudo iptables -A INPUT -p tcp -d 0/0 -s 0/0 --dport 9090 -j ACCEPT


#locate nameserver
ns = PyroUtil.connectNameServer(nshost=mConf.nshost, nsport=mConf.nsport, hkey=mConf.hkey)

#Run a daemon for jobMamager on this machine
daemon = PyroUtil.runDaemon(host=mConf.daemonHost, port=mConf.jobManPort, nathost=mConf.nathost, natport=mConf.jobManNatport)
#Run job manager on a server
jobMan = JobManager.SimpleJobManager2(daemon, ns, mConf.applicationClass, mConf.jobManName, mConf.jobManPortsForJobs, mConf.jobManWorkDir, os.getcwd(), 'mieServerConfig', mConf.jobMan2CmdPath, mConf.jobManMaxJobs, mConf.jobManSocket)

#set up daemon with JobManager
uri = daemon.register(jobMan)
#register JobManager to nameServer
ns.register(mConf.jobManName, uri)
logger.debug ("Daemon for JobManager runs at " + str(uri))
print 80*'-'
print ("Started "+mConf.jobManName)
#waits for requests
daemon.requestLoop()
