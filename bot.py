import subprocess
import telegram
import paramiko
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext import filters, Filters

TOKEN = 'ТОКЕН_ВАШЕГО_СОЗДАНОГО_БОА'
ALLOWED_USERS = [Список, ID, Телеграма, кому разрешено пользоватся ботом, список ИД указывать через запятую]  # список user_id разрешенных пользователей
REMOTE_SERVER_IP = '192.168.0.50'  # адрес удаленного сервера


def start(update, context):
    """Обработчик команды /start."""
    update.message.reply_text('Привет! Я бот поисковой системы.')

def command(update, context):
    """Обработчик команды."""
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        update.message.reply_text('У вас нет разрешения использовать этого бота.')
        return

    # Получение текста команды пользователя
    cmd = update.message.text[len('/command '):]

    # Выполнение команды на удаленном сервере
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(REMOTE_SERVER_IP, username='user')	#, password='password')
    stdin, stdout, stderr = ssh.exec_command(cmd)
    result = stdout.read().decode('utf-8')

    # Отправка результатов пользователю
    update.message.reply_text(result)

def search(update, context):
    """Обработчик текстовых сообщений."""
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        update.message.reply_text('У вас нет разрешения использовать этого бота.')
        return

    # Получение текста сообщения пользователя
    search_query = update.message.text

    # Выполнение поискового запроса на удаленном сервере
    cmd = f'ssh root@{REMOTE_SERVER_IP} "bash ./searchGPT2.sh {search_query}"'
    result = subprocess.check_output(cmd, shell=True).decode('utf-8')

# Разделение ответа на части, если он превышает максимальную длину сообщения
    max_message_length = telegram.constants.MAX_MESSAGE_LENGTH
    result_parts = [result[i:i+max_message_length] for i in range(0, len(result), max_message_length)]

    # Отправка результатов пользователю
    for part in result_parts:
        update.message.reply_text(part)

    # Отправка результатов пользователю
   # update.message.reply_text(result)


def command2(update, context):
    """Обработчик текстовых сообщений."""
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        update.message.reply_text('У вас нет разрешения использовать этого бота.')
        return

    # Получение текста сообщения пользователя
    search_query = update.message.text

    # Выполнение поискового запроса на удаленном сервере
    cmd = f'ssh root@{REMOTE_SERVER_IP} "{search_query}"'
    result = subprocess.check_output(cmd, shell=True).decode('utf-8')

# Разделение ответа на части, если он превышает максимальную длину сообщения
    max_message_length = telegram.constants.MAX_MESSAGE_LENGTH
    result_parts = [result[i:i+max_message_length] for i in range(0, len(result), max_message_length)]

    # Отправка результатов пользователю
    for part in result_parts:
        update.message.reply_text(part)


def main():
    """Главная функция для запуска бота."""
    updater = Updater(TOKEN, use_context=True)

    # Добавление обработчиков команд
    updater.dispatcher.add_handler(CommandHandler('start', start))

    # Добавление обработчиков текстовых сообщений
    updater.dispatcher.add_handler(MessageHandler(Filters.text, search, command2))

    # Запуск бота
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
