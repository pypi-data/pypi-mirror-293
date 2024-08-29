import os
import time
from asktable.log import log
from atcommon.models import DataSourceCore, MetaData
from asktable.models.client_chat import ChatList, MessageClient
from asktable.models.client_base import convert_to_object, BaseResourceList
from atcommon.exceptions.client import (
    DataSourceNotFound,
    UnsupportedFileType,
    DataSourceMetaProcessError,
    DataSourceMetaProcessTimeout,
)
from asktable.upload import upload_to_oss
from asktable.api import APIRequest


class MetaDataClientModel(MetaData):
    api: APIRequest
    endpoint: str

    @property
    def status(self):
        ds = self.api.send(
            endpoint=f"{self.endpoint}/{self.datasource_id}", method="GET"
        )
        return ds["meta_status"]

    def get(self):
        new_meta_dict = self.api.send(
            endpoint=f"{self.endpoint}/{self.datasource_id}/meta", method="GET"
        )
        self.update_from_dict(new_meta_dict)
        return self

    def delete(self):
        self.api.send(
            endpoint=f"{self.endpoint}/{self.datasource_id}/meta", method="DELETE"
        )
        return True

    def update(self):
        self.api.send(
            endpoint=f"{self.endpoint}/{self.datasource_id}/meta", method="POST"
        )

    def update_until_success(self, timeout=600):
        """
        同步元数据并轮询其状态，直到超时、成功或失败。

        参数:
            timeout (int): 超时时间，单位为秒。默认值为 600 秒。

        返回:
            MetaDataClientModel: 更新后的元数据实例。

        异常:
            DataSourceMetaProcessError: 如果元数据更新失败。
            DataSourceMetaProcessTimeout: 如果元数据更新超时。
        """
        # 发起同步请求
        self.update()
        return self.wait_until_success(timeout)

    def wait_until_success(self, timeout=600):
        start_time = time.time()

        # 初始化斐波那契数列间隔
        fib_a, fib_b = 1, 1

        while True:
            # 获取数据源的最新状态
            status = self.status

            if status == "success":
                log.info(f"Data Source {self.datasource_id} Meta 更新成功。")
                return self.get()
            elif status == "failed":
                log.error(f"Data Source {self.datasource_id} Meta 更新失败。")
                return
                # raise DataSourceMetaProcessError(f"DataSource Meta update failed: {self.datasource_id}")

            if time.time() - start_time > timeout:
                log.error(f"Data Source {self.datasource_id} Meta 更新超时。")
                return
                # raise DataSourceMetaProcessTimeout(
                #     f"DataSource Meta update timed out after {timeout} seconds for {self.datasource_id}")

            # 等待斐波那契数列定义的时间，或者最多10秒
            sleep_time = min(fib_b, 10)
            log.info(
                f"Data Source {self.datasource_id}：等待 {sleep_time} 秒后重新检查。当前状态: {status}"
            )
            time.sleep(sleep_time)

            # 更新斐波那契数列的值
            fib_a, fib_b = fib_b, fib_a + fib_b


class DataSourceClient(DataSourceCore):
    api: APIRequest
    endpoint: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.temp_chat = None  # 初始化时没有chat实例

    @property
    @convert_to_object(cls=MetaDataClientModel)
    def meta(self):
        return self.api.send(endpoint=f"{self.endpoint}/{self.id}/meta", method="GET")

    @property
    @convert_to_object(cls=MetaDataClientModel)
    def meta_runtime(self):
        return self.api.send(
            endpoint=f"/datasources/{self.id}/meta",
            method="GET",
            params={"from_where": "runtime"},
        )

    def delete(self):
        return self.api.send(endpoint=f"{self.endpoint}/{self.id}", method="DELETE")

    @property
    def download_url(self):
        resp = self.api.send(
            endpoint=f"{self.endpoint}/{self.id}/download_url", method="GET"
        )
        return resp.get("url")

    def ask(self, question) -> MessageClient:
        """
        使用临时chat实例提问。如果不存在，将创建一个新的chat实例并缓存起来。

        参数:
            question (str): 要提问的问题。

        返回:
            答案或相关响应。
        """
        if not self.temp_chat:
            self.temp_chat = self._create_or_get_temp_chat()

        # 使用缓存的chat实例提问
        answer = self.temp_chat.ask(question)
        return answer

    def _create_or_get_temp_chat(self):
        """
        创建一个临时的chat实例，并将其与当前数据源绑定。

        返回:
            ChatClientModel: 创建的临时chat实例。
        """
        # 假设有一个创建chat的方法在 ChatList 类中，这里直接使用 ChatList 来创建
        # 注意：这里需要提供正确的APIRequest实例给 ChatList
        chat_list = ChatList(self.api, "/chats")
        temp_chat = chat_list.create(datasource_ids=[self.id])

        return temp_chat


