from sqlmodel import Field, Enum as dbEnum, Relationship, Column, DateTime
from datetime import datetime
from pydantic import field_validator

from ..database.database import AutoFieldMixin, SQLModel
from .enums import (IndicationEnum, ProjectManagerEnum, ProjectStatusEnum, StageEnum,
                    RegManagerEnum, RegEntityEnum, RegistrationTypeEnum, SubmissionStatusEnum)
from .note import ProjectNoteRelationship



class ProjectBase(SQLModel):
    project_name: str
    product_id: int = Field(foreign_key="product.id")
    indication: IndicationEnum = Field(sa_column=dbEnum(IndicationEnum))
    portfolio_contact_id: int = Field(foreign_key="user.id")
    project_manager: ProjectManagerEnum = Field(
        sa_column=dbEnum(ProjectManagerEnum))
    reg_manager: RegManagerEnum = Field(sa_column=dbEnum(RegManagerEnum))
    project_status: ProjectStatusEnum = Field(
        sa_column=dbEnum(ProjectStatusEnum))
    reg_entity: RegEntityEnum = Field(sa_column=dbEnum(RegEntityEnum))
    registration_type: RegistrationTypeEnum = Field(
        sa_column=dbEnum(RegistrationTypeEnum))
    notification_entrance: str | None = None
    submission_status: SubmissionStatusEnum = Field(default=SubmissionStatusEnum.Preparation,
                                                    sa_column=dbEnum(SubmissionStatusEnum))
    approved_date: datetime | None = None
    is_three_new: bool = False


class ProjectCreate(ProjectBase):
    pass


class ProjectPublic(ProjectBase):
    id: int


class ProjectUpdate(SQLModel):
    project_name: str | None = None
    product_id: int | None = None
    indication: IndicationEnum | None = None
    portfolio_contact_id: int | None = None
    project_manager: ProjectManagerEnum | None = None
    reg_manager: RegManagerEnum | None = None
    project_status: ProjectStatusEnum | None = None
    reg_entity: RegEntityEnum | None = None
    registration_type: RegistrationTypeEnum | None = None
    notification_entrance: str | None = None
    submission_status: SubmissionStatusEnum | None = None
    approved_date: datetime | None = None
    is_three_new: bool | None = None


class Project(ProjectBase, AutoFieldMixin, table=True):
    id: int | None = Field(default=None, primary_key=True)

    product: "Product" = Relationship(back_populates="projects")  # type: ignore
    tasks: list["Task"] = Relationship(back_populates="project")  # type: ignore
    notes: list["Note"] = Relationship(  # type: ignore
        back_populates="project", link_model=ProjectNoteRelationship)


