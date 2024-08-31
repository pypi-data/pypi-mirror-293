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

import asyncio
from contextlib import nullcontext
import pickle
from concurrent.futures import ThreadPoolExecutor
from random import randbytes
from statistics import mean, median
from time import sleep, time as time_
from typing import Any, Callable, Self, Sequence
import unittest.mock

import pytest

import sodom
from sodom import *
from sodom import literals
from sodom.attrs import Attrs, replace, remove
from sodom.contexts import DEFAULT_HTML_CONTEXT, ABCRenderContext
from sodom.elements import ABCElement, NormalElement, TagElement, VoidElement, text, TextWrapper


def _rand_id():
    return Attrs(id=randbytes(8).hex())


class TestTextElement:
    @pytest.mark.parametrize(
        ('etalon', 'other', 'is_equal'),
        [
            (text('foo'), text('foo'), True),
            (text('foo'), text('bar'), False),
            (text('foo'), object(), False),
        ],
    )
    def test_eq(self: Self, etalon: TextWrapper, other: Any, is_equal: bool):
        assert (etalon == other) == is_equal

    @pytest.mark.parametrize(
        ('parent', 'elem'),
        [
            (nullcontext(), text('foo')),
            (div(), text('foo')),
        ]
    )
    def test_copy(self: Self, parent: NormalElement, elem: TextWrapper):
        with parent:
            copy = elem.__copy__()
        assert all((
            elem.text == copy.text,
            elem.parent is None,
            elem._ctx is None,
        ))


    # @pytest.mark.parametrize(
    #     ('elem', 'result'),
    #     [
    #         (TextWrapper('foo'), 'foo'),
    #         (text('foo'), 'foo'),
    #     ]
    # )
    # def test_stream(self: Self, elem: TextWrapper, result: str):
    #     assert ''.join(elem.stream(ctx=DEFAULT_HTML_CONTEXT)) == result

    @unittest.mock.patch('sodom.contexts.DEFAULT_HTML_CONTEXT')
    def test_stream_uses_context(self, DEFAULT_HTML_CONTEXT: unittest.mock.MagicMock | ABCRenderContext):
        t = text('foo')
        next(iter(t.stream(ctx=DEFAULT_HTML_CONTEXT)))
        DEFAULT_HTML_CONTEXT.text_element_template.assert_called_once_with('foo')
        pass



class TestVoidElement:
    @pytest.mark.parametrize(
        'elem',
        [
            hr(),
            hr(foo='bar'),
        ],
    )
    def test_copy(self, elem: VoidElement):
        copied_elem = elem.__copy__()
        assert elem is not copied_elem
        assert elem == copied_elem

    @pytest.mark.parametrize(
        ('elem', 'rendered'),
        [
            (hr().render_html(), '<!DOCTYPE html><hr>'),
            (hr(foo="bar").render_html(), '<!DOCTYPE html><hr foo="bar">'),
            (hr(foo="bar", baz="").render_html(), '<!DOCTYPE html><hr foo="bar" baz>'),
            (hr(foo="", bar="", baz="").render_html(), '<!DOCTYPE html><hr foo bar baz>'),
        ],
    )
    def test_render(self, elem, rendered):
        assert elem == rendered

    @pytest.mark.parametrize(
        ('elem', 'repred'),
        [
            (repr(elem := hr()), f'<hr @{id(elem)}>'),
            (repr(elem := hr(foo="bar")), f'<hr foo="bar" @{id(elem)}>'),
            (repr(elem := hr(foo="bar", baz="")), f'<hr foo="bar" baz @{id(elem)}>'),
            (repr(elem := hr(foo="", bar="", baz="")), f'<hr foo bar baz @{id(elem)}>'),
        ],
    )
    def test_repr(self, elem, repred):
        assert elem == repred

    def test_parent_changing(self):
        h = hr()
        assert h.parent == None

        with div() as parent1:
            h()
        assert h.parent == parent1
        assert h in parent1._children

        with div() as parent2:
            h()
        assert h.parent == parent2
        assert h in parent2._children


