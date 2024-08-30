from data_analyser.report.presentation.core import Dropdown
from data_analyser.report.presentation.flavours.html import templates


class HTMLDropdown(Dropdown):
    def render(self) -> str:
        return templates.template("dropdown.html").render(**self.content)
