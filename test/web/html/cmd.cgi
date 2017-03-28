#!/bin/sh

_DEBUG_=

########################################
# Функции
########################################


setTZ(){
    #TZ=`echo "$QUERY_STRING" | grep -oE "(^|[?&])tz=[^&]+" | sed "s/%20/ /g" | cut -f 2 -d "=" | sed -e 's/  *$//'`
    if [ ${tz} ]; then
        TZ=$tz
    else
        echo "Ошибка параметра"
        return
    fi

    echo "Зона UTC $TZ<br>"

    TZtoSet=$((8-TZ))

    if [ $TZtoSet -gt 0 ]; then
        TZValue="GMT+$TZtoSet"
        #echo "TZValue=$TZValue"
    else
        TZValue="GMT$TZtoSet"
        #echo "TZValue=$TZValue"
    fi

    echo $TZValue > /etc/TZ && echo "Временная зона изменена успешно.<br>" || echo "<h3>ОШИБКА записи временной зоны.</h3>"

}


setFTP(){

    #_ftp=`echo "$QUERY_STRING" | grep -oE "(^|[?&])ftp=[^&]+" | sed "s/%20/ /g" | cut -f 2 -d "=" | sed -e 's/  *$//'`
    if [ ${ftp} ]; then
        _ftp=${ftp}
    else
        echo "Ошибка параметра"
        return
    fi

    case "$_ftp" in
        on )
            echo "Включаем FTP.<br>"
            echo "Добавляем в автозагрузку<br>"
            cat > "/etc/S89ftp" << EOL  && echo "/etc/init.d/S89ftp создан успешно.<br>" || echo "<h3>ОШИБКА создания /etc/init.d/S89ftp.</h3>"
#!/bin/sh
tcpsvd -vE 0.0.0.0 21 ftpd -w / &
EOL

            echo "Изменяем права файла /etc/init.d/S89ftp<br>"
            if chmod 755 /etc/init.d/S89ftp; then 
                echo "Права изменены.<br>";
            else
                echo "<h3>ОШИБКА изменения прав /etc/init.d/S89ftp</h3>"
                return;
            fi

            echo "Запускаем FTP.<br>"
            tcpsvd -vE 0.0.0.0 21 ftpd -w / &
            echo "FTP включен успешно.<br>"
        ;;

        off)
            echo "Выключаем FTP.<br>"
            echo "Убиваем процесс.<br>"
            #ps | grep /home/watch_process | grep -v "grep" | awk '{print $1}' | xargs kill -9
            killall -9 tcpsvd
            #pidof tcpsvd | xargs kill -9
            echo "Убираем из автозагрузки.<br>"
            rm -f /etc/init.d/S89ftp && echo "FTP выключен успешно.<br>" || echo "<h3>ОШИБКА удаления /etc/init.d/S89ftp.</h3>"
        ;;

        * )
        echo "<h3>ERROR! Неверный параметр для FTP.</h3>"
        ;;

    esac
}

setTELNET(){

    #_telnet=`echo "$QUERY_STRING" | grep -oE "(^|[?&])telnet=[^&]+" | sed "s/%20/ /g" | cut -f 2 -d "=" | sed -e 's/  *$//'`
    if [ ${telnet} ]; then
        _telnet=${telnet}
    else
        echo "Ошибка параметра"
        return
    fi

    case "$_telnet" in
        on )
            echo "Включаем telnet.<br>"
            echo "Добавляем в автозагрузку<br>"
            echo "#!/bin/sh" > /etc/init.d/S88telnet && echo "/etc/init.d/S88telnet создан успешно.<br>" || echo "ОШИБКА создания /etc/init.d/S88telnet.<br>"
            echo "telnetd &" >> /etc/init.d/S88telnet
            echo "Изменяем права файла<br>"
            chmod 755 /etc/init.d/S88telnet && echo "Права изменены.<br>" || echo "ОШИБКА изменения прав /etc/init.d/S88telnet.<br>"
            echo "Запускаем telnet.<br>"
            telnetd &
            echo "telnet включен успешно.<br>"
            #echo "Для завершения перезагрузите камеру.<br>"
            ;;

        off)
            echo "Выключаем telnet.<br>"
            echo "Убиваем процесс.<br>"
            #ps | grep /home/watch_process | grep -v "grep" | awk '{print $1}' | xargs kill -9
            pidof telnetd | xargs kill -9
            echo "Убираем из автозагрузки.<br>"
            rm -f /etc/init.d/S88telnet && echo "telnet выключен успешно.<br>" || echo "ОШИБКА удаления /etc/init.d/S88telnet.<br>"
        ;;

        * )
            echo "<h3>ERROR! Неверный параметр для TELNET.</h3>"
        ;;

    esac
}

