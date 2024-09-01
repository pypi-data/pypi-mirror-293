from collections.abc import Callable
from functools import wraps
from inspect import Parameter, signature
from types import UnionType
from typing import Literal, Type, TypeAliasType, Union, get_args, get_origin


def check_params[R](func: Callable[..., R]) -> Callable[..., R]:
    r"""
    Checks that all given parameters are the expected type.
    :param func:
    :return: The decorated function.
    :raises TypeError: Parameter's value is not of the expected type.
    """

    def compare_types(type1: Type, type2: Type) -> bool:
        def inner_compare_types(_type1: Type, _type2: Type) -> bool:
            _origin1, _args1 = get_origin(_type1), get_args(_type1)
            _origin2, _args2 = get_origin(_type2), get_args(_type2)
            if _origin1 is None and _origin2 is None:
                return _type1 == _type2
            if _origin1 is not None and _origin2 is not None:
                if _origin1 != _origin2: return False
                if not _args1 and not _args2: return True
                if len(_args1) != len(_args2): return False
                return all(
                    inner_compare_types(a1, a2)
                    for a1, a2 in zip(_args1, _args2)
                )
            return False

        def compare_literals(
                literals1: tuple[object, ...],
                literals2: tuple[object, ...]
        ) -> bool: return set(literals1) == set(literals2)

        if isinstance(type1, TypeAliasType):
            type1 = type1.__value__
        if isinstance(type2, TypeAliasType):
            type2 = type2.__value__

        origin1, args1 = get_origin(type1), get_args(type1)
        origin2, args2 = get_origin(type2), get_args(type2)

        if origin1 is Literal and origin2 is Literal:
            return compare_literals(args1, args2)

        return inner_compare_types(type1, type2)

    def validate_type(value: object, annot: Type) -> bool:
        if isinstance(annot, TypeAliasType):
            annot = annot.__value__

        origin = get_origin(annot)
        args = get_args(annot)

        if origin is None:
            return isinstance(value, annot)

        elif origin is tuple:
            if not isinstance(value, tuple):
                return False
            if not args: return True
            t_value: tuple = value
            if len(args) != len(t_value) and not (
                    len(args) == 2 and args[1] is Ellipsis and
                    (isinstance(args[0], UnionType) or get_origin(args[0]) is Union)
            ): return False
            elif len(args) == 2 and args[1] is Ellipsis:
                if get_origin(args[0]) is Union:
                    return all(validate_type(v, args[0]) for v in t_value)
                elif isinstance(args[0], UnionType):
                    return any(validate_type(v, args[0]) for v in t_value)
                else:
                    return all(validate_type(v, args[0]) for v in t_value)
            elif len(args) != len(t_value):
                return False
            return all(validate_type(v, args[i]) for i, v in enumerate(t_value))

        elif origin is list:
            if not isinstance(value, list):
                return False
            if not args: return True
            l_value: list = value
            return all(validate_type(v, args[0]) for v in l_value)

        elif origin is set:
            if not isinstance(value, set):
                return False
            if not args: return True
            s_value: set = value
            return all(validate_type(v, args[0]) for v in s_value)

        elif origin is dict:
            if not isinstance(value, dict):
                return False
            if not args: return True
            d_value: dict = value
            k_check: bool = all(validate_type(k, args[0]) for k in d_value.keys())
            v_check: bool = all(validate_type(v, args[1]) for v in d_value.values())
            return k_check and v_check

        elif origin is Callable:
            if not callable(value):
                return False
            if not args: return True
            if args == (Ellipsis, Ellipsis): return True
            c_value: Callable = value
            c_sig = signature(c_value)
            c_params = c_sig.parameters
            c_annots = [param.annotation for param in c_params.values()]
            c_return = c_sig.return_annotation
            expected_param_types = args[0]
            expected_return_type = args[1]
            if expected_param_types is not Ellipsis:
                if len(c_params) != len(expected_param_types):
                    return False
                if not all(
                        compare_types(v, t) for v, t in zip(
                            c_annots, expected_param_types
                        )
                ): return False
            if expected_return_type is not Ellipsis:
                if not compare_types(c_return, expected_return_type):
                    return False
            return True

        elif origin is Literal:
            return value in args

        elif origin is Union or origin is UnionType:
            return any(validate_type(value, arg) for arg in args)

        raise NotImplementedError(
            f"You stumbled upon a type that has not yet been implemented!\n"
            f"Annotation: {annot}\n"
            f"Type: {type(annot)}\n"
            f"Origin: {origin}\n"
            f"Args: {args}\n"
            f"Value: {value}"
        )

    @wraps(func)
    def wrapper(*args, **kwargs) -> R:
        params = signature(func).parameters
        for arg, param in zip(args, params.values()):
            annot = param.annotation
            if annot != Parameter.empty and not validate_type(arg, annot):
                raise TypeError(
                    f"Invalid type for parameter {param.name}: {type(arg)}. Expected: {annot}"
                )

        kwargs_param: Parameter | None = None
        for param in params.values():
            if param.kind == param.VAR_KEYWORD:
                kwargs_param = param
                break

        for k, v in kwargs.items():
            if k not in params:
                if kwargs_param is None:
                    raise TypeError(f"Got an unexpected keyword argument '{k}'")
                if kwargs_param.annotation == Parameter.empty:
                    continue
                if not validate_type(v, kwargs_param.annotation):
                    raise TypeError(
                        f"Invalid type for keyword argument: {type(v)}. Expected:"
                        f" {kwargs_param.annotation}.\nUsed key: {k}"
                    )
                continue
            annot = params[k].annotation
            if annot != Parameter.empty and not validate_type(v, annot):
                raise TypeError(
                    f"Invalid type for parameter '{k}': {type(v)}. Expected: {annot}"
                )

        return func(*args, **kwargs)

    return wrapper