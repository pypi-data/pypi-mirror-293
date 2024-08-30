from data_analyser.report.presentation.core.table import Table
from data_analyser.report.presentation.flavours.html import templates


class HTMLTable(Table):
    def render(self) -> str:
        return templates.template("table.html").render(**self.content)
