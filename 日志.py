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

import os, sys, glob, inspect, logging
# from logging import handlers
from datetime import datetime

class 日志(logging.Logger):

    保留数量 = 3

    # @classmethod
    def __init__(self, 名称='日志'):
        super().__init__(名称)
        # 获取调用者的信息
        调用者栈帧 = inspect.currentframe().f_back
        调用者文件 = 调用者栈帧.f_globals.get('__file__', __file__)
        调用者目录 = os.path.dirname(os.path.abspath(调用者文件))
        # print(调用者栈帧.f_lineno)

        print(f"调用者文件: {调用者文件}")
        print(f"调用者目录: {调用者目录}")

        目录 = 调用者目录  # 使用调用者的目录

        # 日志文件列表 = sorted(glob.glob(os.path.join(目录, "*.log")))
        # for 旧文件 in 日志文件列表[:-self.保留数量+1]:
        #     os.remove(旧文件)

        # print(__name__)
        # print(__file__)
        # 目录 = os.path.dirname(os.path.abspath(__file__))
        # print(目录, os.path.basename(目录))
        路径 = os.path.join(目录, "日志")
        print(f"{路径=}")
        if not os.path.exists(路径):
            os.makedirs(路径)
        文件 = os.path.join(路径, f"{datetime.now().strftime('%Y%m%d %H_%M_%S')}_{名称}.log")
        # 格式 = '[%(asctime)s.%(msecs)03d] [%(module)s] [%(filename)s %(lineno)d] [%(levelname)s]: %(message)s'
        格式 = (
            '[%(asctime)s.%(msecs)03d] '
            '[插件:%(call_dir)s] [%(call_filename)s 第%(call_lineno)d行] 函数:%(call_funcname)-12s [%(levelname)s]: '
            '%(call_indent_str)s%(message)s'
        )
        时间 = '%Y-%m-%d %H:%M:%S'
        日志格式 = logging.Formatter(格式, 时间)

        # # 创建 logger
        # 日志 = logging.getLogger(名称)
        # 日志.setLevel(logging.DEBUG)
        # 设置当前实例（self）的级别
        self.setLevel(logging.DEBUG)

        # print(1)

        # 文件 handler：记录所有 DEBUG 及以上级别
        文件处理器 = logging.FileHandler(文件, encoding='utf-8')
        # 文件处理器 = handlers.TimedRotatingFileHandler(
        #     文件,
        #     when='midnight',  # 午夜零点切分
        #     interval=1,  # 每 1 天（每到午夜零点）切一次日志
        #     backupCount=3,  # 最多保留 3 个历史备份日志，旧的自动删除
        #     encoding='utf-8',
        #     delay=True,  # 输出第一条日志的时候才创建文件
        # )
        文件处理器.setLevel(logging.DEBUG)
        文件处理器.setFormatter(日志格式)

        # print(2)

        # 控制台 handler：只显示 INFO 及以上（避免 DEBUG 刷屏）
        控制台处理器 = logging.StreamHandler(sys.stdout)
        控制台处理器.setLevel(logging.DEBUG)
        控制台处理器.setFormatter(日志格式)

        # print(3)

        # 日志.addHandler(文件处理器)
        # 日志.addHandler(控制台处理器)
        self.addHandler(文件处理器)
        self.addHandler(控制台处理器)
        # print(4)

        日志文件列表 = sorted(glob.glob(os.path.join(路径, "*.log")))
        # print(5)
        # print(f"{路径=}")
        # print(f"{os.path.join(路径, '*.log')=}")
        # print(f"{glob.glob(os.path.join(路径, '*.log'))=}")
        print(日志文件列表[:-self.保留数量])
        for 旧文件 in 日志文件列表[:-self.保留数量]:  # TimedRotatingFileHandler改为-保留数量+1
            print(f"{旧文件=}")
            os.remove(旧文件)

        # return 日志

    # @classmethod
    # def 缩进(cls):
    #     堆栈 = inspect.stack()
    #     栈帧 = None
    #     # 从栈中查找第一个不是本文件的调用者
    #     # print()
    #     for 调用者 in 堆栈:
    #         # print(f"{帧信息=}")
    #         # print(f"{帧信息.filename=}")
    #         if 调用者.filename !=__file__:
    #             栈帧 = 调用者
    #             break
    #     # print()
    #     # print(f"{stack[-1]=}")
    #
    #     # 调用者栈帧 = inspect.currentframe().f_back
    #     # print(f"{调用者栈帧=}")
    #     # 调用者文件 = 调用者栈帧.f_globals.get('__file__', __file__)
    #     # print(f"{调用者文件=}")
    #     # 行号 = 调用者栈帧.f_lineno
    #     # 栈帧 = stack[-1]
    #     if not 栈帧:
    #         raise Exception("日志没有找到调用者帧信息")
    #
    #     文件 = 栈帧.filename
    #     行号 = 栈帧.lineno
    #     空格 = 0
    #     try:
    #         # 读取源文件
    #         with open(文件, 'r', encoding='utf-8') as f:
    #             全部行 = f.readlines()
    #             # print(全部行)
    #         print()
    #         # 获取调用行（注意：行号从1开始，列表索引从0开始）
    #         if 行号 <= len(全部行):
    #             调用行 = 全部行[行号 - 1]
    #             print(f"{调用行=}")
    #             # 计算缩进长度（空格数）
    #             空格 += len(调用行) - len(调用行.lstrip(' '))
    #             print(f"{空格=}")
    #
    #             # # 检测是否为制表符缩进
    #             # if call_line.startswith('\t'):
    #             #     # 制表符算作4个空格
    #             #     indent_len = call_line.count('\t') * 4
    #             # print(indent_len)
    #
    #             # return indent_len
    #     except Exception as e:
    #         print(f"获取缩进失败: {e}")
    #     return 空格
    #
    #
    #
    # def 信息(self, 信息):   日志.info(self, self.缩进() * " " + 信息)
    # def 调试(self, 信息):   日志.debug(self, self.缩进() * " " + 信息)
    # def 错误(self, 信息):   日志.error(self, self.缩进() * " " + 信息)
    # def 警告(self, 信息):   日志.warning(self, self.缩进() * " " + 信息)
    # def 关键(self, 信息):   日志.critical(self, self.缩进() * " " + 信息)

    @staticmethod
    def 获取():
        # """
        # 跳过内部封装层，拿到真正业务调用方
        # stack索引：
        # 0: 获取调用者信息
        # 1: 输出调用者信息
        # 2: 信息/调试/错误...
        # 3: 业务代码（测试.py）
        # """
        堆栈 = inspect.stack()
        # # 安全边界，防止栈过短
        # 业务帧索引 = 3
        # if len(堆栈) <= 业务帧索引:
        #     return ("未知", "unknown.py", 0, "unknown", 0, "")
        # 栈帧信息 = 堆栈[业务帧索引]

        栈帧 = None
        # print()
        # 从栈中查找第一个不是本文件的调用者
        for 帧信息 in 堆栈:
            # print(f"{帧信息=}")
            # print(f"{帧信息.filename=} {帧信息.function} {帧信息.lineno}")
            if 帧信息.filename !=__file__:
                栈帧 = 帧信息
                break

        调用全路径 = os.path.abspath(栈帧.filename)
        行号 = 栈帧.lineno
        函数名 = 栈帧.function
        # 函数名 = f"{函数名:<20}"
        # 目标 = 16
        # 长度 = 0
        # for c in 函数名:
        #     if ord(c) > 255:
        #         长度 += 2 # 中文汉字算2
        #     else:
        #         长度 += 1
        # 差值 = 目标 - 长度
        # # 函数名 += "　" * max(0, 目标 - 长度)
        # # # 优先补全角空格（每一个占2格）
        # while 差值 >= 2:
        #     函数名 += "　"
        #     差值 -= 2
        # # 剩下不足2的部分，补半角空格
        # 函数名 += " " * 差值

        调用目录 = os.path.basename(os.path.dirname(调用全路径))
        文件名 = os.path.basename(调用全路径)

        缩进空格 = 0
        try:
            文件 = 栈帧.filename
            行号 = 栈帧.lineno
            空格 = 0
            # 读取源文件
            with open(文件, 'r', encoding='utf-8') as f:
                全部行 = f.readlines()
                # print(全部行)
            print()
            # 获取调用行（注意：行号从1开始，列表索引从0开始）
            if 行号 <= len(全部行):
                调用行 = 全部行[行号 - 1]
                print(f"{调用行=}")
                # 计算缩进长度（空格数）
                空格 += len(调用行) - len(调用行.lstrip(' '))
                print(f"{空格=}")

                # # 检测是否为制表符缩进
                # if call_line.startswith('\t'):
                #     # 制表符算作4个空格
                #     indent_len = call_line.count('\t') * 4
                # print(indent_len)
            # with open(调用全路径, "r", encoding="utf-8") as f:
            #     全部行 = f.readlines()
            # idx = 行号 - 1
            # if 0 <= idx < len(全部行):
            #     调用行文本 = 全部行[idx]
            #     前置空白长度 = len(调用行文本) - len(调用行文本.lstrip())
            #     # 处理tab，1tab=4空格
            #     for ch in 调用行文本[:前置空白长度]:
            #         if ch == '\t':
            #             缩进空格 += 4
            #         else:
            #             缩进空格 += 1
        except Exception:
            缩进空格 = 0

        缩进字符串 = " " * 缩进空格
        return 调用目录, 文件名, 行号, 函数名, 缩进空格, 缩进字符串

    def 输出(self, level, msg, *args, **kwargs):
        调用目录, 文件名, 行号, 函数名, 缩进空格, 缩进字符串 = self.获取()
        记录 = self.makeRecord(
            self.name,
            level,
            fn="",
            lno=0,
            msg=msg,
            args=args,
            exc_info=kwargs.get("exc_info"),
            func=None,
            extra={
                "call_dir": 调用目录,
                "call_filename": 文件名,
                "call_lineno": 行号,
                "call_funcname": 函数名,
                # "call_indent": 缩进空格,
                "call_indent_str": 缩进字符串
            }
        )
        self.handle(记录)

    def 信息(self, 信息):
        self.输出(logging.INFO, 信息)

    def 调试(self, 信息):
        self.输出(logging.DEBUG, 信息)

    def 错误(self, 信息):
        self.输出(logging.ERROR, 信息, exc_info=False)

    def 警告(self, 信息):
        self.输出(logging.WARNING, 信息)

    def 关键(self, 信息):
        self.输出(logging.CRITICAL, 信息)

## 去掉注释会导致调用者运行时，这里也创建日志
# 日志 = 创建日志('日志')
# 日志.info('info')
# 日志.debug('debug')
# 日志.error('error')
# 日志.critical('critical')
# # 日志.exception('exception')
# 日志.warning('warning')
# # 日志.log(0, 'log')