setRTSP(){
    #_rtsp=`echo "$QUERY_STRING" | grep -oE "(^|[?&])rtsp=[^&]+" | sed "s/%20/ /g" | cut -f 2 -d "=" | sed -e 's/  *$//'`
    
    if [ ${rtsp} ]; then
        _rtsp=${rtsp}
    else
        echo "Ошибка параметра"
        return
    fi

    webdir=/home/web

    case "$_rtsp" in
        on )
            echo "Включаем RTSP<br>"

            versionLetter=`sed -n 's/version=\(.......\).*/\1/p' /home/version`

            if [ $versionLetter == '1.8.6.1' ]; then
                cp $webdir/srv/rtspsvr /home/rtspsvr
                echo "Для запуска RTSP необходимо перезагрузить камеру.<br>"
            else
                echo "<h3>Firmware not supported</h3>"
            fi

            #sed -i "s/portRtsp=554/portRtsp=5541/" /etc/ui.conf
        ;;

        off )
            rm -f /home/rtspsvr && echo "RTSP выключен успешно.<br>" || echo "<h3>ОШИБКА удаления /home/rtspsvr</h3>"
            #mv /home/recv_X.726 /home/recv.726
        ;;

        * )
            echo "<h3>ERROR! Неверный параметр для RTSP.</h3>"
        ;;
    esac

}

setWIFI(){
  echo "$QUERY_STRING"
  #################################################
  #wifi_name="name"
  #wifi_password="password"
  #################################################
  #sed -i 's/valid1=0/valid1=1/g' /etc/ui.conf
  #sed -i 's/doreset=1/doreset=0/g' /etc/ui.conf
  ##rm /etc/wpa_supplicant.conf
  ##rm /home/wpa_supplicant.conf
  #echo "ctrl_interface=/var/run/wpa_supplicant
  #ap_scan=1
  #network={
  #ssid=\""$wifi_name"\"
  #scan_ssid=1
  #proto=WPA RSN
  #key_mgmt=WPA-PSK
  #pairwise=CCMP TKIP
  #group=CCMP TKIP
  #psk=\""$wifi_password"\"
  #}" > /etc/wpa_supplicant.conf
  #cp /etc/wpa_supplicant.conf /home/wpa_supplicant.conf
  #sleep 5
  ##mv "/home/hd1/test/equip_test.sh" "/home/hd1/test/equip_test.sh.old"
  #rm "/home/hd1/test/equip_test.sh"
  #reboot

}

setPASS(){
    #_newpass=`echo "$QUERY_STRING" | grep -oE "(^|[?&])pass=[^&]+" | sed "s/%20/ /g" | cut -f 2 -d "=" | sed -e 's/  *$//'`
    if [ ${pass} ]; then
        _newpass=${pass}
    else
        echo "Ошибка параметра"
        return
    fi
    
    #echo "$_newpass" | passwd root --stdin
    echo "root:${_newpass}" | chpasswd
}


chainaOFF(){
    echo "$QUERY_STRING"
    #ps | grep /home/watch_process | grep -v "grep" | awk '{print $1}' | xargs kill -9
    #ps | grep /home/cloud | grep -v "grep" | awk '{print $1}' | xargs kill -9
    #sed -i 's|api.xiaoyi.com/v4/ipc/check_did|api.xiaoyi.cox/v4/ipc/check_did|g' /home/cloud
}

rebootCAM(){
    reboot
}

offCAM(){
    poweroff
}

