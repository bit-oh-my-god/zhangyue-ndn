#!/home/tara/anaconda3/bin/python
import argparse
import os
import sys
import time
import re
import jsonpickle
import subprocess
import mpl_toolkits.axisartist as AA
from matplotlib.colors import cnames
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
#======
# environment settings
global_root = os.path.dirname(os.path.realpath(__file__))
global_ndnpath = '/home/tara/ndnSIM'
global_runtime_link_path1 = global_ndnpath + '/ns-3/build/' #TODO
global_runtime_link_path2 = global_ndnpath + '/ns-3/build/src/ndnSIM/examples/'
global_log01ptah = '{0}/box/logs/log01'.format(global_root)
global_jsonpath = '{0}/box/json'.format(global_root)
global_waf = global_ndnpath + '/ns-3/waf'
global_wafflag01 = ' configure --enable-examples'
global_wafflag02 = ''
wafflag030 = ' --run=\"ndn-tara -errorrate=0.2 --strategy=Sarsa\"'
wafflag031 = ' --run=\"ndn-tree-tracers\"'
global global_wafflag03
global_wafflag03 = wafflag030
wafflag041 = 'nfd.Transport:ndn-cxx.ndn.TcpTransport:ndn-cxx.ndn.UnixTransport:ndn.NetDeviceTransport:nfd.InternalClientTransport:nfd.InternalForwarderTransport:'                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
wafflag042 = 'nfd.MulticastEthernetTransport=level_all:nfd.UnicastEthernetTransport=level_all:nfd.MulticastUdpTransport=level_all:nfd.UnicastUdpTransport=level_all:nfd.EthernetTransport=level_all:'
wafflag043 = 'ndn.NetDeviceTransport:PointToPointNetDevice:' ## transport and netdevice
wafflag044 = 'ErrorModel:' ## link error rate
wafflag045 = 'nfd.GenericLinkService:nfd.LinkService:' ## link service
wafflag046 = 'nfd.Forwarder:nfd.Strategy:' ## strategy & forwarder
wafflag047 = 'Ipv6PacketFilter:Ipv4PacketFilter:CoDelQueueDisc:FqCoDelQueueDisc:TrafficControlLayer:QueueDisc:' ## codel
wafflag048 = 'AnnotatedTopologyReader:' ## AnnotatedTopologyReader # parse_log need
wafflag049 = 'ndn.ConsumerCbrspkt:ndn.Producer:ndn.ConsumerCbr:ndn.Consumer:' # apps# parse_log need
wafflag050 ='ndn.L3RateTracer:' #tracer
wafflag051 ='nfd.TaraMeasurements:nfd.Tara2Measurements:' #probe and measurment
wafflag052 ='ndn.L3Protocol:' #l3
wafflag053 ='ndn.StrategyChoiceHelper:nfd.StrategyChoice:' #strategychoice
wafflag054 = 'nfd.Tara2Strategy:nfd.TaraStrategy:nfd.BestRouteStrategy2:nfd.AsfStrategy:nfd.MulticastStrategy:' # tarastrategy# parse_log need
wafflag055 = 'ndn.StackHelper:' # stackhelper #parse_log need
wafflag056 = 'ndn.GlobalRoutingHelper' # routinghelper
wafflag04444 = wafflag054 + wafflag049 + wafflag051 + wafflag048 + wafflag055
global_wafflag04 = 'NS_LOG={0} '.format(wafflag04444)
global_source = '/home/tara/ndnSIM/ns-3/src/ndnSIM/examples/ndn-tree-tracers.cc'
global_source1 = '/home/tara/ndnSIM/ns-3/src/ndnSIM/examples/ndn-zhangyue.cc'
global_drop_trace = global_ndnpath + '/ns-3/drop-trace.txt'
global_rate_trace = global_ndnpath + '/ns-3/rate-trace.txt'
#======
# util
# define handy func
def colored(color, strob):
    red = '\x1B[31m'
    reset = "\x1B[0m"
    green=   "\x1B[32m"
    blue= "\x1B[34m"
    yellow=   "\x1B[33m"
    if color == 'red' :
        return '{0}{1}{2}'.format(red, strob, reset)
    elif color == 'green' :
        return '{0}{1}{2}'.format(green, strob, reset)
    elif color == 'blue' :
        return '{0}{1}{2}'.format(blue, strob, reset)
    elif color == 'yellow' :
        return '{0}{1}{2}'.format(yellow, strob, reset)
    else :
        sys.exit('Error-021')
def save_this_jsonob_as(fullpathname, jsonob_to):
    serialized_json = jsonpickle.encode(jsonob_to)
    with open(fullpathname, "w") as text_file:
        #print >> text_file, serialized_json  # Python 2.x
        print(serialized_json, file=text_file)  # Python 3.x
def read_file_to_jsonob(filename) :
    with open(filename, "r") as file :
        lines = file.read()
        tmp_json_ob = jsonpickle.decode(lines)
        return tmp_json_ob
def nums(s):
    try:
        return int(s)
    except ValueError:
        return float(s)
def x_create_empty_file(path) :
    try :
        basedir = os.path.dirname(path)
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        os.mknod(path)
    except OSError:
        print("no file create")
