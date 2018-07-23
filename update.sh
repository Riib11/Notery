#
# update git
#
echo \>\>\> updating git...
git fetch ~/git/Notery
git pull ~/git/Notery

#
# update python
#
echo \>\>\> updating python3...
pip3 install -e src

#
# update bash command
#
echo \>\>\> updating bash...
cp ~/git/Notery/notery.sh /usr/local/bin/notery
chmod +x /usr/local/bin/notery
chmod +x ~/git/Notery/install.sh