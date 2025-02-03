- репозиторий с лабой должен быть публичным
- зайти на coveralls.io
- перейти в repos
- если нет репозиториев - будет инструкция по подключению, откуда из 3 пункта взять токен `COVERALLS_REPO_TOKEN` с его значение `5c2dVjFbjmdjX2hLt4bYyAwkDU4C2TPZC` из кучи символов и вставить его на гитхабе в settings/secrets and variables/actions в repository secrets добавить новый repository secret, введя имя и значение.
- Вставить в код файла ./github/workflows/python_app.yml это:

>- name: Upload coverage to Coveralls
        env:
          COVERALLS_REPO_TOKEN: ${{ secrets.COVERALLS_REPO_TOKEN }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: coveralls

- запушить
- вставить в README.md эту штуку (ссылки на репозитории coveralls и github):

> \[\!\[Coverage Status](https://coveralls.io/repos/github/ipaingo/square_root_test/badge.svg?branch=main)](https://coveralls.io/github/ipaingo/square_root_test?branch=main)

[![Coverage Status](https://coveralls.io/repos/github/ipaingo/square_root_test/badge.svg?branch=main)](https://coveralls.io/github/ipaingo/square_root_test?branch=main)

- тут ссылка на репозиторий в coveralls и репозиторий на github
- теперь coveralls отслеживает состояние уровня покрытия кода тестами, грац.

По такому же принципу нужно вписать бейдж, свидетельствующий об успешном прохождении прописанных нами тестов Python

> \[\!\[Python tests](https://github.com/ipaingo/square_root_test/actions/workflows/python_app.yml/badge.svg)](https://github.com/ipaingo/square_root_test/actions/workflows/python_app.yml)

[![Python tests](https://github.com/ipaingo/square_root_test/actions/workflows/python_app.yml/badge.svg)](https://github.com/ipaingo/square_root_test/actions/workflows/python_app.yml)