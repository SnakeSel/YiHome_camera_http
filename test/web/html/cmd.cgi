#!/bin/sh

DEBUG=1

########################################
# Функции
########################################
debug(){
    debugfile="debug.log"
    if [ $DEBUG -eq 1 ]; then
        #echo -e $(date +"%Y%m%d %k:%M:%S")
        echo "$(date +'%Y-%m-%d %H:%M:%S')" "$(basename $0)" "$@" >> "${debugfile}"
    fi

}

getvar(){
    echo "$QUERY_STRING" | grep -oE "(^|[?&])$1=[^&]+" | sed "s/%20/ /g" | cut -f 2 -d "=" | sed -e 's/  *$//'
}

setTZ(){
    tz=$(getvar tz)

    if [ -z $tz ]; then
        echo "Ошибка параметра"
        return
    fi

    echo "Зона UTC $tz<br>"

    # Если cloud исполняемый, тогда время GMT8-
    if [ -x /home/cloud ]; then
        TZtoSet=$((8-tz))

        #Если >0 то 
        if [ $TZtoSet -gt 0 ]; then
            TZValue="GMT+$TZtoSet"
            #echo "TZValue=$TZValue"
        else
            TZValue="GMT$TZtoSet"
            #echo "TZValue=$TZValue"
        fi
    else
        #Значит работает ntpd и зона UTC-
        #Если >0 то 
        if [ $tz -gt 0 ]; then
            TZValue="UTC+$tz"
        else
            TZValue="UTC$tz"
        fi

    fi

    echo $TZValue > /etc/TZ && echo "Временная зона изменена на $TZValue.<br>" || echo "<h3>ОШИБКА записи временной зоны.</h3>"

}


setFTP(){
    initfile="/etc/init.d/S89ftp"

    ftp=$(getvar ftp)
    if [ "${ftp}" ]; then
        _ftp=${ftp}
    else
        echo "Ошибка параметра"
        return
    fi

    case "$_ftp" in
        on )
            echo "Включаем FTP.<br>"
            echo "Добавляем в автозагрузку<br>"
            cat > $initfile << "EOL"  && echo "$initfile создан успешно.<br>" || echo "<h3>ОШИБКА создания $initfile.</h3>"
#!/bin/sh
tcpsvd -vE 0.0.0.0 21 ftpd -w / &
EOL

            echo "Изменяем права файла $initfile<br>"
            if chmod 755 $initfile; then 
                echo "Права изменены.<br>";
            else
                echo "<h3>ОШИБКА изменения прав $initfile</h3>"
                return;
            fi

            echo "Запускаем FTP.<br>"
            sh $initfile &
            echo "FTP включен успешно.<br>"
        ;;

        off)
            echo "Выключаем FTP.<br>"
            echo "Убиваем процесс.<br>"
            killall -9 tcpsvd
            killall -9 ftpd
            #pidof tcpsvd | xargs kill -9
            echo "Убираем из автозагрузки.<br>"
            rm -f $initfile && echo "FTP выключен успешно.<br>" || echo "<h3>ОШИБКА удаления $initfile</h3>"
        ;;

        * )
        echo "<h3>ERROR! Неверный параметр для FTP.</h3>"
        ;;

    esac
}

setTELNET(){

    telnet=$(getvar telnet)

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
    rtsp=$(getvar rtsp)

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
            chmod +x /home/rtspsvr && echo "RTSP включен успешно.<br>" || echo "<h3>ОШИБКА включения /home/rtspsvr</h3>"
            #echo "<h3>Для запуска RTSP необходимо перезагрузить камеру.</h3><br>"
            echo "Запускаем RTSP<br>"
            /home/rtspsvr &
            echo "RTSP запущен успешно.<br>"

            #sed -i "s/portRtsp=554/portRtsp=5541/" /etc/ui.conf
        ;;

        off )
            chmod -x /home/rtspsvr && echo "RTSP выключен успешно.<br>" || echo "<h3>ОШИБКА отключения /home/rtspsvr</h3>"
            pidof rtspsvr | xargs kill -9

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
    pass=$(getvar pass)
    if [ ${pass} ]; then
        _newpass=${pass}
    else
        echo "Ошибка параметра"
        return
    fi

    #echo "$_newpass" | passwd root --stdin
    echo "${_newpass}" | chpasswd
}