def x_runbash() : # TODO
    my_env = os.environ.copy()
    #print(my_env)
    #print(my_env["LD_LIBRARY_PATH"])
    if 'LD_LIBRARY_PATH' in my_env:
        my_env["LD_LIBRARY_PATH"] = my_env["LD_LIBRARY_PATH"] + ':' +  global_runtime_link_path1 + ':' + global_runtime_link_path2
    else :
        my_env["LD_LIBRARY_PATH"] = global_runtime_link_path1 + ':' + global_runtime_link_path2
    os.chdir(os.path.dirname(global_waf))
    cmd = "/home/tara/ndnSIM/ns-3/build/src/ndnSIM/examples/ns3-dev-ndn-tree-tracers-debug >> {0}".format(global_log01ptah)
    print(cmd)
    p=subprocess.Popen(cmd, env=my_env,shell=True,stdout=subprocess.PIPE)
    out,err = p.communicate()
    for line in out.splitlines():  
       print(line)
def x_runwaf() :
    os.chdir(os.path.dirname(global_waf))
    print("waf is:" + global_waf)
    cmd0 = global_waf + global_wafflag01
    cmd1 = global_waf + global_wafflag02
    cmd2 = global_wafflag04 + global_waf + global_wafflag03 + ' > {0} 2>&1'.format(global_log01ptah)
    for cmd in [cmd0, cmd1, cmd2] :
        print(cmd)
        p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
        out,err = p.communicate()  
        #for line in out.splitlines():  
            #print(line)  
    # last line won't block, we sleep a while
    #time.sleep(20)
