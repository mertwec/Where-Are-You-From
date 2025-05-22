from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

import crud
from dependencies import api_request as apir
from dependencies.checkers import check_access
from dependencies.database import get_session
from schemas.nationalize import (CountryPrediction, NamePredictionResponse,
                                 PopularNamesResponse, TopNameStat)

route = APIRouter()


@route.get("/names/", response_model=NamePredictionResponse)
async def get_name_info(
    name: str = Query(...), session: AsyncSession = Depends(get_session)
):
    if not name:
        raise HTTPException(
            status_code=400, detail="Query parameter 'name' is required"
        )

    name_record = await crud.get_name(session, name)

    if name_record and check_access(name_record.last_accessed):
        return NamePredictionResponse(
            name=name_record.name,
            results=[
                CountryPrediction(
                    country=pred.country.name,
                    country_code=pred.country.code,
                    probability=pred.probability,
                )
                for pred in name_record.predictions
            ],
        )

    data_nationalization = await apir.get_nationalize(name)
    if not data_nationalization:
        raise HTTPException(
            status_code=502, detail="Failed to fetch from Nationalize.io"
        )

    if not data_nationalization.get("country"):
        raise HTTPException(
            status_code=404, detail="No country prediction found for this name"
        )

    if not name_record:
        name_record = await crud.create_name(session, name)
    else:
        name_record = await crud.increment_requests_name(session, name_record)

    predictions_list = []

    for entry in data_nationalization["country"]:
        code = entry["country_id"]
        probability = entry["probability"]

        country_record = await crud.get_country(session, code)

        if not country_record:
            data_country = await apir.get_country(code)
            country_record = await crud.create_country(
                session, country_code=code, cdata=data_country
            )

        await crud.create_name_country_prediction(
            session, name_record, country_record, probability
        )
        predictions_list.append(
            CountryPrediction(
                country=country_record.name,
                country_code=country_record.code,
                probability=probability,
            )
        )

    return NamePredictionResponse(name=name_record.name, results=predictions_list)


@route.get("/popular-names/", response_model=PopularNamesResponse)
async def get_popular_names(
    country: str = Query(None), session: AsyncSession = Depends(get_session)
):
    if not country:
        raise HTTPException(
            status_code=400, detail="Query parameter 'country' is required"
        )

    country_record = await crud.get_country(session, country_code=country)
    if not country_record:
        raise HTTPException(status_code=404, detail="Country not found")

    names = await crud.get_top_names_by_country(session, country)

    if not names:
        raise HTTPException(
            status_code=404, detail="No name data found for this country"
        )

    return PopularNamesResponse(
        country=country_record.name,
        top_names=[TopNameStat(name=n, probability=p) for n, p in names],
    )
