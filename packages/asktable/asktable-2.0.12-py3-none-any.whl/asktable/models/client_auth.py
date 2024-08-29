from asktable.models.client_base import convert_to_object, BaseResourceList
from atcommon.models.auth import AuthPolicyCore, AuthRoleCore
from asktable.api import APIRequest
from atcommon.exceptions import server as errors


class AuthPolicyClient(AuthPolicyCore):
    api: APIRequest
    endpoint: str

    def delete(self):
        return self.api.send(endpoint=f"{self.endpoint}/{self.id}", method="DELETE")

    @convert_to_object(cls=AuthPolicyCore)
    def update(self, name=None, permission=None, dataset_config=None):
        return self.api.send(
            endpoint=f"{self.endpoint}/{self.id}",
            method="POST",
            data={
                "name": name,
                "permission": permission,
                "dataset_config": dataset_config,
            },
        )


class AuthPolicyList(BaseResourceList):

    __do_not_print_properties__ = ["project_id", "description", "created_at"]

    @convert_to_object(cls=AuthPolicyClient)
    def _get_all_resources(self):
        return self._get_all_resources_request()

    @convert_to_object(cls=AuthPolicyClient)
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
                raise errors.AuthPolicyNotFound(f"Policy with name {name} not found")
        else:
            raise ValueError("id or name must be provided")

    @property
    @convert_to_object(cls=AuthPolicyClient)
    def latest(self):
        return self._get_latest_one_or_none()

    @convert_to_object(cls=AuthPolicyClient)
    def create(self, permission: str, name: str, dataset_config: dict = None):
        return self.api.send(
            endpoint=self.endpoint,
            method="POST",
            data={
                "permission": permission,  # allow, deny
                "name": name,
                "dataset_config": dataset_config,
            },
        )


class AuthRolePolicyList(BaseResourceList):
    """
    用于获取角色的所有策略，没有翻页，没有创建、GET、Latest等操作
    """

    __do_not_print_properties__ = ["project_id", "description", "created_at"]

    @convert_to_object(cls=AuthPolicyClient)
    def _get_all_resources(self):
        return self._get_all_resources_request(with_pagination=False)


class AuthRoleClient(AuthRoleCore):
    api: APIRequest
    endpoint: str

    def delete(self):
        return self.api.send(endpoint=f"{self.endpoint}/{self.id}", method="DELETE")

    @convert_to_object(cls=AuthRoleCore)
    def update(self, name=None, policy_ids: list or None = None):
        # 如果 policy_ids 为 None，则不更新
        # 如果 policy_ids 为 []，则清空所有的 policies
        return self.api.send(
            endpoint=f"{self.endpoint}/{self.id}",
            method="POST",
            data={"name": name, "policy_ids": policy_ids},
        )

    @property
    def policies(self):
        return AuthRolePolicyList(
            api=self.api, endpoint=f"{self.endpoint}/{self.id}/policies"
        )

    def get_variables(self, datasource_ids: str = None):
        return self.api.send(
            endpoint=f"{self.endpoint}/{self.id}/variables",
            method="GET",
            params={"datasource_ids": datasource_ids},
        )


class AuthRoleList(BaseResourceList):

    __do_not_print_properties__ = ["project_id", "description", "created_at"]

    @convert_to_object(cls=AuthRoleClient)
    def _get_all_resources(self):
        return self._get_all_resources_request()

    @convert_to_object(cls=AuthRoleClient)
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
                raise errors.AuthRoleNotFound(f"Role with name {name} not found")

    @property
    @convert_to_object(cls=AuthRoleClient)
    def latest(self):
        return self._get_latest_one_or_none()

    @convert_to_object(cls=AuthRoleClient)
    def create(self, name: str, policy_ids: list = None):
        if policy_ids is None:
            policy_ids = []
        return self.api.send(
            endpoint=self.endpoint,
            method="POST",
            data={"name": name, "policy_ids": policy_ids},
        )

    def delete(self, id=None, name=None):
        if id:
            return self.api.send(endpoint=f"{self.endpoint}/{id}", method="DELETE")
        elif name:
            role = self.get(name=name)
            return self.api.send(endpoint=f"{self.endpoint}/{role.id}", method="DELETE")
        else:
            raise ValueError("id or name must be provided")