chinaOFF(){
    metod=$(getvar metod)

    case "$metod" in
	1 )
	    echo "<h3>Заменяем url сервера проверки.</h3>"
	    echo "Создаем бэкап файла /home/cloud<br>"
	    cp -f /home/cloud /home/cloud_real
	
	    echo "Меняем url сервера<br>"
	    ps | grep /home/watch_process | grep -v "grep" | awk '{print $1}' | xargs kill -9
	    ps | grep /home/cloud | grep -v "grep" | awk '{print $1}' | xargs kill -9
	    sed -i 's|api.xiaoyi.com/v4/ipc/check_did|api.xiaoyi.cox/v4/ipc/check_did|g' /home/cloud

	    echo "Создаем файл в init.d для автоотвязки при обновлении.<br>"
	    cat > "/etc/init.d/S50nochina1" << "EOL"  && echo "/etc/init.d/S50nochina1 создан успешно.<br>" || echo "<h3>ОШИБКА создания /etc/init.d/S50nochina1</h3>"
#!/bin/sh
if [ ! -f /home/cloud_real ]; then
    cp -f /home/cloud /home/cloud_real
    ps | grep /home/watch_process | grep -v "grep" | awk '{print $1}' | xargs kill -9
    ps | grep /home/cloud | grep -v "grep" | awk '{print $1}' | xargs kill -9
    sed -i 's|api.xiaoyi.com/v4/ipc/check_did|api.xiaoyi.cox/v4/ipc/check_did|g' /home/cloud
    reboot
fi
EOL
	    chmod 755 /etc/init.d/S50nochina1
	    echo "Отвязка успешно завершена<br>"
	    echo "Камера будет перезагружена<br>"
	    sync
	    reboot
	;;
	
	2 )
	    echo "<h3>Подменяем ответ сервера проверки</h3>"
	    echo "Меняем файл API сервера<br>"
	    ps | grep /home/watch_process | grep -v "grep" | awk '{print $1}' | xargs kill -9
	    ps | grep /home/cloud | grep -v "grep" | awk '{print $1}' | xargs kill -9
	    ps | grep /home/cloudAPI | grep -v "grep" | awk '{print $1}' | xargs kill -9

	    echo "Создаем бэкап файла /home/cloudAPI<br>"
	    mv -f /home/cloudAPI /home/cloudAPI_real

	    cat << "EOL" >"/home/cloudAPI" && echo "/home/cloudAPI создан успешно.<br>" || echo "<h3>ОШИБКА создания /home/cloudAPI</h3>"
#!/bin/sh

if test "${4#*check_did}" != ${4}
then
  echo '{"allow":true,"code":"20000"}'
else
  ./cloudAPI_real $@
fi
EOL
	    echo "Создаем файл в init.d для автоотвязки при обновлении.<br>"
	    cat > "/etc/init.d/S50nochina2" << "EOL"  && echo "/etc/init.d/S50nochina2 создан успешно.<br>" || echo "<h3>ОШИБКА создания /etc/init.d/S50nochina2</h3>"
#!/bin/sh
if [ ! -f /home/cloudAPI_real ]; then
    #/home/app/script/killapp.sh
    ps | grep /home/watch_process | grep -v "grep" | awk '{print $1}' | xargs kill -9
    ps | grep /home/cloud | grep -v "grep" | awk '{print $1}' | xargs kill -9
    ps | grep /home/cloudAPI | grep -v "grep" | awk '{print $1}' | xargs kill -9

    mv -f /home/cloudAPI /home/cloudAPI_real
    cat >"/home/cloudAPI"<< "EOL2"
#!/bin/sh

if test "${4#*check_did}" != ${4}
then
  echo '{"allow":true,"code":"20000"}'
else
  ./cloudAPI_real $@
fi
EOL2
    sync
    reboot
