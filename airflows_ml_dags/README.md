
Для того, чтобы развернуть airflow выполните команды:
~~~
1) для корректной работы с переменными, созданными из UI

  export FERNET_KEY=$(python -c "from cryptography.fernet import Fernet; FERNET_KEY = Fernet.generate_key().decode(); print(FERNET_KEY)")

2) развернуть докер

  docker-compose up --build
