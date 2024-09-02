from flask import Flask, request, Response, make_response
import inspect
from typing import Callable, Dict, Optional, Tuple, Type

from smartoutlet import ALL_OUTLET_CLASSES, OutletInterface


app = Flask(__name__)


# Cache of outlet type string, to its handler class as well as the arguments it needs to deserialize.
# This can help us avoid rebuilding this on every request.
outlet_cache: Dict[str, Tuple[Type[OutletInterface], Dict[str, Tuple[Callable[[Optional[str]], object], str]]]] = {}


# Cache of parameters to instantiated outlet instances. This can help us avoid costly re-instantiation
# if an outlet is being queried repeatedly.
instance_cache: Dict[str, OutletInterface] = {}


class InvalidOutletException(Exception):
    pass


def create_arg_map(
    outlettype: str,
) -> Tuple[
    Type[OutletInterface], Dict[str, Tuple[Callable[[Optional[str]], object], str]]
]:
    global outlet_cache
    if outlettype in outlet_cache:
        return outlet_cache[outlettype]

    outmap: Dict[str, Tuple[Callable[[Optional[str]], object], str]] = {}

    for clz in ALL_OUTLET_CLASSES:
        if clz.type.lower() == outlettype.lower():
            # Figure out arguments to add for this outlet.
            signature = inspect.signature(clz.__init__)
            for param in signature.parameters.values():
                if param.name == "self":
                    continue
                if param.default is inspect.Parameter.empty:

                    def requiredcreator(
                        annotation: Callable[[str], object]
                    ) -> Callable[[Optional[str]], object]:
                        def cons(arg: Optional[str]) -> object:
                            if arg is None:
                                raise TypeError(
                                    f"Expected {annotation.__name__}, got None!"
                                )
                            return annotation(arg)

                        return cons

                    outmap[param.name] = (
                        requiredcreator(param.annotation),
                        param.annotation.__name__,
                    )
                else:

                    def defaultcreator(
                        annotation: Callable[[str], object], default: object
                    ) -> Callable[[Optional[str]], object]:
                        def cons(arg: Optional[str]) -> object:
                            if arg is None:
                                return default
                            return annotation(arg)

                        return cons

                    outmap[param.name] = (
                        defaultcreator(param.annotation, param.default),
                        param.annotation.__name__,
                    )

            outlet_cache[outlettype] = (clz, outmap)
            return outlet_cache[outlettype]

    raise InvalidOutletException(f"Unrecognized outlet type {outlettype}!")


def instantiate(clz: Type[OutletInterface], argmap: Dict[str, object]) -> OutletInterface:
    global instance_cache

    # First, form the key of this instance.
    keydict: Dict[str, object] = {
        '__clz__': clz.__name__,
        **argmap,
    }
    key = str(tuple(sorted(keydict.items())))
    if key in instance_cache:
        return instance_cache[key]

    inst = clz.deserialize(argmap)
    instance_cache[key] = inst
    return inst


@app.route("/<outlettype>", methods=["GET"])
def query_outlet(outlettype: str) -> Response:
    try:
        clz, args = create_arg_map(outlettype)
    except InvalidOutletException as e:
        return make_response(str(e), 400)

    argmap: Dict[str, object] = {}
    for k, (cons, objtype) in args.items():
        try:
            argmap[k] = cons(request.args.get(k))
        except TypeError:
            return make_response(
                f"Outlet type {outlettype} requires parameter {k} to be of type {objtype}!"
            )

    try:
        inst = instantiate(clz, argmap)
        state = inst.getState()
        if state is None:
            resp = "unknown"
        else:
            resp = "on" if state else "off"

        return make_response(resp, 200)
    except Exception as e:
        return make_response(str(e), 400)


@app.route("/<outlettype>", methods=["PUT", "POST", "PATCH"])
def update_outlet(outlettype: str) -> Response:
    try:
        clz, args = create_arg_map(outlettype)
    except InvalidOutletException as e:
        return make_response(str(e), 400)

    data = request.data.decode("utf-8")
    state = None
    if data.lower() == "on":
        state = True
    elif data.lower() == "off":
        state = False
    else:
        return make_response('Request body should be either "on" or "off"', 400)

    argmap: Dict[str, object] = {}
    for k, (cons, objtype) in args.items():
        try:
            argmap[k] = cons(request.args.get(k))
        except TypeError:
            return make_response(
                f"Outlet type {outlettype} requires parameter {k} to be of type {objtype}!"
            )

    try:
        inst = instantiate(clz, argmap)
        inst.setState(state)
        state = inst.getState()
        if state is None:
            resp = "unknown"
        else:
            resp = "on" if state else "off"

        return make_response(resp, 200)
    except Exception as e:
        return make_response(str(e), 400)
