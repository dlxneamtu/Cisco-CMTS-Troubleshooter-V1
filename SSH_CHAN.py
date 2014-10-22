#!/usr/bin/env python

"""  This Class provide SSH access utility APIs to the user
       device_login(self, device, dev_uname, dev_passw, en_passw)
           - API to telnet login to device via SSH
       send_command(self, cmdstr, waitstr, max_time_out)
           - API to send command to device and returns the output of command
"""
__author__      = "Dan Neamtu"
__copyright__   = "Copyright 2014, Cisco Systems, Inc"
__credits__     = ["Dan Neamtu","Sreeni Inukoti"]
__version__     = "1.0"
__status__      = "Development"

import paramiko
import time, logging

class SSH_CHAN :
    def __init__(self, hostname, uname, passw, gapi):
        self.hostname = hostname
        self.uname = uname
        self.passw = passw
        self.gapi = gapi
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname,22,uname,passw)
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.chan = self.ssh.invoke_shell()

    def get_ssh_chan(self):
        return self.chan

    def resp_has_string(self, strResult, substr):
        bstatus = False
        readline = strResult.split('\n');
        for line in readline:
            if substr in line:
                if (substr == '#' or substr == '$') :
                    if line.count(substr) == 1 :
#                        logging.info("###### Found only one prompt char ###########")
                        bstatus = True
                        break;
                else :
                    bstatus = True
                    break;
        return bstatus

# returns status=1 if successful
    def send_command_old(self, cmdstr, waitstr, max_time_out):
        status = 0
        self.chan.send(cmdstr)
        time.sleep(max_time_out)
        strResult = self.chan.recv(39999)
        if (self.resp_has_string(strResult, waitstr)):
            status = 1
        logging.info(strResult)
        return status, strResult

    def send_command(self, cmdstr, waitstr, max_time_out):
        status = 0
        lpexit = 0
        fdata = ""
        wait_time_out = max_time_out+3

        self.chan.send(cmdstr)
        t0 = time.time()

        while not self.chan.exit_status_ready() :
            if self.chan.recv_ready():
                data = self.chan.recv(19999)
                logging.info(data)
                while data:
                    fdata += data
                    t1 = time.time()
                    t3 = abs(t1 - t0)
#                    logging.info("###### Elapsed time "+str(t3)+" ###########")

                    if (self.resp_has_string(data, waitstr)):
#                        logging.info("###### WAIT STR "+waitstr+" found ###########")
                        status = 1
                        break;

                    elif (self.resp_has_string(data, self.gapi.argWaitString)):
#                       logging.info("######  found argWaitsring ###########")
                        lpexit = 1
                        break;

#                    elif (self.resp_has_string(data, self.gapi.argServerString)):
#                        logging.info("######  found argServerString ###########")
#                        lpexit = 1
#                        break;

                    if (t3 > wait_time_out) :
                        logging.info("###### Timeout WAITING FOR STR "+waitstr+" ###########")
                        lpexit = 1
                        break
                    if self.chan.recv_ready():
#                        logging.info("###### WAITING FOR DATA  ###########")
                        data = self.chan.recv(19999)
                        logging.info(data)
                    else:
                        data = None
#                    logging.info("###### WAITING FOR DATA  ###########")

            if lpexit == 1 or status == 1:
                break;

#        logging.info("return send_command")

        return status, fdata

    def device_login(self, device, dev_uname, dev_passw, en_passw):
        cmdstr = "telnet "+device+"\n"
        status, resp = self.send_command(cmdstr, "Username:", 3)
        if (status == 0):
            print "Username returned status 0 "
            return status;

        cmdstr = dev_uname+"\n"
        status, resp = self.send_command(cmdstr, "Password:", 3)
        if (status == 0):
            print "Password returned status 0 "
            return status;

        cmdstr = dev_passw+"\n"
        status, resp = self.send_command(cmdstr, self.gapi.argEnWaitString, 1)

        if (status == 1):
            cmdstr = "en"+"\n"
            status, resp = self.send_command(cmdstr, "Password: ", 3)
            if (status == 0):
                print "Enable Password returned status 0 "
                return status;

            cmdstr = en_passw+"\n"
            status, resp = self.send_command(cmdstr, self.gapi.argWaitString, 1)
            if (status == 0):
                print "Waiting for prompt returned status 0 "
                return status;

        if (self.resp_has_string(resp, self.gapi.argWaitString)):
            status = 1

        return status

    def chan_close (self):
        self.ssh.close()
