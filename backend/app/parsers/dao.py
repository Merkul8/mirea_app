from datetime import datetime
from typing import Optional

from sqlalchemy import select, and_, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dao import UserDAO
from app.auth.models import Publication, PublicService, User, AuthorType, UserPublication
from database.db import engine_session, connection
from transliterate import translit


class ParserDAO:

    @classmethod
    async def create_publications(cls, data: dict, user: User):
        publications = data.get("publications")
        if not publications:
            raise ValueError("Публикации не найдены")
        else:
            async with engine_session() as session:
                for publication in publications:
                    jornal_params = publication["journal"].split(".")
                    journal = jornal_params[0].strip()
                    curr_service = await PublicationServiceDAO.get_service_by_title(journal, session)
                    lastname_en = translit(str(user.last_name), "ru", reversed=True)
                    authors_list = publication["authors"].split(",")
                    curr_author = authors_list[0].lower()
                    try:
                        pub_year = jornal_params[1].strip()
                    except IndexError:
                        print(publication["journal"])
                        pub_year = "Неопределен"
                    print(lastname_en, user.last_name, curr_author)
                    if user.last_name.lower() in curr_author or lastname_en.lower() in curr_author:
                        author_type = AuthorType("автор")
                    else:
                        author_type = AuthorType("соавтор")
                    instance = Publication(
                        title=publication["title"],
                        citations=publication["citations"] if publication["citations"].isdigit() else "Нет",
                        public_service=publication["journal"],
                        public_service_id=curr_service.id if curr_service else None,
                        author_type=author_type,
                        authors=publication["authors"],
                        publication_year=pub_year
                    )

                    user = await UserDAO.find_one_or_none_by_id(user.id)
                    if user:
                        instance.users.append(user)
                    else:
                        raise ValueError(f"not found User")
                    # print(instance.title)
                    session.add(instance)
                await session.commit()

    @classmethod
    @connection
    async def get_user_publications(cls, user_id: int, session: AsyncSession, year: Optional[str] = None):
        # year = str(datetime.now().year)
        if not year:
            query = (select(Publication)
            .join(UserPublication, UserPublication.publication_id == Publication.id)
            .join(User, User.id == UserPublication.user_id)
            .where(
                User.id == user_id,
            ))
        else:
            query = (select(Publication)
                     .join(UserPublication, UserPublication.publication_id == Publication.id)
                     .join(User,User.id == UserPublication.user_id)
                     .where(and_(
                User.id == user_id,
                Publication.publication_year == year,
                                 )))
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    @connection
    async def update_publication(cls, pub_data: dict, session: AsyncSession):
        const_author = {
            "автор": "author",
            "соавтор": "collaborator"
        }
        pub_data["author_type"] = const_author[pub_data["author_type"]]
        stmt = update(Publication).where(Publication.id == pub_data["id"]).values(**pub_data)
        await session.execute(stmt)
        await session.commit()


class PublicationServiceDAO:

    @classmethod
    async def get_service_by_title(cls, title: str, session: AsyncSession) -> PublicService:
        query = select(PublicService).where(PublicService.title == title)
        result = await session.execute(query)
        return result.scalars().first()
