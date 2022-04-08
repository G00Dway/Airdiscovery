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
echo "[*] Installing APT Pre-Requirements..."
apt install python python3-pip -y
apt install php aircrack-ng -y
apt install php-cgi php-xml -y
apt install mdk3 -y
apt install xterm zenity -y
apt install mdk4 -y
apt install steghide fuseiso -y
apt install bettercap -y
apt install pixiewps -y
echo "[*] ..."
echo "[*] Cleaning Cache..."
apt clean
echo "[*] Installing PIP Pre-Requirements..."
pip3 install colorama scapy future paramiko requests
echo "[*] Done."