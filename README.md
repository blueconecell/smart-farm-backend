# smartFarm

스마트 팜을 조작해주는 앱

### poetry

poetry를 통해 가상환경을 구축하고 가상환경 안에서 서버를 실행시킨다.

https://python-poetry.org/docs/#installation

`poetry --version`명령어를 통해 설치를 확인한다.

`poetry init`으로 가상환경을 준비한다.(모든 내용에 엔터를 눌러 스킵해도 된다.)

`poetry shell`명령어로 가상환경 내부로 진입한다.

### django add start

- 시작하기

`python manage.py runserver`명령어로 서버를 실행시킨다.

- 변경사항 적용하기

```
You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
```

이런 경고문이 나오면 `python manage.py migrate`으로 변경사항을 적용시켜준다

- admin 계정 생성하기

`python manage.py createsuperuser`으로 admin 계정을 생성해줄 수 있다