backupCAM(){
    _date=$(date +%Y%m%d)

    #mtd3=`echo "$QUERY_STRING" | grep -oE "(^|[?&])mtd3=[^&]+" | sed "s/%20/ /g" | cut -f 2 -d "=" | sed -e 's/  *$//'`
    #mtd4=`echo "$QUERY_STRING" | grep -oE "(^|[?&])mtd4=[^&]+" | sed "s/%20/ /g" | cut -f 2 -d "=" | sed -e 's/  *$//'`
    #mtd5=`echo "$QUERY_STRING" | grep -oE "(^|[?&])mtd5=[^&]+" | sed "s/%20/ /g" | cut -f 2 -d "=" | sed -e 's/  *$//'`
    #mtd6=`echo "$QUERY_STRING" | grep -oE "(^|[?&])mtd6=[^&]+" | sed "s/%20/ /g" | cut -f 2 -d "=" | sed -e 's/  *$//'`

    mkdir -p "/home/hd1/backup/${_date}" && echo "Директория '/home/hd1/backup/${_date}' успешно создана.<br>" || echo "<h3>ОШИБКА создания директории</h3>"

    if [[ "$mtd3" = "on" ]]; then
        #echo "mtd3=$mtd3"
        echo "Backup mtd3 <br>"
        cat "/dev/mtdblock3" > "/home/hd1/backup/${_date}/mtdblock3"
    fi 

    if [[ "$mtd4" = "on" ]]; then
        #echo "mtd4=$mtd4"
        echo "Backup mtd4 <br>"
        cat "/dev/mtdblock4" > "/home/hd1/backup/${_date}/mtdblock4"
    fi 

    if [[ "$mtd5" = "on" ]]; then
        #echo "mtd5=$mtd5"
        echo "Backup mtd5 <br>"
        cat "/dev/mtdblock5" > "/home/hd1/backup/${_date}/mtdblock5"
    fi 

    if [[ "$mtd6" = "on" ]]; then
        #echo "mtd6=$mtd6"
        echo "Backup mtd6 <br>"
        cat "/dev/mtdblock6" > "/home/hd1/backup/${_date}/mtdblock6"
    fi 

    echo "Резервное копирование завершено."	
}



########################################
# Скрипт
########################################

# HTML заголовок
cat << EOF

<!DOCTYPE html>

<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <link type="image/x-icon" rel="shortcut icon" href="/favicon.ico" />
    <title></title>
  </head>
  <body>
EOF

#cmd=`echo "$QUERY_STRING" | grep -oE "(^|[?&])cmd=[^&]+" | sed "s/%20/ /g" | cut -f 2 -d "=" | sed -e 's/  *$//'`
source ./post.cgi

if [ ${_DEBUG_} ]; then
    echo "metod=${REQUEST_METHOD}<br>"
    echo "get=$QUERY_STRING<br>"
    echo "post=${QUERY_STRING_POST}<br>"
    echo "cmd=${cmd}<br><hr />"
fi

if [[ "${REQUEST_METHOD}" = "GET" ]]; then
    echo "<h3>get больше не поддерживается. Используйте post</h3><br>"
    exit 0
fi

case "$cmd" in

    settz )
        echo "<h2>Установка временной зоны.</h2><hr />"
        setTZ
        ;;
        
    setftp )
        echo "<h2>Изменение работы FTP</h2><hr />"
        setFTP
        ;;
        
    settelnet )
        echo "<h2>Изменение работы Telnet</h2><hr />"
        setTELNET
        ;;
        
    setpasswd )
        echo "<h2>Изменение пароля root</h2><hr />"
        setPASS
        ;;
        
    setrtsp )
        echo "<h2>Изменение работы RTSP</h2><hr />"
        setRTSP
        ;;
        
    reboot )
        echo "<h2>Перезагрузка камеры.</h2><hr />"
        rebootCAM
        ;;
        
    off )
        echo "<h2>Выключение камеры.</h2><hr />"
        offCAM
        ;;

    backup )
        echo "<h2>Резервное копирование разделов.</h2><hr />"
        backupCAM
        ;;

    * )
        echo "<h2>ERROR! Command unrecognized.</h2><hr />"
        ;;

esac


#конец страницы
cat << EOF2
      <hr />
      <input type="button" onclick="history.back();" value="Вернуться"/>
      <hr />
    </body>
  </html>
EOF2


exit 0