class TestNormalElement:
    @pytest.mark.parametrize(
        'elem',
        [
            div(),
            div(foo='bar'),
            div(hr()),
            div(hr(), foo='bar'),
        ],
    )
    def test_copy(self, elem: NormalElement):
        copied_elem = elem.__copy__()
        assert elem is not copied_elem
        assert elem == copied_elem
        assert elem._children == copied_elem._children

    @pytest.mark.parametrize(
        ('elem', 'rendered'),
        [
            (div().render_html(), '<!DOCTYPE html><div></div>'),
            (div(foo="bar").render_html(), '<!DOCTYPE html><div foo="bar"></div>'),
            (div(foo="bar", baz="").render_html(), '<!DOCTYPE html><div foo="bar" baz></div>'),
            (div(foo="", bar="", baz="").render_html(), '<!DOCTYPE html><div foo bar baz></div>'),

            (div(div()).render_html(), '<!DOCTYPE html><div><div></div></div>'),
            (div(div(), foo="bar").render_html(), '<!DOCTYPE html><div foo="bar"><div></div></div>'),
            (div(div(), foo="bar", baz="").render_html(), '<!DOCTYPE html><div foo="bar" baz><div></div></div>'),
            (div(div(), foo="", bar="", baz="").render_html(), '<!DOCTYPE html><div foo bar baz><div></div></div>'),

            (div(div(), div()).render_html(), '<!DOCTYPE html><div><div></div><div></div></div>'),
            (div(div(), div(), foo="bar").render_html(), '<!DOCTYPE html><div foo="bar"><div></div><div></div></div>'),
            (div(div(), div(), foo="bar", baz="").render_html(), '<!DOCTYPE html><div foo="bar" baz><div></div><div></div></div>'),
            (div(div(), div(), foo="", bar="", baz="").render_html(), '<!DOCTYPE html><div foo bar baz><div></div><div></div></div>'),

            (div(div(div()), div()).render_html(), '<!DOCTYPE html><div><div><div></div></div><div></div></div>'),
            (div(div(div()), div(), foo="bar").render_html(), '<!DOCTYPE html><div foo="bar"><div><div></div></div><div></div></div>'),
            (div(div(div()), div(), foo="bar", baz="").render_html(), '<!DOCTYPE html><div foo="bar" baz><div><div></div></div><div></div></div>'),
            (div(div(div()), div(), foo="", bar="", baz="").render_html(), '<!DOCTYPE html><div foo bar baz><div><div></div></div><div></div></div>'),
        ],
    )
    def test_render(self, elem: str, rendered: str):
        assert elem == rendered

    @pytest.mark.parametrize(
        ('attrs', 'rendered'),
        [
            (Attrs(), ''),
            (Attrs(foo="bar"), ' foo="bar"'),
            (Attrs(foo="bar", baz=""), ' foo="bar" baz'),
            (Attrs(foo="", bar="", baz=""), ' foo bar baz'),
        ],
    )
    def test_render_with_children_via_context(self, attrs, rendered):
        with div(**attrs) as elem:
            pass
        assert elem.render_html() == f'<!DOCTYPE html><div{rendered}></div>'

        with div(**attrs) as elem:
            div()
        assert elem.render_html() == f'<!DOCTYPE html><div{rendered}><div></div></div>'

        with div(**attrs) as elem:
            div()
            div()
        assert elem.render_html() == f'<!DOCTYPE html><div{rendered}><div></div><div></div></div>'

        with div(**attrs) as elem:
            with div():
                div()
            div()
        assert elem.render_html() == f'<!DOCTYPE html><div{rendered}><div><div></div></div><div></div></div>'

    @pytest.mark.parametrize(
        ('elem', 'rendered'),
        [
            (div(), '<div></div>'),
            (div(foo="bar"), '<div foo="bar"></div>'),
            (div(foo="bar", baz=""), '<div foo="bar" baz></div>'),
            (div(foo="", bar="", baz=""), '<div foo bar baz></div>'),

            (div(div()), '<div><div></div></div>'),
            (div(div(), foo="bar"), '<div foo="bar"><div></div></div>'),
            (div(div(), foo="bar", baz=""), '<div foo="bar" baz><div></div></div>'),
            (div(div(), foo="", bar="", baz=""), '<div foo bar baz><div></div></div>'),

            (div(div(), div()), '<div><div></div><div></div></div>'),
            (div(div(), div(), foo="bar"), '<div foo="bar"><div></div><div></div></div>'),
            (div(div(), div(), foo="bar", baz=""), '<div foo="bar" baz><div></div><div></div></div>'),
            (div(div(), div(), foo="", bar="", baz=""), '<div foo bar baz><div></div><div></div></div>'),

            (div(div(div()), div()), '<div><div><div></div></div><div></div></div>'),
            (div(div(div()), div(), foo="bar"), '<div foo="bar"><div><div></div></div><div></div></div>'),
            (div(div(div()), div(), foo="bar", baz=""), '<div foo="bar" baz><div><div></div></div><div></div></div>'),
            (div(div(div()), div(), foo="", bar="", baz=""), '<div foo bar baz><div><div></div></div><div></div></div>'),
        ],
    )
    def test_str(self, elem: NormalElement, rendered: str):
        assert str(elem) == rendered

    @pytest.mark.parametrize(
        ('parent', 'child'),
        [
            (div(), div()),
            (div(div()), div()),
        ],
    )
    def test_add(self, parent: NormalElement, child: NormalElement):
        parent.add(child)
        assert child in parent._children
        assert parent._children[-1] is child

    @pytest.mark.parametrize(
        ('parent', 'child', 'pos'),
        [
            (div(), div(), -1),
            (div(), div(), 0),
            (div(), div(), 1),

            (div(div()), div(), -1),
            (div(div()), div(), 0),
            (div(div()), div(), 1),
            (div(div()), div(), 2),

            (div(div(), div()), div(), -1),
            (div(div(), div()), div(), 0),
            (div(div(), div()), div(), 1),
            (div(div(), div()), div(), 2),
            (div(div(), div()), div(), 3),
        ],
    )
    def test_insert(self, parent: NormalElement, child: NormalElement, pos: int):
        if (0 <= pos <= len(parent._children)):
            ctx = nullcontext()
        else:
            ctx = pytest.raises(AssertionError)

        with ctx:
            parent.insert(pos, child)
            assert parent._children[pos] is child

    @pytest.mark.parametrize(
        ('parent', 'child'),
        [
            (div(div() < _rand_id()), div() < _rand_id()),
            (div((child := div() < _rand_id())), child),

            (div(div() < _rand_id(), div() < _rand_id()), div()),
            (div((child := div() < _rand_id()), div() < _rand_id()), child),
            (div(div() < _rand_id(), (child := div() < _rand_id())), child),

            (div(div() < _rand_id(), div() < _rand_id(), div() < _rand_id()), div()),
            (div((child := div() < _rand_id()), div() < _rand_id(), div() < _rand_id()), child),
            (div(div() < _rand_id(), (child := div() < _rand_id()), div() < _rand_id()), child),
            (div(div() < _rand_id(), div() < _rand_id(), (child := div() < _rand_id())), child),
        ],
    )
    def test_remove(self, parent: NormalElement, child: ABCElement):
        if child in parent._children:
            ctx = nullcontext()
        else:
            ctx = pytest.raises(AssertionError)

        with ctx:
            parent.remove(child)
            assert child not in parent._children
            assert child.parent is None

    def test_pickle(self):
        with div(foo='bar') as doc:
            br()
        p = pickle.dumps(doc)
        unpickled_doc = pickle.loads(p)
        assert doc.render_html(doctype='') == unpickled_doc.render_html(doctype='')

    @pytest.mark.parametrize(
        ('root', 'elems'),
        [
            (
                elem0 := div(
                    elem1 := div(),
                    elem2 := div(
                        elem3 := hr(),
                        elem4 := hr(),
                        elem5 := hr(),
                    ),
                    elem6 := div(),
                    elem7 := div(
                        elem8 := div(),
                        elem9 := div(
                            elem10 := hr(),
                            elem11 := hr(),
                            elem12 := hr(),
                        ),
                        elem13 := div(),
                    ),
                    elem14 := div(),
                ),
                [
                    elem0,
                    elem1,
                    elem2,
                    elem3,
                    elem4,
                    elem5,
                    elem6,
                    elem7,
                    elem8,
                    elem9,
                    elem10,
                    elem11,
                    elem12,
                    elem13,
                    elem14,
                ],
            ),
        ]
    )
    def test_iter(self, root: NormalElement, elems: Sequence[ABCElement]):
        for idx, elem in enumerate(root):
            assert elems[idx] == elem


