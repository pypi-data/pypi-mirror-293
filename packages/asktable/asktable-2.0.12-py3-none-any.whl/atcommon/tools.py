import uuid
import base62
import time
from datetime import datetime


def format_time_ago(unix_timestamp: int) -> str:
    """
    Convert a Unix timestamp to a user-friendly time string.
    """
    if not unix_timestamp:
        return ""
    try:
        unix_timestamp = int(unix_timestamp)
    except:
        return str(unix_timestamp)

    now = int(time.time())
    unix_timestamp = int(unix_timestamp)
    diff = now - unix_timestamp

    # Time calculations
    minute = 60
    hour = 60 * minute
    day = 24 * hour

    if diff < hour:
        return f"{diff // minute} minutes ago" if diff >= minute else "Just now"
    elif diff < day:
        hours = diff // hour
        minutes = (diff % hour) // minute
        return (
            f"{hours} hours {minutes} minutes ago" if minutes else f"{hours} hours ago"
        )
    elif diff < 3 * day:
        return f"{diff // day} days ago"
    else:
        # Convert to specific date and time format for durations longer than 3 days
        return datetime.utcfromtimestamp(unix_timestamp).strftime("%Y-%m-%d %H:%M:%S")


def dict_to_markdown(d, indent=0, table_format_keys=()) -> str:
    # table_format_keys 中的key，会用table来展示，否则默认用列表展示
    # 假定table_format_keys 中的key对应的value是list，且list中的元素是dict，且dict的key是一样的
    markdown = ""
    if isinstance(d, dict):
        for key, value in d.items():
            # print(f"key: {key}, value: {value}, type: {type(value)}")
            if key in table_format_keys and value:
                # 特殊处理fields为表格，动态获取列名
                headers = value[0].keys()  # 从第一个元素获取所有键作为表头
                markdown += f"{'  ' * indent}* **{key}**: \n"
                markdown += f"{'  ' * indent}" + " | ".join(headers) + "\n"
                markdown += (
                    f"{'  ' * indent}" + " | ".join(["---"] * len(headers)) + "\n"
                )
                for field in value:
                    markdown += (
                        f"{'  ' * indent}"
                        + " | ".join([str(field[h]) for h in headers])
                        + "\n"
                    )

                markdown += "\n" + f"{'  ' * indent}-----\n\n"  # 分割线和空行

            else:
                markdown += f"{'  ' * indent}* **{key}**: "
                if isinstance(value, (dict, list)):
                    markdown += "\n" + dict_to_markdown(
                        value, indent + 1, table_format_keys=table_format_keys
                    )
                else:
                    markdown += f"{value}\n"
    elif isinstance(d, list):
        for item in d:
            if isinstance(item, (dict, list)):
                markdown += dict_to_markdown(
                    item, indent, table_format_keys=table_format_keys
                )
            else:
                markdown += f"{'  ' * indent}* {item}\n"
    return markdown


def gen_base62_uuid():
    # 生成一个 UUID
    my_uuid = uuid.uuid4()
    # 转换 UUID 的整数表示为 Base62
    base62_uuid = base62.encode(int(my_uuid))
    return base62_uuid


def gen_id(prefix=None):
    if prefix:
        return f"{prefix}_{gen_base62_uuid()}"
    else:
        return gen_base62_uuid()


def get_current_datetime() -> str:
    # 获取当前日期时间
    now = datetime.now()
    # 格式化日期时间
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    # 获取星期几
    day_of_week = now.strftime("%A")

    return f"Current Date and Time: {current_time}, Day of the Week: {day_of_week}"
