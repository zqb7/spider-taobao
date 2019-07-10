class SingleMode(type):
    """
    单例模式； 参考:http://python.jobbole.com/87791/
    使用 ex:
            class A(object, metaclass=SingleMode):
                pass
    """
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(SingleMode, cls).__call__(*args, **kwargs)
        return cls._instance
