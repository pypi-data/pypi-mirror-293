from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column
from sqlalchemy.types import TIMESTAMP

from sqlmodel import Field, SQLModel, text
from enum import Enum

class StatusEnum(int, Enum):
    in_work = 1
    ready_for_review = 2
    released = 3

class OptionFeatureEnum(str, Enum):
    option = "option"
    feature = "feature"

class CUrlTypeEnum(str, Enum):
    photo  = "photo"
    supplier_site = "supplier_site"
    drawing = "drawing"
    datasheet = "datasheet"
    speed_curves = "speed_curves"
    screw_option = "screw_option"
    step = "step"
    drawings_2D = "2D drawings"
    manual = "manual"
    software = "software"
    models_3D = "3D models"
    certifications = "certifications"
    drawings_3D = "3D drawings"
    catalog = "catalog"
    accessories = "accessories"
    firmware = "firmware"

class CUrlParentEnum(str, Enum):
    article = "article"
    family = "family"
    categorytree = "categorytree"

class SpectableTypeEnum(str, Enum):
    singlecol = "singlecol"
    multicol = "multicol"
    overview = "overview"

class SpectableParentEnum(str, Enum):
    article = "article"
    family = "family"
    product_group = "product_group"
    catalog = "catalog"

class CSpecTableItem(SQLModel):
    id: int|None = Field(default=None)
    pos: str|None = Field(default=None, max_length=32)
    name: str|None = Field(default=None, max_length=256)
    value: str|None = Field(default=None, max_length=256)
    min_value: str|None = Field(default=None, max_length=256)
    max_value: str|None = Field(default=None, max_length=256)
    unit: str|None = Field(default=None, max_length=256)
    user_id: int|None
    upddate: datetime|None
    insdate: datetime|None
    spec_table_id: int|None

class CSpecTable(SQLModel):
    id: int|None = Field(default=None)
    name: str|None = Field(default=None, max_length=256)
    type: SpectableTypeEnum|None
    has_unit: bool|None = None  # switch if unit col is needed or not
    parent: SpectableParentEnum|None
    user_id: int|None
    upddate: datetime|None
    insdate: datetime|None
    parent_id: int|None
    spec_table_items: List[CSpecTableItem]

class CUrl(SQLModel):
    id: int|None = Field(default=None)
    type: CUrlTypeEnum|None
    supplier_url: str|None = Field(default=None, max_length=1024)
    KOCO_url: str|None = Field(default=None, max_length=1024)
    description: str|None = Field(default=None, max_length=1024)
    parent_id: int|None = Field(default=None)
    parent: CUrlParentEnum|None
    user_id: int|None = Field(default=1)
    upddate: datetime|None
    insdate: datetime|None

class COption(SQLModel):
    id: int|None = Field(default=None)
    type: OptionFeatureEnum|None
    option: str|None = Field(default=None, max_length=256)
    category: str|None = Field(default=None, max_length=256)
    user_id: int|None = Field(default=1)
    family_id: int|None = Field(default=None)
    upddate: datetime|None
    insdate: datetime|None

class CApplication(SQLModel):
    id: int|None = Field(default=None)
    application: str|None = Field(default=None, max_length=256)
    family_id: int|None = Field(default=None)
    user_id: int|None = Field(default=1)
    upddate: datetime|None
    insdate: datetime|None

class CArticle(SQLModel):
    id: int|None = Field(default=None)
    article: str|None = Field(default=None, max_length=256)
    description: str|None = Field(default=None, max_length=4096)
    short_description: str|None = Field(default=None, max_length=256)
    upddate: datetime|None
    insdate: datetime|None
    family_id: int|None
    status: StatusEnum|None
    user_id: int|None

class CFamily(SQLModel):
    id: int|None = Field(default=None)
    family: str|None = Field(default=None, max_length=256)
    type: str|None = Field(default=None, max_length=1024)
    description: str|None = Field(default=None, max_length=1024)
    short_description: str|None = Field(default=None, max_length=256)
    upddate: datetime|None
    insdate: datetime|None
    product_group_id: int|None = Field(default=None)
    status: StatusEnum|None
    user_id: int|None = Field(default=1)
    articles: List[CArticle]|None
    applications: List[CApplication]|None
    options: List[COption]|None

class CProductGroup(SQLModel):
    id: Optional[int] = Field(default=None)
    product_group: str = Field(default=None, max_length=256)
    description: Optional[str] = Field(default=None, max_length=1024)
    image_url: Optional[str] = Field(default=None, max_length=1024)
    supplier_site_url: Optional[str] = Field(default=None, max_length=1024)
    catalog_id: Optional[int] = Field(default=None)
    status: StatusEnum|None
    user_id: int|None
    order_priority: int|None
    upddate: datetime|None
    insdate: datetime|None
    families: List[CFamily]|None

class CCatalog(SQLModel):
    id: int|None = Field(default=None)
    supplier: str|None = Field(default=None, max_length=128)
    year: int|None = None
    status: StatusEnum|None
    user_id: int|None
    insdate: datetime|None
    upddate: datetime|None
    product_groups: List[CProductGroup]|None


# class CUser(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str = Field(default=None, min_length=4, max_length=128)
#     first_name: Optional[str] = Field(default=None, max_length=128)
#     last_name: Optional[str] = Field(default=None, max_length=128)
#     email: Optional[str] = Field(default=None, max_length=256)
#     password: Optional[bytes] = Field(default=None, max_length=32)
#     role_id: int = Field(default=1)
#     insdate: datetime = Field(
#         sa_column=Column(
#             TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
#         )
#     )
#     upddate: datetime = Field(
#         sa_column=Column(
#             TIMESTAMP,
#             nullable=False,
#             server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
#         )
#     )


# class CUserRole(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     role: str = Field(default=None, min_length=4, max_length=64)
#     description: Optional[str] = Field(default=None, max_length=1024)
#     insdate: datetime = Field(
#         sa_column=Column(
#             TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
#         )
#     )
#     upddate: datetime = Field(
#         sa_column=Column(
#             TIMESTAMP,
#             nullable=False,
#             server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
#         )
#     )


class CBacklog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    backlog_text: str = Field(default=None, max_length=1024)
    status: int = Field(default=1)
    user_id: int = Field(default=1, foreign_key="cuser.id")
    upddate: datetime = Field(
        sa_column=Column(
            TIMESTAMP,
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        )
    )
    insdate: datetime = Field(
        sa_column=Column(
            TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
        )
    )

class CCategoryTree(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category: str = Field(default=None, max_length=128)
    export_target: str = Field(default=None, max_length=16)
    description: str = Field(default=None, max_length=4096)
    parent_id: int = Field(default=None)
    pos: int = Field(default=1)
    user_id: int = Field(default=1, foreign_key="cuser.id")
    upddate: datetime = Field(
        sa_column=Column(
            TIMESTAMP,
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        )
    )
    insdate: datetime = Field(
        sa_column=Column(
            TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
        )
    )


class CCategoryMapper(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category_id: Optional[int] = Field(default=None, foreign_key=CCategoryTree.id)
    family_id: Optional[int] = Field(default=None, foreign_key=CFamily.id)
    user_id: int = Field(default=1, foreign_key="cuser.id")
    upddate: datetime = Field(
        sa_column=Column(
            TIMESTAMP,
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        )
    )
    insdate: datetime = Field(
        sa_column=Column(
            TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
        )
    )


def Main():
    pass


if __name__ == "__main__":
    Main()
