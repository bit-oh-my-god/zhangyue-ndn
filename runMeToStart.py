#!/home/tara/miniconda2/bin/python
import argparse
import os
import sys
import subprocess
#======
# environment settings
global_pwd = os.path.dirname(os.path.realpath(__file__))
global_runtime_link_path1 = '/home/tara/ndnSIM/ns-3/build/' #TODO
global_runtime_link_path2 = '/home/tara/ndnSIM/ns-3/build/home/tara/ndnSIM/ns-3/build/src/ndnSIM/examples/'
global_log01ptah = '{0}/box/logs/log01'.format(global_pwd)
global_waf = '/home/tara/ndnSIM/ns-3/waf'
global_wafflag01 = ' --run=ndn-tree-tracers'
global_source = '/home/tara/ndnSIM/ns-3/src/ndnSIM/examples/ndn-tree-tracers.cc'
global_source1 = '/home/tara/ndnSIM/ns-3/src/ndnSIM/examples/ndn-zhangyue.cc'
#======
# util
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
    subprocess.Popen(cmd, env=my_env,shell=True)
    print('end')
def x_runwaf() :
    os.chdir(os.path.dirname(global_waf))
    print(global_waf)
    cmd = global_waf + global_wafflag01 + ' > {0}'.format(global_log01ptah)
    subprocess.Popen(cmd,shell=True)
#=========================
#=================================
#=========================
# class define



#=======================
#=================
#========================
# process define
def mainsmain() :
    ob_arg = argparse.ArgumentParser(description='''
    use this to run zhangyue-ndn, 
    example :
    <./runMeToStart.py --runsimulation default>
    ''')
    ob_arg.add_argument("--buildsimulation",help='foo help')
    ob_arg.add_argument("--runsimulation",help='foo help')
    ob_arg.add_argument("--parsesimulation",help='foo help')
    ob_arg.add_argument("--makegraph",help='foo help')
    args = ob_arg.parse_args()
    if args.buildsimulation :
        print("into build proc")
    elif args.runsimulation:
        if args.runsimulation == 'default' :
            print("into run proc")
            runsimu()
        else :
            print("use it as : ./runMeToStart.py --runsimulation default \n available args are <default><>")
            sys.exit("Error-002")
    elif args.parsesimulation :
        print("into parse proc")
    elif args.makegraph :
        print("into graph proc")
    else :
        sys.exit("Error-001")
def runsimu() :
    x_runwaf()
#==============================================================================
#==============================================================================
#==============================================================================
x_create_empty_file(global_log01ptah)
mainsmain()