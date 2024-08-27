from model.project import Project

def test_add_project(app, ensure_login):
    # Создаю уникальное имя для проекта
    base_project_name = "TestProject"
    unique_project_name = base_project_name

    while app.project.is_project_exists(unique_project_name):
        unique_project_name = app.project.generate_unique_name(base_project_name)

    new_project = Project(name=unique_project_name)

    # Шаг 1: Получаю список проектов до добавления нового через SOAP API
    old_projects = app.soap.get_project_list()

    # Вывожу список проектов до добавления нового
    print("Список проектов до добавления нового:", old_projects)

    # Шаг 2: Добавляю новый проект через веб-интерфейс
    app.project.create(new_project)

    # Шаг 3: Получаю список проектов после добавления нового через SOAP API
    new_projects = app.soap.get_project_list()

    # Вывожу список проектов после добавления нового
    print("Список проектов после добавления нового:", new_projects)

    # Шаг 4: Проверяю, что новый проект был добавлен
    assert len(new_projects) == len(old_projects) + 1

    # Проверяю, что новый проект присутствует в списке
    added_project = next((p for p in new_projects if p['name'] == new_project.name), None)
    assert added_project is not None, f"Проект {new_project.name} не был найден в новом списке проектов."
