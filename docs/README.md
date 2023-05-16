## Вопросы на демо:

```
1) Нейминг эндпоинтов, в частности disable == delete? 
2) Что с админом можно ли использовать фласк админ?
3) JWT токен как отдельный класс который работает в рамках AUTH, или отдельные endpoints?
4) Как назначаются роли? 
```

## Service logic:
#### DB model scheme:

```
1. Информация о пользователе:
- id: uuid4(pk)
- login: str(unique)
- first_name
- last_name
- role_id
- password: str
- country
- language
- email
- phone_number
- timezone
- city(optional)
- created_at
- updated_at
- is_active: bool
- subscription(записывается время истечения подписки)
- birth date
- avatar

2. инф о входе
- id записи
- id пользователя 
- user_agent
- timestamp

3. Роли
- id записи
- name
- timestamp
- description
```

#### Algorithm 
```
1 сценарий - новый пользователь
1) аноним заходит на страничку(r)
2) создание пользователя (c)

2 сценарий - существующий пользователь
1) аноним заходит на страничку(r)
2) логинится (u)
3) не аноним читает контент (r)
4) обновление инф о пользователе (u)
5) удаление аккаунта (d) 
6) выход (u)
```
#### Endpoints

```
User Auth Options
POST /api/v1/auth/signup {body}
POST /api/v1/auth/signin {body}
POST /api/v1/auth/signout {body}

User Actions
DELETE /api/v1/auth/user/{user_id}
PATCH /api/v1/auth/user/{user_id}
GET /api/v1/auth/user/{user_id}

JWT options
POST /api/v1/auth/token/create
POST /api/v1/auth/token/refresh

Admin options:

возьмём из фласк(попробуем)
```

