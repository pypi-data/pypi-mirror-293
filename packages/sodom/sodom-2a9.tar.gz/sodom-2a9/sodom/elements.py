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

from abc import ABC, abstractmethod
import html
from contextlib import contextmanager
from contextvars import ContextVar, Token
from functools import partial
from types import TracebackType
from typing import (
    Any,
    Callable,
    ClassVar,
    Generator,
    Iterable,
    Iterator,
    MutableSequence,
    Optional,
    Self,
    Sequence,
)

from sodom.literals import ANY_TAGS, NORMAL_TAGS, VOID_TAGS
from sodom.missing import MISSING


__all__ = [
    '_CURRENT_ELEMENT',
    'isolate',
    'ABCElement',
    'TextWrapper',
    'TagElement',
    'VoidElement',
    'NormalElement',
    'text',
]


_CURRENT_ELEMENT = ContextVar['NormalElement[Any] | None']('_CURRENT_ELEMENT')


@contextmanager
def isolate():
    token = _CURRENT_ELEMENT.set(None)
    try:
        yield
    finally:
        _CURRENT_ELEMENT.reset(token)


class Super:
    __slots__ = (
        '_children',
    )

    _children: Iterable['ABCElement']

    def __init__(self, *children: 'ABCElement') -> None:
        self._children = children

    def __call__(self: Self) -> None:
        for child in self._children:
            child()


class ABCElement(ABC):
    __slots__ = (
        'parent',
        '_ctx',
    )

    REPR_TEMPLATE: ClassVar[Callable[..., str]]

    parent: 'NormalElement | None'
    _ctx: 'ABCRenderContext | None'

    @abstractmethod
    def __eq__(self: Self, other: 'ABCElement | object') -> bool: ...

    def __iter__(self: Self) -> Iterator['ABCElement']:
        yield self

    def __reversed__(self: Self) -> Iterator['NormalElement']:
        yield (current := self)
        while current.parent is not None:
            yield current.parent
            current = current.parent

    @abstractmethod
    def __copy__(self: Self) -> Self: ...

    def __call__(self: Self) -> Self:
        if self.parent is not None:
            self.parent._children.remove(self)
        self.parent = _CURRENT_ELEMENT.get(None)
        if self.parent is not None:
            self.parent._children.append(self)
        return self

    def __mod__(self: Self, ctx: 'ABCRenderContext | None') -> Self:
        self._ctx = ctx
        return self

    def __str__(self: Self) -> str:
        return self.render(ctx=CTX)

    @abstractmethod
    def stream(self: Self, *elems: 'ABCElement', ctx: 'ABCRenderContext') -> Iterator[str]: ...

    def stream_html(
        self: Self,
        *elems: 'ABCElement',
        doctype: str = '<!DOCTYPE html>',
    ) -> Iterator[str]:
        yield from (
            text(doctype, escape=False, use_parent=False)
            .stream(
                self,
                *elems,
                ctx=CTX,
            )
        )

    def render(
        self: Self,
        *elems: 'ABCElement',
        ctx: 'ABCRenderContext',
    ) -> str:
        it = self.stream(
            *elems,
            ctx=ctx,
        )
        return ''.join(it)

    def render_html(
        self: Self,
        *elems: 'ABCElement',
        doctype: str = '<!DOCTYPE html>',
    ) -> str:
        it = self.stream_html(
            *elems,
            doctype=doctype,
        )
        return ''.join(it)

    def render_now(
        self: Self,
        *elems: 'ABCElement',
        ctx: 'ABCRenderContext' = MISSING,
    ) -> None:
        if self._ctx is not None:
            ctx = self._ctx
        if ctx is MISSING:
            raise RuntimeError('ctx is missing')

        import tempfile
        import webbrowser

        tmp_file_path = tempfile.mktemp(
            prefix=(
                f'{ABCElement.render_now.__module__}'
                f'.{ABCElement.render_now.__name__}'
                f'.'
            ),
            suffix='.html',
        )

        with open(tmp_file_path, 'w') as f:
            partitions = self.stream(
                *elems,
                ctx=ctx,
            )
            for partition in partitions:
                f.write(partition)
        webbrowser.open_new_tab(tmp_file_path)

    def render_html_now(
        self: Self,
        *elems: 'ABCElement',
    ) -> None:
        return (text('<!DOCTYPE html>', escape=False, use_parent=False) % CTX).render_now(self)


