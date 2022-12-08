**Предсказание модели классификации FastAPI + Docker**

**Сборка образа**

Для сборки образа и последующего запуска необходимо выполнить команды:

    docker build . -f online_inference/Dockerfile -t my_api:v1 .

    docker run -p 8000:8000 online_inference/my_api:v1

Внутри контейнера будет запущен сервис, посылать запросы к сервису можно с помощью скрипта make_request.py

    python3 make_request.py --host HOST --port PORT --data_path PATH_TO_DATA

Параметры по умолчанию:

    HOST = "localhost"
    PORT = 8000
    PATH_TO_DATA = "./data/data.csv"


**Образ** размещен на dockerhub - https://hub.docker.com/layers/koluzajka/mlops_made/latest/images/sha256-0da2f0f1395f9ec64087a0b10a33630e9cb57fb5cc90bfd9ac8fe550c95f8ac5?context=explore
Его размер 270 MB

**Скачать образ с DockerHub:**

     docker pull koluzajka/mlops_made:latest 
 
**Запустить локально:**

    docker run -p 8000:8000 koluzajka/mlops_made:latest

**Запуск тестов**

Тесты располагаются в папке online_inference/testy.py

      pytest testy.py