class TestAttrs:
    @pytest.mark.parametrize(
        ('attrs', 'rendered'),
        [
            ((Attrs(class_='bar'),), 'class="bar"'),
            ((Attrs(_class='bar'),), 'class="bar"'),
            ((Attrs(_class_='bar'),), 'class="bar"'),

            ((Attrs(class__='bar'),), 'class="bar"'),
            ((Attrs(_class__='bar'),), 'class="bar"'),

            ((Attrs(__class='bar'),), 'class="bar"'),
            ((Attrs(__class_='bar'),), 'class="bar"'),

            ((Attrs(__class__='bar'),), 'class="bar"'),
        ],
    )
    def test_stripping_underscores(self, attrs: Sequence[Attrs], rendered: str):
        assert Attrs.join(*attrs).render(ctx=DEFAULT_HTML_CONTEXT) == rendered

    @pytest.mark.parametrize(
        ('attrs', 'rendered'),
        [
            ((Attrs(data_foo='bar'),), 'data-foo="bar"'),
            ((Attrs(data_foo_='bar'),), 'data-foo-="bar"'),
        ],
    )
    def test_replace_underscores(self, attrs: Sequence[Attrs], rendered: str):
        assert Attrs.join(*attrs).render(ctx=DEFAULT_HTML_CONTEXT) == rendered

    @pytest.mark.parametrize(
        ('elem', 'attrs'),
        [
            (hr(), {'foo': 'bar'}),
            (hr(), Attrs(foo='bar')),

            (hr(), ({'foo': 'bar'},)),
            (hr(), (Attrs(foo='bar'),)),
            (hr(), ({'foo': 'bar'}, Attrs(baz='qux'))),

            (hr(), (Attrs(foo='bar'), Attrs(foo='baz'))),

            (div(), {'foo': 'bar'}),
            (div(), Attrs(foo='bar')),

            (div(), ({'foo': 'bar'},)),
            (div(), (Attrs(foo='bar'),)),
            (div(), ({'foo': 'bar'}, Attrs(baz='qux'))),

            (div(), (Attrs(foo='bar'), Attrs(foo='baz'))),

            (hr(foo='bar'), {'foo': 'bar'}),
            (hr(foo='bar'), Attrs(foo='bar')),

            (hr(foo='bar'), ({'foo': 'bar'},)),
            (hr(foo='bar'), (Attrs(foo='bar'),)),
            (hr(foo='bar'), ({'foo': 'bar'}, Attrs(baz='qux'))),

            (hr(foo='bar'), (Attrs(foo='bar'), Attrs(foo='baz'))),

            (div(foo='bar'), {'foo': 'bar'}),
            (div(foo='bar'), Attrs(foo='bar')),

            (div(foo='bar'), ({'foo': 'bar'},)),
            (div(foo='bar'), (Attrs(foo='bar'),)),
            (div(foo='bar'), ({'foo': 'bar'}, Attrs(baz='qux'))),

            (div(foo='bar'), (Attrs(foo='bar'), Attrs(foo='baz'))),
        ],
    )
    def test_lt_attrs(self, elem: TagElement, attrs: dict[str, str] | Attrs | Sequence[dict[str, str] | Attrs]):
        _elem_orig_attrs = elem.attrs.copy()

        elem < attrs

        if isinstance(attrs, Sequence):
            joined_attrs = Attrs.join(_elem_orig_attrs, *attrs)
        else:
            joined_attrs = Attrs.join(_elem_orig_attrs, attrs)

        assert tuple(elem.attrs.items()) == tuple(joined_attrs.items())

    @pytest.mark.parametrize(
        ('elem', 'attrs'),
        [
            (div(), (Attrs(foo='bar'),),),
            (div(), (Attrs(foo='bar'), Attrs(baz='qux')),),
            (div(), (Attrs(foo='bar'), Attrs(foo='baz')),),

            (div(foo='bar'), (Attrs(foo='bar'),),),
            (div(foo='bar'), (Attrs(foo='bar'), Attrs(baz='qux')),),
            (div(foo='bar'), (Attrs(foo='bar'), Attrs(foo='baz')),),
        ],
    )
    def test_call_attr_with_context(self, elem: NormalElement, attrs: Sequence[Attrs]):
        _elem_orig_attrs = elem.attrs.copy()

        with elem:
            for attr in attrs:
                attr()

        joined_attrs = Attrs.join(_elem_orig_attrs, *attrs)
        assert tuple(elem.attrs.items()) == tuple(joined_attrs.items())

    @pytest.mark.parametrize(
        ('attrs', 'rendered'),
        [
            (Attrs(disabled=''), 'disabled'),
        ],
    )
    def test_empty_attr_adding(self, attrs: Attrs, rendered: str):
        assert attrs.render(ctx=DEFAULT_HTML_CONTEXT) == rendered

    @pytest.mark.parametrize(
        ('attrs', 'replacer'),
        [
            (Attrs(disabled=''), Attrs(disabled=replace('disabled'))),
            (Attrs(disabled='true'), Attrs(disabled=replace('disabled'))),
            (Attrs(disabled='true'), Attrs(disabled=replace(''))),
        ],
    )
    def test_replace(self, attrs: Attrs, replacer: Attrs):
        attrs |= replacer
        assert all((
            attrs[k] == w and attrs[k] is w and isinstance(w, replace)
            for k, w in replacer.items()
        ))

    @pytest.mark.parametrize(
        ('attrs', 'remover'),
        [
            (Attrs(disabled=''), Attrs(disabled=remove())),
            (Attrs(disabled='true'), Attrs(disabled=remove())),
            (Attrs(disabled='true'), Attrs(disabled=remove())),
        ],
    )
    def test_remove(self, attrs: Attrs, remover: Attrs):
        attrs |= remover
        assert all((
            k not in attrs and isinstance(w, remove)
            for k, w in remover.items()
        ))

    @pytest.mark.parametrize(
        ('oper', 'left', 'right'),
        [
            (Attrs.merge, Attrs(), Attrs()),
            (Attrs.merge, Attrs(foo='bar'), Attrs()),
            (Attrs.merge, Attrs(), Attrs(foo='bar')),
            (Attrs.merge, Attrs(foo='bar'), Attrs(foo='baz')),
            (Attrs.merge, Attrs(foo='bar', qux='quux'), Attrs(foo='baz')),
            (Attrs.merge, Attrs(foo='bar'), Attrs(foo='baz', qux='quux')),
            (Attrs.merge, Attrs(foo='bar', qux='quux'), Attrs(foo='baz', qux='quux')),

            (Attrs.merge, Attrs(), Attrs(foo='')),
            (Attrs.merge, Attrs(foo=''), Attrs()),
            (Attrs.merge, Attrs(foo=''), Attrs(foo='')),
            (Attrs.merge, Attrs(bar=''), Attrs(foo='')),
            (Attrs.merge, Attrs(foo=''), Attrs(bar='')),
            (Attrs.merge, Attrs(foo='', bar=''), Attrs(foo='', bar='')),

            (Attrs.__or__, Attrs(), Attrs()),
            (Attrs.__or__, Attrs(foo='bar'), Attrs()),
            (Attrs.__or__, Attrs(), Attrs(foo='bar')),
            (Attrs.__or__, Attrs(foo='bar'), Attrs(foo='baz')),
            (Attrs.__or__, Attrs(foo='bar', qux='quux'), Attrs(foo='baz')),
            (Attrs.__or__, Attrs(foo='bar'), Attrs(foo='baz', qux='quux')),
            (Attrs.__or__, Attrs(foo='bar', qux='quux'), Attrs(foo='baz', qux='quux')),

            (Attrs.__or__, Attrs(), Attrs(foo='')),
            (Attrs.__or__, Attrs(foo=''), Attrs()),
            (Attrs.__or__, Attrs(foo=''), Attrs(foo='')),
            (Attrs.__or__, Attrs(bar=''), Attrs(foo='')),
            (Attrs.__or__, Attrs(foo=''), Attrs(bar='')),
            (Attrs.__or__, Attrs(foo='', bar=''), Attrs(foo='', bar='')),
        ],
    )
    def test_merge(self, oper, left: Attrs, right: Attrs):
        new = oper(left, right)
        assert new is not left
        assert new is not right
        assert tuple(new.items()) == tuple(Attrs.join(left, right).items())

    @pytest.mark.parametrize(
        ('oper', 'left', 'right'),
        [
            (Attrs.merge_update, Attrs(), Attrs()),
            (Attrs.merge_update, Attrs(foo='bar'), Attrs()),
            (Attrs.merge_update, Attrs(), Attrs(foo='bar')),
            (Attrs.merge_update, Attrs(foo='bar'), Attrs(foo='baz')),
            (Attrs.merge_update, Attrs(foo='bar', qux='quux'), Attrs(foo='baz')),
            (Attrs.merge_update, Attrs(foo='bar'), Attrs(foo='baz', qux='quux')),
            (Attrs.merge_update, Attrs(foo='bar', qux='quux'), Attrs(foo='baz', qux='quux')),

            (Attrs.merge_update, Attrs(), Attrs(foo='')),
            (Attrs.merge_update, Attrs(foo=''), Attrs()),
            (Attrs.merge_update, Attrs(foo=''), Attrs(foo='')),
            (Attrs.merge_update, Attrs(bar=''), Attrs(foo='')),
            (Attrs.merge_update, Attrs(foo=''), Attrs(bar='')),
            (Attrs.merge_update, Attrs(foo='', bar=''), Attrs(foo='', bar='')),

            (Attrs.__ior__, Attrs(), Attrs()),
            (Attrs.__ior__, Attrs(foo='bar'), Attrs()),
            (Attrs.__ior__, Attrs(), Attrs(foo='bar')),
            (Attrs.__ior__, Attrs(foo='bar'), Attrs(foo='baz')),
            (Attrs.__ior__, Attrs(foo='bar', qux='quux'), Attrs(foo='baz')),
            (Attrs.__ior__, Attrs(foo='bar'), Attrs(foo='baz', qux='quux')),
            (Attrs.__ior__, Attrs(foo='bar', qux='quux'), Attrs(foo='baz', qux='quux')),

            (Attrs.__ior__, Attrs(), Attrs(foo='')),
            (Attrs.__ior__, Attrs(foo=''), Attrs()),
            (Attrs.__ior__, Attrs(foo=''), Attrs(foo='')),
            (Attrs.__ior__, Attrs(bar=''), Attrs(foo='')),
            (Attrs.__ior__, Attrs(foo=''), Attrs(bar='')),
            (Attrs.__ior__, Attrs(foo='', bar=''), Attrs(foo='', bar='')),
        ],
    )
    def test_merge_update(self, oper, left: Attrs, right: Attrs):
        new = oper(left, right)
        assert new is left
        assert new is not right
        assert all((w in left[k] for k, w in right.items()))

    @pytest.mark.parametrize(
        ('attrs'),
        [
            Attrs(class_='foo') | {'class': 'bar'},
            Attrs({'class': 'foo'}) | {'class_': 'bar'},
            Attrs({'class_': 'foo'}) | {'class_': 'bar'},
        ],
    )
    def test_initial_and_merged_attr_name_unmatch(self, attrs: Attrs):
        assert attrs['class'] == 'foo bar'


