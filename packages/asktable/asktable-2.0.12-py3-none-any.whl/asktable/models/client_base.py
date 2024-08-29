from tabulate import tabulate
from asktable.log import log
from asktable.api import APIRequest


def convert_to_object(cls):
    """
    将JSON对象转换为Model对象的装饰器
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            json_or_list_data = func(*args, **kwargs)
            # 如果返回的是JSON or List对象
            if isinstance(json_or_list_data, list):
                obj_list = []
                for json_data in json_or_list_data:
                    obj = cls.load_from_dict(json_data)
                    # 将API对象传递给Model对象（从函数的第一个参数 self 中获取）
                    obj.api = args[0].api
                    obj.endpoint = args[0].endpoint
                    obj_list.append(obj)
                return obj_list
            elif isinstance(json_or_list_data, dict):
                obj = cls.load_from_dict(json_or_list_data)
                # 将API对象传递给Model对象（从函数的第一个参数 self 中获取）
                obj.api = args[0].api
                obj.endpoint = args[0].endpoint
                return obj
            elif json_or_list_data is None:
                return None
            elif isinstance(json_or_list_data, BaseResourceList):
                return json_or_list_data
            else:
                log.error(f"Unsupported data type: {type(json_or_list_data)}")
                raise ValueError(f"Unsupported data type {type(json_or_list_data)}")

        return wrapper

    return decorator


class BaseResourceList:
    __do_not_print_properties__ = []

    def __init__(
        self,
        api: APIRequest,
        endpoint: str,
        order="desc",
        page_size=20,
        page_number=1,
        extra_params=None,
    ):
        self.api = api
        self.endpoint = endpoint
        self.order = order
        self.page_size = page_size
        self.page_number = page_number
        self.extra_params = extra_params if extra_params else {}

    def __iter__(self):
        # 实现迭代器协议，允许直接迭代资源列表
        self._current = 0
        self._resources = self._get_all_resources() or []
        return self

    def __next__(self):
        if self._current >= len(self._resources):
            raise StopIteration
        resource = self._resources[self._current]
        self._current += 1
        return resource

    def _get_all_resources(self):
        """
        让子类实现，方便添加修饰函数
        """
        raise NotImplementedError

    def _get_all_resources_request(self, with_pagination=True):
        """
        使用翻页的方式获取所有资源
        """

        if with_pagination:
            params = {
                "order": self.order,
                "page_number": self.page_number,
                "page_size": self.page_size,
                **self.extra_params,
            }
            response = self.api.send(
                endpoint=self.endpoint, method="GET", params=params
            )

            data = response.get("data", [])
        else:
            params = self.extra_params
            data = self.api.send(endpoint=self.endpoint, method="GET", params=params)

        return data

    def _get_latest_one_or_none(self):
        """
        获取最新的一个资源
        """
        x = self._get_all_resources_request()
        if x:
            return x[0]
        else:
            return None

    def to_dict(self):
        return [resource.to_dict() for resource in self]

    def __repr__(self):
        # 将资源转换为字典列表
        resources_dicts = self.to_dict()

        # 去掉 __do_not_print_properties__ 字段
        if self.__do_not_print_properties__:
            for ds in resources_dicts:
                for i in self.__do_not_print_properties__:
                    ds.pop(i)

        # 截断长值
        max_start_length = 30  # 设置前面部分最大长度
        max_end_length = 10  # 设置后面部分最大长度
        for ds in resources_dicts:
            for key, value in ds.items():
                if isinstance(value, dict):
                    value = str(value)
                if isinstance(value, str) and len(value) > (
                    max_start_length + max_end_length
                ):
                    ds[key] = (
                        value[:max_start_length] + "........" + value[-max_end_length:]
                    )  # 截断并添加省略号
        # 使用 tabulate 来生成表格格式的字符串
        return tabulate(resources_dicts, headers="keys", tablefmt="plain")

    def count(self):
        return len(self._get_all_resources())
