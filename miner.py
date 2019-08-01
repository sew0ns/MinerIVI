import colorama
import vk_api
import time
from datetime import datetime
from python_rucaptcha import ImageCaptcha

# Настройка публикации
message = '#хочумиллиард'
owner = '-15106510'
post = '289251'
count = 0

# Запуск скрипта
colorama.init()
author = 'win8de'
version = '1.0.0'
login_message = 'Авторизация успешно пройдена! Ваш ID: {}'
hello_message = 'Запуск IVI-Miner v{} | Разработчик {}'
count_message = 'Написано комментариев под постом IVI: {}'
print(colorama.Fore.MAGENTA + hello_message.format(version, colorama.Fore.GREEN + author) + colorama.Fore.RESET)

# Ключ RuCaptcha
ru_key = input("Введите ключ RuCaptcha: ")

def auth_handler():
    key = input("Введите код 2FA: ")
    remember_device = True
    return key, remember_device


def captcha_handler(captcha):
    print(colorama.Fore.MAGENTA + '[' + datetime.strftime(datetime.now(), "%H:%M:%S") + '] ' + 'Решение капчи... Пожалуйста, подождите...' + colorama.Fore.RESET)
    image_link = captcha.get_url()
    user_answer = ImageCaptcha.ImageCaptcha(rucaptcha_key=ru_key).captcha_handler(captcha_link=image_link)
    if not user_answer['error']:
        key = user_answer['captchaSolve']
    elif user_answer['error']:
        print(user_answer['errorBody']['text'])
        print(user_answer['errorBody']['id'])
    return captcha.try_again(key)

try:
    # Авторизация
    login = input("Логин: ")
    password = input("Пароль: ")
    vk_session = vk_api.VkApi(login, password, captcha_handler=captcha_handler,auth_handler=auth_handler);
    vk_session.auth()
    vk = vk_session.get_api()

    # Проверка страницы
    user_info = vk.users.get()
    user_id = user_info[0]["id"]
    print(colorama.Fore.GREEN + '[' + datetime.strftime(datetime.now(), "%H:%M:%S") + '] ' + login_message.format(user_id) + colorama.Fore.RESET)

    # Цикл
    while True:
        count = count + 1
        print(colorama.Fore.MAGENTA + '[' + datetime.strftime(datetime.now(), "%H:%M:%S") + '] ' + count_message.format(count) + colorama.Fore.RESET)
       # time.sleep(1)
        try:
            vk.wall.createComment(owner_id=owner, post_id=post, message=message)
            vk.account.setOnline()
        except:
            print('Ошибка решения капчи. Перезапуск...')
            time.sleep(1)
            continue
except:
    print(colorama.Fore.RED + 'Сбой запуска!' + colorama.Fore.RESET)



