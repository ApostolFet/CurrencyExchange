# Деплой приложения 

1. Склонировать репозиторий на сервер

```sh
  git clone git@github.com:ApostolFet/CurrencyExchange.git
  cd CurrencyExchange
```

2. Создать виртуальное окружение

```sh
python -m venv .venv
```
3. Активировать виртуальное окружение

```sh
. .venv/bin/activate
```

4. Установить пакет

```sh
pip install .
```

5. Скопировать пример конфига в config.toml
```sh
cp config.example.toml config.toml
```

6. Откройте кофиг и отредактируйте параметры
```sh
nano config.toml
```

7. Выполните миграции базы данных:
```sh
currency-exchange-migrations-up
```


8. Скопируйте шаблон сервисного файла в директорию, где находятся ваши сервисы.
  ```sh
  cp ./systemd/currency_exchange.service /etc/systemd/system/
  ```

9. Изменить в шаблоне путь до рабочей категории и до виртуального окружения
  ```sh
  nano /etc/systemd/system/currency_exchange.service
  ```

Пример заполненного шаблона:
```service
[Unit]
Description=CurrencyExchange APP
After=network.target


[Service]
WorkingDirectory=/home/user_name/projects/CurrencyExchange/
ExecStart=/home/user_name/projects/CurrencyExchange/.venv/bin/currency-exchange-run
Restart=on-failure


[Install]
WantedBy=multi-user.target
```

10. После сохранения сервисного файла включите службу
```sh
systemctl enable currency_exchange.service
```
Если вы изменяете сервисный файл, то для обновлния конфигурации нужно выполнить следующую команду
```sh
systemctl daemon-reload
```

11. Запустите службу: 
```sh
systemctl start currency_exchange.service 
```

После запуска службы, приложение должено начать корректно работать

Полезные команды:

- Просмотр журнала службы:
```sh
journalctl -u currency_exchange.service
```


- Просмотр статуса службы:
```sh
systemctl status currency_exchange.service
```
