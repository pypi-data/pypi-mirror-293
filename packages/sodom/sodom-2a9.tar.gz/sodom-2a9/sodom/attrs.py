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

from functools import reduce
from keyword import iskeyword
from operator import truth
from typing import ClassVar, Iterable, Mapping, Self, final


@final
class remove(str): pass
@final
class replace(str): pass


class Attrs(dict[str, str]):
    DEFAULT_SEPARATOR: ClassVar[str] = ' '

    def __init__(self, *args, **kwargs):
        fake_self = dict(*args, **kwargs)
        super().__init__()

        for k, w in fake_self.items():
            self[k] = w

    def __setitem__(self, attr_name: str, attr_value: str) -> None:
        if iskeyword(stripped_attr_name := attr_name.strip('_')):
            attr_name = stripped_attr_name
        return super().__setitem__(attr_name, attr_value)

    def __call__(self: Self) -> None:
        from sodom.elements import _CURRENT_ELEMENT

        parent = _CURRENT_ELEMENT.get(None)
        assert parent is not None, 'attribute should be called in context of NormalElement'
        parent.attrs.merge_update(self)

    def merge(
        self: Self,
        *others: Mapping[str, str],
        sep: str = DEFAULT_SEPARATOR,
    ) -> 'Attrs':
        '''Merge attributes into new Attrs instance.'''
        copied_self = Attrs(self)
        copied_self.merge_update(*others, sep=sep)
        return copied_self

    def merge_update(
        self: Self,
        *others: Mapping[str, str],
        sep: str = DEFAULT_SEPARATOR,
    ) -> Self:
        '''Merge attributes inplace.'''
        for other in others:
            if other:
                other = Attrs(other)
                for k, v in other.items():
                    if type(v) is remove:
                        del self[k]
                    elif type(v) is replace:
                        self[k] = v
                    else:
                        self[k] = sep.join(filter(
                            truth,
                            (
                                self.get(k, ''),
                                v,
                            ),
                        ))
        return self

    @classmethod
    def join(
        cls: type[Self],
        *others: Mapping[str, str],
        sep: str = DEFAULT_SEPARATOR,
    ) -> 'Attrs':
        result = reduce(lambda l, r: l.merge_update(r, sep=sep), others, cls())
        return result

    def stream(self: Self, *, ctx: 'ABCRenderContext') -> Iterable[str]:
        it = iter(self.items())

        while (attr := next(it, None)) is not None:
            attr_name, attr_value = attr

            if iskeyword(stripped_attr_name := attr_name.strip('_')):
                attr_name = stripped_attr_name

            if ctx.underscore_replacer != '_':
                attr_name = attr_name.replace('_', ctx.underscore_replacer)

            # attribute value must be significant otherwise empty will be rendered.
            if attr_value:
                attr_formatted = ctx.attr_template(k=attr_name, q=ctx.quotes, w=attr_value)
            else:
                attr_formatted = attr_name
            yield attr_formatted

    def render(self: Self, *, ctx: 'ABCRenderContext') -> str:
        it = self.stream(ctx=ctx)
        result = ''.join(it)
        return result

    __or__ = merge
    __ior__ = merge_update  # type: ignore


from sodom.contexts import ABCRenderContext
