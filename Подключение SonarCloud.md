- следовать инструкции, выложенной Кулаковым на каппе, зайти на sonarcloud.io
- зайти туда с помощью своего github, полностью заполнив всё, что от тебя хотят
- выбрать в открывшемся списке свой аккаунт и свой репозиторий
- после пропадания всех окон зайти в левую нижнюю вкладку Administration, затем Analysis Method
- там выбрать Analyze a project with Github Actions
- ввести имя `SONAR_TOKEN` и значение `d4ba0bb65048ed6d92f44f90ca9efa4ec6ae8f2b` токена на гитхабе в settings/secrets and variables/actions в repository secrets добавить новый repository secret
- там же sonarcloud заботливо даст целый гайд, согласно которому нужно выбрать опцию python project
- по этому гайду нужно создать файл sonarcloud.yml и вставить туда содержимое из гайда (просто скопировать готовенький код из гайда и вставить в файл, да-да)
- по нему же создать файл sonarcloud.properties и вставить туда уже готовое, находящиеся в гайде его содержимое
- завести в файле `README.md` бейджи с сонарклауда, вписав в них свой project id, его можно глянуть, зайдя в My Projects > выбрать свой проект > Administration слева снизу в углу экрана > Update Key > скопировать ключ (твой: `ipaingo_square_root_test`)

> \[\!\[Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ipaingo_square_root_test&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=ipaingo_square_root_test)
> 
>\[\!\[Bugs](https://sonarcloud.io/api/project_badges/measure?project=ipaingo_square_root_test&metric=bugs)](https://sonarcloud.io/summary/new_code?id=ipaingo_square_root_test)
>
>\[\!\[Code Smells](https://sonarcloud.io/api/project_badges/measure?project=ipaingo_square_root_test&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=ipaingo_square_root_tes
>
>\[\!\[Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=ipaingo_square_root_test&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ipaingo_square_root_test&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=ipaingo_square_root_test)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=ipaingo_square_root_test&metric=bugs)](https://sonarcloud.io/summary/new_code?id=ipaingo_square_root_test)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=ipaingo_square_root_test&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=ipaingo_square_root_test)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=ipaingo_square_root_test&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?)