fi
EOL
	    chmod 755 /etc/init.d/S50nochina2
	    echo "Отвязка успешно завершена<br>"
	    echo "Камера будет перезагружена<br>"
	    sync
	    reboot

	;;
	
	no )
	    echo "Убираем отвязку от Китая 1<br>"
	    rm -f /etc/init.d/S50nochina1
	    ps | grep /home/watch_process | grep -v "grep" | awk '{print $1}' | xargs kill -9
	    ps | grep /home/cloud | grep -v "grep" | awk '{print $1}' | xargs kill -9
	    cp -f /home/cloud_real /home/cloud

	    echo "Убираем отвязку от Китая 2<br>"
	    rm -f /etc/init.d/S50nochina2
	    ps | grep /home/watch_process | grep -v "grep" | awk '{print $1}' | xargs kill -9
	    ps | grep /home/cloud | grep -v "grep" | awk '{print $1}' | xargs kill -9
	    ps | grep /home/cloudAPI | grep -v "grep" | awk '{print $1}' | xargs kill -9
	    cp -f /home/cloudAPI_real /home/cloudAPI

	    echo "Отвязка успешно удалена<br>"
	    echo "Для завершения перезагрузите камеру<br>"
	;;
	* )
	    echo "Неверный параметр<br>"
	    return
	;;
    esac
}

rebootCAM(){
    reboot
}

offCAM(){
    poweroff
}

backupCAM(){
    _date=$(date +%Y%m%d)

    mtd3=$(getvar mtd3)
    mtd4=$(getvar mtd4)
    mtd5=$(getvar mtd5)
    mtd6=$(getvar mtd6)

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

cloudchina(){
    initfile="/etc/init.d/S90ntpd"
    cloud=$(getvar cloud)

    if [ -z $cloud ]; then
        echo "Ошибка параметра"
        return
    fi

    case "$cloud" in
        on )
            echo "Выключаем ntpd<br>"
            killall -9 ntpd
            rm -f $initfile

            echo "Измененяем формат таймзоны<br>"
            tzfile=$(cat /etc/TZ)
            carrentTZ=${tzfile//[^0-9]/}
            tztoset=$((8-carrentTZ))
            TZValue="GMT+$tztoset"
            echo "$TZValue" > /etc/TZ && echo "Временная зона изменена на $TZValue.<br>" || echo "<h3>ОШИБКА записи временной зоны.</h3>"

            echo "Включаем Китайские сервисы<br>"
            chmod +x /home/goolink /home/cloud /home/web/mini_httpd
            /home/cloud &
            ;;

        off)
            echo "<h3>Внимание! После этого перестанет работать стандартное мобильное приложение, доступ к камере будет только через telnet/ftp/http/rtsp!</h3>"
            echo "Выключаем Китайские сервисы<br>"
            chmod -x /home/goolink /home/cloud /home/web/mini_httpd
            killall -9 cloud
            killall -9 goolink
            killall -9 mini_httpd

            echo "Включаем запуск ntpd<br>"
            echo "while ! nslookup ru.pool.ntp.org; do sleep 1; done; ntpd -p ru.pool.ntp.org" > $initfile
            chmod 755 $initfile
            sh $initfile

            echo "Измененяем формат таймзоны<br>"
            tzfile=$(cat /etc/TZ)
            carrentTZ=${tzfile//[^0-9]/}
            tztoset=$((8-carrentTZ))
            TZValue="UTC-$tztoset"
            echo "$TZValue" > /etc/TZ && echo "Временная зона изменена на $TZValue.<br>" || echo "<h3>ОШИБКА записи временной зоны.</h3>"

        ;;

        * )
            echo "<h3>ERROR! Неверный параметр для TELNET.</h3>"
        ;;

    esac

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
#source ./post.cgi
cmd=$(getvar cmd)

if [ ${DEBUG} ]; then
    echo "metod=${REQUEST_METHOD}<br>"
    echo "get=$QUERY_STRING<br>"
    echo "post=${QUERY_STRING_POST}<br>"
    echo "cmd=${cmd}<br><hr />"
fi

#if [[ "${REQUEST_METHOD}" = "GET" ]]; then
#    echo "<h3>get больше не поддерживается. Используйте post</h3><br>"
#    exit 0
#fi

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

    chinaoff )
        echo "<h2>Отвязка от Китая.</h2><hr />"
        chinaOFF
        ;;

    backup )
        echo "<h2>Резервное копирование разделов.</h2><hr />"
        backupCAM
        ;;

    setcloud )
        echo "<h2>Изменение работы Китайских сервисов</h2><hr />"
        cloudchina
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
