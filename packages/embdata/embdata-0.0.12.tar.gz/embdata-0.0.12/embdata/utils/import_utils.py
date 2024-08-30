import importlib
import platform
import sys
from importlib.util import LazyLoader, find_spec, module_from_spec
from types import ModuleType

from xtyping import TYPE_CHECKING, Any, Literal, Union

if TYPE_CHECKING:
    from matplotlib.figure import Figure as MatplotlibFigure
    from plotext import _figure as PlotextFigure  # noqa
    from plotext._figure import _figure_class as PlotextFigure  # noqa
    matplotlib = Any
    plotext = Any
else:
    MatplotlibFigure = Any
    PlotextFigure = Any
    lazy = Any
    eager = Any
    reload = Any

plt = None

def import_plt(
    backend: Literal["matplotlib", "plotext"] | None = "plotext",
) -> Union["MatplotlibFigure", "PlotextFigure"]:
    global plt # noqa
    if backend == "matplotlib":
        mpl = smart_import("matplotlib")
        if platform.system() == "Darwin":
            mpl.use("TkAgg")
        plt = smart_import("matplotlib.pyplot")
        return plt
    if backend == "plotext":
        plt = smart_import("plotext")
        return plt
    msg = f"Unknown plotting backend {backend}"
    raise ValueError(msg)


def reload(module: str) -> None:
    if module in globals():
        return importlib.reload(globals()[module])
    return importlib.import_module(module)


def smart_import(name: str,  mode: Literal["lazy", "eager", "reload"] = "eager") -> ModuleType:
    if name in globals():
        return globals()[name] if mode != "reload" else reload(name)

    if mode == "lazy":
        spec = find_spec(name)
        if spec is None:
            msg = f"Module {name} not found"
            raise NameError(msg)
        loader = LazyLoader(spec.loader)
        spec.loader = loader
        module = module_from_spec(spec)
        sys.modules[name] = module
        loader.exec_module(module)

    try:
        module = importlib.import_module(name)
        return reload(name) if mode == "reload" else module
    except ImportError as e:
        msg = f"Module {name} not found. Install with `pip install {name}`"
        raise NameError(msg) from e

