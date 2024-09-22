import inspect, logging, sys, os

class Logger():
    def __init__(self, name=__name__, level=logging.DEBUG) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.level = level

        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s')
        if not self.logger.handlers:
            ch = logging.StreamHandler()
            ch.setLevel(level)
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

    def error(self, message:str, exception:Exception = None, **kwargs):
        extra = {
            "kwargs": kwargs
        }
        
        if not exception:
            self.logger.error(f"{message}", extra=extra)
        else:
            traceback_entries = self._format_trace(traceback_obj=exception.__traceback__)
            formatted_trace = "\n".join([f"\t[{frame_no}] [{module_name}]: {formatted_string}" for frame_no, module_name, formatted_string in traceback_entries])
            self.logger.error(f"{message} \n{str(exception)} - Traceback : \n{formatted_trace}", extra=extra)

    def info(self, message:str, **kwargs):
        extra = {
            "kwargs": kwargs
        }
        self.logger.info(msg=message, extra=extra)

    def debug(self, message:str, **kwargs):
        extra = {
            "kwargs": kwargs
        }
        self.logger.debug(msg=message, extra=extra)

    def _format_trace(self, traceback_obj=None, levels=2):
        if traceback_obj:
            frames = inspect.getinnerframes(traceback_obj)
        else:
            frames = inspect.stack()[levels:]

        trace = []
        frameNo = 0
        for frame, _, line, function, src, pos in frames:
            code = src[pos].strip() if pos else '(no source)'
            name = self.get_frame_name(frame)
            if function == '?':
                prettyargs = ''
            else:
                prettyargs = self._format_args(frame)

            trace.append((frameNo, name, "%s%s at line %d: %s" % (function, prettyargs, line, code)))
            frameNo += 1

        return trace

    @classmethod
    def get_frame_name(cls, frame=None):
        if not frame:
            frame = sys._getframe().f_back.f_back

        name = frame.f_globals["__name__"]
        if name == '__main__':
            name = os.path.basename(frame.f_code.co_filename)

        return name
    
    def _format_args(self, frame):
        (args, varargs, varkw, frame_locals) = inspect.getargvalues(frame)
        try:
            prettyargs = inspect.formatargvalues(args, varargs, varkw, frame_locals,
                                                 formatvalue=self._format_value)
        except:
            prettyargs = '(?)'
        return prettyargs