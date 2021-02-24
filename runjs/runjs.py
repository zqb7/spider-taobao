import ctypes

lib = ctypes.cdll.LoadLibrary('./librunjs.so')
lib.runjs.argtypes = [ctypes.c_char_p]
lib.runjs.restype = ctypes.c_char_p


def runjs(js):
    return lib.runjs(js.encode("utf-8"))