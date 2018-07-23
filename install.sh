#
# install python
#
echo \>\>\> installing python3 module
pip3 install -e src

#
# install bash command
#
echo \>\>\> install bash commands
cp ~/git/Notery/notery.sh /usr/local/bin/notery
chmod +x /usr/local/bin/notery
chmod +x ~/git/Notery/install.sh