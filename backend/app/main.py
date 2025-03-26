from fastapi import FastAPI
from sqlmodel import select
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


import uvicorn
import os
import logging


from .config import settings
from .schemas.enums import get_all_enums
from .routers import (auth, user, sse, cro, product,
                      project, task, note, sample, message, gap)
from .utils.dependencies import TokenDep, SessionDep
from .schemas import *

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI(redoc_url=None)


# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONT_END_HOST, "http://127.0.0.1:8000"],  # 允许前端源,allow credetial时不能为*
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],
)  # 允许所有头


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(product.router)
app.include_router(project.router)
app.include_router(task.router)
app.include_router(note.router)
app.include_router(cro.router)
app.include_router(sample.router)
app.include_router(gap.router)
app.include_router(message.router)
app.include_router(sse.router)


app.mount('/static', StaticFiles(directory='app/statics'), name="static")


@app.get('/', tags=['root'])
def root(session: SessionDep):

    logging.info("Handling request to the root endpoint")
    return {"message": "welcome to api docs"}


@app.get('/schema/{model_name}', tags=['root'])
def get_model_schema(model_name: str):
    model = globals().get(model_name)
    if not model:
        return None
    # return model.__table__.columns
    return model.__table__.columns.keys()


@app.get("/enums", tags=['root'])
async def get_enums(token: TokenDep):
    logging.info("Handling request to the enums endpoint")
    return get_all_enums()


@app.get("/task-library", tags=['root'])
async def get_task_library(session: SessionDep):
    logging.info("Handling request to the tasklibrary endpoint")
    stmt = select(TaskLibrary.id, TaskLibrary.task_category, TaskLibrary.task_name_prefix.label(
        'task_name'), TaskLibrary.default_task_owner_id, User.name.label('default_task_owner_name')).outerjoin(User, User.id == TaskLibrary.default_task_owner_id)
    task_library = session.exec(stmt).mappings().all()
    return task_library


if __name__ == "__main__":
    # uvicorn.run("app.main:app", reload=True, app_dir=os.path.dirname(os.path.abspath(__file__)),
    #             ssl_keyfile="../key.key",
    #             ssl_certfile='../crt.crt')
    uvicorn.run("app.main:app", reload=True, app_dir=os.path.dirname(os.path.abspath(__file__)))
