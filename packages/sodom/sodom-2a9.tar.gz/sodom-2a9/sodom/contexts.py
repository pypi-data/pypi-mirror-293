__license__ = '''
sodom
Copyright (C) 2023, 2024  Dmitry Protasov (inbox@protaz.ru)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License (version 3) as
published by the Free Software Foundation.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General
Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''


from abc import ABC
from dataclasses import dataclass, field
from functools import reduce
from keyword import iskeyword
from operator import truth
import re
from typing import Any, Callable, ClassVar, assert_never
from sodom.guardians import is_normal_element, is_void_element
from sodom.literals import ANY_TAGS


__all__ = [
    'ABCRenderContext',
    'ctx',
    'xctx',
    'pyctx',
    'DEFAULT_HTML_CONTEXT',
    'DEFAULT_XHTML_CONTEXT',
    'DEFAULT_PYTHON_CONTEXT',
    'CTX',
    'XCTX',
    'PYCTX',
]


def _opening_html_tag_content(
    ctx: 'ABCRenderContext',
    tag: ANY_TAGS,
    attrs: 'Attrs',
    /,
) -> str:
    result = ctx.separator.join(
        filter(
            truth,
            (
                tag,
                ctx.separator.join(
                    attrs.stream(ctx=ctx)
                ),
            ),
        ),
    )

    return result


def _opening_python_tag_content(
    ctx: 'ABCRenderContext',
    tag: ANY_TAGS,
    attrs: 'Attrs',
    /,
) -> str:
    result = ''.join(
        filter(
            truth,
            (
                tag,
                '(',
                ctx.separator.join(
                    attrs.stream(ctx=ctx)
                ),
            ),
        ),
    )

    return result


@dataclass(frozen=True, slots=True, kw_only=True)
class ABCRenderContext(ABC):
    quotes: str
    underscore_replacer: str
    separator: str

    text_element_template: Callable[[str], str]
    void_element_template: Callable[[str], str]
    normal_element_begin_template: Callable[[str], str]
    normal_element_end_template: Callable[[str], str]

    attr_template: Callable[..., str]
    element_attrs_template: Callable[['ABCRenderContext', ANY_TAGS, 'Attrs'], str]

    finalizer: Callable[['ABCRenderContext', 'ABCElement', str], str]


@dataclass(frozen=True, slots=True, kw_only=True)
class HTMLRenderContext(ABCRenderContext):
    DEFAULT_QUOTES: ClassVar[str] = '"'
    DEFAULT_UNDERSCORE_REPLACER: ClassVar[str] = '-'
    DEFAULT_SEPARATOR: ClassVar[str] = ' '
    DEFAULT_FINILIZER: ClassVar[Callable[['HTMLRenderContext', 'ABCElement', str], str]] = lambda _, __, s: s

    quotes: str = field(default=DEFAULT_QUOTES)
    underscore_replacer: str = field(default=DEFAULT_UNDERSCORE_REPLACER)
    separator: str = field(default=DEFAULT_SEPARATOR)

    text_element_template: Callable[[str], str] = field(default='{}'.format)
    void_element_template: Callable[[str], str] = field(default='<{}>'.format)
    normal_element_begin_template: Callable[[str], str] = field(default='<{}>'.format)
    normal_element_end_template: Callable[[str], str] = field(default='</{}>'.format)

    attr_template: Callable[..., str] = field(default='{k}={q}{w}{q}'.format)
    element_attrs_template: Callable[['ABCRenderContext', ANY_TAGS, 'Attrs'], str] = \
        field(default=_opening_html_tag_content)

    finalizer: Callable[['HTMLRenderContext', 'ABCElement', str], str] = DEFAULT_FINILIZER


@dataclass(frozen=True, slots=True, kw_only=True)
class PythonRenderContext(ABCRenderContext):
    DEFAULT_QUOTES: ClassVar[str] = '\''
    DEFAULT_UNDERSCORE_REPLACER: ClassVar[str] = '_'
    DEFAULT_SEPARATOR: ClassVar[str] = ', '
    DEFAULT_TABULATION: ClassVar[str] = '\t'

    @staticmethod
    def DEFAULT_FINILIZER(ctx: 'PythonRenderContext', elem: 'ABCElement', s: str) -> str:
        # add tabulation
        parents = tuple(reversed(elem))
        count = len(parents) - 1
        root = parents[-1]
        s = f'{''.join(ctx.tabulation * count)}{s}'
        # add pass to no children element
        if is_normal_element(elem) and not elem._children:
            s = f'{s[:-1]} pass\n'
        # add sodom importing
        if elem.parent is None:
            s = f'from sodom import *\n\n\n{s}'
            s = f'{s[:-2]} as document{s[-2:]}'
        # add root printing
        last = tuple(root)[-1]
        if last is elem:
            s = f'{s}\n\n\ndocument.render_html_now()'
        return s

    @staticmethod
    def DEFAULT_ATTR_REPLATE(*, k: str, q: str, w: str) -> str:
        if iskeyword(k):
            k = f'{k}_'
        k = k.replace('-', '_')
        return '{k}={q}{w}{q}'.format(k=k, q=q, w=w)

    quotes: str = field(default=DEFAULT_QUOTES)
    underscore_replacer: str = field(default=DEFAULT_UNDERSCORE_REPLACER)
    separator: str = field(default=DEFAULT_SEPARATOR)
    tabulation: str = field(default=DEFAULT_TABULATION)

    text_element_template: Callable[[str], str] = field(default='text(\'{}\')\n'.format)
    void_element_template: Callable[[str], str] = field(default='{})\n'.format)
    normal_element_begin_template: Callable[[str], str] = field(default='with {}):\n'.format)
    normal_element_end_template: Callable[[str], str] = field(default=lambda _: '')

    attr_template: Callable[..., str] = field(default=DEFAULT_ATTR_REPLATE)
    element_attrs_template: Callable[['ABCRenderContext', ANY_TAGS, 'Attrs'], str] = \
        field(default=_opening_python_tag_content)

    finalizer: Callable[['PythonRenderContext', 'ABCElement', str], str] = field(default=DEFAULT_FINILIZER)

ctx = HTMLRenderContext
xctx = None  # reserved for XHTML renderer
pyctx = PythonRenderContext

CTX = DEFAULT_HTML_CONTEXT = HTMLRenderContext()
XCTX = DEFAULT_XHTML_CONTEXT = None  # reserved for XHTML renderer
PYCTX = DEFAULT_PYTHON_CONTEXT = PythonRenderContext()


from sodom.elements import ABCElement, NormalElement, VoidElement
from sodom.attrs import Attrs
