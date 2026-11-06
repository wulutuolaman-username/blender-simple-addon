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

import ast, addon_utils

class 检测面板:

    面板列表 = []

    # @classmethod
    # def 初始化(cls):
    #     if len(cls.面板列表) == 0:
    #         cls.重新检测()

    @classmethod
    def 重新检测(self):
        self.面板列表 = []  # 重新初始化
        from .__init__ import bl_info
        # from .__init__ import bl_info, Addon_Item, Addon_Preferences
        for mod in addon_utils.modules(refresh=False):
            作者 = getattr(mod, "bl_info", {}).get("author", None)
            if 作者 != bl_info["author"]:
                continue

            # 名称 = mod.__name__
            # print(名称)
            self.解析插件文件(mod.__name__, mod.__file__)
            addon_utils.module_bl_info(mod)["展开面板"] = False

        # # 重新建立CollectionProperty
        # 字典 = {}
        # 查重 = set()
        # 偏好 = Addon_Preferences.获取偏好()
        #
        # for 选项 in 偏好.简易插件订单号:
        #     选项: Addon_Item
        #     字典[选项.名称] = 选项.订单
        #
        # 偏好.简易插件订单号.clear()
        #
        # for 面板 in self.面板列表:
        #     名称 = 面板["名称"]
        #
        #     if 名称 in 查重:
        #         continue
        #     查重.add(名称)
        #
        #     选项: Addon_Item
        #     选项 = 偏好.简易插件订单号.add()
        #     选项.名称 = 名称
        #     if 名称 in 字典:
        #         选项.订单 = 字典[名称]

    @classmethod
    def 判断类型(cls, self, 面板):
        # print(面板["class"])
        # print(self.bl_category, 面板["bl_category"], self.bl_category == 面板["bl_category"])
        # print(self.bl_space_type, 面板["bl_space_type"], self.bl_space_type == 面板["bl_space_type"])
        # print(self.bl_region_type, 面板["bl_region_type"], self.bl_region_type == 面板["bl_region_type"])
        # print(self.bl_category == 面板["bl_category"] if hasattr(self, "bl_category") else True and \
        #       self.bl_space_type == 面板["bl_space_type"] if hasattr(self, "bl_space_type") else True and \
        #       self.bl_region_type == 面板["bl_region_type"] if hasattr(self, "bl_region_type") else True and \
        #       True)
        # print()
        # and 比 if-else 优先级高
        return (self.bl_category == 面板["bl_category"] if hasattr(self, "bl_category") else True) and \
               (self.bl_space_type == 面板["bl_space_type"] if hasattr(self, "bl_space_type") else True) and \
               (self.bl_region_type == 面板["bl_region_type"] if hasattr(self, "bl_region_type") else True) and \
               True

    # AST 语法树静态解析代码文件
    @classmethod
    def 解析插件文件(cls, 名称, 路径):
        """ 从插件文件源代码解析面板 """
        # 读取文件全部源码字符串
        with open(路径, "r", encoding="utf8") as f:
            语法树 = ast.parse(f.read())

        bl_info = {}
        # 面板 = {}

        # 遍历语法树顶层所有节点（文件最外层代码：变量赋值、类定义、函数定义等）
        for 语法节点 in 语法树.body:
            # 判断当前节点是赋值语句
            if isinstance(语法节点, ast.Assign):
                # 遍历赋值语句所有被赋值的目标
                for 赋值目标 in 语法节点.targets:
                    # 获取赋值目标变量名id，没有 id 属性时返回空字符串
                    if getattr(赋值目标, "id", "") == "bl_info":
                        try:
                            # 安全解析字面量字典 / 列表，只能解析常量（字典、字符串、数字、元组）
                            bl_info = ast.literal_eval(语法节点.value)  # type:ignore
                        except:
                            pass

            # 顶层节点判断：如果是类定义（class XXX:）
            if isinstance(语法节点, ast.ClassDef):
                # 循环遍历所有父类，ast.unparse(base)把父类语法节点转回字符串（如bpy.types.Panel）
                if not any(
                    "Panel" in ast.unparse(父类)  # type:ignore
                    for 父类 in 语法节点.bases
                ):
                    continue

                # print(node.name)

                bl_category, bl_space_type, bl_region_type = (None,) * 3

                # 遍历 Panel 类内部所有代码行（类内部的赋值、函数 draw 等语句）
                for 代码 in 语法节点.body:
                    # 只处理类内部的赋值语句，过滤 draw 方法、poll 方法等函数
                    if isinstance(代码, ast.Assign):
                        # 遍历赋值语句所有被赋值的目标
                        for 赋值目标 in 代码.targets:
                            def 查找属性(名称, 代码=代码):
                                # 获取赋值目标变量名id，没有 id 属性时返回空字符串
                                if getattr(赋值目标, "id", "") == 名称:
                                    # 属性值是下标取值，例如 bl_category = bl_info["name"]
                                    # ast.Subscript 代表 变量[键] 这种语法
                                    if isinstance(代码.value, ast.Subscript):
                                        try:
                                            if getattr(代码.value.value, "id", "") == "bl_info":
                                                # 取出下标内的常量（字符串），从全局提前解析好的bl_info字典中读取对应值返回
                                                # ast.Constant 是字符串 / 数字常量节点
                                                常量 = 代码.value.slice
                                                if isinstance(常量, ast.Constant):
                                                    return bl_info.get(常量.value)
                                        except:
                                            pass

                                    # ast.Constant 是字符串 / 数字常量节点
                                    elif isinstance(代码.value, ast.Constant):
                                        return 代码.value.value

                            bl_category, bl_space_type, bl_region_type = 查找属性("bl_category") if bl_category is None else bl_category, 查找属性("bl_space_type") if bl_space_type is None else bl_space_type, 查找属性("bl_region_type") if bl_region_type is None else bl_region_type
                            # print(node.name, bl_category, bl_space_type, bl_region_type)

                            # if getattr(t, "id", "") == "bl_category":
                            #     if isinstance(stmt.value, ast.Subscript):
                            #         try:
                            #             if getattr(stmt.value.value, "id", "") == "bl_info":
                            #                 key = stmt.value.slice
                            #                 if isinstance(key, ast.Constant):
                            #                     bl_category = bl_info.get(key.value)
                            #         except:
                            #             pass
                            #
                            #     elif isinstance(stmt.value, ast.Constant):
                            #         bl_category = stmt.value.value

                # 面板["class"] = 语法节点.name
                # 面板["bl_category"] = bl_category
                # 面板["bl_space_type"] = bl_space_type
                # 面板["bl_region_type"] = bl_region_type

                cls.面板列表.append({
                    "名称":名称,
                    "class": 语法节点.name,
                    "bl_category": bl_category,
                    "bl_space_type": bl_space_type,
                    "bl_region_type": bl_region_type,
                })


        # if 面板列表 and 面板列表[0]["bl_category"] == bl_info["author"]:
        # print()
        # print('路径', file_path)
        # for p in cls.面板列表:
        #     print(p)

        # return 面板
        return cls.面板列表