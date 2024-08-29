from datetime import datetime


class BaseCoreModel:
    __properties_init__ = []

    def __init__(self, **kwargs):
        for k in self.__properties_init__:
            setattr(self, k, kwargs.get(k))

    @classmethod
    def load_from_dict(cls, data: dict):
        if not data:
            return None
        return cls(**data)

    def to_dict(self):
        data = {}
        for k in self.__properties_init__:
            value = getattr(self, k)
            # 检查属性是否为 datetime 实例
            if isinstance(value, datetime):
                # 将 datetime 转换为 ISO 格式的字符串
                data[k] = value.isoformat()
            else:
                data[k] = value
        return data

    @classmethod
    def load_from_model(cls, model_obj):
        if not model_obj:
            return None

        data = {}
        for k in cls.__properties_init__:
            if hasattr(model_obj, k):
                data[k] = getattr(model_obj, k)
            else:
                data[k] = None
        return cls(**data)
