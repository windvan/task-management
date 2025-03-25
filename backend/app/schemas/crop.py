from sqlmodel import Field
from ..database.database import AutoFieldMixin, SQLModel


class CropBase(SQLModel):
    crop_name_cn: str = Field(index=True, unique=True)
    crop_name_en: str | None = Field(default=None, index=True)
    required_trials: int
    comments: str | None = None


class CropCreate(CropBase):
    pass


class CropPublic(CropBase):
    id: int


class CropUpdate(SQLModel):
    crop_name_cn: str | None = None
    crop_name_en: str | None = None
    required_trials: int | None = None
    comments: str | None = None


class Crop(CropBase, AutoFieldMixin, table=True):
    id: int | None = Field(default=None, primary_key=True)
