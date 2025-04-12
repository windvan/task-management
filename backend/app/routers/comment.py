from fastapi import APIRouter, status, HTTPException, Depends, Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import selectinload, joinedload
from sqlmodel import select

from ..schemas.user import User

from ..schemas.comment import ProjectComment, TaskComment, CommentsOut
from ..schemas.task import Task
from ..schemas.project import Project
from ..utils.dependencies import SessionDep

router = APIRouter(prefix='/comments', tags=["Comment"])


@router.post("/project")
def create_project_comment(proj_comment: dict, session: SessionDep):
    print('\n\n\n\n', proj_comment)
    db_comment = ProjectComment.model_validate(proj_comment)
    session.add(db_comment)
    session.commit()
    session.refresh(db_comment)

    created_by_name = session.exec(select(User.name).where(
        User.id == db_comment.created_by)).one()

    comment_dict = db_comment.model_dump()
    comment_dict.update({
        'created_by_name': created_by_name,
        'children': []
    })

    return comment_dict


@router.post("/task")
def create_task_comment(task_comment: dict, session: SessionDep):
    db_comment = TaskComment.model_validate(task_comment)
    session.add(db_comment)
    session.commit()
    session.refresh(db_comment)

    created_by_name = session.exec(select(User.name).where(
        User.id == db_comment.created_by)).one()

    comment_dict = db_comment.model_dump()
    comment_dict.update({
        'created_by_name': created_by_name,
        'children': []
    })

    return comment_dict


# @router.get("/all", )
# def get_all_comments(session: SessionDep):

#     proj_stmt = (
#         select(ProjectComment, User.name.label('created_by_name'))
#         .join(User, User.id == ProjectComment.created_by)
#         .where(ProjectComment.parent_id.is_(None))  # 只选择顶级评论,Model中已指定懒加载策略
#         .options(joinedload(ProjectComment.children))
#     )

#     task_stmt = (
#         select(TaskComment, User.name.label('created_by_name'))
#         .join(User, User.id == TaskComment.created_by)
#         .where(TaskComment.parent_id == None)  # 只选择顶级评论
#         .options(joinedload(TaskComment.children))
#     )

#     proj_comments = session.exec(proj_stmt).unique().all()
#     task_comments = session.exec(task_stmt).unique().all()

#     # 处理结果，返回嵌套数据
#     result = {'project_comments': [{**comment.model_dump(), 'children': comment.children, 'created_by_name': created_by_name}
#                                    for comment, created_by_name in proj_comments],
#               'task_comments': [{**comment.model_dump(), 'children': comment.children, 'created_by_name': created_by_name}
#                                 for comment, created_by_name in task_comments]}
#     return result


@router.get("/task/{task_id}")
def get_task_comments(task_id: int, session: SessionDep):
    task_stmt = (
        select(TaskComment)
        .where(TaskComment.parent_id.is_(None), TaskComment.task_id == task_id)
        .options(
            joinedload(TaskComment.creater).load_only(User.name),
            selectinload(TaskComment.children, recursion_depth=2).joinedload(
                TaskComment.creater).load_only(User.name)
        )
    )

    proj_id = session.exec(select(Task).where(
        Task.id == task_id)).one().project_id

    proj_stmt = (
        select(ProjectComment)
        .where(ProjectComment.parent_id.is_(None), ProjectComment.project_id == proj_id)
        .options(
            joinedload(ProjectComment.creater).load_only(User.name),
            selectinload(ProjectComment.children, recursion_depth=2).joinedload(
                ProjectComment.creater).load_only(User.name)

        )
    )

    proj_comments = session.exec(proj_stmt).unique().all()
    task_comments = session.exec(task_stmt).unique().all()

    # 处理结果，返回嵌套数据
    result = {'project_comments': [{**parent.model_dump(), 'created_by_name': parent.creater.name,
                                    'children': [{**child.model_dump(), "created_by_name": child.creater.name}
                                                 for child in parent.children]}
                                   for parent in proj_comments],
              'task_comments': [{**parent.model_dump(), 'created_by_name': parent.creater.name,
                                 'children': [{**child.model_dump(), "created_by_name": child.creater.name}
                                              for child in parent.children]}
                                for parent in task_comments]}
    return result


@router.get("/project/{project_id}")
def get_project_comments(project_id: int, session: SessionDep):

    proj_stmt = (
        select(ProjectComment)
        .where(ProjectComment.parent_id.is_(None), ProjectComment.project_id == project_id)
        .options(
            joinedload(ProjectComment.creater),
            selectinload(ProjectComment.children, recursion_depth=2).joinedload(
                ProjectComment.creater)
        )
    )

    project = session.get(Project, project_id)
    related_task_ids = [task.id for task in project.tasks]
    task_stmt = (
        select(TaskComment)
        .where(TaskComment.parent_id.is_(None), TaskComment.task_id.in_(related_task_ids))
        .options(
            joinedload(TaskComment.creater).load_only(User.name),
            joinedload(TaskComment.task).load_only(Task.task_name, Task.id),
            selectinload(TaskComment.children, recursion_depth=2).options(
                joinedload(TaskComment.creater).load_only(User.name),
                joinedload(TaskComment.task).load_only(Task.task_name, Task.id)
            )
        )
    )

    proj_comments = session.exec(proj_stmt).unique().all()
    task_comments = session.exec(task_stmt).unique().all()
# group by task_id
    task_comments_by_id = {}
    for parent in task_comments:
        task_id = parent.task.id
        comment_data = {
            **parent.model_dump(),
            'created_by_name': parent.creater.name,
            'task_name': parent.task.task_name,
            'children': [{
                **child.model_dump(),
                "created_by_name": child.creater.name,
                'task_name': child.task.task_name
            } for child in parent.children]
        }
        if task_id not in task_comments_by_id:
            task_comments_by_id[task_id] = []
        task_comments_by_id[task_id].append(comment_data)
    # 处理结果，返回嵌套数据
    result = {'project_comments': [{**parent.model_dump(), 'created_by_name': parent.creater.name,
                                    'children': [{**child.model_dump(), "created_by_name": child.creater.name}
                                                 for child in parent.children]}
                                   for parent in proj_comments],
              'task_comments': task_comments_by_id}
    return result


@router.patch("/project/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
# only handle update severity, no response data
def update_project_comment(comment_id: int, updates: dict, session: SessionDep):
    db_comment = session.get(ProjectComment, comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="comment not found")
    db_comment.sqlmodel_update(updates)
    session.add(db_comment)
    session.commit()
    return


@router.patch("/task/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
# only handle update severity, no response data
def update_task_comment(comment_id: int, updates: dict, session: SessionDep):
    db_comment = session.get(TaskComment, comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="comment not found")
    db_comment.sqlmodel_update(updates)
    session.add(db_comment)
    session.commit()
    return
