База телефонных номеров

Как все это запускать?
- создаем папку
- cd в папку
- git init
- git clone https://github.com/AlekseiKhatkevich/telephone_numbers.git
- cd .\telephone_numbers\
- docker-compose up --build -d
- docker-compose exec web python manage.py migrate
- docker-compose exec web python manage.py populate (ждем минутку пока данные не зальются в базу данных)
- docker-compose exec web pytest (проверяем все тестами)
- вроде все...

