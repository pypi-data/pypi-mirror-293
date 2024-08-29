from atcommon.models.base import BaseCoreModel


class ProjectCore(BaseCoreModel):
    id: str
    name: str
    locked: int
    created_at: str
    modified_at: str

    __properties_init__ = ["id", "name", "created_at", "modified_at", "locked"]

    def __repr__(self):
        return f"<Project {self.id} [{self.name}]>"


class APIKeyCore(BaseCoreModel):
    id: str
    hashed_ak_value: str
    original_ak_value: str
    masked_ak_value: str
    project_id: str
    status: int
    ak_role: str
    last_used_at: str
    created_at: str

    __properties_init__ = [
        "id",
        "hashed_ak_value",
        "original_ak_value",
        "masked_ak_value",
        "project_id",
        "status",
        "ak_role",
        "created_at",
        "last_used_at",
    ]

    def __repr__(self):
        return (
            f"<Token {self.id}({self.project_id})"
            f" [{self.status}-{self.last_used_at}]>"
        )


class AuthInfo(BaseCoreModel):
    project_id: str
    ak_role: str
    chat_role: dict | None = None
    user_profile: dict | None = None
    exp: str | None = None

    __properties_init__ = [
        "project_id",
        "ak_role",
        "chat_role",
        "user_profile",
        "exp",
    ]

    def __repr__(self):
        return f"<project_id {self.project_id}, ak_role {self.ak_role}>"
