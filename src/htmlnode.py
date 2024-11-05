class HtmlNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children=None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        props = ""
        if self.props is None:
            return props
        for key, value in self.props:
            props += f" {key}={value}"
        return props

    def __repr__(self) -> str:
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"
