
# Проект Yatube API
### Особенности проекта
Данное API предоставляет доступ к сервису Yatube, обеспечивающее возможность работы с ресурсами сайта. 
API позволяет просматривать список постов, групп и комментариев к конкретному посту, 
детальную информацию о посте, комментарии и группе, также возможно удаление, исправление, публикация новых постов и комментариев.
Также через API авторизованный пользователь может подписаться на автора.<br>

> Полный список ресурсов доступен по адресу `/redoc`
<!--- После загрузки на удаленный сервер будет живая ссылка --->
### Структура проекта:
Проект API состоит из приложений `posts, api`
1. Приложение `posts` определяет структуру хранимых данных, связанных с моделями: Follow, Post, Group.
2. Приложение `api` обрабатывает HTTP запросы клиента к ресурсам API.

### Инструкция по запуску проекта на своей машине:
1. Скачиваем репозиторий
2. Устанавливаем и активируем виртуальное окружение  
3. Устанавливаем зависимости `pip install -r requirements.txt`
4. Запустить миграции `python manage.py migrate`  
5. Создать суперюзера для доступа к админке `python manage.py createsuperuser`
6. Запуск проекта `python manage.py runserver`
### Инструкция по созданию dummy data
Открываем shell `python manage.py shell`, далее попеременно в терминал вводим следующие строчки кода, по окончании вызовите функцию `exit()`.
```{r}
>>> from posts.models import User, Post, Group, Comment
>>> user = User.objects.get(pk=1)
>>> group = Group.objects.create(title='Dummy group', slug='group')
>>> for i in range(1, 11):
...     Post.objects.create(author=user, group=group, text=f'Post text {i}')
>>> Comment.objects.create(post=Post.objects.get(pk=1), author=user, text='Comment text')
>>> User.objects.create(username='anotheruser')
```
### Примеры запросов в shell
Открываем shell `python manage.py shell`, далее попеременно в терминал вводим следующие строчки кода, по окончании вызовите функцию `exit()`.
```{r}
# Пример GET-запроса, не требующего авторизации
>>> import requests
>>> import json
>>> from django.urls import reverse
>>> domain = 'http://127.0.0.1:8000'
>>> response = requests.get(domain + reverse('api:post-list'))
>>> assert (response.status_code == 200)

# Получение JWT-токена для работы с ресурсами, требующими авторизации
>>> data = {"username": "<your_username>", "password": "<your_password>"}
>>> response = requests.post(url=(domain + reverse('api:jwt-create')), data=data)
>>> assert (response.status_code == 200)
>>> JWT_token = 'Bearer ' + response.json().get("access")

# Пример POST-запроса с токеном
>>> data={text="Some text"}
>>> headers={"Authorization": JWT_token}
>>> response = requests.post(url=(domain + reverse('api:post-list')), data=data, headers=headers)
>>> assert (response.status_code == 201)
>>> response_auth.json() # созданный пост

# Пример POST-запроса без токена
>>> response = requests.post(url=(domain + reverse('api:post-list')), data=data)
>>> assert (response.status_code == 401)
```

