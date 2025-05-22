from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from werkzeug.security import generate_password_hash

from models.nationalize import Country, Name, NameCountryPrediction
from schemas.user import InputUserData

# async def get_name(session: AsyncSession, name: str) -> Name:
#     stmt = select(Name).where(Name.name == name)
#     return await session.scalar(stmt)


async def get_name(session: AsyncSession, name: str) -> Name:
    stmt = (
        select(Name)
        .where(Name.name == name)
        .options(
            selectinload(Name.predictions)
            # .selectinload(NameCountryPrediction.name)
            .selectinload(NameCountryPrediction.country)
        )
    )
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_country(session: AsyncSession, country_code: str) -> Country:
    stmt = (
        select(Country)
        .where(Country.code == country_code)
        .options(
            # Загружаем predictions асинхронно
            selectinload(Country.predictions)
            # И для каждой prediction загружаем связанные данные страны
            .selectinload(NameCountryPrediction.country)
        )
    )
    result = await session.execute(stmt)
    return result.scalars().first()


async def create_name(session: AsyncSession, name: str) -> Name:
    name_record = Name(name=name, request_count=1)
    session.add(name_record)
    await session.commit()
    await session.refresh(name_record)
    return name_record


async def increment_requests_name(session: AsyncSession, name_record: Name) -> Name:
    session.add(name_record)
    await session.commit()
    await session.refresh(name_record)
    return name_record


async def create_country(
    session: AsyncSession, country_code: str, cdata: dict
) -> Country:
    country = Country(
        code=country_code,
        name=cdata.get("name", {}).get("common"),
        region=cdata.get("region"),
        independent=cdata.get("independent", False),
        google_maps=cdata.get("maps", {}).get("googleMaps"),
        open_street_map=cdata.get("maps", {}).get("openStreetMaps"),
        capital_name=cdata.get("capital", [None])[0],
        capital_lat=cdata.get("capitalInfo", {}).get("latlng", [None])[0],
        capital_lng=cdata.get("capitalInfo", {}).get("latlng", [None, None])[1],
        flag_png=cdata.get("flags", {}).get("png"),
        flag_svg=cdata.get("flags", {}).get("svg"),
        flag_alt=cdata.get("flags", {}).get("alt"),
        coat_png=cdata.get("coatOfArms", {}).get("png"),
        coat_svg=cdata.get("coatOfArms", {}).get("svg"),
        borders=cdata.get("borders"),
    )

    session.add(country)
    await session.commit()
    await session.refresh(country)
    return country


async def create_name_country_prediction(
    session: AsyncSession,
    name_record: Name,
    country_record: Country,
    probability: float,
) -> NameCountryPrediction:
    prediction = NameCountryPrediction(
        name=name_record, country=country_record, probability=probability
    )
    session.add(prediction)

    await session.commit()
    await session.refresh(prediction)
    return prediction


async def get_top_names_by_country(session: AsyncSession, country_code: str):
    stmt = (
        select(
            Name.name,
            func.max(NameCountryPrediction.probability).label("max_probability"),
        )
        .join(NameCountryPrediction, Name.id == NameCountryPrediction.name_id)
        .where(NameCountryPrediction.country_code == country_code)
        .group_by(Name.name)
        .order_by(desc("max_probability"))
        .limit(5)
    )
    result = await session.execute(stmt)
    names = result.all()
    return names