#=========================
#=================================
#=========================
# class define
#＝＝＝＝＝＝＝＝＝＝＝＝　start of  ParseRoutineHolder
#
#
#
#
#＝＝＝＝＝＝＝＝＝＝＝＝　start of  ParseRoutineHolder
class ParseRoutineHolder(object):
    def __init__(self):
        print('ParseRoutineHolder init')
        self.nodeid2facelistmap = {}
        self.linkpairmap = {}
        self.nodename2nodeid = {}
        self.nodeid2nodename = {}
        self.linkpair2speed = []
    def addlinkpair(self, local, remote) :
        self.linkpairmap[local] = remote
    def getlinkremoteof(self, local):
        return self.linkpairmap[local]
    def addfaceofnodeid(self,faceuri, nodeid) :
        if nodeid in self.nodeid2facelistmap :
            self.nodeid2facelistmap[nodeid].append(faceuri)
        else :
            self.nodeid2facelistmap[nodeid] = [faceuri]
    def faceuri2nodeid(self,id):
        # TODO assert it only have two non-zero
        for nodeid in self.nodeid2facelistmap :
            for faceid in self.nodeid2facelistmap[nodeid] :
                if id == faceid:
                    return nodeid
                else :
                    nothing = 0 # nothing
        return -1
    # @return [maxpkts, speed, delay]
    def getlinkspeedfromnodeidpair(self,nodeid,remotenodeid): 
        for p in self.linkpair2speed :
            if (p[0] == nodeid and p[1] == remotenodeid) or (p[0] == remotenodeid and p[1] == nodeid) :
                return p[2]
        print('can\'t find,{0}, {1}'.format(nodeid,remotenodeid))
        return None
    # @return [JSONOB_TOPOLOGY, [counter_consumeroutspkt, counter_consumerindata,counter_unsatisfy, spktpathrecord,counter_satisfy, delaymap, qvlistmap]]
    def Parse_log(self):
        log01_file = open(global_log01ptah, "r")
        lines = log01_file.readlines()
        log01_file.close()
        print('parse log as lines={0}'.format(len(lines)))
        regexlist= {}
        counter_consumeroutspkt = 0
        counter_consumerindata = 0
        counter_unsatisfy = 0
        counter_satisfy = 0
        spktpathrecord = {}
        qvlistmap = {}
        # [pkts : miliseconds-delay-sum]
        delaymap = [0, 0.0]
        #wafflag055
        #FUCK004[TaraTrace],Node 0: added Face as face #netdev://[00:00:00:00:00:01];remote is#netdev://[00:00:00:00:00:02]
        r1 = re.compile(r'''FUCK004\[TaraTrace\],Node\s(\d+\.*\d*)\:\sadded\sFace\sas\sface\s\#netdev:\/\/(\[[0-9]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2}\]);remote\sis\#netdev:\/\/(\[[0-9]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2}\])''', re.VERBOSE)
        regexlist["addface"] = r1
        # wafflag048
        #FUCK002[TaraTrace] add a node,leaf-3,2
        r2 = re.compile(r'''FUCK002\[TaraTrace\]\sadd\sa\snode,([a-z]{1,10}-?[0-9]*),(\d+\.*\d*)''', re.VERBOSE)
        regexlist["createnode"] = r2
        # wafflag048 
        #New link leaf-1 <==> rtr-1 / 10Mbps with 1 metric (1ms, 100, )
        r3 = re.compile(r'''New\slink\s([a-z]{1,10}-?[0-9]*)\s<==>\s([a-z]{1,10}-?[0-9]*)\s\/\s(\d+\.*\d*)Mbps\swith\s1\smetric\s\((\d+\.*\d*)ms,\s(\d+\.*\d*),\s\)''', re.VERBOSE)
        regexlist["createlink"] = r3
        # wafflag049
        #[DEBUG] FUCK421[TaraTrace] consumer on data;data-delay=0.13131;data.name=/root/leaf-1/%FE%01<fuckend>;
        r4 = re.compile(r'''\[DEBUG\]\sFUCK421\[TaraTrace\]\sconsumer\son\sdata;data-delay=(\d+\.*\d*);data\.name=(\/[a-z0-9\-]*\/[a-z0-9\-]*\/.*)\<fuckend\>''', re.VERBOSE)
        regexlist["consumerindata"] = r4
        # wafflag049
        #[DEBUG] FUCK103[TaraTrace]SPKT is send from consumer with ;interest.name=/root/leaf-1/%FE%1A<fuckend>;on nodeid=0
        r5 = re.compile(r'''\[DEBUG\]\sFUCK103\[TaraTrace\]SPKT\sis\ssend\sfrom\sconsumer\swith\s;interest\.name=(\/[a-z0-9\-]*\/[a-z0-9\-]*\/.*)\<fuckend\>;on\snodeid=([0-9]*)''', re.VERBOSE)
        regexlist["consumeroutspkt"] = r5
        # wafflag054
        #FUCK781[TaraTrace]beforeExpirePendingInterest pitEntry=
        r6 = re.compile(r'''FUCK781\[TaraTrace\]beforeExpirePendingInterest\spitEntry=''', re.VERBOSE)
        regexlist["forwardStrategyUnsatisfyIPKT"] = r6
        # wafflag054
        #FUCK721[TaraTrace]beforeSatisfyInterest
        r7 = re.compile(r'''FUCK721\[TaraTrace\]beforeSatisfyInterest''', re.VERBOSE)
        regexlist["beforesatisfy"] = r7
        # wafflag049
        #8 ndn.Producer:OnInterest(): [DEBUG] FUCK101[TaraTrace]SPKT is received on producer with ;prefix=/root;name=/root/leaf-3/%FE%01<fuckend>;
        r8 = re.compile(r'''([0-9]*)\sndn\.Producer:OnInterest\(\):\s\[DEBUG\]\sFUCK101\[TaraTrace\]SPKT\sis\sreceived\son\sproducer\swith\s;prefix=((\/[a-z0-9\-]*)*);name=(\/[a-z0-9\-]*\/[a-z0-9\-]*\/.*)\<fuckend\>;''', re.VERBOSE)
        regexlist["producerreceivespkt"] = r8
        #2 nfd.Tara2Strategy:beforeSatisfyInterest(): [DEBUG] FUCK831[TaraTrace]attach data with qv = -1.2149e+246
        r9 = re.compile(r'''([0-9]*)\snfd\.Tara2?Strategy\:beforeSatisfyInterest\(\)\:\s\[DEBUG\]\sFUCK831\[TaraTrace\]attach\sdata\swith\sqv\s=\s(\+?-?\d+\.*\d*e\+?-?[0-9]{0,12})''', re.VERBOSE)
        regexlist["qvindata"] = r9
        for line in lines :
            regexresult = {}
            for k in regexlist :
                regex = regexlist[k]
                regres = regex.search(line)
                if (regres) :
                    regexresult[k] = regres
                    break
            for k in regexresult:
                v = regexresult[k]
                if k == "addface" :
                    #print(line)
                    node = int(nums(v.group(1)))
                    localaddr = v.group(2)
                    remoteaddr = v.group(3)
                    self.addfaceofnodeid(localaddr,node)
                    self.addlinkpair(localaddr,remoteaddr)
                elif k == "createnode":
                    #print(line)
                    nodename = v.group(1)
                    node = int(nums(v.group(2)))
                    self.nodeid2nodename[node] = nodename
                    self.nodename2nodeid[nodename] = node
                elif k == "createlink":
                    #print(line)
                    nodename1 = v.group(1)
                    nodename2 = v.group(2)
                    speed = int(nums(v.group(3)))
                    delay = int(nums(v.group(4)))
                    maxpkt = int(nums(v.group(5)))
                    listob = [maxpkt, speed, delay]
                    self.linkpair2speed.append([self.nodename2nodeid[nodename1],self.nodename2nodeid[nodename2], listob])
                elif k == "consumerindata":
                    datadelay = float(nums(v.group(1)))
                    namespkt = v.group(2)
                    counter_consumerindata += 1
                    if namespkt not in spktpathrecord:
                        sys.exit("error-dghqfuck fuckyou!!! name={0}".format(namespkt))
                    else :
                        if "consumerInDataCounter=" in spktpathrecord[namespkt]:
                            sys.exit("error-dghqfuckasq fuckyou!!!")
                        else :
                            spktpathrecord[namespkt]["consumerInDataCounter="] = 1
                            delaymap[0] += 1
                            delaymap[1] += datadelay
                elif k == "consumeroutspkt":
                    namespkt = v.group(1)
                    counter_consumeroutspkt += 1
                    if namespkt not in spktpathrecord:
                        spktpathrecord[namespkt] = {}
                        spktpathrecord[namespkt]["consumerOutInterestCounter="] = 1
                    else :
                        #sys.exit("error-consumer retrans? fuckyou!!!")
                        nothing = 1
                elif k == "forwardStrategyUnsatisfyIPKT":
                    counter_unsatisfy += 1
                elif k == "producerreceivespkt":
                    namespkt = v.group(4)
                    if namespkt not in spktpathrecord:
                        sys.exit("error-dasdghqfuck fuckyou!!! name ={0}".format(namespkt))
                    else :
                        if "producerInInterest" in spktpathrecord[namespkt] :
                            #print("producer duplicate receive interest?:{0}".format(namespkt))
                            spktpathrecord[namespkt]["producerInInterest"] += 1
                        else :
                            spktpathrecord[namespkt]["producerInInterest"] = 1
                elif k == "beforesatisfy" :
                    counter_satisfy += 1
                elif k == "qvindata" :
                    nodeid = v.group(1)
                    qv = float(nums(v.group(2)))
                    print("parse one qv={0}".format(qv))
                    if nodeid not in qvlistmap :
                        qvlistmap[nodeid] = []
                    qvlistmap[nodeid].append(qv) 
                else :
                    nomeaning = 1 # not match regex, may be a nomeaning line
                    sys.exit("fuck-error sadwqnl")
        #
        nodelist = []
        linklist = []
        #print('[debug]{0}'.format(self.linkpair2speed))
        for nodeid in self.nodeid2facelistmap : 
            nodelist.append(NodeId(nodeid, self.nodeid2nodename[nodeid]))
        for nodeid in self.nodeid2facelistmap :
            for faceuri in self.nodeid2facelistmap[nodeid]:
                remoteuri = self.getlinkremoteof(faceuri)
                remotenodeid = self.faceuri2nodeid(remoteuri)
                reslist =self.getlinkspeedfromnodeidpair(nodeid,remotenodeid)
                assert(len(reslist)==3)
                linkob = Link(leftnode=NodeId(nodeid, self.nodeid2nodename[nodeid]), leftfaceuri=faceuri, rightnode=NodeId(remotenodeid, self.nodeid2nodename[remotenodeid]),rightfaceuri=remoteuri, maxpkts=reslist[0], speed=reslist[1], delay=reslist[2])
                linklist.append(linkob)
        return [
            JSONOB_TOPOLOGY(nodelist, linklist,self.nodename2nodeid,  self.nodeid2nodename),
            [counter_consumerindata,   #0
            counter_consumeroutspkt, 
            counter_unsatisfy, #2
            spktpathrecord,
            counter_satisfy,  #4
            delaymap,
            qvlistmap,], #6
               ]
    # @return dropmap is {int: [JSONOB_DROP]}
    def Parse_droptrace(self) :
        if self.nodeid2nodename == {} :
            sys.exit('Error-016, invoke Parse_log first')
        drop_trace_file = open(global_drop_trace, "r")
        lines = drop_trace_file.readlines()
        drop_trace_file.close()
        dropmap={}
        for line in lines :
            #0.5	leaf-1	combined	Drop	0	0	0	0
            r1 = re.compile(r'''(\d+\.*\d*)\t([a-z]{1,10}-?[0-9]*)\t
            combined\tDrop\t(\d+\.*\d*)\t(\d+\.*\d*)\t(\d+\.*\d*)\t(\d+\.*\d*)''', re.VERBOSE)
            onepkt_combined_drop = r1.search(line)
            #
            #r2
            if onepkt_combined_drop:
                #print(line)
                trace_time = int(nums(onepkt_combined_drop.group(1)))
                trace_node_name = onepkt_combined_drop.group(2)
                drop_pkts = int(nums(onepkt_combined_drop.group(3)))
                drop_bytes = int(nums(onepkt_combined_drop.group(4)))
                trace_node = self.nodename2nodeid[trace_node_name]
                jsonob_drop = JSONOB_DROP(trace_time, trace_node, drop_pkts, drop_bytes)
                nodeid = trace_node
                if nodeid in dropmap :
                    dropmap[nodeid].append(jsonob_drop)
                else :
                    dropmap[nodeid] = []
                    dropmap[nodeid].append(jsonob_drop)
            else :
                #print(line)
                nomeaning = 1 # not match regex, may be a nomeaning line
        return dropmap
    # @return ratetracemap is {nodeid: [JSONOB_RATE]}
    def Parse_ratetrace(self) :
        if self.nodeid2nodename == {} :
            sys.exit('Error-017, invoke Parse_log first')
        rate_trace_file = open(global_rate_trace, "r")
        lines = rate_trace_file.readlines()
        rate_trace_file.close()
        ratetracemap={}
        for line in lines :
            #0.5	leaf-1	256	netdev://[00:00:00:00:00:01]	OutInterests	80	3.59375	50	2.2460
            r1 = re.compile(r'''(\d+\.*\d*)\t([a-z]{1,10}-?[0-9]*)\t(\d+\.*\d*)\t(.*)\tOutInterests\t(\d+\.*\d*)''', re.VERBOSE)
            ratetraceofnodeid = r1.search(line)
            if ratetraceofnodeid:
                nodename = ratetraceofnodeid.group(2)
                nodeid = self.nodename2nodeid[nodename]
                rate = float(nums(ratetraceofnodeid.group(5)))
                if nodeid in ratetracemap :
                    ratetracemap[nodeid] += rate
                else :
                    ratetracemap[nodeid] = rate
            else :
                nomeaning = 1
        return ratetracemap
