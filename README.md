<h1>Cкрипт оценки репозиториев Github</h1>

<h3>Требования:</h3>

* Версия Python - от 3.6.x


<h3>Что делает cкрипт:</h3>

Скрипт принимает на вход ссылку на открытый репозиторий пользователя Github и выставляет ему оценку по следующим критериям:
<h1>Cкрипт оценки репозиториев Github</h1>

<h3>Требования:</h3>

* Версия Python - от 3.6.x


<h3>Что делает cкрипт:</h3>

Скрипт принимает на вход ссылку на открытый репозиторий пользователя Github и выставляет ему оценку по следующим критериям:

* Количество звёзд (0 звёзд – 0 баллов, 1-50 – 1 балл, >50 – 2 балла).
* Количество контрибьюторов (1 – 0 баллов, 2-10 – 1 балл, > 10 – 2 балла).
* Наличие лицензии (1 балл, если есть).
* Наличие ридми (1 балл, если есть).
* Наличие смердженных пул-реквестов за последние 30 дней (1, если есть).
* Наличие интеграции с Travis CI (1, если есть).
* Наличие форков (1, если есть).
* Наличие .editorconfig (1, если есть).

По результатам оценки скрипт выдает итоговое количество баллов, которое набрал репозиторий.


<h4>Как пользоваться скриптом: </h4>

1. Скачайте репозиторий к себе локально
2. В командной строке перейдите в директорию, где сохранён репозиторий
3. Запустите файл scoring_repos.py

```
$ python scoring_repos.py
> python scoring_repos.py 
```

4. В консоли появится предложение ввести название репозитория в формате аккаунт/название репозитория

```
>python scoring_repos.py
Укажите репозиторий в формате owner/repo
devmanorg/fiasko_bro # пример ввода репозитория
```
5. На выходе cкрипт выдает оценку в таком формате.
```
>python scoring_repos.py
Укажите репозиторий в формате owner/repo
devmanorg/fiasko_bro
Оценка репо: 8
```
Спасибо [@Melevir](https://github.com/Melevir) за помощь в этом нелегком деле :)

Если у вас остались какие-то вопросы, можете писать мне [сюда](https://t.me/TanyaKulagina) :)