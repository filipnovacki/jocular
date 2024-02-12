from enum import Enum
import json

import jsonpickle


class RenderType(Enum):
    HTML = "html"
    PLAIN = "plain"


class ExportType(Enum):
    JSON = "json"
    PRINT = "print"
    IPY_DISPLAY = "ipy_display"


class Cloze:
    def export(self, export_format: ExportType = ExportType.IPY_DISPLAY):
        if export_format == ExportType.JSON:
            return jsonpickle.dumps(self)
        elif export_format == ExportType.PRINT:
            print(jsonpickle.dumps(self))
        elif ExportType.IPY_DISPLAY:
            if self._is_running_in_jupyter():
                from IPython import display
                return display.JSON(json.loads(jsonpickle.dumps(self)), expanded=False)
            raise SystemError("Can't render like this because I'm not run in Jupyter notebook")

    def _is_running_in_jupyter(self):
        try:
            shell_type = get_ipython().__class__.__name__
            if shell_type == 'ZMQInteractiveShell':  # jupyter notebook
                return True
            return False
        except NameError:
            return False  # standard python interpreter

    @staticmethod
    def import_question(import_text: str):
        return jsonpickle.loads(import_text)