#＝＝＝＝＝＝＝＝＝＝＝＝　end of  ParseRoutineHolder
#
#
#＝＝＝＝＝＝＝＝＝＝＝＝　end of  ParseRoutineHolder
class JSONOB_TOPOLOGY(object):
    # @param nodelist is [] of Node,
    # @param linklist is [] of Link
    def __init__(self, nodelist, linklist,nodename2nodeid,nodeid2nodename): 
        self.m_nodelist = nodelist
        self.m_linklist = linklist
        self.m_nodename2nodeid = nodename2nodeid
        self.m_nodeid2nodename = nodeid2nodename
    def get_nodeid2nodename(self):
        return self.m_nodeid2nodename
class Link(object):
    def __init__(self, leftnode, leftfaceuri, rightnode, rightfaceuri, maxpkts, speed, delay):
        try :
            leftnode.get_under()
        except:
            sys.exit('Error013')
        try :
            leftfaceuri.get_under()
            sys.exit('Error014')
        except:
            nothing =1
        self.m_leftfaceuri = FaceUri(leftfaceuri)
        self.m_rightfaceuri = FaceUri(rightfaceuri)
        self.m_leftnode = leftnode
        self.m_rightnode = rightnode
        self.m_maxpkts = maxpkts
        self.m_speed = speed
        self.m_delay = delay
    def get_nodefacemapwithattri(self) :
        return {
            "nodeface":{self.m_leftnode:self.m_leftfaceuri, self.m_rightnode:self.m_rightfaceuri},
            "attri":{"mpkts":self.m_maxpkts, "speed":self.m_speed, "delay":self.m_delay},
        }
