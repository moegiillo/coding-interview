# coding-interview

## API Server 起動

```bash
# PostgreSQLコンテナ作成・起動
$ docker compose up --build

# python 仮想環境作成、migration
$ pipenv sync
$ pipenv shell
$ python manage.py migrate

# Django server 起動
$ python manage.py runserver
```

## API テスト

```bash
# PostgreSQLコンテナ作成・起動
$ docker compose up --build

# python 仮想環境作成、migration
$ pipenv sync
$ pipenv shell
$ python manage.py migrate

# テスト実行
$ python manage.py test -v 2
```
