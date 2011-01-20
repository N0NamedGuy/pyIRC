import sys
from ircclient import *


CMDS_FILE = 'cmds'
DEF_PORT = '6667'

global irc_running
global irc_client
global irc_host 

irc_running = None
irc_client = None
irc_host = None

class pyirc(ircclient):
    
    def __init__(self, host, port):
        ircclient.__init__(self, host, port)

    def event_priv_msg(self, user, msg):
        ircclient.event_priv_msg(self, user, msg)
        print '<%s> %s' % (user.get_nick(), msg)

def parse_cmd(cmd):
    cmd_tokens = cmd.split(' ')
    global irc_client
    global irc_host
    
    if (cmd_tokens[0] == '/server' and len(cmd_tokens) == 2):
        irc_host = cmd_tokens[1].split(':')
        if len(irc_host) == 1:
            irc_host[1] = 6667

        irc_host[1] = int(irc_host[1])

        print 'Connecting to %s (port %d)' % (irc_host[0], irc_host[1])

        irc_client = pyirc(irc_host[0], int(irc_host[1]))
        irc_client.connect()

    elif cmd[0] == '/':
        print 'sending %s' % (cmd[1:].strip(),)
        if irc_client != None:
            irc_client.send(cmd[1:].strip())

def load_cmds(cmds_file):
    f = open(cmds_file)
    lines = f.readlines()
    f.close()
    
    for line in lines:
        parse_cmd(line)
        

if __name__ == '__main__':
    
    load_cmds(CMDS_FILE)
    if irc_client != None:
        try:
            irc_client.recv_loop()
        except KeyboardInterrupt:
            irc_client.quit('')
            irc_client.close()