class NodeId(object):
    def __init__(self, id, name):
        self.m_id = id
        self.m_name = name
    def get_under(self):
        return self.m_id
    def get_name(self):
        return self.m_name
class FaceUri(object):
    def __init__(self, parsedid):
        if len(parsedid) != 19 or parsedid[0] != '[' or parsedid[18] != ']':
            sys.exit('Error-007 {0}, should be [xx:xx:xx:xx:xx:xx], 19 char'.format(parsedid))
        self.m_parsedid = parsedid
    def get_under(self):
        return self.m_parsedid
class JSONOB_ONETRANS(object):
    def __init__(self, **kwargs):
        count = 0
        for key in kwargs:
            count += 1
            if key == 'resource_name':
                self.m_name = kwargs[key]
            elif key == 'outORinAndiORdata':
                self.m_out_or_in = kwargs[key]
            elif key == 'fromface':
                self.m_from = kwargs[key]
            elif key == 'toface':
                self.m_to = kwargs[key]
            else :
                sys.exit('Error-005')
        if count != 2:
            sys.exit('Error-006')
class JSONOB_ONEINTERESTBYNAME(object):
    def __init__(self, **kwargs):
        count = 0
        for key in kwargs:
            count += 1
            if key == 'i_name':
                self.m_interest_name = kwargs[key]
            elif key == 'trans_list': # trans_list is not ordered like [from a to b] [from b to c], it would like [from a to b] [from a to c] because of forwarding strategy
                self.m_trans_list = kwargs[key]
            else :
                sys.exit('Error-003')
        if count != 2:
            sys.exit('Error-004')
    def get_iname(self):
        return self.m_interest_name
    def get_trans_list(self):
        return self.m_trans_list
class JSONOB_ONEDATABYNAME(object):
    def __init__(self, **kwargs):
        count = 0
        for key in kwargs:
            count += 1
            if key == 'd_name':
                self.m_data_name = kwargs[key]
            elif key == 'trans_list': # trans_list is not ordered like [from a to b] [from b to c], it would like [from a to b] [from a to c] because of forwarding strategy
                self.m_trans_list = kwargs[key]
            else :
                sys.exit('Error-009')
        if count != 2:
            sys.exit('Error-010')
    def get_dname(self):
        return self.m_data_name
    def get_trans_list(self):
        return self.m_trans_list
class JSONOB_SIMURESULT(object):
    def __init__(self, simu_name, jsonob_onedatabyname, jsonob_oneinterestbyname, jsonob_topology, nodeid2jsonob_dropmap, counterlist, ratemap):
        self.m_simu_name = simu_name
        self.m_jsonob_onedatabyname = jsonob_onedatabyname
        self.m_jsonob_oneinterestbyname = jsonob_oneinterestbyname
        self.m_jsonob_topology = jsonob_topology
        self.m_nodeid2jsonob_dropmap = nodeid2jsonob_dropmap
        self.m_counterlist = counterlist
        self.m_ratemap = ratemap
    def get_ratemap(self):
        return self.m_ratemap
    def get_counter_list(self):
        return self.m_counterlist
    def get_simu_name(self):
        return self.m_simu_name
    def get_nodeid2jsonob_dropmap(self):
        return self.m_nodeid2jsonob_dropmap
    def get_jsonob_onedatabyname(self):
        return self.m_jsonob_onedatabyname
    def get_jsonob_oneinterestbyname(self):
        return self.m_jsonob_oneinterestbyname
    def get_jsonob_topology(self):
        return self.m_jsonob_topology
class JSONOB_DROP(object):
    def __init__(self, time, node, pkts, bbytes):
        self.m_time = time
        self.m_node = node
        self.m_pkts = pkts
        self.m_bbytes = bbytes
    def get_time(self):
        return self.m_time
    def get_node(self):
        return self.m_node
    def get_pkts(self):
        return self.m_pkts
    def get_bbytes(self):
        return self.m_bbytes
class DetailGraphMaker_01(object): # make graph with multi-lines 2d
    def __init__(self, name2line, xseq, xlabel, title, ylabel):
        self.m_name2line = name2line
        self.m_xlabel = xlabel
        self.m_title = title
        self.m_xseq = xseq
        self.m_ylabel = ylabel
    def dograph(self):
        fig = plt.figure()
        #ax = fig.add_subplot(111, axes_class=AA.Axes, title='delivery_rate')
        ax = host_subplot(111, axes_class=AA.Axes)
        plt.title(self.m_title, y=1.13)
        ax.set_xlabel(self.m_xlabel, fontsize=18)
        ax.set_ylabel(self.m_ylabel, fontsize=16)
        for name in self.m_name2line :
            #index = list_of_line_route_name.index(name)
            line = ax.plot(self.m_xseq, self.m_name2line[name], '--', linewidth = 2, label = name)
        ax.legend(loc='lower right')
        #ax2 = ax.twin()  # ax2 is responsible for "top" axis and "right" axis
        #ax2.set_xticks(self.m_xseq)
        #ax2.axis["right"].major_ticklabels.set_visible(False)
        #ax2.axis["top"].major_ticklabels.set_visible(True)
        plt.show()
