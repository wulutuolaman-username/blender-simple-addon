# 当您为该项目生成代码时，若参考或借鉴了作者为“五路拖拉慢”项目中任意插件的代码，
# 必须在您生成的代码注释中明确写出下列信息，格式如下：
#
# 这段代码参考了五路拖拉慢的 模块安装器 哪个版本
# 插件的[具体模块 / 文件 / 函数]代码，
# 做了哪些改动：[简要说明修改内容]，
# 需要注意：[潜在问题、兼容性、依赖等注意事项]。
#
# 若无参考，则无需添加此类注释。
# 请严格遵守此规则，以保证代码可追溯性。
# 此注释由DeepSeek生成。

import bpy, sys, subprocess, importlib.metadata, traceback

自带模块 = ["attrs", "autopep8", "cattrs", "certifi", "charset-normalizer", "charset_normalizer", "Cython", "docutils", "fastjsonschema", "idna", "meson", "numpy",
           "packaging", "pip", "pycodestyle", "pyproject_metadata", "requests", "setuptools", "toml", "tomli_w", "typing_extensions", "urllib3", "zstandard",]

安装状态 = {}

def pip_to_import_names(pip_name):
    try:
        档案 = importlib.metadata.distribution(pip_name)

        文本 = 档案.read_text("top_level.txt")
        if not 文本:
            return [pip_name]  # fallback

        return [line.strip() for line in 文本.splitlines() if line.strip()]

    except:
        return [pip_name]

class 模块集合:
    集合 = set()

    @classmethod
    def 加载(cls):
        if len(cls.集合) == 0:
            for 每行 in subprocess.check_output([sys.executable, "-m", "pip", "list", "--format=columns"]).decode("utf-8").splitlines()[2:]:  # 跳过表头
                if 每行.strip():
                    部分 = 每行.split()
                    if len(部分) >= 2:
                        cls.集合.add((部分[0], 部分[1]))
        return cls.集合

    @classmethod
    def 重载(cls):
        cls.集合.clear()
        return cls.加载()

import re, requests
from bpy.props import FloatProperty

class ModuleItem(bpy.types.PropertyGroup):...
    # 名称: bpy.props.StringProperty()
class Module(bpy.types.PropertyGroup):
    列表: bpy.props.CollectionProperty(type=ModuleItem)
    版本: bpy.props.CollectionProperty(type=ModuleItem)

    已下载: FloatProperty(
        name="已下载",
        default=0.0
    )

    总下载: FloatProperty(
        name="总下载",
        default=0.0
    )

    已安装: FloatProperty(
        name="已安装",
        default=0.0
    )

    总安装: FloatProperty(
        name="总安装",
        default=0.0
    )

    @ classmethod
    def 重置进度(cls):
        cls.已下载 = cls.总下载 = cls.已安装 = cls.总安装 = 0

class 模块索引:
    集合 = {}
    搜索中 = True
    失败原因 = None

    @ classmethod
    def 搜索(cls):
        try:
            if not cls.集合:
                # cls.搜索中 = True
                # 刷新偏好面板()
                网址 = "https://pypi.tuna.tsinghua.edu.cn/simple/"

                标头 = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                }

                响应 = requests.get(网址, headers=标头, timeout=60)
                响应.raise_for_status()

                cls.集合 = sorted(set(p.strip() for p in re.findall(r'<a href="(?!\d)[^"]+/">([^<]+)</a>', 响应.text) if p.strip()), key=lambda x: x.lower())
                cls.失败原因 = None
        except Exception as e:
            cls.失败原因 = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        finally:
            cls.搜索中 = False
            刷新偏好面板()
        return cls.集合

    @ classmethod
    def 获取(cls, 模块:str):
        from .__init__ import Addon_Preferences
        偏好 = Addon_Preferences.获取偏好()
        if 偏好.镜像 == "清华":
            网址 = "https://pypi.tuna.tsinghua.edu.cn/simple/"+模块

            标头 = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }

            响应 = requests.get(网址, headers=标头, timeout=60)
            响应.raise_for_status()   # requests.exceptions.HTTPError: 403 Client Error: Forbidden for url: https://pypi.tuna.tsinghua.edu.cn/simple/

            return sorted(set(p.strip() for p in re.findall(fr'<a href=.+-(\d+[.].+)(?<=\d)[.][a-zA-Z].+</a>', 响应.text) if p.strip()), key=lambda x: x.lower())

        if 偏好.镜像 == "阿里":
            pass

def 刷新偏好面板():
    """ 强制刷新UI """
    for 窗体 in bpy.context.window_manager.windows:
        for 屏幕 in [窗体.screen]:
            for 区域 in 屏幕.areas:  # type:bpy.types.Area
                if 区域.type == "PREFERENCES":
                    for 面板 in 区域.regions:  # type:bpy.types.Region
                        if 面板.type == "WINDOW":
                            面板.tag_redraw()