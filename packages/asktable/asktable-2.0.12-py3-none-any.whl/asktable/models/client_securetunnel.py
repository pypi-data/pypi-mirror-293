from asktable.models.client_base import convert_to_object, BaseResourceList
from atcommon.models.securetunnel import SecureTunnelCore, SecureTunnelLinkCore
from asktable.api import APIRequest


class SecureTunnelLinkList(BaseResourceList):
    __do_not_print_properties__ = ["created_at"]

    @convert_to_object(cls=SecureTunnelLinkCore)
    def _get_all_resources(self):
        return self._get_all_resources_request()


class SecureTunnelClient(SecureTunnelCore):
    api: APIRequest
    endpoint: str

    def delete(self):
        return self.api.send(endpoint=f"{self.endpoint}/{self.id}", method="DELETE")

    def update(self, name=None, unique_key=None, client_info=None):
        return self.api.send(
            endpoint=f"/securetunnels/{self.id}",
            method="POST",
            data={"name": name, "unique_key": unique_key, "client_info": client_info},
        )

    @property
    def links(self):
        return SecureTunnelLinkList(
            self.api, endpoint=f"{self.endpoint}/{self.id}/links"
        )


class SecureTunnelList(BaseResourceList):
    __do_not_print_properties__ = ["project_id", "created_at", "info"]

    @convert_to_object(cls=SecureTunnelClient)
    def create(self, name=None):
        data = {"name": name} if name else {}
        return self.api.send(endpoint=self.endpoint, method="POST", data=data)

    @convert_to_object(cls=SecureTunnelClient)
    def _get_all_resources(self):
        return self._get_all_resources_request()

    @property
    @convert_to_object(cls=SecureTunnelClient)
    def latest(self):
        return self._get_latest_one_or_none()

    @convert_to_object(cls=SecureTunnelClient)
    def get(self, id):
        return self.api.send(endpoint=f"{self.endpoint}/{id}", method="GET")