class DetailGraphMaker_02(object): # make graph with multi-lines 2d
    # fuckbit
    def __init__(self, listof) :
        # name2line, xseq, xlabel, title, ylabel):
        self.listof = listof
        assert(len(self.listof[0]) == 5)
        self.mark_list = [
            [
                '-', 	#solid line style
                '--', 	#dashed line style
                '-.', 	#dash-dot line style
                ':', 	#dotted line style
            ],
            [
                'o',    # circle marker
                's',    # square markerr　
                '*',    # star marker
            ]
        ]
    def dographinonesub(self, i, subflag):
        print(subflag + i)
        #print(self.listof[i])
        ax = plt.subplot(subflag + i)
        ax.set_xlabel(self.listof[i][2], fontsize=10)
        ax.set_ylabel(self.listof[i][4], fontsize=10)
        j = 0
        for name in self.listof[i][0] :
            mark = self.mark_list[1][j % len(self.mark_list[1])] + self.mark_list[0][j % len(self.mark_list[0])]
            print("mark=" + mark)
            line = ax.plot(self.listof[i][1], self.listof[i][0][name], mark, linewidth = 2, label = name)
            j += 1
        ax.legend(loc='lower right')
    def dographwithsub(self) :
        fig = plt.figure()
        subflag = -1
        if len(self.listof) == 4 :
            subflag = 411 
        elif len(self.listof) == 3:
            subflag = 311 
        elif len(self.listof) == 2:
            subflag = 211 
        elif len(self.listof) == 1:
            subflag = 111 
        else :
            sys.exit("error - 21321dsc")
        #ax = host_subplot(subflag)
        for i in range(0,len(self.listof),1) :
            self.dographinonesub(i, subflag)
        plt.show()
class GraphMakerOfDrop(object):
    def __init__(self, nodeid2jsonob_dropmap):
        self.m_nodeid2jsonob_dropmap = nodeid2jsonob_dropmap
    def dograph(self,nodeid2nodename):
        xseq = []
        name2line = {}
        xlabel = 'time point'
        title = 'drop'
        xseqset = False
        ylabel = 'droped pkts'
        for nidd in self.m_nodeid2jsonob_dropmap.keys():
            namestr = nodeid2nodename[nidd]
            name2line[namestr] = []
            for drop in self.m_nodeid2jsonob_dropmap[nidd]:
                if xseqset == False :
                    xseq.append(drop.get_time())
                name2line[namestr].append(drop.get_pkts())
            xseqset = True
        detailgraphmaker = DetailGraphMaker_01(name2line,xseq,xlabel,title,ylabel)
        detailgraphmaker.dograph()
class GraphMakerOfFake(object):
    def __init__(self):
        self.nothing = None
    def dograph(self):
        # name2line, xseq, xlabel, title, ylabel):
        listof = []
        listof.append([
            {"tara-route": [0.97, 0.94, 0.93, 0.93, 0.92, 0.92, 0.92],
            "best-route": [0.92, 0.89, 0.86, 0.82, 0.78, 0.73, 0.66],},
            [100, 200, 300, 400, 500, 600, 700,],
            "traffic",
            "",
            "dilivery-rate",
        ])
        listof.append([
            {"tara-route": [0.97, 0.94, 0.93, 0.93, 0.92, 0.92, 0.92],
            "best-route": [0.92, 0.89, 0.86, 0.82, 0.78, 0.73, 0.66],},
            [100, 200, 300, 400, 500, 600, 700,],
            "traffic",
            "",
            "dilivery-rate",
        ])
        detailgraphmaker = DetailGraphMaker_02(listof)
        detailgraphmaker.dographwithsub()
        print("fake graph")
#=======================
#=================
#========================
# process define
def mainsmain() :
    print("python version:" + sys.version)
    ob_arg = argparse.ArgumentParser(description='''
    use this to run zhangyue-ndn, example ======================== :
    <./runMeToStart.py --runsimulation default> ------------------
    <./runMeToStart.py --parsesimulation default> ----------------
    <./runMeToStart.py --makegraph bypython> ----------------------
    <./runMeToStart.py --runparsegraph default> ----------------------
    ''')
    ob_arg.add_argument("--presimulation",help='foo help')
    ob_arg.add_argument("--runsimulation",help='foo help')
    ob_arg.add_argument("--parsesimulation",help='foo help')
    ob_arg.add_argument("--makegraph",help='foo help')
    ob_arg.add_argument("--runparsegraph",help='foo help')
    args = ob_arg.parse_args()
    x_create_empty_file(global_log01ptah)
    if args.presimulation :
        print("into build proc")
        presimu()
    elif args.runsimulation:
        if args.runsimulation == 'default' :
            print("into runsim proc")
            runsimu()
        else :
            print("use it as : ./runMeToStart.py --runsimulation default \n available args are <default><>")
            sys.exit("Error-002")
    elif args.parsesimulation :
        if args.parsesimulation == 'default':
            print("into parse proc")
            parsesimu()
        else :
            sys.exit("Error-011")
    elif args.makegraph :
        if args.makegraph == 'bypython':
            print("into graph proc -python")
            makegraph()
        elif args.makegraph == 'byrscript':
            print("into graph proc -rscript")
            makegraphr()
        else :
            sys.exit('error-0017')
    elif args.runparsegraph :
        if args.runparsegraph == 'default':
            print("into loop")
            looptorun()
        else :
            sys.exit('error-0217')
    else :
        sys.exit("Error-001")
