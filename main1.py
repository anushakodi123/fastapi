from fastapi import FastAPI, Query
from typing import Annotated
from pydantic import AfterValidator
import random

app = FastAPI()

data = {"isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",}

def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id

@app.get("/items")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/items")
async def read_items(q: Annotated[str | None, Query(min_length=3, max_length=30, pattern="^fixedquery$")] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/items")
async def read_items(q: Annotated[list[str], Query()]= None):
    query_items = {"q": q}
    return query_items

@app.get("/items")
async def read_items(q: Annotated[str | None, Query(title="Query string", description="Query string for the items to search in the database that have a good match",
                                                    min_length=3)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/items")
async def read_items(q: Annotated[str | None, Query(alias="item-query")] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/items")
async def read_items(hidden_query: Annotated[ str | None, Query(alias="hidden-query", include_in_schema=False)]= None):
    if hidden_query:
        return {"hidden_query": hidden_query}
    return {"hidden_query": "Not Found"}

@app.get("/items")
async def read_items(id: Annotated[ str | None, AfterValidator(check_valid_id)]=None):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {"id": id, "name": item}






