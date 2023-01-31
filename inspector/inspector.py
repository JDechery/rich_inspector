from operator import attrgetter
from typing import List, Any

import numpy as np
import pandas as pd
from IPython.core.magic import Magics, magics_class, line_magic
from pympler import asizeof
from rich.console import Console
from rich.table import Table


class UserVariable:
    def __init__(self, name: str, var: Any):
        self.name = name
        self.var = var
        self.type = type(var).__name__
        self.preview = self.get_preview()
        self.size = self.memory_usage()
        self.size_readable = self.sizeof_fmt(self.size)

    def get_preview(self, max_width=80) -> str:
        if isinstance(self.var, (pd.DataFrame, pd.Series)):
            with pd.option_context('display.max_rows', 6,
                                   'display.large_repr', 'info',
                                   'display.max_info_rows', 1,
                                   'display.max_info_columns', 8
                                   ):
                return str(self.var)
        elif isinstance(self.var, np.ndarray):
            return (
                f"{self.var.dtype} array {self.var.shape}\n" + 
                np.array2string(self.var, suppress_small=True, precision=4, threshold=60, edgeitems=2)
            )
        else:
            strvar = str(self.var)
            return strvar[:max_width] + ("..." if len(strvar) > max_width else "")

    def memory_usage(self) -> int:
        if isinstance(self.var, pd.DataFrame):
            return self.var.memory_usage().sum()
        elif isinstance(self.var, pd.Series):
            return self.var.memory_usage()
        elif isinstance(self.var, np.ndarray):
            return self.var.nbytes
        else:
            return asizeof.asizeof(self.var)

    @staticmethod
    def sizeof_fmt(num, suffix="B") -> str:
        for unit in ["", "Ki", "Mi", "Gi"]:
            if abs(num) < 1024.0:
                return f"{num:3.1f}{unit:>3}{suffix}"
            num /= 1024.0
        return f"{num:.1f}Ti{suffix}"


@magics_class
class VariableInspector(Magics):
    console = Console()

    @staticmethod
    def build_table() -> Table:
        table = Table(title="User Variables", show_lines=True)

        table.add_column("Name", justify="left", style="cyan", no_wrap=True)
        table.add_column("Type", justify="right", style="yellow")
        table.add_column("Size", justify="right", style="green")
        table.add_column("Preview", justify="left")
        return table
    
    @staticmethod
    def format_table_data(table, var_data) -> Table:
        for row in sorted(var_data, key=attrgetter('size'), reverse=True):
            table.add_row(row.name, row.type, row.size_readable, row.preview)
        return table

    def collect_variable_data(self) -> List[UserVariable]:
        user_vars = set(self.shell.user_ns) - set(self.shell.user_ns_hidden)
        rows = [
            UserVariable(
                name=name, 
                var=self.shell.user_ns[name]
                )
            for name in user_vars
        ]
        return rows

    @line_magic
    def inspect(self, line):
        table = self.build_table()
        var_data = self.collect_variable_data()
        table = self.format_table_data(table, var_data)

        self.console.print(table)

    @line_magic
    def ins(self, line):
        self.inspect(line)


def load_ipython_extension(ipython):
    ipython.register_magics(VariableInspector)
