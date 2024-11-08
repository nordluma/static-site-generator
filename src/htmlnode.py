from typing import Mapping, Union, Sequence

type HtmlNodes = Sequence[Union[HtmlNode, LeafNode]] | None

type MaybeStr = str | None


class HtmlNode:
    def __init__(
        self,
        tag: MaybeStr = None,
        value: MaybeStr = None,
        children: HtmlNodes = None,
        props: Mapping[str, MaybeStr] | None = None,
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
        for key, value in self.props.items():
            props += f" {key}={value}"
        return props

    def __repr__(self) -> str:
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HtmlNode):
    def __init__(
        self,
        tag: MaybeStr,
        value: MaybeStr = None,
        props: Mapping[str, MaybeStr] | None = None,
    ):
        super().__init__(tag, value, props=props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __eq__(self, other) -> bool:
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.props == other.props
        )


class ParentNode(HtmlNode):
    def __init__(
        self,
        tag: MaybeStr,
        children: list[LeafNode] | None,
        props: dict[str, MaybeStr] | None = None,
    ):
        super().__init__(tag, children=children, props=props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("parent node has to have a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("a parent node has to have children")
        child_nodes = [child.to_html() for child in self.children]
        return f"<{self.tag}>{"".join(child_nodes)}</{self.tag}>"
