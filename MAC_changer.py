#!/usr/bin/env python3

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i","--interface",dest="interface",help="Defines interface for MAC change")
    parser.add_option("-m","--mac",dest="new_mac",help="Defines new MAC ")

    (options,arguments) = parser.parse_args()
    
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info...")
    elif not options.new_mac:
        parser.error("[-] Please specify an new mac, use --help for more info...")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for" + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "either", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    print("[+] Changed MAC address for" + interface + " to " + new_mac)
def get_current_mac(interface):
    old_mac_address = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",str(old_mac_address))

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print('[-] Mac address is empty')
    

options = get_arguments()

current_mac = get_current_mac(options.interface)

print('Current MAC: '+str(current_mac))

change_mac(options.interface, options.new_mac)
new_mac = get_current_mac(options.interface)
if new_mac == options.new_mac:
    print("[+] MAC address chanded successfully. New MAC: ",new_mac)
else:
    print("[-] MAC did not changed")
    
change_mac(options.interface, current_mac)
new_mac = get_current_mac(options.interface)
if new_mac == current_mac:
    print("[+] MAC address chanded successfully. New MAC: ",new_mac)
else:
    print("[-] MAC did not changed")
