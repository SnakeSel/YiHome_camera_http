#!/bin/bash

#source ./template/func

########################################
# Переменные
########################################

# Общая
_uptime=$(uptime)
#_firmware=$(cat /home/version | grep version -m1)
_firmware=$(sed -n 's/version=\(........\).*/\1/p' /home/version)

# Сеть
_wifi=$(grep -m1 "ssid" /etc/wpa_supplicant.conf | sed 's/ssid=//')
_ip=$(ipaddr | grep ra0 | tail -n 1 | awk '{print $2}' | sed 's/\/24//')
_port=$(netstat -tualnp)


# сервисы
#_srvrtsp=$([ "$(pidof rtspsvr)" ] && echo UP || echo DOWN)
_srvtelnet=$([ "$(pidof telnetd)" ] && echo UP || echo DOWN)
_srvftp=$([ "$(pidof tcpsvd)" ] && echo UP || echo DOWN)

if [ "$(pidof rtspsvr)" ];then
    _srvrtsp="UP"
    rtspstream="| <b>stream:</b> <a href="rtsp://${_ip}:554/ch0.h264">HD</a> | <a href="rtsp://${_ip}:554/ch1.h264">SD</a>"
else
    _srvrtsp="DOWN"
    rtspstream=""
fi

# Ресурсы
_df=$(df -h | grep -v 'tmpfs')
_free=$(free)
#_cpu=$(ps | awk '{s += $3} END {print s "%"}')


########################################
# HTML страница
########################################
cat header

cat << EOF
   <table width="100%" cellpadding="0" cellspacing="10" border="0">
    <tbody>
        <tr>
            <td width="40%">
                <h2>Общая информация</h2>
                <ul>
                    <li><strong>Uptime:</strong> ${_uptime}</li>
                    <li><strong>Firmware:</strong> ${_firmware}</li>
                </ul>
            </td>

            <td width="2" bgcolor="#000000"></td>

            <td>
                <h2>Сервисы</h2>
                <ul>
                  <li><strong>RTSP:    </strong> ${_srvrtsp} $rtspstream</li>
                  <li><strong>telnet:  </strong> ${_srvtelnet}</li>
                  <li><strong>FTP:     </strong> ${_srvftp}</li>
                </ul>
            </td>

            <td width="2" bgcolor="#000000"></td>

            <td width="40%">
                <h2>Сеть</h2>
                <ul>
                  <li><strong>Wi-Fi:</strong> ${_wifi}</li>
                  <li><strong>IP:</strong> ${_ip}</li>
                  <li>
                    <div class="spoil">
                      <div class="smallfont"><input type="button" value="Открытые порты" class="input-button" onclick="if (this.parentNode.parentNode.getElementsByTagName('div')[1].getElementsByTagName('div')[0].style.display != '') { this.parentNode.parentNode.getElementsByTagName('div')[1].getElementsByTagName('div')[0].style.display = ''; this.innerText = ''; this.value = 'Свернуть'; } else { this.parentNode.parentNode.getElementsByTagName('div')[1].getElementsByTagName('div')[0].style.display = 'none'; this.innerText = ''; this.value = 'Открытые порты'; }"/>
                      </div>
                      <div class="alt2">
                        <div style="display: none; text-align:left;">
                        <pre>${_port}</pre>
                        </div>
                      </div>
                    </div>
                  </li>
                </ul>
            </td>

        </tr>
    </tbody>
    </table>

    <h2>Ресурсы</h2>
    <table border="1" cellpadding="2">
      <thead>
        <tr>
          <th scope="col">Диск</th>
          <th scope="col">ОЗУ</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><pre>${_df}</pre></td>
          <td><pre>${_free}</pre></td>
        </tr>
      </tbody>
    </table>
</br>
</br>
EOF
cat footer

exit 0
