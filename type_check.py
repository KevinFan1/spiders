import functools
import inspect
from inspect import Parameter

"""
类型检查装饰器小demo
"""
def func_check(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        signature = inspect.signature(func)
        # 参数类型
        params = signature.parameters

        # (input_value, <Parameter "a: int">)
        # 判断传进来的值是否符合类型注解
        for in_value, parameter in zip(args, params.values()):
            # <class 'inspect._empty'> param.empty == _empty
            # 获取参数的类型
            param_type = parameter.annotation
            # 如果不为空和类型不是注解的类型，抛出错误
            if param_type is not Parameter.empty and not isinstance(
                    in_value, param_type):
                raise TypeError(
                    f'parameter "{parameter.name}" should be {param_type.__name__}, but got {type(in_value).__name__}'
                )

        # 以赋值形式传参
        for k, v in kwargs.items():
            # 判断是否是自定义的参数
            if k in list(params.keys()):
                # 获取进来的值
                in_value = kwargs[k]
                # 获取自定义参数的注解类型
                param_type = params[k].annotation
                # 如果不为空和类型不是注解的类型，抛出错误
                if param_type is not Parameter.empty and not isinstance(
                        in_value, param_type):
                    raise TypeError(
                        f'parameter "{params[k].name}" should be {param_type.__name__}, but got {type(in_value).__name__}'
                    )

        # 结果类型检验
        ret = func(*args, **kwargs)
        ret_type = signature.return_annotation
        if not isinstance(ret, (Parameter.empty, ret_type)):
            raise TypeError(
                f'the result of function "{func.__name__}" should be {ret_type.__name__}, but got {type(ret).__name__}'
            )

        return ret

    return wrapper


@func_check
def test(a: int, b: str, c: str = None) -> str:
    return f'{a}{b}{c}'


print(test(b='1', a=1, c='3'))