class TextWrapper(ABCElement):
    __slots__ = (
        'text',
    )

    REPR_TEMPLATE: ClassVar[Callable[..., str]] = '<"{}"{} @{}>'.format

    text: str

    def __init__(
        self,
        text: str,
        /,
        *,
        parent: 'NormalElement[Any] | None' = None,
        escape: bool = True,
        use_parent: bool = MISSING,
        ctx: 'ABCRenderContext | None' = None,
    ) -> None:
        assert \
            (parent is not None) ^ (use_parent is not MISSING), \
            'Should be used only [parent] xor [use_parent].'

        if escape:
            text = html.escape(text)

        self.text = text
        self.parent = parent
        self._ctx = ctx

        if use_parent is not MISSING and use_parent:
            self()

    def __eq__(self: Self, other: ABCElement | object) -> bool:
        return (
            isinstance(other, TextWrapper)
            and self.text == other.text
        )

    def __copy__(self: Self) -> Self:
        copied_self = type(self)(self.text, use_parent=False)
        return copied_self

    def stream(
        self: Self,
        *elems: ABCElement,
        ctx: 'ABCRenderContext' = MISSING,
    ) -> Iterator[str]:
        if self._ctx is not None:
            ctx = self._ctx
        if ctx is MISSING:
            raise RuntimeError('ctx is missing')

        result = ctx.text_element_template(self.text)
        yield ctx.finalizer(ctx, self, result)

        if elems:
            for elem in elems:
                yield from elem.stream(ctx=ctx)

    def __repr__(self) -> str:
        return self.REPR_TEMPLATE(
            self.text[:50],
            '[...]' * (len(self.text) > 50),
            id(self),
        )


class TagElement[TAG: ANY_TAGS](ABCElement):
    __slots__ = (
        'tag',
        'attrs',
    )

    tag: TAG
    attrs: 'Attrs'

    def __eq__(self: Self, other: ABCElement | object) -> bool:
        return (
            isinstance(other, type(self))
            and self.tag == other.tag
            and self.attrs == other.attrs
        )

    def __call__(
        self: Self,
        **attrs: str,
    ) -> Self:
        result = super().__call__()
        if attrs:
            self.attrs.merge_update(attrs)
        return result

    def __lt__(
        self: Self,
        others: dict[str, str] | Sequence[dict[str, str]],
    ) -> Self:
        if isinstance(others, dict):
            others = (others,)
        self.attrs.merge_update(*others)
        return self


class VoidElement[TAG: VOID_TAGS](TagElement[TAG]):
    __slots__ = ()

    REPR_TEMPLATE: ClassVar[Callable[..., str]] = '<{} @{}>'.format

    def __init__(
        self,
        tag: TAG,
        /,
        **attrs: str,
    ) -> None:
        self.tag = tag
        self.attrs = Attrs(attrs)
        self.parent = None
        self._ctx = None
        self()

    @isolate()
    def __copy__(self: Self) -> Self:
        copied_self = type(self)(self.tag, **self.attrs) % self._ctx
        return copied_self

    def stream(
        self: Self,
        *elems: ABCElement,
        ctx: 'ABCRenderContext' = MISSING,
    ) -> Iterator[str]:
        if self._ctx is not None:
            ctx = self._ctx
        if ctx is MISSING:
            raise RuntimeError('ctx is missing')

        tag_content = ctx.element_attrs_template(
            ctx,
            self.tag,
            self.attrs,
        )
        result = ctx.void_element_template(tag_content)

        yield ctx.finalizer(ctx, self, result)

        if elems:
            for elem in elems:
                yield from elem.stream(ctx=ctx)

    def __repr__(self: Self) -> str:
        ctx = self._ctx or CTX

        result = self.REPR_TEMPLATE(
            ctx.element_attrs_template(
                ctx,
                self.tag,
                self.attrs,
            ),
            id(self),
        )

        return result


