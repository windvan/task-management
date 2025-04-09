from .enums import (TaskCategoryEnum, TaskProgressEnum, TaskStatusEnum,
                    CostCenterEnum, PaymentMethodEnum, PaymentStatusEnum)
from ..database.db import AutoFieldMixin, SQLModel
from .note import TaskNoteRelationship
from sqlmodel import Field, Enum as dbEnum, Column, Relationship, DateTime
from pydantic import EmailStr
from decimal import Decimal
from datetime import datetime



class TaskBase(SQLModel):
    project_id: int = Field(foreign_key="project.id")
    tags: str | None = None  # "#tag1# #tag2#"
   
    task_name: str
    task_owner_id: int = Field(foreign_key="user.id")
    task_status: TaskStatusEnum = Field(
        default=TaskStatusEnum.Idle, sa_column=dbEnum(TaskStatusEnum))

    expected_delivery_date: datetime | None = None
    
    start_year: int
    pi_number: str | None = None
    tk_number: str | None = None
    gap_id: int | None = Field(default=None, foreign_key="gap.id")
    cost_center: CostCenterEnum | None = Field(
        default=None, sa_column=dbEnum(CostCenterEnum))
    tox_gov_approved: bool = False
    ecotox_gov_approved: bool = False
    budget_confirmed: bool = False
    doc_link: str | None = None

    actual_cost: Decimal | None = Field(
        default=None, max_digits=10, decimal_places=2)
    po_placed: bool = False
    contract_signed: bool = False
    payment_method: PaymentMethodEnum = Field(
        default=PaymentMethodEnum.Half_Half, sa_column=dbEnum(PaymentMethodEnum))
    payment_status: PaymentStatusEnum = Field(
        default=PaymentStatusEnum.Not_Start, sa_column=dbEnum(PaymentStatusEnum))
    vv_doc_uploaded: bool = False
    vv_doc_number: str | None = None

    task_confirmed: bool | None = False
    planned_start: datetime | None = None
    expected_finish: datetime | None = None
    actual_start: datetime | None = None
    actual_finish: datetime | None = None
    delivery_date: datetime | None = None
    stuff_days: float | None = None
    task_progress: TaskProgressEnum = Field(
        default=TaskProgressEnum.Not_Start, sa_column=dbEnum(TaskProgressEnum))
    crop: str | None = None
    target: str | None = None
    cro_id: int | None = Field(default=None, foreign_key="cro.id")
    sample_id: int | None = Field(default=None, foreign_key="sample.id")
    study_notified: bool = False
    estimated_cost: Decimal | None = Field(
        default=None, max_digits=10, decimal_places=2)
    analytes: str | None = None
    key_results: str | None = Field(default=None, max_length=2000)
    guidelines: str | None = None

    test_item_data_sheet: bool = False
    ssd_finished: bool = False
    sed_uploaded: bool = False
    global_study_manager: str | None = None
    global_study_manager_email: EmailStr | None = None
    cro_study_director: str | None = None


class TaskCreate(TaskBase):
    pass


class TaskPublic(TaskBase):
    id: int


class TaskUpdate(SQLModel):
    project_id: int | None = None
    tags: str | None = None
    task_name: str | None = None
    task_status: TaskStatusEnum | None = None

    start_year: int | None = None
    expected_delivery_date: datetime | None = None
    task_owner_id: int | None = None

    budget_confirmed: bool | None = None
    cost_center: CostCenterEnum | None = None
    tox_gov_approved: bool | None = None
    ecotox_gov_approved: bool | None = None

    pi_number: str | None = None
    tk_number: str | None = None
    # gap的变化,不一定导致所有的task都需要调整
    # 因此,每个scoping task保存一个gap截图,每个gap截图,可以被多个task引用(一对多关系)
    gap_id: int | None = None
    doc_link: str | None = None

    task_confirmed: bool | None = False
    actual_cost: Decimal | None = None
    po_placed: bool | None = None
    contract_signed: bool | None = None
    payment_method: PaymentMethodEnum | None = None
    payment_status: PaymentStatusEnum | None = None
    vv_doc_uploaded: bool | None = None
    vv_doc_number: str | None = None

    task_progress: TaskProgressEnum | None = None
    planned_start: datetime | None = None
    expected_finish: datetime | None = None
    actual_start: datetime | None = None
    actual_finish: datetime | None = None
    delivery_date: datetime | None = None
    stuff_days: float | None = None

    cro_id: int | None = None
    sample_id: int | None = None
    study_notified: bool | None = None
    estimated_cost: Decimal | None = None
    analytes_count: int | None = None
    analytes: str | None = None
    key_results: str | None = None
    guidelines: str | None = None

    test_item_info_sent: bool | None = None
    ssd_finished: bool | None = None
    sed_uploaded: bool | None = None
    global_study_manager: str | None = None
    cro_study_director: str | None = None


class Task(TaskBase, AutoFieldMixin, table=True):
    id: int | None = Field(default=None, primary_key=True)

    project: "Project" = Relationship(back_populates="tasks", sa_relationship_kwargs={  # type: ignore
                                      "foreign_keys": "Task.project_id"})
    task_owner: "User" = Relationship(back_populates="tasks", sa_relationship_kwargs={  # type: ignore
                                      "foreign_keys": "Task.task_owner_id"})  # type: ignore
    cro: "Cro" = Relationship(back_populates="tasks", sa_relationship_kwargs={  # type: ignore
        "foreign_keys": "Task.cro_id"})  # type: ignore
    gap: "Gap" = Relationship(back_populates="tasks", sa_relationship_kwargs={  # type: ignore
        "foreign_keys": "Task.gap_id"})  # type: ignore
    sample: "Sample" = Relationship(back_populates="tasks", sa_relationship_kwargs={  # type: ignore
            "foreign_keys": "Task.sample_id"})  # type: ignore
    notes: list["Note"] = Relationship(  # type: ignore
        back_populates="task", link_model=TaskNoteRelationship)
    comments: list["TaskComment"] = Relationship(back_populates="task")  # type: ignore



class TaskLibrary(SQLModel, AutoFieldMixin, table=True):
    __tablename__ = "task_library"
    id: int = Field(primary_key=True)
    task_category: TaskCategoryEnum = Field(sa_column=dbEnum(TaskCategoryEnum))
    task_name: str
    default_task_owner_id: int | None = Field(foreign_key='user.id')


class TaskLibraryCreate(SQLModel):
    task_category: TaskCategoryEnum = Field(sa_column=dbEnum(TaskCategoryEnum))
    task_name: str
    default_task_owner_id: int | None = None

