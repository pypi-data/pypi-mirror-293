# sodom
__sodom__ if you prefer ___HTML via Python___.

__sodom__ is a project that utilizes Python's context manager to generate HTML on serverside. It provides a native way to create HTML documents using plaint dependency-free Python.

No more need to use templating engines and limited language subsets ([`jinja`](https://jinja.palletsprojects.com), [`mako`](https://www.makotemplates.org/)), strange syntax of nested arrays ([`lxml.builder.E`](https://lxml.de/tutorial.html#the-e-factory)) or unsupported one ([`pyxl`](https://github.com/pyxl4/pyxl4)). There is [`dominate`](https://github.com/Knio/dominate) and you want to use it? __sodom__ is faster.

## Example
```python
# sodom/example.py
...

import platform

from sodom import *
from sodom.attrs import Attrs


def __example__():
    with html(lang='en') as doc:
        with head():
            with slot(name='HEADER'):
                meta(charset='utf-8')
                meta(
                    name='viewport',
                    content='width=device-width, initial-scale=1, shrink-to-fit=no',
                )
                slot(name='title')
                link(
                    rel='stylesheet',
                    href='https://cdn.jsdelivr.net/npm/bulma@1.0.0/css/bulma.min.css',
                )
        with body():
            with section() < Attrs(class_='section'):
                with div(class_='container'):
                    title('Hello world!!1!')
                    with p(class_='subtitle'):
                        text('My first website with ')
                        with a(href='https://pypi.org/project/sodom/'):
                            strong('sodom')
                        text(' on your '); strong(f'{platform.node()}/{platform.system()}'); text('!')

    doc.render_html_now()
```


## Installation
```bash
python -m pip install git+https://codeberg.org/protasov/sodom
```
or
```bash
python -m pip install sodom
```

## Concepts
### Elements
[`sodom.elements.*`](sodom/elements.py)

__sodom__ provide 3 types of elements:
- `NormanElement` - HTML element that may has `Attrs` and contain nested elements such as another `NormanElement`, `VoidElement` or `text`
    ```python
    from sodom import *
    from sodom.renderers import render_now

    with div() as doc:
        br()
        text('foo')

    render_now(doc)
    ```

- `VoidElement` - HTML element that may has only `Attrs`
    ```python
    from sodom import *
    from sodom.renderers import render_now

    doc = input(type='number')

    render_now(doc)
    ```

- `text` - HTML element appends provided text into children list of `NormalElement`
    ```python
    from sodom import *
    from sodom.renderers import render_now

    text('bar')  # raise exception, `text` should be called in NormalElement context
    # -----
    with div() as doc:
        text('baz')

    render_now(doc)
    ```

### Attributes
[`sodom.attrs.*`](sodom/attrs.py)

sodom has special `Attrs` class to represent HTML attributes. It inherit builtin `dict[str, str]` and provide base tools to merging attributes. Merge means adding attribute values to end of existing ones or create new attribute.

```python
# merge into new `Attrs` instance
Attrs(foo='bar').merge({'foo': 'baz'})
Attrs(foo='bar').merge(Attrs(foo='baz'))
Attrs(foo='bar').merge(dict(foo='baz'))
Attrs(foo='bar') | {'foo': 'baz'}
Attrs(foo='bar') | Attrs(foo='baz')
Attrs(foo='bar') | dict(foo='baz')
# merge into left `Attrs` instance
Attrs(foo='bar').merge_update({'foo': 'baz'})
Attrs(foo='bar').merge_update(Attrs(foo='baz'))
Attrs(foo='bar').merge_update(dict(foo='baz'))
Attrs(foo='bar') |= {'foo': 'baz'}
Attrs(foo='bar') |= Attrs(foo='baz')
Attrs(foo='bar') |= dict(foo='baz')
# result:
Attrs({'foo': 'bar baz'})
```

### Render context
[`sodom.contexts.*`](sodom/contexts.py)

Render context is a list of settings to generate code from Elements.

__sodom__ provide ABCRenderContext as abstract base class and `HTMLRenderContext` as a context to generate HTML code.

```python
from sodom import *
from sodom.contexts import *

doc = div(foo_bar='baz')
doc.render_now(ctx=ctx(underscore_replacer='_'))
```
Result:
```html
<!--instead of default `<div foo-bar="baz"></div>` you'll receive:-->
<div foo_bar="baz"></div>
```

### Renderings

You can render elements and attr after building via:
- (for elements:)
    - `DOMElement.stream` - to stream result of rendering via render context from `ctx=`
        - `VoidElement.stream`
        - `NormalElement.stream`
    - `DOMElement.stream_html` - to stream result of rendering via HTMLRenderContext
        - `VoidElement.stream_html`
        - `NormalElement.stream_html`
    - `DOMElement.render` - to render via render context from `ctx=`
        - `VoidElement.render`
        - `NormalElement.render`
    - `DOMElement.render_html` - to render HTML via HTMLRenderContext
        - `VoidElement.render_html`
        - `NormalElement.render_html`
    - `DOMElement.render_now` - to render HTML into your default browser (/default profile)
        - `VoidElement.render_now`
        - `NormalElement.render_now`
- (for attributes:)
    - `Attrs.stream` - to stream result of rendering via render context from `ctx=`
    - `Attrs.render` (`VoidElement.render`, `NormalElement.render`) - to render via render context from `ctx=`

#### Streaming

__sodom__ also support _streaming_ rendered elements - every element of element tree can be rendered and yielded separately via `DOMElement.stream`. It can be useful if your http server support something like:
- [Starlette: StreamingResponse](https://www.starlette.io/responses/#streamingresponse)
- [Flask: Streaming Contents](https://flask.palletsprojects.com/en/latest/patterns/streaming/)

##### Schemes of streaming:
- `NormalElement`:
    - tag head
    - yield from element's children
    - tag end
- `VoidElement` and `text`
    - whole element

## More features

### Performance:
sodom is faster than `dominate`. Check `sodom.tests.test_performance_dominate` or use `pytest -vv -s -k test_performance sodom/tests.py`

### Processing/Threading/Asyncing:
Actively using `ContextVar`. Tested with `asyncio` and `ThreadPoolExecutor`. Check `sodom.tests.TestContext`

## Feedback
If you have any feedback, text me `inbox@protaz.ru`
