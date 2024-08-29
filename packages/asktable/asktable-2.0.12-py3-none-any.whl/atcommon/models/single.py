from atcommon.models.base import BaseCoreModel


class Q2SCore(BaseCoreModel):
    id: str
    project_id: str
    datasource_id: str
    role_id: str
    role_variables: dict
    question: str
    query: dict
    status: str
    err_msg: str
    duration: int

    __properties_init__ = [
        "id",
        "project_id",
        "datasource_id",
        "role_id",
        "role_variables",
        "question",
        "query",
        "status",
        "err_msg",
        "duration",
        "created_at",
        "modified_at",
    ]


class Q2ACore(BaseCoreModel):
    id: str
    project_id: str
    datasource_id: str
    role_id: str
    role_variables: dict
    max_rows: int
    question: str
    answer_text: str
    answer: dict
    status: str
    err_msg: str
    duration: int

    __properties_init__ = [
        "id",
        "project_id",
        "datasource_id",
        "role_id",
        "role_variables",
        "max_rows",
        "question",
        "answer_text",
        "answer",
        "status",
        "err_msg",
        "duration",
        "created_at",
        "modified_at",
    ]


