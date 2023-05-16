import aioredis
import uvicorn
from api.v1 import films, genres, persons
from core import elastic_config, project_config, redis_config
from db import elastic, redis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title=project_config.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    redis.redis = aioredis.from_url(f"redis://{redis_config.REDIS_HOST}:{redis_config.REDIS_PORT}")
    elastic.es = AsyncElasticsearch(
        hosts=[f"{elastic_config.ELASTIC_HOST}:{elastic_config.ELASTIC_PORT}"]
    )


@app.on_event("shutdown")
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])
app.include_router(persons.router, prefix="/api/v1/persons", tags=["persons"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=project_config.BACKEND_PORT,
    )
