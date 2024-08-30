from ipywidgets import widgets

from data_analyser.report.presentation.core.root import Root


class WidgetRoot(Root):
    def render(self, **kwargs) -> widgets.VBox:
        return widgets.VBox(
            [self.content["body"].render(), self.content["footer"].render()]
        )
