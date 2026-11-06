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

import os, bpy, sys, site, subprocess, importlib, shutil  # noqa: F401
from .模块 import *

def 卸载模块(self:bpy.types.Operator, 模块):
    # try:
    subprocess.call([sys.executable, "-m", "pip", "uninstall", 模块, "-y"])
    安装状态[模块] = "完成卸载"
    # self.report({"INFO"}, f'{模块}模块卸载成功')
    self.report({'INFO'}, f'{模块}模块卸载成功')
    # 关键：清理模块缓存
    导入模块 = pip_to_import_names(模块)
    for 导入 in 导入模块:
        if 导入 in sys.modules:
            del sys.modules[导入]
    # 卸载后清理所有 site-packages 目录里的损坏残留
    清理残留(self)
    importlib.invalidate_caches()  # 重新扫描可导入模块
    site.main()  # 重新加载 site-packages 路径，让新安装的包进入 sys.path
    模块集合.重载()
    # except:
    #     # self.report({"INFO"}, f'未检测到需要卸载的{模块}模块')
    #     self.report({'INFO'}, f'未检测到需要卸载的{模块}模块')

def 清理残留(self:bpy.types.Operator):
    # 但 ~il 和 ~v2 目录因为 Blender 还在运行、文件锁没释放，所以 PermissionError 清理失败。这两个等下次重启后再清理就能成功了。
    for 目录 in sys.path:
        if "site-packages" not in 目录:
            continue
        if not os.path.exists(目录):
            continue
        for 项目 in os.listdir(目录):
            if 项目.startswith("-") or 项目.startswith("~"):
                完整路径 = os.path.join(目录, 项目)
                try:
                    if os.path.isdir(完整路径):
                        shutil.rmtree(完整路径)
                    else:
                        os.remove(完整路径)
                    print(f"已清理损坏残留: {完整路径}")
                except Exception as e:
                    self.report({'ERROR'}, f'清理失败 {完整路径} \n{e}')

class Uninstall_Packages(bpy.types.Operator):
    bl_idname = "wulutuolaman_addon.uninstall_module"
    bl_label = "卸载模块"
    bl_options = {'REGISTER', 'UNDO'}

    模块: bpy.props.StringProperty()

    def execute(self, context):
        卸载模块(self, self.模块)
        return {'FINISHED'}  # ✅ 必须是 set 类型！