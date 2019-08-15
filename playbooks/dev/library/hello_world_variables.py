#!/usr/bin/python

from ansible.module_utils.basic import *

def main():
    module = AnsibleModule(argument_spec={})
    theReturnValue = {"hello": "world"}
    module.exit_json(changed=False, meta=theReturnValue)



    #module.params.update({"bigip":bigip})
    #module.params.update({"What-Happened?":output})

    # returns all the modules parameters as part of the "result"
    #module.exit_json(changed=True, meta= module.params)



if __name__ == '__main__':
    main()