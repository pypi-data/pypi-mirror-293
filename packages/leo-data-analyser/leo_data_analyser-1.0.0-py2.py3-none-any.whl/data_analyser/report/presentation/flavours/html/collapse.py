from data_analyser.report.presentation.core import Collapse
from data_analyser.report.presentation.flavours.html import templates


class HTMLCollapse(Collapse):
    def render(self) -> str:
        return templates.template("collapse.html").render(**self.content)
