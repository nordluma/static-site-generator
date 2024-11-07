class HtmlNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[object] | None = None,
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


class LeafNode(HtmlNode):
    def __init__(
        self,
        tag: str | None,
        value: str | None = None,
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HtmlNode):
    def __init__(
        self,
        tag: str | None,
        children: list[object] | None,
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("parent node has to have a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("a parent node has to have children")
        child_nodes = [child.to_html() for child in self.children]
        return f"<{self.tag}>{"".join(child_nodes)}</{self.tag}>"
