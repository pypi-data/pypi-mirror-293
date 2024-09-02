import abc
import typing
import asyncio
import functools

from chariot_scaffold import data_mapping, log
from chariot_scaffold.core.config import Lang


class Base(metaclass=abc.ABCMeta):
    def __init__(self, title=None, description=None, model=None):
        self.__vars_name = None
        self.__defaults = None
        self.__comments = None
        self.__annotations = None
        self.__params_name = None
        self._func_name = None
        self._types = {}

        self.model = model
        self.title = title
        self.description = description

        self.input = {}
        self.output = {}

    def __call__(self, func):
        self.bind_func_info(func)
        self.generate_func_info()
        self.hook()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            mapping = self.get_params_mapping(*args, **kwargs)
            if self.model:
                self.check_model(mapping)

            res = func(*args, **kwargs)
            return res

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            mapping = self.get_params_mapping(*args, **kwargs)
            if self.model:
                self.check_model(mapping)

            res = await func(*args, **kwargs)
            return res

        wrapper_func = async_wrapper if asyncio.iscoroutinefunction(func) else wrapper
        return wrapper_func

    def generate_func_info(self):
        self.bind_parameters()
        self.bind_defaults()
        self.bind_output()

    def bind_func_info(self, func):
        self.__vars_name = func.__code__.co_varnames
        self.__params_name = [self.__vars_name[i] for i in range(func.__code__.co_argcount)]  # 参数名
        self.__annotations = func.__annotations__ # 注解
        self.__comments = func.__doc__ # 注释
        self.__defaults = func.__defaults__ # 默认值
        self._func_name = func.__name__

    def bind_parameters(self):
        """
        绑定参数名,title,description,type
        """
        for param in self.__params_name:
            if param != 'self':
                self.input[param] = {
                    "name": param, "default": None, "title": None, "description": None, "type": None, "required": False,
                    "print": False, "enum": None
                }

                anno = self.__annotations.get(param)
                if isinstance(anno, typing._AnnotatedAlias):  # noqa
                    res = self.match_annotated(anno)
                    self.input[param].update(res)
                else:
                    self.input[param]["title"] = self.lang_checking(param)
                    self.input[param]["description"] = self.lang_checking(param)

    def bind_defaults(self):
        """
        绑定default默认值和required是否必填
        """
        # required和default属性绑定
        defaults_length = len(self.__defaults) if self.__defaults else 0

        # 参考python传参机制
        re_params_name = self.__params_name[::-1]                       # 翻转参数名的意义是python的默认值是从后往前找的
        re_defaults = self.__defaults[::-1] if defaults_length else []  # 默认值同上从后往前匹配， 注意空列表无法翻转

        for i in range(len(self.__params_name)):
            if re_params_name[i] != 'self':
                # 有默认值可以不传参, 无默认值则必传
                if i < defaults_length:
                    self.input[re_params_name[i]]["default"] = re_defaults[i]

                    if self.input[re_params_name[i]]["default"] is None:  # 参数类型为list,dict的默认值为None的全部处理成[],{}
                        if self.input[re_params_name[i]]["type"] == "[]string":     # 千乘array,object类型无法传入null
                            self.input[re_params_name[i]]["default"] = []
                        if self.input[re_params_name[i]]["type"] == "[]object":
                            self.input[re_params_name[i]]["default"] = {}

                    # 默认值映射枚举, 枚举类型默认值第一个
                    if str(type(self.input[re_params_name[i]]["default"].__class__)) == "<class 'enum.EnumMeta'>":
                        self.input[re_params_name[i]]["enum"] = [i.value for i in list(self.input[re_params_name[i]]["default"].__class__)] #todo 枚举值的key映射出去，实际使用值
                        self.input[re_params_name[i]]["default"] = self.input[re_params_name[i]]["default"].value

                else:
                    self.input[re_params_name[i]]["required"] = True

    def bind_output(self):
        """
        绑定output
        """
        output_type = self.__annotations.get("return")
        if output_type:
            # 返回值注解绑定
            if isinstance(output_type, dict):
                self.match_basemodel(output_type)
                # print(self._types)
                self.output = self._types
            else:
                # 返回值默认绑定
                self.output["output"] = {
                    "type": self.match_datatype(output_type),
                    "title": Lang("输出", "output").convert(),
                    "description": Lang("默认输出", "Default Output").convert()
                }

    def check_model(self, kwargs):
        """
        参数强类型校验
        :param kwargs: 参数
        :return: None
        """
        self.model(**kwargs)

    def get_params_mapping(self, *args, **kwargs) -> dict:
        """
        绑定args、kwargs与参数之间的映射关系, 便于强类型校验使用
        :param args:
        :param kwargs:
        :return: mapping
        """
        mapping = {}

        # 先绑定默认值
        if self.__defaults:
            for i in range(len(self.__defaults)):
                mapping[list(self.__params_name)[::-1][i]] = list(self.__defaults)[::-1][i]

        # 再按顺序填入arg
        for i in range(len(args)):
            if self.__params_name[i] != "self":
                mapping[self.__params_name[i]] = args[i]

        # 最后合并kwargs
        mapping.update(kwargs)
        return mapping

    @staticmethod
    def lang_checking(param):    # 兼容过去默认绑定中文的插件
        if isinstance(param, str):
            return {"zh-CN": param, "en": param}
        elif isinstance(param, Lang):
            return param.convert()

    @staticmethod
    def match_datatype(anno):
        # 用来匹配映射数据类型
        match str(type(anno)):
            case "<class 'type'>" | "<class 'types.GenericAlias'>":
                return data_mapping[str(anno)].__name__
            case "<class 'typing.NewType'>":
                return anno.__name__
            case _:
                log.warning(f"发现未适配的类型：{anno}, {str(type(anno))}")

    def match_annotated(self, annotated: typing._AnnotatedAlias): # noqa
        """
        对于每个步骤中的注解解析提供更进一步的封装
        """
        assert len(annotated.__metadata__) >= 2, "Annotated中至少需要包含title, description"
        param_type = annotated.__origin__
        title = annotated.__metadata__[0]
        description = annotated.__metadata__[1]

        if param_type.__class__.__name__ == "ModelMetaclass":
            return {
                "title": self.lang_checking(title),
                "description": self.lang_checking(description),
                "type": param_type.__name__
            }
        else:
            return {
                "title": self.lang_checking(title),
                "description": self.lang_checking(description),
                "type": self.match_datatype(param_type)
            }

    def match_basemodel(self, annotation):
        for k, v in annotation.items():
            # if type(v).__name__ == "ModelMetaclass":    # pydantic basemodel
            #     if self._types.get(k) is None:
            #         self._types[k] = v.__annotations__
            #
            #     annotation[k] = v.__annotations__
            #     self.match_basemodel(annotation[k])
            if v.__class__.__name__ == "_AnnotatedAlias":
                if self._types.get(k) is None:
                    self._types[k] = self.match_annotated(v)
                # annotation[k] = self.match_annotated(v)

    @abc.abstractmethod
    def hook(self):
        ...
