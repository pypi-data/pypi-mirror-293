import os
import importlib
import inspect

from model.Crawler import Crawler


def load_crawler_classes(crawlers_directory):
    crawler_classes = {}

    # 获取项目根目录的绝对路径
    project_root = os.path.abspath(os.getcwd())
    # 获取需要扫描的目录的绝对路径
    absolute_crawlers_directory = os.path.join(project_root, crawlers_directory)

    # 遍历目录下的所有文件
    for root, _, files in os.walk(absolute_crawlers_directory):
        for filename in files:
            if filename.endswith('.py') and filename != '__init__.py':
                # 计算相对于项目根目录的模块路径并转换为模块名称
                module_path = os.path.relpath(os.path.join(root, filename), start=project_root)
                module_name = module_path.replace(os.path.sep, '.').replace('.py', '')

                try:
                    # 动态导入模块
                    module = importlib.import_module(module_name)
                    # 检查模块中的每个对象
                    for name, obj in inspect.getmembers(module):
                        # 确保这是一个子类并且不是基类
                        if inspect.isclass(obj) and issubclass(obj, Crawler) and obj != Crawler:
                            crawler_name, _ = os.path.splitext(filename)
                            crawler_classes[crawler_name] = obj
                except Exception as e:
                    print(f"Failed to import {module_name}: {e}")

    return crawler_classes
