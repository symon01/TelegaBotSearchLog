#!/bin/bash

# запрос для поиска в файле
search_query="$1"

# ключевые слова для парсинга данных
keyword1="SIP"
keyword2="record"
keyword3="DIALSTATUS"

# путь к файлу, в котором нужно искать
file_path="/var/log/asterisk/full"

# сколько последних строк лога нужно обработать
num_lines=100000

# ищем строки, содержащие запрос, в последних 10000 строках файла,
# и выводим только те строки, в которых есть упоминание хотя бы одного ключевого слова
tail -n $num_lines $file_path | grep "$search_query" | grep -E "$keyword1|$keyword2|$keyword3"