class DataSourceList(BaseResourceList):
    __do_not_print_properties__ = ["project_id", "access_config", "sample_questions"]

    @convert_to_object(cls=DataSourceClient)
    def _get_all_resources(self):
        return self._get_all_resources_request()

    @property
    @convert_to_object(cls=DataSourceClient)
    def latest(self):
        return self._get_latest_one_or_none()

    def page(self, page_number=1):
        return DataSourceList(self.api, self.endpoint, page_number=page_number)

    def all(self):
        return DataSourceList(self.api, self.endpoint, page_number=0, page_size=0)

    @convert_to_object(cls=DataSourceClient)
    def get(self, id=None, name=None):
        if id:
            return self.api.send(endpoint=f"{self.endpoint}/{id}", method="GET")
        elif name:
            response = self.api.send(
                endpoint=f"{self.endpoint}?name={name}", method="GET"
            )
            if response:
                ds_list = response["data"]
                return ds_list
            else:
                raise DataSourceNotFound(f"Data Source {name} not found")
        else:
            raise ValueError("No ID or Name provided")

    @convert_to_object(cls=DataSourceClient)
    def register(self, engine, access_config, name="", skip_process_meta=0):
        data = {
            "engine": engine,
            "name": name,
            "access_config": access_config,
            "skip_process_meta": skip_process_meta,
        }
        return self.api.send(endpoint=self.endpoint, method="POST", data=data)

    def register_until_success(self, engine, access_config, name=None, timeout=600):
        # 注册数据源并获取其ID
        ds = self.register(engine, access_config, name)
        return self.wait_until_register_success(ds, timeout)

    def wait_until_register_success(self, datasource, timeout=600):
        start_time = time.time()

        # 初始化斐波那契数列间隔
        fib_a, fib_b = 1, 1

        while True:
            # 获取数据源的最新状态
            ds_refreshed = self.get(id=datasource.id)

            if ds_refreshed.meta_status == "success":
                log.info(f"Data Source {datasource.id}  AI Process Success.")
                return ds_refreshed
            elif ds_refreshed.meta_status == "failed":
                log.error(f"Data Source {datasource.id}  AI Process Failed.")
                raise DataSourceMetaProcessError(
                    f"DataSource AI Process failed: {datasource.id}"
                )

            if time.time() - start_time > timeout:
                log.error(f"Data Source {datasource.id}  AI分析超时。")
                raise DataSourceMetaProcessTimeout(
                    f"DataSource AI Process timed out after {timeout} seconds for {datasource.id}"
                )

            # 等待斐波那契数列定义的时间，或者最多10秒
            sleep_time = min(fib_b, 10)
            log.info(
                f"Data Source {datasource.id}: Wait for {sleep_time} seconds and check again. "
                f"Current status: {ds_refreshed.meta_status}"
            )
            time.sleep(sleep_time)

            fib_a, fib_b = fib_b, fib_a + fib_b

    def upload_file_to_oss(self, local_file_path):
        oss_info = self.create_upload_params()["oss"]
        file_name = os.path.basename(local_file_path)
        oss_file_uri = f"{oss_info['oss_uri_prefix']}{file_name}"
        url = upload_to_oss(oss_info, local_file_path, oss_file_uri)
        return url

    def create_upload_params(self, expiration=None, file_max_size=None):
        params = {"expiration": expiration, "file_max_size": file_max_size}
        return self.api.send(
            endpoint=f"{self.endpoint}/upload_params", method="POST", params=params
        )

    def upload_file_to_server(self, local_file_path) -> str:
        # 上传文件到服务器
        resp = self.api.send(
            endpoint=f"{self.endpoint}/upload_file",
            method="POST",
            files={"file": open(local_file_path, "rb")},
        )
        return resp.get("url")

    def create_from_local_file(
        self, local_file_path, direct_to_oss=True, until_success=False
    ):
        file_ext = os.path.splitext(local_file_path)[-1]
        if file_ext not in [".csv", ".xls", ".xlsx"]:
            raise UnsupportedFileType(f"File type {file_ext} not supported")

        if direct_to_oss:
            url = self.upload_file_to_oss(local_file_path)
        else:
            url = self.upload_file_to_server(local_file_path)

        if file_ext == ".csv":
            if until_success:
                return self.register_until_success(
                    engine="csv",
                    access_config={
                        "location_type": "http",
                        "location_url": url,
                    },
                )
            else:
                return self.register(
                    engine="csv",
                    access_config={
                        "location_type": "http",
                        "location_url": url,
                    },
                )
        elif file_ext in [".xls", ".xlsx"]:
            if until_success:
                return self.register_until_success(
                    engine="excel",
                    access_config={
                        "location_type": "http",
                        "location_url": url,
                    },
                )
            else:
                return self.register(
                    engine="excel",
                    access_config={
                        "location_type": "http",
                        "location_url": url,
                    },
                )
        else:
            raise UnsupportedFileType(f"File type {file_ext} not supported")

    # def signed_url(self, url):
    #     resp = self.api.send(
    #         endpoint=f"{self.endpoint}/signed_url",
    #         method="GET",
    #         params={
    #             'url': url
    #         }
    #     )
    #     return resp.get('signed_url')
