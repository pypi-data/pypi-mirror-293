from asktable.models.client_base import convert_to_object, BaseResourceList
from asktable.api import APIRequest
from atcommon.models import Q2SCore, Q2ACore, StrucQuery, BIAnswer


class Q2SClient(Q2SCore):
    api: APIRequest
    endpoint: str


class Q2SList(BaseResourceList):
    __do_not_print_properties__ = ["project_id"]

    @convert_to_object(cls=Q2SClient)
    def _get_all_resources(self):
        return self._get_all_resources_request()

    @convert_to_object(cls=StrucQuery)
    def create(self, datasource_id, question: str, **kwargs) -> Q2SClient:
        return self.api.send(
            endpoint=self.endpoint,
            method="POST",
            data={
                "datasource_id": datasource_id,
                "question": question,
                **kwargs
            },
        )


class Q2AClient(Q2ACore):
    api: APIRequest
    endpoint: str


class Q2AList(BaseResourceList):
    __do_not_print_properties__ = ["project_id"]

    @convert_to_object(cls=Q2AClient)
    def _get_all_resources(self):
        return self._get_all_resources_request()

    @convert_to_object(cls=BIAnswer)
    def create(self, datasource_id, question: str, **kwargs) -> Q2AClient:
        return self.api.send(
            endpoint=self.endpoint,
            method="POST",
            data={
                "datasource_id": datasource_id,
                "question": question,
                **kwargs
            },
        )
