#!/bin/sh

dr=`dirname $0`

# HTTP
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



# RTSP
versionLetter=`sed -n 's/version=\(.......\).*/\1/p' /home/version`

case $versionLetter in
    1.8.6.1) file='M'
        ;;
    *) file='None'
        ;;
esac

if [ $file != 'None' ]; then
    filename="${dr}/rtspsvr${file}"

    if test -f $filename; then
        if ! cmp $filename /home/rtspsvr; then
            test -f /home/rtspsvr && mv /home/rtspsvr /home/rtspsvr.backup
            cp $filename /home/rtspsvr
        fi
    fi
else
    echo "Firmware not supported"
fi


# fix bootcycle
mv $dr/equip_test.sh $dr/equip_test-moved.sh
rm -rf $dr

reboot
