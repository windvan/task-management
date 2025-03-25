from sqlmodel import Field, Relationship
from decimal import Decimal

from ..database.database import AutoFieldMixin, SQLModel


class Image(SQLModel):
    img_name: str
    img_data: bytes


class GapBase(SQLModel):
    crop_name: str | None = None
    crop_name_cn: str | None = None
    control_target: str | None = None
    control_target_cn: str | None = None
    app_rate_min: Decimal | None = None
    app_rate_max: Decimal | None = None
    water_volumn_min: int | None = None
    water_volumn_max: int | None = None
    app_method: str | None = None
    app_number: int | None = None
    app_interval_min: int | None = None
    # app_interval_max: int | None = None
    app_time: str | None = None
    app_time_bbch: str | None = None
    phi: int | None = None
    additional_comments: str | None = None


class GapCreate(GapBase):
    app_rate_unit: str = "g a.i./ha"
    water_volumn_unit: str = "L/ha"
    snapshot: Image


class GapPublic(GapBase):
    id: int
    app_rate_unit: str
    water_volumn_unit: str
    snapshot: Image


class GapUpdate(GapBase):
    snapshot: Image | None = None


class Gap(GapBase, AutoFieldMixin, table=True):
    id: int | None = Field(default=None, primary_key=True)
    app_rate_unit: str = "g a.i./ha"
    water_volumn_unit: str = "L/ha"
    snapshot_url: str | None = None

    tasks: list["Task"] = Relationship(back_populates='gap',  # type: ignore
                                       sa_relationship_kwargs={"foreign_keys": "Task.gap_id"})


# class GapTaskRelationship(SQLModel, table=True):
#     __tablename__ = "gap_task_rel"
#     gap_id: int = Field(foreign_key="gap.id", primary_key=True)
#     task_id: int = Field(foreign_key="task.id", primary_key=True)
