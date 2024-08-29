import argparse
import sys
import os
import requests

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


def encrypt_the_str(s):
    return s[:2] + "*" * (len(s) - 4) + s[-2:]


def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="Interactive CLI for AskTable client.")
    parser.add_argument(
        "-a",
        "--api_url",
        type=str,
        default="https://api.asktable.com",
        help="The AskTable API URL",
    )
    parser.add_argument(
        "-k", "--api_key", type=str, default="", help="The api-key for authentication."
    )

    args = parser.parse_args()

    # 导入 AskTable 类
    from asktable import AskTable
    from asktable.exceptions import Unauthorized, ServerConnectionError

    at = AskTable(api_key=args.api_key, api_url=args.api_url)
    encrypted_api_key = encrypt_the_str(args.api_key)
    print(f"\n-- AskTable 客户端({at.version})初始化...")
    print("-- 连接服务器(-a)：", args.api_url)
    try:
        response = requests.get("https://www.baidu.com")
        response.raise_for_status()
    except requests.exceptions.RequestException:
        print("\n[ERROR]连接服务器异常！请检查本机网络...\n")
        return
    try:
        k = at.me
    except Unauthorized:
        print(f"-- 使用API Key (-k)： API Key '{args.api_key}' 无效，请检查是否正确。")
        return
    except ServerConnectionError:
        print(f"\n[ERROR]连接服务器异常！请检查服务器状态...\n")
        return
    print("-- 使用API Key (-k)：", encrypted_api_key)
    print(
        "-- 您可以使用 'at' 来访问 AskTable，比如：通过 'at.datasources' 来查询数据源列表"
    )
    print("   完整的使用方法，请参考帮助文档：https://docs.asktable.com/\n")

    try:
        # 尝试导入 IPython
        from IPython import start_ipython

        start_ipython(argv=[], user_ns={"at": at})
    except ImportError:
        # 如果 IPython 未安装，使用标准 Python shell
        import code

        code.interact(local=locals())


if __name__ == "__main__":
    main()