class NormalElement[TAG: NORMAL_TAGS](TagElement[TAG]):
    __slots__ = (
        '_children',
        '_context_token',
    )

    REPR_TEMPLATE: ClassVar[Callable[..., str]] = '<{} @{}>:{}</{}>'.format

    _children: MutableSequence['ABCElement']
    _context_token: Token | None

    def __init__(
        self,
        tag: TAG,
        /,
        *children: 'ABCElement | str',
        **attrs: str,
    ) -> None:
        self.tag = tag
        self.attrs = Attrs(attrs)
        self.parent = None
        self._ctx = None
        self()
        self._children = list['DOMElement']()
        if children:
            self.add(*children)
        self._context_token = None

    def add(
        self: Self,
        *children: 'ABCElement | str',
    ) -> None:
        new_children: list[ABCElement] = list[Any](children)

        for idx, child in enumerate(new_children):
            if isinstance(child, str):
                new_children[idx] = child = TextWrapper(child, parent=self)
            elif child.parent is not None:
                child.parent.remove(child)
            child.parent = self

        self._children.extend(new_children)

    def insert(
        self: Self,
        index: int,
        *children: 'ABCElement | str',
    ) -> None:
        assert index >= 0
        assert index <= len(self._children)

        new_children: list[ABCElement] = list[Any](children)

        for idx, child in enumerate(new_children):
            if isinstance(child, str):
                new_children[idx] = child = TextWrapper(child, parent=self)
            if child.parent is not None:
                child.parent.remove(child)
            child.parent = self

        moved_children = self._children[index:]
        self._children[index:] = [*new_children, *moved_children]

    def remove(
        self: Self,
        *children: 'ABCElement',
    ) -> None:
        assert all(child in self._children for child in children)

        for child in children:
            self._children.remove(child)
            child.parent = None

    def clear(self: Self) -> None:
        for child in self._children:
            child.parent = None
        self._children.clear()

    @contextmanager
    def overwrite(self: Self) -> Generator[Super, None, None]:
        super_ = Super(*self._children)
        self.clear()

        with self:
            yield super_

    def __eq__(self: Self, other: ABCElement | object) -> bool:
        return (
            isinstance(other, type(self))
            and self.tag == other.tag
            and self.attrs == other.attrs
            and (
                isinstance(other, NormalElement)
                and self._children == other._children
            )
        )

    def __copy__(self: Self) -> Self:
        copied_self = type(self)(self.tag, **self.attrs) % self._ctx

        if self._children:
            for child in self._children:
                copied_child = child.__copy__()
                copied_self._children.append(copied_child)
                copied_child.parent = copied_self

        return copied_self

    def __getstate__(self: Self, *args, **kwargs):
        *results, state = super().__getstate__(*args, **kwargs)  # type: ignore
        state.pop('_context_token', None)
        return *results, state

    def __enter__(self: Self) -> Self:
        self._context_token = _CURRENT_ELEMENT.set(self)
        return self

    def __exit__(
        self: Self,
        exc_type: Optional[type[Exception]],
        exc_value: Optional[Exception],
        exc_traceback: Optional[TracebackType],
    ) -> None:
        assert \
            self._context_token is not None, \
            f'invalid state of {NormalElement.__name__}._context_token'
        _CURRENT_ELEMENT.reset(self._context_token)
        self._context_token = None

    def __iter__(self: Self) -> Iterator[ABCElement]:
        yield self
        for child in self._children:
            yield from child

    def __len__(self: Self) -> int:
        return self._children.__len__()

    def stream(
        self: Self,
        *elems: ABCElement,
        ctx: 'ABCRenderContext' = MISSING,
    ) -> Iterator[str]:
        if self._ctx is not None:
            ctx = self._ctx
        if ctx is MISSING:
            raise RuntimeError('ctx is missing')

        tag_content = ctx.element_attrs_template(
            ctx,
            self.tag,
            self.attrs,
        )

        tag_begin = ctx.normal_element_begin_template(
            tag_content,
        )
        yield ctx.finalizer(ctx, self, tag_begin)

        if self._children:
            for child in self._children:
                yield from child.stream(ctx=ctx)
        tag_end = ctx.normal_element_end_template(self.tag)
        yield tag_end

        if elems:
            for elem in elems:
                yield from elem.stream(ctx=ctx)


    def __repr__(self: Self) -> str:
        ctx = self._ctx or CTX

        result = self.REPR_TEMPLATE(
            ctx.element_attrs_template(
                ctx,
                self.tag,
                self.attrs,
            ),
            id(self),
            len(self._children),
            self.tag,
        )

        return result


text = partial(TextWrapper, use_parent=True)


from sodom.attrs import Attrs
from sodom.contexts import CTX, ABCRenderContext
