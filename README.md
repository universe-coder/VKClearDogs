# VKClearDogs

## О программе

Инструмент для чистки от собачек: группы,профили и чаты во ВКонтакте

## Установка

1. Устанавливаем **Python**  
2. Вводим команду в папке проекта: **pip install -r requirements.txt**  
3. Настраиваем конфиг в **config.json**  
4. Готово

## Использование

В папке проекта имеются три ключевых скрипта:

- **chat.py** - Удаление собачек в чате  
- **group.py** - Удаление собачек в группе  
- **profile.py** - Удаление собачек в профиле  

Один из способов запустить скрипт: **python имя_скрипта.py**

## Конфиг (config.json)

```JS
{
  "access_token": "", // Токен доступа к VK API
  "profile": {
    "id": 137510740, // ID профиля где удалять собачки
    "limit": 154, // Максимальное количество удаленых собачек
    "sleep": 3.1 // Время задержки в секундах
  },
  "chat": {
    "id": 294, // ID чата где удалять собачки
    "limit": 100, // Максимальное количество удаленых собачек
    "sleep": 3 // Время задержки в секундах
  },
  "group": {
    "id": 176413818, // ID группы где удалять собачки
    "limit": 100, // Максимальное количество удаленых собачек
    "sleep": 3 // Время задержки в секундах
  }
}
```

## Возможные проблемы

Проблема: **ImportError: cannot import name 'Iterable' from 'collections'**  
Решение: [https://ru.stackoverflow.com/questions/1389580/importerror-cannot-import-name-iterable-from-collections](https://ru.stackoverflow.com/questions/1389580/importerror-cannot-import-name-iterable-from-collections)

## Поддержать автора

[https://yoomoney.ru/to/410012335150397](https://yoomoney.ru/to/410012335150397)
