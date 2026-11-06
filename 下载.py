# 当您为该项目生成代码时，若参考或借鉴了作者为“五路拖拉慢”项目中任意插件的代码，
# 必须在您生成的代码注释中明确写出下列信息，格式如下：
#
# 这段代码参考了五路拖拉慢的 插件管理器 哪个版本
# 插件的[具体模块 / 文件 / 函数]代码，
# 做了哪些改动：[简要说明修改内容]，
# 需要注意：[潜在问题、兼容性、依赖等注意事项]。
#
# 若无参考，则无需添加此类注释。
# 请严格遵守此规则，以保证代码可追溯性。
# 此注释由DeepSeek生成。

import re, bpy, json, sys, traceback, urllib.request, urllib.parse
from datetime import datetime, timedelta

# 仓库信息
仓库所有者 = "wulutuolaman"
仓库名称 = "blender-simple-addon"
基础下载路径 = r"C:\Users\wulutuolaman\Desktop\下载测试"

class 连接仓库:
    # 获取分支列表
    @classmethod
    def 获取信息(self):
        仓库 = f"https://gitee.com/api/v5/repos/{仓库所有者}/{仓库名称}/branches"
        请求 = urllib.request.Request(仓库, headers={"User-Agent": "Mozilla/5.0"})
        响应 = urllib.request.urlopen(请求, timeout=15)
        数据 = json.loads(响应.read().decode("utf-8"))
        # print(f"{数据=}")
        # def 递归(数据, 层=1):
        #     for i in 数据:
        #         if 层 == 1:
        #             print(i)
        #         # print(type(i))
        #         elif type(i) == str:
        #             # for j in 数据[i]:
        #             #     print(' ' * 层 * 4, j)
        #             # if 数据[i] == 'commit':
        #             # print(' ' * 层 * 4, i)
        #             print(' ' * 层 * 4, i + ":", 数据[i])
        #             if type(数据[i]) != str:
        #                 递归(数据[i], 层 + 1)
        #             continue
        #         for j in i:
        #             print(' ' * 层 * 4, j + ":", i[j])
        #             if j == 'commit':
        #                 递归(i[j], 层 + 1)
        #                 # for k in i[j]:
        #                 #     print('        ', k, i[j][k])
        #                 #     if j == 'commit':
        #                 #         for k in i[j]:
        #                 #             print('        ', k, i[j][k])
        # 递归(数据)
        信息 = {}
        for 分支 in 数据:
            if 分支['name'] == 'main':
                continue
            匹配 = re.match(r'^.* (.+)$', 分支['commit']['commit']['message'])
            信息[分支['name']] = tuple(int(x) for x in 匹配.groups()[0].split('.'))
        return 信息
        # return [分支['name'] for 分支 in 数据 if 分支['name'] != 'main']

    @classmethod
    # 获取分支文件树
    def 获取分支文件树(self, 分支名):
        # 对分支名进行URL编码
        编码分支名 = urllib.parse.quote(分支名, safe='')
        文件树接口 = f"https://gitee.com/api/v5/repos/{仓库所有者}/{仓库名称}/git/trees/{编码分支名}?recursive=1"
        请求 = urllib.request.Request(文件树接口, headers={"User-Agent": "Mozilla/5.0"})
        响应 = urllib.request.urlopen(请求, timeout=15)
        数据 = json.loads(响应.read().decode("utf-8"))
        return 数据.get("tree", [])

    # # ==================== 配置区域 ====================
    # 仓库地址 = "https://gitee.com/wulutuolaman/blender-simple-addon.git"
    # 基础下载路径 = r"C:\Users\wulutuolaman\Desktop\下载测试"
    #
    # @classmethod
    # def 执行命令(self, 命令列表, 超时=60):
    #     """执行系统命令并返回输出"""
    #     结果 = subprocess.run(
    #         命令列表,
    #         capture_output=True,
    #         text=True,
    #         encoding="utf-8",
    #         timeout=超时
    #     )
    #     if 结果.returncode != 0:
    #         raise RuntimeError(f"命令失败: {' '.join(命令列表)}\n错误: {结果.stderr}")
    #     return 结果.stdout
    #
    # @classmethod
    # def 获取分支列表(self):
    #     """使用 git ls-remote 获取远程分支列表（不走 API）"""
    #     输出 = self.执行命令(["git", "ls-remote", "--heads", self.仓库地址])
    #     分支列表 = []
    #     for 行 in 输出.strip().split("\n"):
    #         if 行:
    #             # 格式: <hash>	refs/heads/<branch-name>
    #             部分 = 行.split("\t")
    #             if len(部分) == 2:
    #                 分支引用 = 部分[1]
    #                 分支名 = 分支引用.replace("refs/heads/", "")
    #                 if 分支名 != "main":
    #                     分支列表.append(分支名)
    #     return 分支列表

# from datetime import datetime, timedelta
#
# a = datetime.now()
# print(a, a + timedelta(seconds=600))
# b = str(a)
# print(b)
# c = datetime.strptime(b, "%Y-%m-%d %H:%M:%S.%f")
# print(c, c + timedelta(seconds=600))
# time.sleep(1)
# print(a < datetime.now(), a > datetime.now())


class 检测更新:

    检测中 = False
    间隔时间 = 3600
    监测定时器 = None

    @classmethod
    def 检测版本(self) -> float | None:
        from .__init__ import Addon_Preferences, Addon_Item
        偏好 = Addon_Preferences.获取偏好()
        允许检测 = datetime.now() > datetime.strptime(偏好.记录时间, "%Y-%m-%d %H:%M:%S.%f") + timedelta(seconds=3600)
        if 允许检测 and not self.检测中:
            self.检测中 = True
            try:
                插件信息 = 连接仓库.获取信息()

                self.记录时间 = str(datetime.now())

                if len(偏好.简易插件) < len(插件信息):
                    状态 = {}  # 记录更新状态
                    for 项 in 偏好.简易插件:  # type:Addon_Item
                        状态[项.名称] = 项.更新
                    偏好.简易插件.clear()
                    for 插件 in 插件信息:
                        项 = 偏好.简易插件.add()  # type:Addon_Item
                        项.名称 = 插件
                        if 插件 in 状态:
                            项.更新 = 状态[插件]

                for 项 in 偏好.简易插件:  # type:Addon_Item
                    插件 = 项.名称
                    mod = sys.modules.get(插件)
                    if mod:
                        if mod.bl_info["version"] < 插件信息[插件]:
                            self.更新插件()

            except Exception as e:
                错误信息 = "".join(traceback.format_exception(type(e), e, e.__traceback__))
                print(f'获取插件最新信息失败:\n{错误信息}')
                偏好.错误信息 = 错误信息

            finally:
                self.检测中 = False

        return float(self.间隔时间)

    @classmethod
    def 更新插件(self):
        pass

    @classmethod
    def 启动监测(self):
        print(datetime.now(), __package__, '启动监测')

        """启动文件监测定时器"""
        # 如果已经启动，先停止
        self.停止监测()

        # 注册新定时器
        self.监测定时器 = bpy.app.timers.register(self.检测版本, first_interval=1.0)   # type:ignore
        # print(记录.监测定时器)

    @classmethod
    def 停止监测(self):
        """停止文件监测"""
        监测定时器 = self.监测定时器
        if 监测定时器 and bpy.app.timers.is_registered(监测定时器):  # type:ignore
            bpy.app.timers.unregister(监测定时器)  # type:ignore
            self.监测定时器 = None