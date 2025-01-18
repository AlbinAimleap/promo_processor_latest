import importlib
import pkgutil
from pathlib import Path
from promo_processor.processor import PromoProcessor

__all__ = []

package_dir = Path(__file__).parent / "processors"

def load_processors():
    for (_, module_name, _) in pkgutil.iter_modules([package_dir]):
        module = importlib.import_module(f"{__package__}.processors.{module_name}")
        if hasattr(module, '__all__'):
            __all__.extend(module.__all__)
        else:
            __all__.extend([attr for attr in dir(module) 
                          if not attr.startswith('_') 
                          and isinstance(getattr(module, attr), type)
                          and issubclass(getattr(module, attr), PromoProcessor)])


def base_round(value , places=2):
    str_value = str(value)
    if '.' in str_value:
        base, decimal = str_value.split('.')
        if len(decimal)>places:
            decimal=decimal[:places]
        str_value = '.'.join([base,decimal])
    return float(str_value) 

load_processors()