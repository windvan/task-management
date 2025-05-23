from ..schemas import TaskLibrary, TaskComment, ProjectComment
from sqlmodel import Session, select, text
from pydantic import ConfigDict
from ..database.db import engine
from sqlalchemy.orm import joinedload, selectinload
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select


# 1. clear TaskLibrary##################
# task_library_data = [
#     TaskLibrary(task_category="Tox_Study",
#                 task_name="Acute Oral", default_task_owner_id=3, created_by=1),
#     TaskLibrary(task_category="Tox_Study",
#                 task_name="Acute Dermal", default_task_owner_id=3, created_by=1),
#     TaskLibrary(task_category="Tox_Study",
#                 task_name="Eye Irritation", default_task_owner_id=3, created_by=1),
#     TaskLibrary(task_category="Tox_Study",
#                 task_name="Skin Irritation", default_task_owner_id=3, created_by=1),
#     TaskLibrary(task_category="Tox_Study",
#                 task_name="Skin Sensitization", default_task_owner_id=3, created_by=1),
#     TaskLibrary(task_category="Tox_Study",
#                 task_name="Acute inhalation", default_task_owner_id=3, created_by=1),
#     TaskLibrary(task_category="Eco_Tox_Study",
#                 task_name="Avian Acute oral toxicity", default_task_owner_id=2, created_by=1),
#     TaskLibrary(task_category="Eco_Tox_Study",
#                 task_name="Acute toxcity to daphnia", default_task_owner_id=2, created_by=1),
#     TaskLibrary(task_category="Eco_Tox_Study",
#                 task_name="Algal Growth Inhibition", default_task_owner_id=2, created_by=1),
#     TaskLibrary(task_category="Eco_Tox_Study",
#                 task_name="Acute toxicity to trichogrammatid", default_task_owner_id=2, created_by=1),
#     TaskLibrary(task_category="Eco_Tox_Study",
#                 task_name="Acute toxicity to silkworm", default_task_owner_id=2, created_by=1),
#     TaskLibrary(task_category="Eco_Tox_Study",
#                 task_name="Acute toxicity to ladybird", default_task_owner_id=2, created_by=1),
#     TaskLibrary(task_category="Eco_Tox_Study",
#                 task_name="Acute oral toxicity to bee", default_task_owner_id=2, created_by=1),
#     TaskLibrary(task_category="Eco_Tox_Study",
#                 task_name="Acute contact toxicity to bee", default_task_owner_id=2, created_by=1),
#     TaskLibrary(task_category="Eco_Tox_Study",
#                 task_name="Acute toxicity to earthworm", default_task_owner_id=2, created_by=1),
#     TaskLibrary(task_category="Eco_Tox_Study",
#                 task_name="Acute fish toxicity", default_task_owner_id=2, created_by=1),
#     TaskLibrary(task_category="Risk_Assessment",
#                 task_name="Operator risk assessment", default_task_owner_id=3, created_by=1),
#     TaskLibrary(task_category="Risk_Assessment",
#                 task_name="Environment risk assessment", default_task_owner_id=2, created_by=1),
#     TaskLibrary(task_category="Risk_Assessment",
#                 task_name="Dietary risk assessment", default_task_owner_id=None, created_by=1),
#     TaskLibrary(task_category="Residue_Study",
#                 task_name="Residue study", default_task_owner_id=None, created_by=1),
#     TaskLibrary(task_category="Processing_Residue_Study",
#                 task_name="Processing_residue_study", default_task_owner_id=None, created_by=1),
#     TaskLibrary(task_category="Pre_Scoping",
#                 task_name="OPEX_Scoping", default_task_owner_id=3, created_by=1),
#     TaskLibrary(task_category="Pre_Scoping",
#                 task_name="DRA_Scoping", default_task_owner_id=None, created_by=1),
#     TaskLibrary(task_category="Pre_Scoping",
#                 task_name="ERA_Scoping", default_task_owner_id=2, created_by=1),
#     TaskLibrary(task_category="Pre_Scoping",
#                 task_name="Residue_Scoping", default_task_owner_id=None, created_by=1),
#     TaskLibrary(task_category="Others",
#                 task_name="Deco_Doc", default_task_owner_id=7, created_by=1),
#     TaskLibrary(task_category="Others",
#                 task_name="Statement", default_task_owner_id=None, created_by=1),
#     TaskLibrary(task_category="Others",
#                 task_name="Label_Review", default_task_owner_id=7, created_by=1),
#     TaskLibrary(task_category="Others",
#                 task_name="Check_List", default_task_owner_id=7, created_by=1),
#     TaskLibrary(task_category="Others",
#                 task_name="Risk_Matrix", default_task_owner_id=7, created_by=1),
#     TaskLibrary(task_category="Others",
#                 task_name="Gov_Doc_Tox", default_task_owner_id=3, created_by=1),
#     TaskLibrary(task_category="Others",
#                 task_name="Gov_Doc_EcoTox", default_task_owner_id=2, created_by=1),
# ]

# with Session(engine) as session:
#     session.exec(text('DELETE FROM task_library'))
#     for task_item in task_library_data:
#         session.add(task_item)
#     session.commit()


# 2. load relationship fileds ###################
proj_stmt = (
    select(ProjectComment)
    .where(ProjectComment.parent_id.is_(None))

)

task_stmt = (
    select(TaskComment)
    .where(TaskComment.parent_id.is_(None))

)
with Session(engine) as session:
    # 使用新的查询语法
    proj_comments = session.scalars(proj_stmt).unique().all()
    task_comments = session.scalars(task_stmt).unique().all()


print('\n\nfirst project comment children\n',proj_comments[0].children)
print('\n\nproj_comments\n', proj_comments)
print('\n\ntask_comments\n', task_comments)
