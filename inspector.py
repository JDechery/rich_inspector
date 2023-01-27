import sys
from typing import List, Any
from operator import attrgetter

from IPython.core.magic import Magics, magics_class, line_cell_magic
from rich.console import Console
from rich.table import Table


class UserVariable:
    def __init__(self, name: str, var: Any):
        self.name = name
        self.size = sys.getsizeof(var)
        self.size_readable = self.sizeof_fmt(self.size)

    @staticmethod
    def sizeof_fmt(num, suffix="B"):
        for unit in ["", "Ki", "Mi", "Gi"]:
            if abs(num) < 1024.0:
                return f"{num:3.1f}{unit:>3}{suffix}"
            num /= 1024.0
        return f"{num:.1f}Ti{suffix}"
    
    def __rich__(self):
        pass


@magics_class
class VariableInspector(Magics):
    console = Console()

    @staticmethod
    def build_table():
        table = Table(title="User Variables")

        table.add_column("Name", justify="right", style="cyan", no_wrap=True)
        table.add_column("Size", justify="right", style="green")
        return table
    
    def collect_variable_data(self) -> List[UserVariable]:
        user_vars = set(self.shell.user_ns) - set(self.shell.user_ns_hidden)
        rows = [
            UserVariable(name=name, var=self.shell.user_ns[name])
            for name in user_vars
            ]
        return rows


    @line_cell_magic
    def inspect(self, line, cell=None):
        table = self.build_table()

        var_data = self.collect_variable_data()
        [
            table.add_row(row.name, row.size_readable)
            for row in sorted(var_data, key=attrgetter('size'))
        ]
        self.console.print(table)


def load_ipython_extension(ipython):
    ipython.register_magics(VariableInspector)
