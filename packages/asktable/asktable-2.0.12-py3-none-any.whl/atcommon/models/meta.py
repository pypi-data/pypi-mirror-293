import re
from typing import Dict, List, Optional
from copy import deepcopy
from functools import wraps
import json
from tabulate import tabulate
from atcommon.tools import dict_to_markdown


def json_to_string(func):
    # 将函数返回的JSON dict对象转换为字符串
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return json.dumps(result, indent=4, ensure_ascii=False)

    return wrapper


class DataBaseObject:
    #  用于存储到数据库中的属性
    _save_in_db_properties = []

    @property
    def db_properties(self):
        return {
            k: v for k, v in self.__dict__.items() if k in self._save_in_db_properties
        }

    def to_dict(self):
        raise NotImplementedError

    @json_to_string
    def to_string(self):
        return self.to_dict()

    #
    # def to_dict_for_analysis(self):
    #     raise NotImplementedError
    #
    # @json_to_string
    # def to_string_for_analysis(self):
    #     return self.to_dict_for_analysis()


class DataField(DataBaseObject):
    _save_in_db_properties = [
        "name",
        "full_name",
        "origin_desc",
        "curr_desc",
        "curr_desc_stat",
        "sample_data",
        "data_type",
    ]
    _in_dict_properties = _save_in_db_properties + [
        "related_field",
        "related_field_precision_rate",
    ]

    def __init__(
        self,
        name,
        table,
        origin_desc=None,
        curr_desc=None,
        curr_desc_stat=None,
        related_field=None,
        related_field_precision_rate=None,
        sample_data=None,
        data_type=None,
        **kwargs,
    ):
        self.name = name
        self.origin_desc = origin_desc
        self.table = table  # Reference to the DataTable
        self.full_name = f"{self.table.schema.name}.{self.table.name}.{self.name}"
        if curr_desc:
            self.curr_desc = curr_desc
            self.curr_desc_stat = curr_desc_stat
        else:
            self.curr_desc = origin_desc
            self.curr_desc_stat = "origin"
        self.sample_data = sample_data
        self.data_type = data_type
        self.related_field = related_field  # Reference to related DataField, if any
        self.related_field_precision_rate = related_field_precision_rate

    def set_related_field(self, field):
        self.related_field = field

    def __repr__(self):
        return f"<DataField(name='{self.full_name}', curr_desc='{self.curr_desc}')>"

    def to_dict(self, includes=(), excludes=()):
        # includes 为空，则默认全部取
        # excludes 优先级高于 includes

        _d = {}
        for i in self._in_dict_properties:
            if i in excludes or (includes and i not in includes):
                continue
            _d[i] = getattr(self, i)

        if self.related_field:
            _d["related_field"] = self.related_field.full_name
        return _d


