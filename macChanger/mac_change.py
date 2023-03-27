#!/usr/bin/env python3

import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help = "Interface to change mac address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New mac address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-]Syntax Error. Enter python3 mac_changer.py -h")
    elif not options.new_mac:
        parser.error("[-]Syntax Error. Enter python3 mac_changer.py -h")

    return options

def mac_changer(interface, new_mac):
    print("[+] changing mac address of "+interface+" to "+new_mac);
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", options.interface])
    mac_addr_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result);
    if mac_addr_search_result:
        return mac_addr_search_result.group(0)
    else:
        print("[-] No mac address available.")


if __name__=="__main__":
    options = get_arguments()
    current_mac = get_current_mac(options.interface)
    print("current Mac = "+str(current_mac))
    mac_changer(options.interface, options.new_mac)
    current_mac = get_current_mac(options.interface)
    if current_mac == options.new_mac:
        print("[+] mac address of "+options.interface+"is successfully changed to "+options.new_mac)
    else:
        print("[-] mac address of "+options.interface+" has failed.")
