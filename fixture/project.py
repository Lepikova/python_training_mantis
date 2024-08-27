from selenium.webdriver.common.by import By
import random

class ProjectHelper:

    def __init__(self, app):
        self.app = app
        self._manage_projects_page_open = False

    def open_manage_page(self):
        wd = self.app.wd
        self.app.open_home_page()
        wd.find_element(By.LINK_TEXT, "Manage").click()

    def open_manage_projects_page(self):
        wd = self.app.wd
        # Если страница уже открыта, не открываю ее снова
        if not self._manage_projects_page_open:
            self.open_manage_page()
            wd.find_element(By.LINK_TEXT, "Manage Projects").click()
            self._manage_projects_page_open = True

    def close_manage_projects_page(self):
        # Метод для сброса флага, если необходимо перейти на другую страницу
        self._manage_projects_page_open = False

    def is_project_exists(self, project_name):
        wd = self.app.wd
        self.open_manage_projects_page()
        projects = self.get_project_list()
        return any(project["name"] == project_name for project in projects)

    def generate_unique_name(self, base_name):
        return f"{base_name}_{random.randint(1, 9999)}"

    def create(self, project):
        wd = self.app.wd
        self.open_manage_projects_page()
        # Нажимаю на кнопку "Create New Project"
        wd.find_element(By.XPATH, "//input[@value='Create New Project']").click()
        # Ввожу имя новой группы
        wd.find_element(By.NAME, "name").click()
        wd.find_element(By.NAME, "name").clear()
        wd.find_element(By.NAME, "name").send_keys(project.name)
        # Нажимаю на кнопку "Add Project"
        wd.find_element(By.XPATH, "//input[@value='Add Project']").click()
        # Закрываю текущую страницу управления проектами
        self.close_manage_projects_page()

    def get_project_list(self):
        wd = self.app.wd
        self.open_manage_projects_page()
        project_list = []
        # Извлекаю все строки таблицы, которые содержат проекты (исключая заголовки)
        rows = wd.find_elements(By.CSS_SELECTOR,
                                "tr.row-1, tr.row-2")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 5:
                name = cells[0].text.strip()  # Имя проекта
                status = cells[1].text.strip()  # Статус проекта
                view_status = cells[3].text.strip()  # Видимость проекта (public/private)
                description = cells[4].text.strip()  # Описание проекта
                project_list.append({
                    "name": name,
                    "status": status,
                    "view_status": view_status,
                    "description": description
                })
        print("Полученный список проектов:", project_list)
        return project_list

    def delete_first_project(self):
        self.open_manage_projects_page()
        projects = self.get_project_list()

        if not projects:
            raise Exception("Нет доступных проектов для удаления")

        first_project = projects[0]
        project_name = first_project["name"]

        # Нажимаю на проект
        project_elements = self.app.wd.find_elements(By.XPATH, f"//a[text()='{project_name}']")
        if not project_elements:
            raise Exception(f"Проект с именем {project_name} не найден для удаления")

        project_elements[0].click()

        # Нажимаю кнопку "Удалить проект"
        self.app.wd.find_element(By.XPATH, "//input[@value='Delete Project']").click()

        # Подтверждаю удаление
        self.app.wd.find_element(By.XPATH, "//input[@value='Delete Project']").click()