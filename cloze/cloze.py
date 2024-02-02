import jsonpickle

from cloze.templates import fill_numerical


class Cloze:
    def export(self, export_format: str = "json", print_out=True):
        if export_format == "json":
            if not print_out:
                return jsonpickle.dumps(self)
            print(jsonpickle.dumps(self))


