import os
from tracemalloc import start
import colorama
import subprocess
import random
import sys
import scapy
import csv
import time
import shutil
from datetime import datetime
import time
from colorama import Fore, Back, Style
import re
colorama.init()
main = "/usr/share/airdiscover"
log = "/usr/share/airdiscover/conf/airdiscover.log"
pixie_php = "/usr/share/airdiscover/pixie.php"
version_log = "/usr/share/airdiscover/VERSION"
update_check = True
active_wireless_networks = []
INTERFACE="" #select interface
MONITOR="DISABLED"
NETWORK_SELECTED=""
MANUALINT=""
BSSID="None"
ESSID="None"
CHANNEL="None"
CRYPTO="None"
def check_for_essid(essid, lst):
    check_status = True
    if len(lst) == 0:
        return check_status
    for item in lst:
        if essid in item["ESSID"]:
            check_status = False

    return check_status

def start_scan():
    try:
        while True:
            subprocess.call("clear", shell=True)
            for file_name in os.listdir():
                    fieldnames = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key']
                    if ".csv" in file_name:
                        with open(file_name) as csv_h:
                            csv_h.seek(0)
                            csv_reader = csv.DictReader(csv_h, fieldnames=fieldnames)
                            for row in csv_reader:
                                if row["BSSID"] == "BSSID":
                                    pass
                                elif row["BSSID"] == "Station MAC":
                                    break
                                elif check_for_essid(row["ESSID"], active_wireless_networks):
                                    active_wireless_networks.append(row)

            print(Fore.BLUE+"[*]"+Fore.RESET+" Scanning... Press Ctrl+C when you want to select\n")
            print(Fore.GREEN+"No |\tBSSID              |\tChannel|\tESSID                         |")
            print(Fore.GREEN+"___|\t___________________|\t_______|\t______________________________|")
            for index, item in enumerate(active_wireless_networks):
                print(f"{index}\t{item['BSSID']}\t{item['channel'].strip()}\t\t{item['ESSID']}")
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("")
    while True:
        choice = input(Fore.CYAN+"[?]"+Fore.RESET+" Please select your choice: ")
        try:
            if active_wireless_networks[int(choice)]:
                break
        except:
            print(Fore.RED+"[-]"+Fore.RESET+" Please try again.")
    hackbssid = active_wireless_networks[int(choice)]["BSSID"]
    hackchannel = active_wireless_networks[int(choice)]["channel"].strip()
    with open("/usr/share/airdiscovery/temp/settings/target-bssid.txt", 'w') as target_bssid:
        target_bssid.write(hackbssid)
    with open("/usr/share/airdiscovery/temp/settings/target-channel.txt", 'w') as target_channel:
        target_channel.write(hackchannel)
    sys.exit()
if __name__ == "__main__":
    start_scan()