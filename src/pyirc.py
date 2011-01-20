import sys
from ircclient import *
from threading import Thread

CMDS_FILE = 'cmds'
DEF_PORT = '6667'

global irc_running
global irc_client
global irc_host 

irc_running = False
irc_client = None
irc_host = None

class pyirc(ircclient):
    
    def __init__(self, host, port):
        ircclient.__init__(self, host, port)

    def event_priv_msg(self, user, msg):
        ircclient.event_priv_msg(self, user, msg)
        print '<%s> %s' % (user.get_nick(), msg)

    def event_channel_msg(self, user, chan, msg):
        ircclient.event_channel_msg(self, user, chan, msg)
        print '<%s>@%s %s' % (user.get_nick(), chan, msg)

    def event_join(self, user, chan):
        ircclient.event_join(self, user, chan)
        print '* %s joined %s' % (user.get_nick(), chan)
    

class client_thread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global irc_client
        irc_client.recv_loop() 

def parse_cmd(cmd):
    cmd_tokens = cmd.split(' ')
    global irc_client
    global irc_host
    
    if (cmd_tokens[0].lower() == '/server' and len(cmd_tokens) == 2):
        irc_host = cmd_tokens[1].split(':')
        if len(irc_host) == 1:
            irc_host[1] = 6667

        irc_host[1] = int(irc_host[1])

        print '* Connecting to %s (port %d)' % (irc_host[0], irc_host[1])

        irc_client = pyirc(irc_host[0], int(irc_host[1]))
        irc_client.connect()

    elif cmd[0] == '/':
        if irc_client != None:
            irc_client.send(cmd[1:])

def load_cmds(cmds_file):
    f = open(cmds_file)
    lines = f.readlines()
    f.close()
    
    for line in lines:
        parse_cmd(line.strip())

if __name__ == '__main__':
    load_cmds(CMDS_FILE)
    irc_running = True
    if irc_client != None:
        client_th = client_thread()
        client_th.start()

        try:
            for line in iter(sys.stdin.readline, ""):
                parse_cmd(line)
        except KeyboardInterrupt:
            irc_running = False
            irc_client.quit('')
            irc_client.close()
