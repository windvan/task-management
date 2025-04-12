from ..schemas import TaskLibrary, TaskComment, ProjectComment, User
from sqlmodel import Session, select, text
from pydantic import ConfigDict
from ..database.db import engine
from sqlalchemy.orm import joinedload, selectinload
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select


# 2. load relationship fileds ###################
task_stmt = (
    select(TaskComment)
    .where(TaskComment.parent_id.is_(None))
    .options(
        joinedload(TaskComment.creater),
        selectinload(TaskComment.children, recursion_depth=2).joinedload(
            TaskComment.creater) 
    )
)


with Session(engine) as session:
    # 使用新的查询语法
    task_comments = session.exec(task_stmt).unique().all()

print('\n\ntaskcomments\n',
      task_comments[0][0].children)

result = [{**parent.model_dump(), 'created_by_name': parent.creater.name,
           'children': [{**child.model_dump(), "created_by_name": child.creater.name}
                        for child in parent.children]}
          for parent, in task_comments]
print('\n', result)