@pytest.mark.asyncio
async def test_building_html_in_two_tasks():
    for _ in range(10):
        async def task1():
            await asyncio.sleep(2)
            with div() as d:
                await asyncio.sleep(2)
                text('task1')
                text('task1')
            return d

        async def task2():
            with div() as d:
                await asyncio.sleep(2)
                text('task2')
                text('task2')
                await asyncio.sleep(2)
            return d

        div1, div2 = await asyncio.gather(
            task1(),
            task2(),
        )

        assert div1.parent == None
        assert div2.parent == None
        assert div1._children[0] == text('task1')
        assert div1._children[1] == text('task1')
        assert div2._children[0] == text('task2')
        assert div2._children[1] == text('task2')


def test_building_html_in_two_threads():
    for _ in range(10):
        def task1():
            sleep(2)
            with div() as d:
                sleep(2)
                text('task1')
                text('task1')
            return d

        def task2():
            with div() as d:
                sleep(2)
                text('task2')
                text('task2')
                sleep(2)
            return d

        with ThreadPoolExecutor(2) as pool:
            t1 = pool.submit(task1)
            t2 = pool.submit(task2)
        div1 = t1.result()
        div2 = t2.result()

        assert div1.parent == None
        assert div2.parent == None
        assert div1._children[0] == text('task1')
        assert div1._children[1] == text('task1')
        assert div2._children[0] == text('task2')
        assert div2._children[1] == text('task2')