class DataTable(DataBaseObject):
    """
    name: 表名（sheet名、collection名）
    origin_desc: 数据源中的原始描述
    curr_desc: 当前在 RMB 中的描述
    curr_desc_stat: 当前描述的状态，可选值：origin, human, ai
    custom_configs: 自定义字段，用于存储一些额外的信息, dict类型，用json.dumps()转换为字符串存储
        对于Excel数据源的表格，custom_configs 中存储的是：tables

    """

    _save_in_db_properties = [
        "name",
        "full_name",
        "origin_desc",
        "curr_desc",
        "curr_desc_stat",
    ]

    _in_dict_properties = _save_in_db_properties

    def __init__(
        self,
        name,
        schema,
        origin_desc=None,
        curr_desc=None,
        curr_desc_stat=None,
        **kwargs,
    ):
        self.name = name
        self.origin_desc = origin_desc
        self.schema = schema  # Reference to the DataSchema
        self.full_name = f"{self.schema.name}.{self.name}"
        if curr_desc:
            self.curr_desc = curr_desc
            self.curr_desc_stat = curr_desc_stat
        else:
            # 如果没有指定 curr_desc，则默认使用 origin_desc
            self.curr_desc = origin_desc
            self.curr_desc_stat = "origin"
        self.fields = []
        self.fields_dict: Dict[str, DataField] = {}

    def add_field(self, field: DataField):
        self.fields.append(field)
        self.fields_dict[field.name] = field

    def remove_field(self, field_name: str):
        field = self.fields_dict.pop(field_name)
        self.fields.remove(field)

    def get_field(self, field_name):
        return self.fields_dict.get(field_name)

    def __repr__(self):
        return f"<DataTable(name='{self.full_name}', curr_desc='{self.curr_desc}')>"

    def to_dict(self, level="field", includes=(), excludes=()):
        _d = {}
        for i in self._in_dict_properties:
            if i in excludes or (includes and i not in includes):
                continue
            _d[i] = getattr(self, i)

        if level == "field":
            _d["fields"] = [
                f.to_dict(includes=includes, excludes=excludes) for f in self.fields
            ]
        return _d

    # def to_dict_for_analysis(self):
    #     # 如果有任何一个字段的 curr_desc 为空，则需要AI生成
    #     # table 中去掉一些不需要的字段，减少token数量
    #     # 保留：name, curr_desc
    #     need_analyse = any(not f.curr_desc for f in self.fields)
    #     if not self.curr_desc:
    #         need_analyse = True
    #     return self.to_dict(includes=('name', 'curr_desc')) if need_analyse else {}


class DataSchema(DataBaseObject):
    _save_in_db_properties = [
        "name",
        "origin_desc",
        "curr_desc",
        "curr_desc_stat",
        "custom_configs",
    ]
    _in_dict_properties = _save_in_db_properties

    def __init__(
        self,
        name,
        metadata,
        origin_desc=None,
        curr_desc=None,
        curr_desc_stat=None,
        custom_configs=None,
        **kwargs,
    ):
        self.name = name
        self.metadata = metadata  # Reference to the MetaData
        self.origin_desc = origin_desc
        if curr_desc:
            self.curr_desc = curr_desc
            self.curr_desc_stat = curr_desc_stat
        else:
            self.curr_desc = origin_desc
            self.curr_desc_stat = "origin"
        self.custom_configs = custom_configs
        self.tables = []
        self.tables_dict: Dict[str, DataTable] = {}

    def add_table(self, table: DataTable):
        self.tables.append(table)
        self.tables_dict[table.name] = table

    def remove_table(self, table_name: str):
        table = self.tables_dict.pop(table_name)
        self.tables.remove(table)

    def get_table(self, table_name):
        return self.tables_dict.get(table_name)

    @property
    def custom_configs_dict(self):
        if not self.custom_configs:
            return {}
        if isinstance(self.custom_configs, dict):
            return self.custom_configs
        elif isinstance(self.custom_configs, str):
            return json.loads(self.custom_configs)
        else:
            raise ValueError(
                f"Invalid custom_configs type: {type(self.custom_configs)}"
            )

    def set_custom_config(self, key, value):
        configs = self.custom_configs_dict
        configs[key] = value
        self.custom_configs = json.dumps(configs)

    def get_custom_config(self, key):
        return self.custom_configs_dict.get(key)

    def __repr__(self):
        return f"<Schema: {self.name}>"

    def to_dict(self, level="field", includes=(), excludes=()):
        # level: field, table, schema
        _d = {}
        for i in self._in_dict_properties:
            if i in excludes or (includes and i not in includes):
                continue
            _d[i] = getattr(self, i)

        if level in ("table", "field"):
            _d["tables"] = [
                t.to_dict(level, includes=includes, excludes=excludes)
                for t in self.tables
            ]
        return _d

    # def to_dict_for_analysis(self):
    #     # if table.to_dict_for_analyse() is empty, it will be ignored
    #     need_infer_tables = [table.to_dict_for_analysis() for table in self.tables
    #                          if table.to_dict_for_analysis()]
    #     if need_infer_tables or (not self.curr_desc):
    #         return {
    #             'name': self.name,
    #             'curr_desc': self.curr_desc,
    #             'tables': need_infer_tables
    #         }
    #     else:
    #         return {}


