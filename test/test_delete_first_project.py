from model.project import Project


def test_delete_first_project(app):
    app.project.open_manage_projects_page()
    projects = app.project.get_project_list()

    # Создаю новый проект, если проектов нет
    if len(app.project.get_project_list()) == 0:
        app.project.create(Project(name="чтобы было"))
        # После создания проекта снова получаю список
        projects = app.project.get_project_list()

    # Удаляю первый проект из списка
    app.project.delete_first_project()

    # Проверяю, что проект был удалён
    updated_projects = app.project.get_project_list()
    assert len(updated_projects) < len(projects)
    assert all(project["name"] != projects[0]["name"] for project in updated_projects)
