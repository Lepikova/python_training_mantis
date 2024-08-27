from model.project import Project


def test_delete_first_project(app, ensure_login):
    # Получаю список проектов до удаления через SOAP API
    projects = app.soap.get_project_list()

    # Вывожу список проектов до удаления
    print("Список проектов до удаления:", projects)

    # Создаю новый проект, если проектов нет
    if len(projects) == 0:
        new_project = Project(name="чтобы было")
        app.project.create(new_project)

        # После создания проекта снова получаю список через SOAP API
        projects = app.soap.get_project_list()
        print("Список проектов после добавления нового проекта (для удаления):", projects)

    # Удаляю первый проект из списка
    app.project.delete_first_project()

    # Получаю список проектов после удаления через SOAP API
    updated_projects = app.soap.get_project_list()

    # Вывожу список проектов после удаления
    print("Список проектов после удаления:", updated_projects)

    # Проверяю, что проект был удалён
    assert len(updated_projects) == len(projects) - 1, "Количество проектов не уменьшилось на 1 после удаления."
    assert all(project["name"] != projects[0]["name"] for project in
               updated_projects), "Удаленный проект все еще присутствует в списке."
