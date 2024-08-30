from data_analyser.report.presentation.core.sample import Sample
from data_analyser.report.presentation.flavours.html import templates


class HTMLSample(Sample):
    def render(self) -> str:
        sample_html = self.content["sample"].to_html(
            classes="sample table table-striped"
        )
        return templates.template("sample.html").render(
            **self.content, sample_html=sample_html
        )