def _sodom_case():
    with sodom.body() as root:
        with sodom.div(class_='d-flex flex-column flex-md-row align-items-center p-3 px-md-4 mb-3 bg-white border-bottom box-shadow'):
            with sodom.h5(class_='my-0 mr-md-auto font-weight-normal'):
                sodom.text('Company name')
            with sodom.nav(class_='my-2 my-md-0 mr-md-3'):
                with sodom.a(class_='p-2 text-dark', href='#'):
                    sodom.text('Features')
                with sodom.a(class_='p-2 text-dark', href='#'):
                    sodom.text('Enterprise')
                with sodom.a(class_='p-2 text-dark', href='#'):
                    sodom.text('Support')
                with sodom.a(class_='p-2 text-dark', href='#'):
                    sodom.text('Pricing')
    result = root.render_html(doctype='')
    return result


def _dominate_case():
    with dominate_tags.body() as root: # type: ignore
        with dominate_tags.div(cls='d-flex flex-column flex-md-row align-items-center p-3 px-md-4 mb-3 bg-white border-bottom box-shadow'): # type: ignore
            with dominate_tags.h5(cls='my-0 mr-md-auto font-weight-normal'): # type: ignore
                dominate_text('Company name')
            with dominate_tags.nav(cls='my-2 my-md-0 mr-md-3'): # type: ignore
                with dominate_tags.a(cls='p-2 text-dark', href='#'): # type: ignore
                    dominate_text('Features')
                with dominate_tags.a(cls='p-2 text-dark', href='#'): # type: ignore
                    dominate_text('Enterprise')
                with dominate_tags.a(cls='p-2 text-dark', href='#'): # type: ignore
                    dominate_text('Support')
                with dominate_tags.a(cls='p-2 text-dark', href='#'): # type: ignore
                    dominate_text('Pricing')
    result = root.render(pretty=False)
    return result