class MetaData(DataBaseObject):

    STATUS_PROCESSING = "processing"
    STATUS_FAILED = "failed"
    STATUS_SUCCESS = "success"
    STATUS_UNPROCESSED = "unprocessed"

    def __init__(self, name, datasource_id=""):
        self.name = name
        self.datasource_id = datasource_id
        self.schemas = []
        self.schemas_dict: Dict[str, DataSchema] = {}

    def add_schema(self, schema: DataSchema):
        self.schemas.append(schema)
        self.schemas_dict[schema.name] = schema

    def remove_schema(self, schema_name: str):
        schema = self.schemas_dict.pop(schema_name)
        self.schemas.remove(schema)

    def get_schema(self, schema_name):
        return self.schemas_dict.get(schema_name)

    def get_tables_by_schema(self):
        result = {}
        for s in self. schemas:
            result[s.name] = [t.name for t in s.tables]
        return result

    def filter_for_process(self) -> "MetaData":
        """
        返回一个新的 MetaData 对象，其中只包含需要分析的字段。
        """
        return self.load_from_processed_simple_dict(self.to_simple_dict_for_process())

    @classmethod
    def load_from_dict(cls, data: dict):
        """
        Load metadata from a dictionary structure.
        The expected format is:
        {
            'name': 'metadata_name',
            'datasource_id': '',
            'schemas': [
                {
                    'name': 'schema_name',
                    'tables': [
                        {
                            'name': 'table_name',
                            'fields': [
                                {
                                    'name': 'field_name',
                                    'origin_desc': 'original description',
                                    'related_field': 'schema2.table2.field2'
                                    ...
                                },
                                ...
                            ],
                            ...
                        },
                        ...
                    ],
                    ...
                },
                ...
            ]
        }
        """
        # 临时字典，用于存储字段引用
        field_refs = {}
        metadata = cls(data.get("name"), data.get("datasource_id"))
        # 首先，创建所有的 schema、table 和 field，但不设置 related_field
        for schema_data in data.get("schemas", []):
            schema = DataSchema(
                name=schema_data.get("name", ""),
                metadata=metadata,
                origin_desc=schema_data.get("origin_desc"),
                curr_desc=schema_data.get("curr_desc"),
                curr_desc_stat=schema_data.get("curr_desc_stat"),
                custom_configs=schema_data.get("custom_configs"),
            )

            for table_data in schema_data.get("tables", []):
                table = DataTable(
                    name=table_data.get("name", ""),
                    schema=schema,
                    origin_desc=table_data.get("origin_desc"),
                    curr_desc=table_data.get("curr_desc"),
                    curr_desc_stat=table_data.get("curr_desc_stat"),
                )

                for field_data in table_data.get("fields", []):
                    field = DataField(
                        name=field_data.get("name", ""),
                        table=table,
                        origin_desc=field_data.get("origin_desc"),
                        curr_desc=field_data.get("curr_desc"),
                        curr_desc_stat=field_data.get("curr_desc_stat"),
                        sample_data=field_data.get("sample_data"),
                        data_type=field_data.get("data_type"),
                    )
                    table.add_field(field)
                    # 创建一个唯一键来标识每个字段
                    field_key = f"{schema.name}.{table.name}.{field.name}"
                    field_refs[field_key] = field

                schema.add_table(table)

            metadata.add_schema(schema)

        # 现在，使用 field_refs 字典来设置 related_field 属性
        for _s in data.get("schemas", []):
            for _t in _s.get("tables", []):
                for _f in _t.get("fields", []):
                    field = field_refs.get(
                        f"{_s.get('name', '')}.{_t.get('name', '')}.{_f.get('name', '')}"
                    )
                    related_field_key = _f.get("related_field")
                    if related_field_key and related_field_key in field_refs:
                        # 设置相关字段的引用
                        field.set_related_field(field_refs[related_field_key])
        return metadata

    def update_from_dict(self, data: dict):
        """
        Update the existing metadata with the given dictionary.
        """
        # 临时存储字段关联信息
        temp_related_fields = {}

        # 更新或添加schemas
        for schema_data in data.get("schemas", []):
            schema_name = schema_data.get("name", "")
            schema = self.schemas_dict.get(schema_name)
            if not schema:
                # 如果找不到schema，就创建一个新的
                schema = DataSchema(
                    name=schema_name,
                    metadata=self,
                    origin_desc=schema_data.get("origin_desc"),
                    curr_desc=schema_data.get("curr_desc"),
                    curr_desc_stat=schema_data.get("curr_desc_stat"),
                    custom_configs=schema_data.get("custom_configs"),
                )
                self.add_schema(schema)
            else:
                # 更新schema的属性
                schema.origin_desc = schema_data.get("origin_desc", schema.origin_desc)
                schema.curr_desc = schema_data.get("curr_desc", schema.curr_desc)
                schema.curr_desc_stat = schema_data.get(
                    "curr_desc_stat", schema.curr_desc_stat
                )
                schema.custom_configs = schema_data.get(
                    "custom_configs", schema.custom_configs
                )

            # 更新或添加tables
            for table_data in schema_data.get("tables", []):
                table_name = table_data.get("name", "")
                table = schema.tables_dict.get(table_name)
                if not table:
                    # 如果找不到table，就创建一个新的
                    table = DataTable(
                        name=table_name,
                        schema=schema,
                        origin_desc=table_data.get("origin_desc"),
                        curr_desc=table_data.get("curr_desc"),
                        curr_desc_stat=table_data.get("curr_desc_stat"),
                    )
                    schema.add_table(table)
                else:
                    # 更新table的属性
                    table.origin_desc = table_data.get("origin_desc", table.origin_desc)
                    table.curr_desc = table_data.get("curr_desc", table.curr_desc)
                    table.curr_desc_stat = table_data.get(
                        "curr_desc_stat", table.curr_desc_stat
                    )

                # 更新或添加fields
                for field_data in table_data.get("fields", []):
                    field_name = field_data.get("name", "")
                    field = table.fields_dict.get(field_name)
                    if not field:
                        # 如果找不到field，就创建一个新的
                        field = DataField(
                            name=field_name,
                            table=table,
                            origin_desc=field_data.get("origin_desc"),
                            curr_desc=field_data.get("curr_desc"),
                            curr_desc_stat=field_data.get("curr_desc_stat"),
                            sample_data=field_data.get("sample_data"),
                            data_type=field_data.get("data_type"),
                        )
                        table.add_field(field)
                    else:
                        # 更新field的属性
                        field.origin_desc = field_data.get(
                            "origin_desc", field.origin_desc
                        )
                        field.curr_desc = field_data.get("curr_desc", field.curr_desc)
                        field.curr_desc_stat = field_data.get(
                            "curr_desc_stat", field.curr_desc_stat
                        )
                        field.sample_data = field_data.get(
                            "sample_data", field.sample_data
                        )
                        field.data_type = field_data.get("data_type", field.data_type)

                    # 保存字段关联信息
                    full_field_name = f"{schema_data.get('name')}.{table_data.get('name')}.{field_data.get('name')}"
                    related_field_name = field_data.get("related_field")
                    if related_field_name:
                        # 存储字段关联信息，稍后处理
                        temp_related_fields[full_field_name] = related_field_name

        # 更新related_field
        for field_name, related_field_name in temp_related_fields.items():
            field = self.get_field_by_full_name(field_name)
            related_field = self.get_field_by_full_name(related_field_name)
            if field and related_field:
                # 设置字段关联
                field.set_related_field(related_field)

    def to_dict(self, level="field", includes=(), excludes=()):
        # level: field, table, schema
        # includes 默认取全部
        # excludes 优先级高于includes
        return {
            "name": self.name,
            "datasource_id": self.datasource_id,
            "schemas": [
                schema.to_dict(level, includes=includes, excludes=excludes)
                for schema in self.schemas
            ],
        }

    def to_dict_for_prompt(self, with_data_type=False):
        if with_data_type:
            includes = ("name", "full_name", "curr_desc", "data_type")
        else:
            includes = ("name", "full_name", "curr_desc")

        result = {
            "name": self.name,
            # 'datasource_id': self.datasource_id,
            "schemas": [
                schema.to_dict(level="field", includes=includes)
                for schema in self.schemas
            ],
        }

        # 修改fields的结构，减少token数量
        for schema in result["schemas"]:
            for table in schema.get("tables", []):
                for field in table.get("fields", []):
                    field.pop("full_name", None)
                    # 去掉无用的 related_field
                    if field.get("related_field") is None:
                        field.pop("related_field", None)
                        field.pop("related_field_precision_rate", None)

                    # 更名，更直接，更少的字符
                    field["desc"] = field.pop("curr_desc", None)

        return result

    def to_markdown_for_prompt(self, with_data_type=False) -> str:
        return dict_to_markdown(
            self.to_dict_for_prompt(with_data_type=with_data_type),
            table_format_keys=("fields",),
        )

    def to_simple_dict_for_process(self) -> dict:
        schemas = []
        for s in self.schemas:
            tables = []
            for t in s.tables:
                if t.curr_desc and all([f.curr_desc for f in t.fields]):
                    continue
                fields = []
                for f in t.fields:
                    if f.curr_desc and f.curr_desc_stat in ("human", "origin"):
                        fields.append((f.name, f.curr_desc))
                    else:
                        fields.append((f.name, ""))
                tables.append({"name": t.name, "fields": fields})
            schemas.append({"name": s.name, "tables": tables})
        return {
            "name": self.name,
            "datasource_id": self.datasource_id,
            "schemas": schemas,
        }

    @classmethod
    def load_from_processed_simple_dict(cls, data: dict) -> "MetaData":
        """
        data =
        {
            "name": [name],
            "datasource_id": [datasource_id],
            "schemas": [
                {
                    "name": [schema_name],
                    "curr_desc": [schema_curr_desc],
                    "tables": [
                        {
                            "name": [table_name],
                            "curr_desc": [table_curr_desc],
                            "fields": [
                                ["field_name_1", "filed_curr_desc_1"],
                                ["field_name_2", "filed_curr_desc_2"],
                            ]
                        },
                    ]
                }
            ]
        }
        """
        metadata = cls(data.get("name", ""), data.get("datasource_id", ""))

        # 遍历分析后的数据中的 schema
        for schema_data in data.get("schemas", []):
            schema = DataSchema(
                name=schema_data.get("name", ""),
                metadata=metadata,
                curr_desc=schema_data.get("curr_desc", ""),
            )

            # 遍历 schema 中的 table
            for table_data in schema_data.get("tables", []):
                table = DataTable(
                    name=table_data.get("name", ""),
                    schema=schema,
                    curr_desc=table_data.get("curr_desc", ""),
                )

                # 遍历 table 中的 fields
                for field_data in table_data.get("fields", []):
                    field = DataField(
                        name=field_data[0],  # field 名称
                        table=table,
                        curr_desc=field_data[1],  # field 描述
                    )
                    table.add_field(field)

                schema.add_table(table)

            metadata.add_schema(schema)

        return metadata

    def get_field_by_full_name(self, full_name):
        """
        根据字段的完整名称来查找字段对象。
        完整名称格式为 "schema_name.table_name.field_name"
        """
        schema_name, table_name, field_name = full_name.split(".")
        for schema in self.schemas:
            if schema.name == schema_name:
                for table in schema.tables:
                    if table.name == table_name:
                        for field in table.fields:
                            if field.name == field_name:
                                return field
        return None

    @property
    def overview(self):
        return f"<{self.datasource_id}>[{self.schema_count}S|{self.table_count}T|{self.field_count}F]"

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        output = "\n"
        for schema in self.schemas:
            schema_data = []  # Prepare data for the current schema
            schema_desc = schema.name
            schema_desc += f" ({schema.curr_desc})" if schema.curr_desc else ""
            schema_desc += "\n" + "-" * 30

            for table in schema.tables:
                table_name = table.name
                table_desc = table.curr_desc if table.curr_desc else ""
                analysed_f = len([f for f in table.fields if f.curr_desc])
                all_f = len(table.fields)
                fields = f"{analysed_f}/{all_f}"
                schema_data.append(
                    {
                        "Table Name": table_name,
                        "Table Desc": table_desc,
                        "Fields(analysed/all)": fields,
                    }
                )

            output += (
                f"{schema_desc}\n"
                + tabulate(schema_data, headers="keys", tablefmt="plain")
                + "\n\n"
            )

        return output

    @property
    def schema_count(self):
        return len(self.schemas)

    @property
    def table_count(self):
        return sum([len(schema.tables) for schema in self.schemas])

    @property
    def field_count(self):
        return sum(
            [len(table.fields) for schema in self.schemas for table in schema.tables]
        )

    def split_into_chunks(self, max_tables_per_chunk=5) -> List["MetaData"]:
        """
        Split the MetaData into smaller MetaData chunks, each with a maximum of 10 tables.
        """
        chunks = []
        current_chunk = None
        table_count = 0

        for schema in self.schemas:
            for table in schema.tables:
                # 当前 chunk 已满或不存在时，创建新的 chunk
                if current_chunk is None or table_count >= max_tables_per_chunk:
                    current_chunk = MetaData(
                        name=f"{self.name}_chunk{len(chunks) + 1}",
                        datasource_id=self.datasource_id,
                    )
                    chunks.append(current_chunk)
                    table_count = 0

                # 在新的 chunk 中添加当前 schema 和 table
                cloned_schema = current_chunk.schemas_dict.get(schema.name)
                if cloned_schema is None:
                    cloned_schema = DataSchema(
                        name=schema.name,
                        metadata=current_chunk,
                        origin_desc=schema.origin_desc,
                        curr_desc=schema.curr_desc,
                        curr_desc_stat=schema.curr_desc_stat,
                        custom_configs=schema.custom_configs,
                    )
                    current_chunk.add_schema(cloned_schema)

                # 使用 deepcopy 来复制表
                cloned_table = deepcopy(table)

                # 请确保在复制前后，更新 cloned_table 的 schema 属性
                cloned_table.schema = cloned_schema

                # 现在可以安全地添加 cloned_table 到新 schema 中
                cloned_schema.add_table(cloned_table)

                table_count += 1

        return chunks

    def filter_tables_by_names(self, table_full_names: List[str]) -> "MetaData":
        """
        Filter tables by their full names and create a new MetaData instance containing only these tables.

        :param table_full_names: A list of full names of tables to be included in the new MetaData instance.
        :return: A new MetaData instance with the specified tables.
        """
        # 创建一个新的 MetaData 实例
        filtered_metadata = MetaData(
            name=f"{self.name}_filtered", datasource_id=self.datasource_id
        )

        for full_name in table_full_names:
            schema_name, table_name = full_name.rsplit(".", 1)

            # 查找匹配的 schema 和 table
            schema = self.get_schema(schema_name)
            if schema:
                table = schema.get_table(table_name)
                if table:
                    # 如果找到匹配的 table，则复制到新的 MetaData 实例中
                    # 首先确保 schema 存在于新的 MetaData 实例中
                    filtered_schema = filtered_metadata.get_schema(schema_name)
                    if not filtered_schema:
                        # 如果不存在，则复制 schema 到新的 MetaData 实例中
                        filtered_schema = DataSchema(
                            name=schema.name,
                            metadata=filtered_metadata,
                            origin_desc=schema.origin_desc,
                            curr_desc="",  # 因为过滤了部分meta，所以curr_desc置空
                            curr_desc_stat=schema.curr_desc_stat,
                            custom_configs=schema.custom_configs,
                        )
                        filtered_metadata.add_schema(filtered_schema)

                    # 然后复制 table 到新的 schema 中
                    cloned_table = deepcopy(table)
                    # 更新 cloned_table 的 schema 属性为新的 schema
                    cloned_table.schema = filtered_schema
                    filtered_schema.add_table(cloned_table)

        return filtered_metadata

    #
    # def get_schema_names(self, pattern=None) -> List[str]:
    #     """
    #     Return a list of schema names that match the given pattern.
    #     """
    #     if pattern:
    #         regex = re.compile(pattern)
    #         return [schema.name for schema in self.schemas if regex.match(schema.name)]
    #     return [schema.name for schema in self.schemas]
    #
    # def get_table_names(self, schema_pattern=None, table_pattern=None):
    #     table_names = []
    #     schema_regex = re.compile(schema_pattern) if schema_pattern else None
    #     table_regex = re.compile(table_pattern) if table_pattern else None
    #     for schema in self.schemas:
    #         if not schema_pattern or schema_regex.match(schema.name):
    #             for table in schema.tables:
    #                 if not table_pattern or table_regex.match(table.name):
    #                     table_names.append(f"{schema.name}.{table.name}")
    #     return table_names
    #
    # def get_field_names(self, schema_pattern=None, table_pattern=None, field_pattern=None) -> dict[str, List[str]]:
    #     """
    #     Return a dictionary of field names, where the key is the table name and the value is a list of field names.
    #     """
    #     field_names = {}
    #     schema_regex = re.compile(schema_pattern) if schema_pattern else None
    #     table_regex = re.compile(table_pattern) if table_pattern else None
    #     field_regex = re.compile(field_pattern) if field_pattern else None
    #     for schema in self.schemas:
    #         if not schema_pattern or schema_regex.match(schema.name):
    #             for table in schema.tables:
    #                 if not table_pattern or table_regex.match(table.name):
    #                     fields_in_table = []
    #                     for field in table.fields:
    #                         if not field_pattern or field_regex.match(field.name):
    #                             fields_in_table.append(f"{schema.name}.{table.name}.{field.name}")
    #                     field_names[f"{schema.name}.{table.name}"] = fields_in_table
    #     return field_names

    def filter_by_regex(
        self, schema_pattern=None, table_pattern=None, field_pattern=None
    ) -> "MetaData":
        """
        Filter the metadata by regular expressions and return
        a new MetaData instance containing only the matching items.
        if a pattern is None, it will not be used for filtering, so all items will be included.
        """
        filtered_metadata = MetaData(
            name=f"{self.name}_regex_filtered", datasource_id=self.datasource_id
        )

        # 预编译正则表达式
        schema_regex = re.compile(schema_pattern) if schema_pattern else None
        table_regex = re.compile(table_pattern) if table_pattern else None
        field_regex = re.compile(field_pattern) if field_pattern else None

        # 遍历所有schemas
        for schema in self.schemas:
            # 检查schema是否匹配
            if schema_regex and not schema_regex.match(schema.name):
                continue  # 如果schema不匹配，则跳过当前schema

            # 创建一个新的schema对象
            new_schema = DataSchema(
                name=schema.name,
                metadata=filtered_metadata,
                origin_desc=schema.origin_desc,
                curr_desc="",  # 因为过滤了部分meta，所以curr_desc置空
                curr_desc_stat=schema.curr_desc_stat,
                custom_configs=schema.custom_configs,
            )
            schema_added = False

            # 遍历所有tables
            for table in schema.tables:
                # 检查table是否匹配
                if table_regex and not table_regex.match(table.name):
                    continue  # 如果table不匹配，跳过当前table

                # 创建一个新的table对象
                new_table = DataTable(
                    name=table.name,
                    schema=new_schema,
                    origin_desc=table.origin_desc,
                    curr_desc=table.curr_desc,
                    curr_desc_stat=table.curr_desc_stat,
                )
                table_added = False

                # 遍历所有fields
                for field in table.fields:
                    # 检查field是否匹配
                    if field_regex and not field_regex.match(field.name):
                        continue  # 如果field不匹配，跳过当前field

                    # 添加匹配的field到new_table
                    new_field = deepcopy(field)
                    new_field.table = new_table
                    new_table.add_field(new_field)
                    table_added = True

                # 如果new_table添加了至少一个field，将其加入到new_schema
                if table_added:
                    new_schema.add_table(new_table)
                    schema_added = True

            # 如果new_schema添加了至少一个table，将其加入到filtered_metadata
            if schema_added:
                filtered_metadata.add_schema(new_schema)

        return filtered_metadata


