import socket
import ctypes
import sys, os
import numpy as np
import glob

fpath = os.path.dirname(os.path.abspath(__file__))
lib_path = glob.glob(os.path.join(fpath, "reader_api*.so"))[0]
lib = ctypes.cdll.LoadLibrary(lib_path)

lib.read_data.argtypes = [ctypes.c_void_p]
lib.read_data.restype = ctypes.POINTER(ctypes.c_byte)

class ShmReader():
    """
    This class acts as a shared memory connection to vtd.

    The class methods can be used to convert frame
    buffers from a shared memory region and map them
    directly to a numpy array.

    Args:
        key (str): Shared memory key

    """
    def __init__(self, key='0x816a'):
        ikey = int(key, 16)
        self._reader = lib.create_shm_reader(ikey)

    def __enter__(self):
        return self

    def get_buffer(self):
        """Read buffer from shared memory.

        Returns:
            Numpy array with buffer data and
            resolution nx, ny according to
            Image Generator settings.
        """
        ptr = lib.read_data(self._reader)
        shape = (100, 100)
        return np.copy(np.ctypeslib.as_array(ptr, shape=shape))

    def __exit__(self, exception_type, exception_value, traceback):
        lib.release_shm_reader(self._reader)

