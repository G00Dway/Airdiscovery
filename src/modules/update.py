import os
import time
import colorama
import configparser
import sys
from colorama import Fore
colorama.init()
file_all = None


def config_database(string):
    if "path" in string and "config" in string and "level" in string and "bash_script" in string and "git" in string:
        print(Fore.YELLOW+'[+]'+Fore.RESET+' Config File Seems Valid, Updating...')
    else:
        print(Fore.RED+'[-]'+Fore.RESET+' Config File Seems Corrupted, Exiting...')
        sys.exit()
    def columns():
        try:
            if os.path.exists(path) and os.path.exists(config_name) and os.path.exists(level) and os.path.exists(bash):
                print(Fore.BLUE+'[*]'+Fore.RESET+' Checking For Updates...')
                os.system('bash /usr/share/airdiscover/src/modules/update_bash.sh')
                try:
                    if os.path.exists("/usr/share/airdiscover/cache/update_version.log"):
                        with open("/usr/share/airdiscover/cache/update_version.log", "r") as t:
                            version = t.read()
                        print(Fore.BLUE+'[*]'+Fore.RESET+f' Updating To Version: {version}...')
                        if "http" in git or "https" in git:
                            pass
                        else:
                            print(Fore.RED+'[-]'+Fore.RESET+' The Link Name Is Invalid In Config File...')
                            sys.exit()
                        if os.path.exists("/usr/var/airdiscover-trash"):
                            pass
                        else:
                            os.mkdir('/usr/var/airdiscover-trash')
                        try:
                            if os.path.exists("/usr/var/airdiscover-trash/airdiscover"):
                                os.system('rm -rf /usr/var/airdiscover-trash/airdiscover')
                            else:
                                pass
                            os.system('git clone '+git+' /usr/var/airdiscover-trash/airdiscover > /dev/null 2>&1')
                            print(Fore.BLUE+'[*]'+Fore.RESET+' Running Post-Install Script...')
                            os.system('rm -rf /usr/share/airdiscover')
                            os.system('rm -rf /usr/bin/airdiscover')
                            os.system('bash /usr/var/airdiscover-trash/airdiscover/setup.sh')
                        except:
                            pass
                        os.system('clear')
                        print(Fore.YELLOW+'[+]'+Fore.RESET+f' Successfully Updated To Version: {version}')
                        print(Fore.BLUE+'[*]'+Fore.RESET+' Dont Forget To Restart Airdiscover!')
                        time.sleep(2)
                        sys.exit()
                    else:
                        sys.exit()
                except:
                    pass
        except:
            pass
    data_file = "/usr/share/airdiscover/src/modules/update.conf"
    config_file = configparser.RawConfigParser()
    config_file.read(data_file)
    path = config_file['UPDT']['path']
    config_name = config_file['UPDT']['config']
    level = config_file['UPDT']['level']
    bash = config_file['UPDT']['bash_script']
    git = config_file['UPDT']['git']
    columns()
            






try:
    if os.path.exists("/usr/share/airdiscover") and os.path.exists("/usr/share/airdiscover/src/modules/update.conf"):
        with open("/usr/share/airdiscover/src/modules/update.conf", "r") as config:
            configration = config.read()
        file_all = True
    else:
        print(Fore.RED+'[-]'+Fore.RESET+' Unable To Continue, Update Files Was Not Found On Database...')
        sys.exit()
except Exception as error:
    print(Fore.RED+'[-]'+Fore.RESET+' Error: '+error)

if True:
    config_database(configration)
else:
    sys.exit()
