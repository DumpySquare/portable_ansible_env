#!/usr/bin/python

import re
import paramiko
from ansible.module_utils.basic import *

def main():
    output = [] # create an empty list to log all out output

    # define the fields coming from the ansible module
    fields = {
        "bigip": {"default": True, "type": "str"},
        "local_user": {"default": True, "choices": ['admin', 'root'], "type": "str"},
        "new_password": {"default": True, "no_log": True, "type": "str"},
        "old_password": {"default": True, "no_log": True, "type": "list"}
    }
    
    # pulls in the "fields" above to be used as a dict
    module = AnsibleModule(argument_spec=fields)
    
    i = 0   # counter for number of old passwords

    # assign module params as local variables - makes them easier to use/change
    bigip = module.params['bigip']  
    uname = module.params['local_user']
    passwds = module.params['old_password']
    newpass = module.params['new_password']
    
    while True:
        log = "Trying to connect to %s as %s with %s (%i/%i)" % (bigip,uname, passwds[i], i, len(passwds))
        output.append(log)  # broke into two lines to clean things up

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(bigip, username=uname, password=passwds[i], look_for_keys=False, allow_agent=False)
            output.append("  ~~~~~~~~~~  Connected  ~~~~~~~~~~  ")
            output.append("    Connected to %s as %s with %s" % (bigip, uname, passwds[i]))
            break
        
        except paramiko.AuthenticationException:
            i += 1      # increment our password counter for this attempt

        if i == len(passwds):
            # no passwords worked - quit with fail
            module.fail_json(msg="No root/admin passwords worked...")


    setadmin = "tmsh modify auth user admin password %s" % newpass
    output.append(" -- Executing:  %s" % setadmin)
    stdin, stdout, stderr = ssh.exec_command(setadmin)
    output.append(stdout.read())
    
    setroot = "echo -e \"%s\\n%s\" | tmsh modify auth password root" % (newpass, newpass)
    output.append(" -- Executing:  %s" % setroot)
    stdin, stdout, stderr = ssh.exec_command(setroot)
    output.append(stdout.read())
    
    output.append(" -- Saving config:  tmsh save sys config -- ")
    stdin, stdout, stderr = ssh.exec_command("tmsh save sys config")
    output.append(stdout.read())
    
    ssh.close   # close ssh session
    module.exit_json(change=True, response=output)

if __name__ == '__main__':
    main()