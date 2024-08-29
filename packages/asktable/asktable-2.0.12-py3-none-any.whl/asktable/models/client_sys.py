from asktable.models.client_base import convert_to_object, BaseResourceList
from asktable.api import APIRequest
from atcommon.models.project import ProjectCore, APIKeyCore
from typing import Optional


class APIKeyClient(APIKeyCore):
    api: APIRequest
    endpoint: str

    def delete(self):
        return self.api.send(
            endpoint=f"{self.endpoint}/{self.id}",
            method="DELETE",
        )


class APIKeyList(BaseResourceList):

    @convert_to_object(cls=APIKeyClient)
    def _get_all_resources(self):
        return self._get_all_resources_request(with_pagination=False)

    @convert_to_object(cls=APIKeyClient)
    def create(self, ak_role: str) -> APIKeyClient:
        return self.api.send(
            endpoint=self.endpoint,
            method="POST",
            data={"ak_role": ak_role},
        )

    def delete(self, key_id: str):
        return self.api.send(
            endpoint=self.endpoint + f"/{key_id}",
            method="DELETE",
        )


class ProjectClient(ProjectCore):
    api: APIRequest
    endpoint: str

    def delete(self):
        return self.api.send(
            endpoint=f"{self.endpoint}/{self.id}",
            method="DELETE",
        )

    def lock(self):
        return self.api.send(
            endpoint=f"{self.endpoint}/{self.id}",
            method="POST",
            data={"locked": 1},
        )

    def unlock(self):
        return self.api.send(
            endpoint=f"{self.endpoint}/{self.id}",
            method="POST",
            data={"locked": 0},
        )

    def rename(self, name: str):
        return self.api.send(
            endpoint=f"{self.endpoint}/{self.id}",
            method="POST",
            data={"name": name},
        )

    @property
    def api_keys(self):
        return APIKeyList(self.api, self.endpoint + f"/{self.id}/api-keys")

    def get_token(
        self,
        ak_role: str = "asker",
        role_id: Optional[str] = "",
        role_variables: dict = {},
        user_profile: dict = {},
        ttl: int = 60 * 15,
    ):
        return self.api.send(
            endpoint=self.endpoint + f"/{self.id}/tokens",
            method="POST",
            data={
                "ak_role": ak_role,
                "chat_role": {
                    "role_id": role_id,
                    "role_variables": role_variables,
                },
                "user_profile": user_profile,
                "token_ttl": ttl,
            },
        )


class ProjectList(BaseResourceList):

    @convert_to_object(cls=ProjectClient)
    def _get_all_resources(self):
        return self._get_all_resources_request()

    @convert_to_object(cls=ProjectClient)
    def create(self, name: str) -> ProjectClient:
        return self.api.send(
            endpoint=self.endpoint,
            method="POST",
            data={"name": name},
        )

    @convert_to_object(cls=ProjectClient)
    def get(self, id: str = None, project_ids: list = None) -> ProjectClient:
        if id:
            return self.api.send(
                endpoint=f"{self.endpoint}/{id}",
                method="GET",
            )
        elif project_ids:
            response = self.api.send(
                endpoint=self.endpoint,
                method="GET",
                params={
                    "project_ids": ",".join(project_ids),
                    "page_size": 0,
                    "page_number": 0,
                },
            )
            projects = response.get("data")
            return projects
        else:
            raise ValueError("id or project_ids must be provided")

    def delete(self, project_id: str):
        return self.api.send(
            endpoint=self.endpoint + f"/{project_id}",
            method="DELETE",
        )
