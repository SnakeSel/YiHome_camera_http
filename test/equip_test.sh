#!/bin/sh


# HTTP
dr=`dirname $0`

cat > "/etc/init.d/S87lighttpd" << EOL
#!/bin/sh
cd /home/web
./lighttpd -f ./lighttpd.conf &
EOL

chmod 755 /etc/init.d/S87lighttpd

cp -af $dr/web/* /home/web/
ln -s /home/hd1/record /home/web/html/video
chmod 744 /home/web/lighttpd
chmod 644 /home/web/html/*
chmod 744 /home/web/html/*.cgi

sync

# fix bootcycle
mv $dr/equip_test.sh $dr/equip_test-moved.sh
rm -rf $dr

reboot
