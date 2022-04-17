echo "[*] Configuring Airdiscover..."
chmod +x src/bin/airdiscover
cp -r src/bin/airdiscover /usr/bin
echo "[*] Building Database In /usr/share..."
mkdir /usr/share/airdiscover
mkdir /usr/share/airdiscover/conf
touch /usr/share/airdiscover/conf/airdiscover.log
cp -r uninstall.sh /usr/share/airdiscover
mkdir /usr/share/airdiscover/handshakes
touch /usr/share/airdiscover/pixie.php
echo "[*] Creating .airdr Directory In /root..."
mkdir /root/.airdr
mkdir /root/.airdr/handshakes
mkdir /root/.airdr/files
echo "[*] Copying Database Files..."
cp -r src /usr/share/airdiscover
cp -r ui /usr/share/airdiscover
cp -r temp /usr/share/airdiscover
cp -r VERSION /usr/share/airdiscover
cp -r .git /usr/share/airdiscover
echo "[*] Installing APT Pre-Requirements..."
apt install python python3-pip php aircrack-ng php-cgi php-xml mdk3 xterm zenity mdk4 steghide fuseiso bettercap pixiewps -y
echo "[*] ..."
echo "[*] Cleaning Cache..."
apt clean
echo "[*] Installing PIP Pre-Requirements..."
pip3 install colorama scapy future paramiko requests
echo "[*] Done."
echo "[+] Type 'airdiscover' In Terminal To Run Script"
