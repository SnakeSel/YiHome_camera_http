#!/bin/sh

records="/tmp/hd1/record"

printf "Content-type: text/html\r\n\r\n"
printf "<!DOCTYPE html>\r\n"
printf "<html lang=\"ru\">\r\n"
printf "<head>\r\n"
printf "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">\r\n"
printf "<meta name=\"author\" content=\"Корниенко Аркадий Борисович\">\r\n"
printf "<title>Содержание sd-карты камеры</title>\r\n"
printf "<style>\r\n"
printf "body {padding: 0 0 50px 25px}\r\n"
printf ".f18 {font-size:18px;font-weight:bold;text-decoration:none}\r\n"
printf ".hid {visibility:hidden}\r\n"
printf "</style>\r\n"
printf "</head>\r\n"
printf "<body>\r\n"

cat << EOF
   <header>
      <a href="/"><img alt="" src="yi.jpg" style="width: 30px; height: 30px; float: left;" /></a>
      <h1>&nbsp;Xiaomi Yi Home Camera</h1>
    </header>
    <hr />
    <nav>
      <a href="/">Начало</a>  |
      <a href="/video/" target="_blank">Файлы</a> |
      <strong>Записи</strong> |
      <a href="/cfg.cgi">Настройки</a>
    </nav>
    <hr />
EOF

if [ "$QUERY_STRING" ]; then

  printf "<h2>Содержание&nbsp;папки $QUERY_STRING &nbsp;на&nbsp;камерe</h2>\r\n"
  printf "<a href=\"#\" onClick=\"history.go(-1)\"><strong>Вернуться</strong></a><br><br>\r\n"

  printf "<video id=\"video\" style=\"position:fixed;left:400px;top:300px;width:720px\" controls autoplay></video>\r\n"

  printf "<table>\r\n"
  printf "<tr><td width=100><b>Время (минута)</b><td width=150><b>Имя файла</b><td width=150><b>Сохранить файл</b>\r\n"

  #for f in `ls -r ${records}/$QUERY_STRING | grep mp4`; do
  for f in $(ls -r ${records}/$QUERY_STRING | grep -E '^[0-9]{2}M[0-9]{2}S*\.mp4$'); do
#    if [ ${#f} == 10 ]; then
        fl="/video/${QUERY_STRING}/${f}"
        printf "<tr>\n"
        printf "<td> %s" "${f:0:2}"
        printf "<td> %s" "<a href=\"javascript:document.getElementById('video').setAttribute('src','${fl}')\" onclick=\"this.style.color='rgb(85,26,139)'\">${f}</a>"
        printf "<td> %s\n" "<a href=\"${fl}\" class=\"f18\" onclick=\"this.style.color='rgb(85,26,139)'\" download=\"${f}\">&#128190;</a>" #&#128427;
#    fi
  done

else

  printf "<h2>Содержание&nbsp;sd-карты&nbsp;камеры</h2>\r\n"
  printf "<table>\r\n"
  printf "<tr><td width=250><b>Дата и время</b><td width=250><b>Папка</b>\r\n"

  for f in `ls -r ${records} | grep H`; do
    if [ ${#f} == 14 ]; then
        printf "<tr>\n"
        printf "<td> %s" "${f:8:2}-${f:5:2}-${f:0:4} ${f:11:2}:00"
        printf "<td> %s\n" "<a href=?${f}>${f}</a><span class=\"f18 hid\">&#128427;</span>"
    fi
  done

fi

printf "</table>\r\n"
printf "</body>\r\n"
printf "</html>\r\n"