def merge_metas(allow_metas: list[MetaData], deny_metas: list[MetaData]) -> MetaData:
    # 创建一个新的 MetaData 实例作为结果
    result_meta = MetaData(name="MergedMetaData")

    # 先合并所有允许的 meta
    for allow_meta in allow_metas:
        for schema in allow_meta.schemas:
            result_schema = result_meta.get_schema(schema.name)
            if not result_schema:
                # 如果结果 meta 中还没有这个 schema，复制它
                result_schema = DataSchema(
                    name=schema.name,
                    metadata=result_meta,
                    origin_desc=schema.origin_desc,
                    curr_desc=schema.curr_desc,
                    curr_desc_stat=schema.curr_desc_stat,
                    custom_configs=schema.custom_configs,
                )
                result_meta.add_schema(result_schema)

            for table in schema.tables:
                result_table = result_schema.get_table(table.name)
                if not result_table:
                    # 如果结果 schema 中还没有这个 table，复制它
                    result_table = DataTable(
                        name=table.name,
                        schema=result_schema,
                        origin_desc=table.origin_desc,
                        curr_desc=table.curr_desc,
                        curr_desc_stat=table.curr_desc_stat,
                    )
                    result_schema.add_table(result_table)

                for field in table.fields:
                    # 检查这个 field 是否已经在结果 table 中
                    result_field = result_table.get_field(field.name)
                    if not result_field:
                        # 如果不在，复制它
                        new_field = DataField(
                            name=field.name,
                            table=result_table,
                            origin_desc=field.origin_desc,
                            curr_desc=field.curr_desc,
                            curr_desc_stat=field.curr_desc_stat,
                            related_field=field.related_field,
                            related_field_precision_rate=field.related_field_precision_rate,
                            sample_data=field.sample_data,
                            data_type=field.data_type,
                        )
                        result_table.add_field(new_field)

    # 然后剔除所有禁止的 meta
    for deny_meta in deny_metas:
        for schema in deny_meta.schemas:
            for table in schema.tables:
                for field in table.fields:
                    # 尝试找到并移除 field
                    full_field_name = f"{schema.name}.{table.name}.{field.name}"
                    field_to_remove = result_meta.get_field_by_full_name(
                        full_field_name
                    )
                    if field_to_remove:
                        # field_to_remove.table.fields.remove(field_to_remove)
                        field_to_remove.table.remove_field(field_to_remove.name)
                        # 如果 table 中没有 field 了，也移除 table
                        if not field_to_remove.table.fields:
                            # field_to_remove.table.schema.tables.remove(field_to_remove.table)
                            field_to_remove.table.schema.remove_table(
                                field_to_remove.table.name
                            )
                            # 如果 schema 中没有 table 了，也移除 schema
                            if not field_to_remove.table.schema.tables:
                                # result_meta.schemas.remove(field_to_remove.table.schema)
                                result_meta.remove_schema(
                                    field_to_remove.table.schema.name
                                )

    return result_meta