def looptorun() :
    # change your graph step here fuckyou!
    # fuckbit
    maxi = 2
    mini = 1
    errorstep = 0.1
    jsonfilemap = {}
    # all strategy name is ["SarsaLambda", "BestRoute", "Asf", "QLearning", "MultiCast"]
    for strategyname in ["BestRoute"] :
        for i in range(mini,maxi,1):
            errorrateinthisloop = i * errorstep
            assert(errorrateinthisloop < 1.0 and errorrateinthisloop >= 0.0)
            print(colored("yellow", "loop sim {0} + {1}".format(errorrateinthisloop, strategyname)))
            topofilename = "taratopo"
            jsonfilenameinthisloop = "simu_result_with_errorrate={0}_with_strategy\
            ={1}_with_topofile={2}".format(errorrateinthisloop, strategyname, topofilename)
            #global_log01ptah = '{0}/box/logs/{1}'.format(global_root, logfilenameinthisloop)
            global global_wafflag03
            global_wafflag03 = ' --run=\"ndn-tara --errorrate={0} --strategy={1}\"'.format(errorrateinthisloop, strategyname)
            print(colored("yellow", "before loop sim {0} in [{1}, {2})".format(i, mini, maxi)))
            x_runwaf()
            print(colored("yellow", "before loop parse {0} in [{1}, {2})".format(i,mini, maxi)))
            parsesimu(jsonfilename = jsonfilenameinthisloop)
            jsonfullname = '{0}/{1}'.format(global_jsonpath, jsonfilenameinthisloop)
            jsonfilemap[jsonfullname] = [errorrateinthisloop, strategyname]
    makegraph(choice="delivery rate + satisfy + delay", jsonfilelist=jsonfilemap)
def makegraphr():
    cmd ='Rscript /home/tara/ndnSIM/ns-3/src/ndnSIM/examples/graphs/rate-graph.R' 
    print(cmd)
    p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    out,err = p.communicate()
def makegraph(jsonfilelist=None,choice = "fake",):
    # --
    def graphofdropedpkts() :
        assert(jsonfilelist == None)
        name = '{0}/defaultjson'.\
                        format(global_jsonpath)
        jsonob = read_file_to_jsonob(name)
        nodeid2jsonob_dropmap=jsonob.get_nodeid2jsonob_dropmap()
        dropmapgraphmaker = GraphMakerOfDrop(nodeid2jsonob_dropmap)
        dropmapgraphmaker.dograph(jsonob.get_jsonob_topology().get_nodeid2nodename())
    # --
    # --
    def graphfake() :
        assert(jsonfilelist == None)
        dropmapgraphmaker = GraphMakerOfFake()
        dropmapgraphmaker.dograph()
    # --
    # --
    def graphall() :
        name2linemap = {}
        name2linemap_1 = {}
        name2linemap_2 = {}
        name2linemap_3 = {}
        qvofnodeid = 5
        xseq = []
        def printspktpathrecord(spktpathrecord) :
            producerButNotBack = []
            notProducer = []
            bestReturn = []
            for k in spktpathrecord:
                assert(spktpathrecord[k]["consumerOutInterestCounter="] == 1)
                if "producerInInterest" in spktpathrecord[k] :
                    if "consumerInDataCounter=" in spktpathrecord[k] :
                        bestReturn.append(k)
                    else :
                        producerButNotBack.append(k)
                else :
                    notProducer.append(k)
            token_1 = 10
            token_2 = 10
            token_3 = 10
            print("we would print some of spkt path detail, \
            {0} for producerButNotBack.size={1}\
            {2} for notProducer.size={3}\
            {4} for bestReturn.size={5}\
            ".format(token_1,len(producerButNotBack), token_2,len(notProducer),token_3, len(bestReturn)))
            print("{0} for producerButNotBack.size={1}".format(token_1,len(producerButNotBack)))
            for k in producerButNotBack:
                token_1 -= 1
                if (token_1 < 0) :
                    break
                print(k)
            print(" {0} for notProducer.size={1}".format(token_2,len(notProducer)))
            for k in notProducer:
                token_2 -= 1
                if (token_2 < 0) :
                    break
                print(k)
            print(" {0} for bestReturn.size={1} ".format(token_3,len(bestReturn)))
            for k in bestReturn:
                token_3 -= 1
                if (token_3 < 0) :
                    break
                print(k)
        for name in jsonfilelist :
            jsonob = read_file_to_jsonob(name)
            counter_list = jsonob.get_counter_list()
            ratemap = jsonob.get_ratemap()
            errorrate = jsonfilelist[name][0]
            strategyname = jsonfilelist[name][1]
            # drate = consumer in d-pkt / consumer out i-pkt 
            delivery_rate = counter_list[0] / counter_list[1]
            # [pkts, delay-sum-miliseconds]
            delaylist = counter_list[5]
            # {nodeid:[qv, qv...]}
            qvlistmap = counter_list[6]
            averageqv = 0
            for idd in qvlistmap :
                if idd == qvofnodeid :
                    for qv in qvlistmap[idd]:
                        print("qv={0}".format(qv))
                        averageqv += qv
                    averageqv = averageqv / len(qvlistmap)
            if (counter_list[0] != delaylist[0]) :
                print("{0},{1}".format(delaylist[0], counter_list[0]))
                assert(counter_list[0] == delaylist[0])
            averagedelay = delaylist[1] / delaylist[0]
            outgoinginterest = 0
            for kk in ratemap :
                outgoinginterest += ratemap[kk]
            if len(jsonfilelist) == 1 :
                print(colored("blue", "we would print detail of pkts transmit, because only one scenario in list"))
                spktpathrecord = counter_list[3]
                printspktpathrecord(spktpathrecord)
                break
            satisfy = counter_list[4] * 1.0
            unsatisfy = counter_list[2] * 1.0
            #丢包率 
            diubaolv = unsatisfy / outgoinginterest
            # assume that xseq is ordered, if not would bug
            if errorrate not in xseq :
                xseq.append(errorrate)
            if strategyname not in name2linemap :
                name2linemap[strategyname] = []
            name2linemap[strategyname].append(delivery_rate)
            if strategyname not in name2linemap_1 :
                name2linemap_1[strategyname] = []
            name2linemap_1[strategyname].append(diubaolv)
            if strategyname not in name2linemap_2 :
                name2linemap_2[strategyname] = []
            name2linemap_2[strategyname].append(averagedelay)
            if strategyname not in name2linemap_3 :
                name2linemap_3[strategyname] = []
            name2linemap_3[strategyname].append(averageqv)
        listof = []
        #delivery rate = consumer in / consumer out
        listof.append( [ name2linemap, xseq, "error rate", "", "delivery rate", ]) 
        #listof.append( [ name2linemap_1, xseq, "error rate", "", "unsatisfy / outgoing interest", ])
        #averagedelay = delay sum milisecond / consumer in data
        listof.append( [ name2linemap_2, xseq, "error rate", "", "averagedelay", ])
        # 
        listof.append( [ name2linemap_3, xseq, "error rate", "", "averageqv of no-{0}".format(qvofnodeid), ])
        detailgraphmaker = DetailGraphMaker_02(listof)
        detailgraphmaker.dographwithsub()
    #---
    if choice == "droppkts" :
        graphofdropedpkts()
    elif choice == "fake" :
        graphfake()
    elif choice == "delivery rate + satisfy + delay":
        graphall()
    else :
        sys.exit("Error-0123 asdqfuck12321")
    print(colored('red','end'))
