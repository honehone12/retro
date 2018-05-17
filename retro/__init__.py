import os
import sys

from enum import Enum

try:
    # Work around TensorFlow import issues
    dlopenflags = None
    dlopenflags = sys.getdlopenflags()
    sys.setdlopenflags(os.RTLD_NOW | os.RTLD_GLOBAL)
except AttributeError:
    pass

from retro._retro import Movie, RetroEmulator, core_path
import retro.data

if dlopenflags:
    sys.setdlopenflags(dlopenflags)


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
core_path(os.path.join(os.path.dirname(__file__), 'cores'))

for path in ('VERSION.txt', '../VERSION'):
    try:
        with open(os.path.join(os.path.dirname(__file__), path)) as f:
            __version__ = f.read()
            break
    except IOError:
        pass

__all__ = ['Movie', 'RetroEmulator', 'Actions', 'State', 'get_core_path', 'get_romfile_system', 'get_system_info', 'make']

retro.data.init_core_info(core_path())


class Actions(Enum):
    ALL = 0
    FILTERED = 1
    DISCRETE = 2
    MULTI_DISCRETE = 3


class State(Enum):
    DEFAULT = -1
    NONE = 0


def get_core_path(corename):
    return os.path.join(core_path(), retro.data.EMU_CORES[corename])


def get_romfile_system(rom_path):
    extension = os.path.splitext(rom_path)[1]
    if extension in retro.data.EMU_EXTENSIONS:
        return retro.data.EMU_EXTENSIONS[extension]
    else:
        raise Exception("Unsupported rom type at path: {}".format(rom_path))


def get_system_info(system):
    if system in retro.data.EMU_INFO:
        return retro.data.EMU_INFO[system]
    else:
        raise KeyError("Unsupported system type: {}".format(system))


def make(game, state=State.DEFAULT, inttype=retro.data.Integrations.DEFAULT, **kwargs):
    from retro.retro_env import RetroEnv
    try:
        retro.data.get_romfile_path(game, inttype)
    except FileNotFoundError:
        if not retro.data.get_file_path(game, "rom.sha", inttype):
            raise
        else:
            raise FileNotFoundError('Game not found: %s. Did you make sure to import the ROM?' % game)
    return RetroEnv(game, state, inttype=inttype, **kwargs)
