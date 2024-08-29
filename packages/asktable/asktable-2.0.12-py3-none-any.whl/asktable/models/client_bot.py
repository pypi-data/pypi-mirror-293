from asktable.models.client_base import convert_to_object, BaseResourceList
from asktable.api import APIRequest
from atcommon.exceptions import server as errors
from atcommon.models.chatbot import BotCore


class BotClient(BotCore):
    api: APIRequest
    endpoint: str

    def delete(self):
        return self.api.send(endpoint=f"{self.endpoint}/{self.id}", method="DELETE")

    @convert_to_object(cls=BotCore)
    def update(
        self,
        **kwargs
    ):
        return self.api.send(
            endpoint=f"{self.endpoint}/{self.id}",
            method="POST",
            data=kwargs,
        )


class BotList(BaseResourceList):
    __do_not_print_properties__ = ["project_id", "created_at"]

    @convert_to_object(cls=BotClient)
    def _get_all_resources(self):
        return self._get_all_resources_request()

    @convert_to_object(cls=BotClient)
    def get(self, id=None, name=None):
        if id:
            return self.api.send(endpoint=f"{self.endpoint}/{id}", method="GET")
        elif name:
            response = self.api.send(
                endpoint=self.endpoint, method="GET", params={"name": name}
            )
            data = response.get("data", [])
            if data:
                return data[0]
            else:
                raise errors.BotNotFound(f"Chatbot with name {name} not found")
        else:
            raise ValueError("id or name must be provided")

    @property
    @convert_to_object(cls=BotClient)
    def latest(self):
        return self._get_latest_one_or_none()

    @convert_to_object(cls=BotClient)
    def create(
        self,
        name: str,
        datasource_ids: str,
        **kwargs,
    ):
        return self.api.send(
            endpoint=self.endpoint,
            method="POST",
            data={
                "name": name,
                "datasource_ids": datasource_ids,
                **kwargs,
            },
        )