try:
    from dominate import tags as dominate_tags
    from dominate.util import text as dominate_text
except ImportError:
    pass
else:
    def _time_list(func: Callable, runs: int):
        case_time_list = []

        result = None
        for _ in range(runs):
            start = time_()
            result = func()
            current = time_() - start
            case_time_list.append(current)

        sum_sodom_time_list = sum(case_time_list)
        mean_sodom_time_list = mean(case_time_list)
        median_sodom_time_list = median(case_time_list)

        print()
        print(f'\t{func.__name__} :::')
        if result:
            print(f'\t>>> { result.replace('\n', '\n\t>>> ')}')
        print(f'\ttotal={sum_sodom_time_list}; median={median_sodom_time_list}; average={mean_sodom_time_list}')

        return result, (sum_sodom_time_list, median_sodom_time_list, mean_sodom_time_list), case_time_list

    def test_performance_dominate():
        RUNS = 10_000

        sodom_result, (sum_sodom_time_list, median_sodom_time_list, mean_sodom_time_list), _ = _time_list(_sodom_case, RUNS)
        dominate_result, (sum_dominate_time_list, median_dominate_time_list, mean_dominate_time_list), _ = _time_list(_dominate_case, RUNS)

        print()
        ratio_sum = sum_dominate_time_list / sum_sodom_time_list
        ratio_median = median_dominate_time_list / median_sodom_time_list
        ratio_average = mean_dominate_time_list / mean_sodom_time_list
        print(f'\truns: {RUNS}; ratio:: ratio_total={ratio_sum}, ratio_median={ratio_median}, ratio_average={ratio_average}')

        assert sodom_result == dominate_result