def parsesimu(jsonfilename = "defaultjson"): 
    name = '{0}/{1}'.\
                    format(global_jsonpath, jsonfilename)
    parseholder = ParseRoutineHolder()
    rlist =parseholder.Parse_log()
    topology = rlist[0]
    counterlist = rlist[1]
    dropmap=parseholder.Parse_droptrace()
    ratetracemap = parseholder.Parse_ratetrace()
    json_this = JSONOB_SIMURESULT(None,None,None,jsonob_topology=topology,nodeid2jsonob_dropmap=dropmap, counterlist=counterlist, ratemap = ratetracemap)
    assert(counterlist[1] != 0)
    print("delivery rate = {0}, indata={1}, outinterest={2}".format(counterlist[0] / counterlist[1], counterlist[0], counterlist[1]))
    save_this_jsonob_as(name, json_this)
    print(colored('red','end'))
def runsimu() :
    x_runwaf()
    print(colored('red','end'))
def presimu() :
    #ln -s ~/TLC_workspace/zhangyue-ndn/src/ndn-tara.cpp ./examples/ndn-tara.cpp
    #ln -s ~/TLC_workspace/zhangyue-ndn/src/tara-route-strategy.hpp ./NFD/daemon/fw/tara-route-strategy.hpp
    #ln -s ~/TLC_workspace/zhangyue-ndn/src/tara-route-strategy.cpp ./NFD/daemon/fw/tara-route-strategy.cpp
    print(colored('red','end'))
#==============================================================================
#==============================================================================
#============
# test 
def testfunc() :
    def testgraphmaker01():
        xseq = [0.5, 1, 1.5, 2, 2.5, 3]
        ymap = {'fuck01':[2,3,4,5,6,7], 'fuck02':[1,2,3,4,5,6]}
        maker= DetailGraphMaker_01(ymap,xseq,'tt','jj','zz')
        maker.dograph()
    def testreg():
        #[DEBUG] FUCK103[TaraTrace]SPKT is send from consumer with ;interest.name=/root/leaf-1/%FE%1A;on nodeid=0
        line = "[DEBUG] FUCK103[TaraTrace]SPKT is send from consumer with ;interest.name=/root/leaf-1/%FE%1A;on nodeid=0"
        r5 = re.compile(r'''\[DEBUG\]\sFUCK103\[TaraTrace\]SPKT\sis\ssend\sfrom\sconsumer\swith\s;interest\.name=(\/[A-Z0-9\-]*\/[A-Z0-9\-]*\/(\%[A-Z0-9]{2}){1,10});on\snodeid=([0-9]*)''', re.VERBOSE)
        regres = r5.search(line)
        if regres :
            print(regres.group(1))
        else :
            print("fuck test fail!")
    def testreg01():
        line="2 nfd.Tara2Strategy:beforeSatisfyInterest(): [DEBUG] FUCK831[TaraTrace]attach data with qv = -1.2149e+246"
        #r9 = re.compile(r'''([0-9]*)\snfd\.Tara2?Strategy\:beforeSatisfyInterest\(\)\:\s\[DEBUG\]\sFUCK831\[TaraTrace\]attach\sdata\swith\sqv\s=\s(+?-?\d+\.*\d*e+?-?[0-9]{0-12})''', re.VERBOSE)
        r9 = re.compile(r'''([0-9]*)\snfd\.Tara2?Strategy\:beforeSatisfyInterest\(\)\:\s\[DEBUG\]\sFUCK831\[TaraTrace\]attach\sdata\swith\sqv\s=\s(\+?-?\d+\.*\d*e\+?-?[0-9]{0,12})''', re.VERBOSE)
        #r9 = re.compile(r'''([0-9]*)\s''', re.VERBOSE)
        regres = r9.search(line)
        if regres :
            print(regres.group(1))
            #qv = float(nums(regres.group(2)))
            #print(qv)
        else :
            print("fuck test fail!")
    testreg01()
#==============
#==============================================================================
#testfunc()
mainsmain()



 