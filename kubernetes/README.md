В этой ДЗ использовался докер образ из ДЗ 2

Образ размещен на dockerhub - https://hub.docker.com/layers/koluzajka/mlops_made/latest/images/sha256-0da2f0f1395f9ec64087a0b10a33630e9cb57fb5cc90bfd9ac8fe550c95f8ac5?context=explore Его размер 270 MB

**Скачать образ с DockerHub:**

  docker pull koluzajka/mlops_made:latest 

**Запустить локально:**

  docker run -p 8000:8000 koluzajka/mlops_made:latest
