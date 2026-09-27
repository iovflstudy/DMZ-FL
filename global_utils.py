"""
Global utilities for DMZ-FL.

Provides the lightweight registry pattern (mirroring FLPoison):
decorators register attacks / aggregators / ledgers / backends by name, and
`import_all_modules` auto-discovers every module in a package directory so that
registration side-effects run on import.
"""
import importlib.util
import logging
import os
import random
import numpy as np


class Register(dict):
    """A dict subclass that doubles as a decorator-based registry."""

    def register(self, name=None):
        def _wrap(cls):
            key = name or cls.__name__
            if key in self:
                raise ValueError(f"Duplicate registration: {key}")
            self[key] = cls
            return cls
        return _wrap

    def get(self, name):
        if name not in self:
            raise KeyError(f"'{name}' not registered. Available: {list(self)}")
        return self[name]


def import_all_modules(package_dir):
    """Import every .py file in a directory so its @register decorators fire."""
    pkg_name = os.path.basename(package_dir)
    for fname in sorted(os.listdir(package_dir)):
        if fname.startswith('_') or not fname.endswith('.py'):
            continue
        mod_name = f"{pkg_name}.{fname[:-3]}"
        spec = importlib.util.spec_from_file_location(
            mod_name, os.path.join(package_dir, fname))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)


def setup_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    except ImportError:
        pass


def setup_logger(name, output_dir, level=logging.INFO):
    os.makedirs(output_dir, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()
    fh = logging.FileHandler(os.path.join(output_dir, 'run.log'))
    sh = logging.StreamHandler()
    fmt = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    fh.setFormatter(fmt); sh.setFormatter(fmt)
    logger.addHandler(fh); logger.addHandler(sh)
    return logger