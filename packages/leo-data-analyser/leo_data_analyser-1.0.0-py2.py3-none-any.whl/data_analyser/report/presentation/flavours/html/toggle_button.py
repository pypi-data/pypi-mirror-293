from data_analyser.report.presentation.core import ToggleButton
from data_analyser.report.presentation.flavours.html import templates


class HTMLToggleButton(ToggleButton):
    def render(self) -> str:
        return templates.template("toggle_button.html").render(**self.content)
