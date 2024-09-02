from __future__ import annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING
import html as _py_html

import htmp

if _TYPE_CHECKING:
    from htmp.container import Container
    from htmp.protocol import AttrsType


class Element:

    def __init__(self, name: str, void: bool, attrs: AttrsType | None = None):
        self.name = name
        self.attrs = attrs or {}
        self.void = void
        return

    def tag(self, indent: int = 3, length_threshold: int = 80) -> str:
        """Get the HTML syntax of the element's opening tag."""
        attrs = []
        for key, val in sorted(self.attrs.items()):
            if val is None:
                continue
            if isinstance(val, bool):
                if val:
                    attrs.append(f"{key}")
            else:
                attrs.append(f'{key}="{_py_html.escape(str(val))}"')
        tag_start = f"<{self.name}"
        tag_end = f"{' /' if self.void else ''}>"
        if not attrs:
            return f"{tag_start}{tag_end}"
        oneliner = f"{tag_start} {' '.join(attrs)}{tag_end}"
        if indent < 0 or (length_threshold > 0 and len(oneliner) <= length_threshold):
            return oneliner
        attrs_str = "\n".join([f"{indent * ' '}{attr}" for attr in attrs])
        return f"{tag_start}\n{attrs_str}{tag_end}"

    def display(self, ipython: bool = False, as_md: bool = False) -> None:
        """Display the element in an IPython notebook."""
        if ipython:
            return htmp.display.ipython(str(self), as_md=as_md)
        return htmp.display.browser(str(self))

    def __str__(self):
        """HTML syntax of the element as a one-line string."""
        return self.str(indent=-1)

    def str(self, indent: int = 3, tag_length_threshold: int = 80) -> str:
        """Get the HTML syntax of the element."""
        ...


class VoidElement(Element):

    def __init__(self, name: str, attrs: AttrsType | None = None):
        super().__init__(name=name, void=True, attrs=attrs)
        return

    def str(self, indent: int = 3, tag_length_threshold: int = 80) -> str:
        return self.tag(indent=indent, length_threshold=tag_length_threshold)

    def __repr__(self):
        class_open = f"{self.name.upper()}("
        if not self.attrs:
            return f"{class_open})"
        indent = 3 * " "
        lines = [class_open, f"{indent}attrs={{"]
        for key, val in self.attrs.items():
            lines.append(f'{2 * indent}"{key}": "{val}",')
        lines.append(f"{indent}}}")
        lines.append(")")
        return "\n".join(lines)


class ContentElement(Element):

    def __init__(self, name: str, content: Container, attrs: AttrsType | None = None):
        super().__init__(name=name, void=False, attrs=attrs)
        self.content = content
        return

    def str(self, indent: int = 3, tag_length_threshold: int = 80) -> str:
        content = self.content.str(indent=indent)
        if indent < 0:
            sep = ""
        else:
            sep = "\n"
            if indent > 0:
                content = "\n".join([f"{indent * ' '}{line}" for line in content.split("\n")])
        start_tag = self.tag(indent=indent, length_threshold=tag_length_threshold)
        end_tag = f"</{self.name}>"
        return f"{start_tag}{sep}{content}{sep}{end_tag}"

    def __repr__(self):
        indent = 3 * " "
        lines = [f"{self.name.upper()}("]
        if self.content:
            lines.append(f"{indent}content={{")
            for content_id, content in self.content.items():
                content_repr = repr(content).strip()
                content_repr_lines = content_repr.splitlines()
                for line in content_repr_lines[:-1]:
                    lines.append(f"{2 * indent}{line}")
                lines.append(f"{2 * indent}{content_repr_lines[-1]},")
            lines.append(f"{indent}}},")
        if self.attrs:
            lines.append(f"{indent}attrs={{")
            for key, val in self.attrs.items():
                lines.append(f'{2 * indent}"{key}": "{val}",')
            lines.append(f"{indent}}},")
        lines.append(")")
        return "\n".join(lines)


