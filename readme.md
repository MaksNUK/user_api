# userAPI

### Задание:

> Используя Percona MySQL 8.0.23, Python 3.6 и Flask разработать REST API,
обеспечивающий проверку Request и Response данных и документацию в Swagger UI.

### REST API должен иметь следующий функционал:
1. Создание и авторизацию пользователя по паре login/password.
2. Каждый авторизованный пользователь должен иметь возможность ввода и редактирования своего профиля (имя, аватар).
3. Каждый авторизованный пользователь должен иметь возможность создания списка товаров, доступных только ему.
4. Каждый товар должен иметь уникальный идентификатор, артикул (уникален в пределах списка товаров пользователя), название и картинку.
5. Товар может содержать набор цен (любое неограниченное количество) в различных валютах с условием, что для каждой валюты может быть задана только одна цена.
6. Постраничный вывода списка товаров с возможностью фильтрации по артикулу (соответствие) и по имени (вхождение) и сортировки по артикулу или имени.

### Стек:
- Percona MySQL 8.0.23*
- Python 3.6*
- Flask*
- connexion 2.9.0
- SQLAlchemy 1.4.23


### Docker-compose
Для запуска:
```sh
docker-compose up
```
