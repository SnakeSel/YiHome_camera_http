#!/bin/bash

########################################
# Переменные
########################################

cmdurl=/cmd.cgi/

# Подсчет TZ
#carrentTZ=$(cat /etc/TZ | sed 's/GMT//')
tzfile=$(cat /etc/TZ)
carrentTZ=${tzfile//[^0-9+-]/}
# Если cloud исполняемый, тогда время GMT8-
if [ -x /home/cloud ]; then
    _tz=$((8-carrentTZ))
else
    _tz=$carrentTZ
fi

# На всякий еще раз оставляем только цифры и + -
#_tz=${_tz//[^0-9+-]/}

# Services
[ "$(pidof tcpsvd)" ] && _ftpon="checked" || _ftpoff="checked"
[ "$(pidof telnetd)" ] && _telneton="checked" || _telnetoff="checked"

if [ ! -f /home/rtspsvr ]; then
    _rtspdisable="disabled"
fi

if [ -x /home/rtspsvr ]; then
    _rtspon="checked"
else
    _rtspoff="checked"
fi

if [ -x /home/cloud ]; then
    _cloudon="checked"
else
    _cloudoff="checked"
fi

# Backup
_dfhd1=$(df -h | grep hd1 | awk '{print $4}')
_date=$(date +%Y%m%d)
[ "$_dfhd1" ] && _disableHD1="" || _disableHD1="disabled"


########################################
# HTML страница
########################################
cat header
cat << EOF
    <table border="1" cellpadding="4" cellspacing="0" align="center" >
    <tbody>
        <tr>
            <td>
                <form action="$cmdurl" method="get">
                    <p><h3>FTP</h3></p>
                    <p><input type="radio"  $_ftpon name="ftp" value="on" />Включен</p>
                    <p><input type="radio"  $_ftpoff name="ftp" value="off" />Выключен</p>
                    <p><button type="submit" name="cmd" value="setftp">Изменить</button></p>
                </form>
                </td>
            <td>
                <form action="$cmdurl" method="get">
                    <p><h3>Telnet</h3></p>

                    <p><input type="radio"  ${_telneton} name="telnet" value="on" />Включен</p>
                    <p><input type="radio"  ${_telnetoff} name="telnet" value="off" />Выключен</p>
                    <p><button type="submit" name="cmd" value="settelnet">Изменить</button></p>
                </form>

            </td>
            <td>
                <form action="$cmdurl" method="get">
                    <p><h3>RTSP</h3></p>
 
                    <p><input type="radio"  ${_rtspon} name="rtsp" value="on"  ${_rtspdisable}/>Включен</p>
                    <p><input type="radio"  ${_rtspoff} name="rtsp" value="off"  ${_rtspdisable}/>Выключен</p>
                    <p><button type="submit" name="cmd" value="setrtsp"  ${_rtspdisable}>Изменить</button></p>
                </form>

            </td>
            <td>
                <form action="$cmdurl" method="get">
                    <p><h3>Китайские<br>сервисы</h3></p>
 
                    <p><input type="radio"  ${_cloudon} name="cloud" value="on" />Включен</p>
                    <p><input type="radio"  ${_cloudoff} name="cloud" value="off" />Выключен</p>
                    <p><button type="submit" name="cmd" value="setcloud" >Изменить</button></p>
                </form>

            </td>

        </tr>
    </tbody>
    </table>

    <hr />
    <table width="100%" cellpadding="0" cellspacing="10" border="0">
    <tbody>
        <tr>
            <td>
                <form action="$cmdurl" method="get">
                    <h3>Часовой пояс</h3>
                    Текущее время:<br>
                    $(date)<br>
                    <p><input type=number size=2 maxlength=1 name="tz" value="${_tz}" /></p>
                    <p><button type="submit" name="cmd" value="settz">Изменить</button></p>
                </form>
            </td>
            <td width="2" bgcolor="#000000"></td>
		<td>
		    <form action="$cmdurl" method="get">
		      <p><h3>Бэкап разделов камеры.</h3></p>
		      <p>Сохранение на карту памяти в папку: "backup/${_date}"</p>
		      <p>Свободно на карте: ${_dfhd1}${_disableHD1}</p>
		      <p><input type="checkbox"  name="mtd3" ${_disableHD1}/>mtd3 (os)</p>
		      <p><input type="checkbox"  name="mtd4" ${_disableHD1}/>mtd4 (rootfs)</p>
		      <p><input type="checkbox"  name="mtd5" ${_disableHD1}/>mtd5 (home)</p>
		      <p><input type="checkbox"  name="mtd6" ${_disableHD1}/>mtd6 (vd)</p>
		      <p><button type="submit" name="cmd" value="backup" ${_disableHD1}>Сохранить</button></p>
		    </form>

		</td>
         <!--   <td>
                <form action="$cmdurl" method="get">
                    <h3>Отвязка от китая</h3>
                    Только для китайских версий камеры.<br>
                    Исправляет ошибку "Камера работает только в Китае"<br>
                    <select name="metod">
                        <option value="1" selected>Замена адреса сервера</option>
                        <option value="2">Замена кода ответа</option>
                        <option value="no">Убрать отвязку</option>
                    </select>
                    <p><button type="submit" name="cmd" value="chinaoff">Применить</button></p>
                </form>
            </td>
            <td width="2" bgcolor="#000000"></td>
            <td>
                <form action="$cmdurl" accept-charset="utf-8" method="get">
                    <h3>Изменить пароль пользователя root</h3>
                    Доступ по телнет будет возможен только по новому паролю!<br>
                    В целях избежания ошибок скрипта, используйте только латинские буквы и цифры (без спец символов).
                    <p><input type="password"  name="pass" /></p>
                    <p><button type="submit" name="cmd" value="setpasswd">Изменить</button></p>
                </form>
            </td> -->
        </tr>
    </tbody>
    </table>

EOF
cat footer

exit 0
