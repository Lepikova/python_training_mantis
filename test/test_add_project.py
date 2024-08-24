from model.project import Project


def test_add_project(app):
    # Создаем уникальное имя для проекта
    base_project_name = "TestProject"
    unique_project_name = base_project_name
    while app.project.is_project_exists(unique_project_name):
        unique_project_name = app.project.generate_unique_name(base_project_name)

    new_project = Project(name=unique_project_name)

    # Шаг 1: Получаем список проектов до добавления нового
    old_projects = app.project.get_project_list()

    # Шаг 2: Добавляем новый проект
    app.project.create(new_project)

    # Шаг 3: Получаем список проектов после добавления нового
    new_projects = app.project.get_project_list()

    # Шаг 4: Проверяем, что новый проект был добавлен
    assert len(new_projects) == len(old_projects) + 1

    # Проверяем, что новый проект присутствует в списке
    added_project = next((p for p in new_projects if p["name"] == new_project.name), None)
