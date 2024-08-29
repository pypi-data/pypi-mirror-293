from typing import Union
from atcommon.models.base import BaseCoreModel
from datetime import datetime


class AuthPolicyCore(BaseCoreModel):
    project_id: str
    id: str
    permission: str
    name: str
    description: str
    dataset_config: dict

    __properties_init__ = [
        "project_id",
        "id",
        "permission",
        "name",
        "description",
        "dataset_config",
        "created_at",
        "modified_at",
    ]

    def __repr__(self):
        return f"[{self.name}]<{self.id}>"


class AuthRoleCore(BaseCoreModel):
    project_id: str
    id: str
    name: str
    description: str
    created_at: Union[str, datetime]
    modified_at: Union[str, datetime]

    __properties_init__ = [
        "project_id",
        "id",
        "name",
        "description",
        "created_at",
        "modified_at",
    ]

    def __repr__(self):
        return f"[{self.name}]<{self.id}>"


class AuthRoleVariableCore(BaseCoreModel):
    role_id: str
    datasource_id: str
    variables: list

    __properties_init__ = [
        "role_id",
        "datasource_id",
        "variables",
    ]

    def __repr__(self):
        return f"[{self.role_id}]<{self.datasource_id}>[{self.variables}]"
