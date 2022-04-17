cd /usr/share/airdiscover
BRANCH="main"
LAST_UPDATE=`git show --no-notes --format=format:"%H" $BRANCH | head -n 1`
LAST_COMMIT=`git show --no-notes --format=format:"%H" origin/$BRANCH | head -n 1`

git remote update > /dev/null 2>&1
if [ $LAST_COMMIT != $LAST_UPDATE ]; then
        wget https://raw.githubusercontent.com/G00Dway/Airdiscovery/main/VERSION -O /usr/share/airdiscover/cache/update_version.log > /dev/null 2>&1
else
        echo -e "\033[1;32m[+] \033[0mNo Update Detected."
fi