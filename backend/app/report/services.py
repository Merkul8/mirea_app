from app.auth.models import Publication, User
from app.parsers.dao import ParserDAO

import pandas as pd
import uuid


class Report:
    report = {
        "Фамилия": [],
        "Имя": [],
        "Отчество": [],
        "Должность": [],
        "Ученая степень": [],
        "Тип трудовых отношений": [],
        "Наименование публикации": [],
        "Наименование издания": [],
        "Библиографическая ссылка": [],
        "Кол-во цитирований": [],
        "Количество авторов": [],
    }

    def __init__(self, user: User = None, users: list[User] = None):
        self.user = user
        self.users = users
        if not user and not users:
            raise ValueError("Должен быть передан один из параметров: user or users")

    async def get_user_report(self) -> str:
        data: list[Publication] = await ParserDAO.get_user_publications(self.user.id)
        for publication in data:
            await self._add_user_data_row(self.user, publication)
        df = pd.DataFrame(self.report)
        file_name = f"report_{self.user.last_name}_{uuid.uuid4()}.xlsx"
        df.to_excel(f"C:\\Users\merku\PycharmProjects\mirea_app\\backend\static\\{file_name}")
        return file_name

    async def get_users_report(self) -> str:
        for user in self.users:
            data: list[Publication] = await ParserDAO.get_user_publications(user.id)
            for publication in data:
                await self._add_user_data_row(user, publication)
        df = pd.DataFrame(self.report)
        file_name = f"report_{uuid.uuid4()}.xlsx"
        df.to_excel(f"../../static/reports/{file_name}")
        return file_name

    async def _add_user_data_row(self, user: User, publication: Publication) -> None:

        # user data
        self.report["Фамилия"].append(user.last_name)
        self.report["Имя"].append(user.first_name)
        self.report["Отчество"].append(user.patronymic)
        self.report["Должность"].append(user.post)
        self.report["Ученая степень"].append(user.academic_degree)
        self.report["Тип трудовых отношений"].append(user.work_type)

        # publication data
        self.report["Наименование публикации"].append(publication.title)
        self.report["Наименование издания"].append(publication.public_service.split(".")[0].strip())
        self.report["Библиографическая ссылка"].append(f"{publication.authors} {publication.title} // {publication.public_service}")
        self.report["Кол-во цитирований"].append(publication.citations)
        self.report["Количество авторов"].append(len(publication.authors.split(",")))

