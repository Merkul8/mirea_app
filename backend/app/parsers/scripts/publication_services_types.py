import pandas as pd
from app.auth.models import PublicService, ServiceType
from database.db import engine_session
import config


async def services_categories_to_db():
    df = pd.read_excel(config.CATEGORIES_PUBLIC_SERVICES_PATH, sheet_name="Table 1", skiprows=1)
    services = []
    for name, category in zip(df.iloc[:, 1], df.iloc[:, 4]):
        services.append(
            PublicService(title=name, service_type=ServiceType(category))
        )
    async with engine_session() as session:
        session.add_all(services)
        await session.commit()
