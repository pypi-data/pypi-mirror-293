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

from typing import Literal, TypedDict
import warnings


warnings.warn('importing experimental module')


class WindowEvent(TypedDict, total=False):
    on_afterprstr: str
    on_beforeprstr: str
    on_beforeunload: str
    on_error: str
    on_hashchange: str
    on_load: str
    on_message: str
    on_offline: str
    on_online: str
    on_pagehide: str
    on_pageshow: str
    on_popstate: str
    on_resize: str
    on_storage: str
    on_unhandledrejection: str
    on_unload: str


class FormEvent(TypedDict, total=False):
    on_blur: str
    on_change: str
    on_contextmenu: str
    on_focus: str
    on_input: str
    on_invalid: str
    on_reset: str
    on_search: str
    on_select: str
    on_submit: str


class KeyboardEvent(TypedDict, total=False):
    on_keydown: str
    on_keypress: str
    on_keyup: str


class MouseEvent(TypedDict, total=False):
    on_click: str
    on_dblclick: str
    on_mousedown: str
    on_mousemove: str
    on_mouseout: str
    on_mouseover: str
    on_mouseup: str
    on_wheel: str


class DragEvent(TypedDict, total=False):
    on_drag: str
    on_dragend: str
    on_dragenter: str
    on_dragleave: str
    on_dragover: str
    on_dragstart: str
    on_drop: str


class ClipboardEvent(TypedDict, total=False):
    on_copy: str
    on_cut: str
    on_paste: str


class Event(
    WindowEvent,
    FormEvent,
    KeyboardEvent,
    MouseEvent,
    DragEvent,
    ClipboardEvent,
    total=False,
):
    """Event Attributes for HTML elements."""


class Global(
    Event,
    total=False,
):
    id: str
    accesskey: str
    class_: str
    contenteditable: Literal["true", "false"]
    dir: Literal["ltr", "rtl", "auto"]
    draggable: Literal["true", "false"]
    enterkeyhstr: Literal["enter", "done", "go", "next", "previous", "search", "send"]
    hidden: Literal["true", "false"]
    inert: Literal[""]
    inputmode: Literal["none", "text", "search", "tel", "url", "email", "numeric", "decimal"]
    lang: str
    popover: Literal[""]
    spellcheck: Literal["true", "false"]
    style: str
    tabindex: str
    title: str
    translate: Literal["yes", "no"]


##### NORMAL #####
class A(Global, total=False):
    download: str
    href: str
    hreflang: str
    media: str
    ping: str
    referrerpolicy: Literal[
        "no-referrer",
        "no-referrer-when-downgrade",
        "origin",
        "origin-when-cross-origin",
        "same-origin",
        "strict-origin",
        "strict-origin-when-cross-origin",
        "unsafe-url",
    ]
    rel: Literal[
        "alternate",
        "author",
        "bookmark",
        "external",
        "help",
        "license",
        "next",
        "nofollow",
        "noreferrer",
        "noopener",
        "prev",
        "search",
        "tag",
    ]
    target: str
    type: str


class AUDIO(Global, total=False):
    src: str
    preload: Literal["auto", "metadata", "none"]
    autoplay: Literal[""]
    controls: Literal[""]
    loop: Literal[""]
    muted: Literal[""]
    mediagroup: str


class BLOCKQUOTE(Global, total=False):
    cite: str


class BUTTON(Global, total=False):
    autofocus: Literal[""]
    disabled: Literal[""]
    form: str
    formaction: str
    formenctype: Literal[
        "application/x-www-form-urlencoded",
        "multipart/form-data",
        "text/plain",
    ]
    formmethod: Literal["get", "post"]
    formnovalidate: Literal[""]
    formtarget: str
    popovertarget: str
    popovertargetaction: Literal["show", "hide", "toggle"]
    name: str
    type: Literal["submit", "reset", "button"]
    value: str


class CANVAS(Global, total=False):
    width: str
    height: str


class DATA(Global, total=False):
    value: str


class DEL(Global, total=False):
    cite: str
    datetime: str


class DETAILS(Global, total=False):
    open: Literal[""]


class DIALOG(Global, total=False):
    open: Literal[""]


class FIELDSET(Global, total=False):
    disabled: Literal[""]
    form: str
    name: str


class FORM(Global, total=False):
    accept_charset: str
    action: str
    autocomplete: Literal["on", "off"]
    enctype: Literal[
        "application/x-www-form-urlencoded",
        "multipart/form-data",
        "text/plain",
    ]
    method: Literal["get", "post"]
    name: str
    novalidate: Literal[""]
    rel: Literal[
        "external",
        "help",
        "license",
        "next",
        "nofollow",
        "noopener",
        "noreferrer",
        "opener",
        "prev",
        "search",
    ]
    target: str


class HTML(Global, total=False):
    xmlns: str


class IFRAME(Global, total=False):
    allow: str
    allowfullscreen: Literal[""]
    allowpaymentrequest: Literal[""]
    height: str
    frameborder: str
    loading: Literal["eager", "lazy"]
    name: str
    referrerpolicy: Literal[
        "no-referrer",
        "no-referrer-when-downgrade",
        "origin",
        "origin-when-cross-origin",
        "same-origin",
        "strict-origin-when-cross-origin",
        "unsafe-url",
    ]
    sandbox: Literal[
        "allow-forms",
        "allow-postrer-lock",
        "allow-popups",
        "allow-same-origin",
        "allow-scripts",
        "allow-top-navigation",
    ]
    src: str
    srcdoc: str
    scrolling: str
    width: str


class INS(Global, total=False):
    cite: str
    datetime: str


class LABEL(Global, total=False):
    for_: str
    name: str


class LI(Global, total=False):
    value: str


class MAP(Global, total=False):
    name: str


class METER(Global, total=False):
    form: str
    high: str
    low: str
    max: str
    min: str
    optimum: str
    value: str


class OL(Global, total=False):
    reversed: Literal[""]
    start: str
    type: Literal["1", "a", "A", "i", "I"]


class OPTGROUP(Global, total=False):
    disabled: Literal[""]
    label: str


class OPTION(Global, total=False):
    disabled: Literal[""]
    label: str
    selected: Literal[""]
    value: str


class OUTPUT(Global, total=False):
    for_: str
    form: str
    name: str


class PROGRESS(Global, total=False):
    max: str
    value: str


class Q(Global, total=False):
    cite: str


class SCRIPT(Global, total=False):
    async_: Literal[""]
    crossorigin: Literal["anonymous", "use-credentials"]
    defer: Literal[""]
    stregrity: str
    nomodule: Literal[""]
    referrerpolicy: Literal[
        "no-referrer",
        "no-referrer-when-downgrade",
        "origin",
        "origin-when-cross-origin",
        "same-origin",
        "strict-origin",
        "strict-origin-when-cross-origin",
        "unsafe-url",
    ]
    src: str
    type: str


class SELECT(Global, total=False):
    autofocus: Literal[""]
    disabled: Literal[""]
    form: str
    multiple: Literal[""]
    name: str
    required: Literal[""]
    size: str


class STYLE(Global, total=False):
    media: str
    type: Literal["text/css"]


class TD(Global, total=False):
    colspan: str
    headers: str
    rowspan: str


class TEXTAREA(Global, total=False):
    autofocus: Literal[""]
    cols: str
    dirname: str
    disabled: Literal[""]
    form: str
    maxlength: str
    name: str
    placeholder: str
    readonly: Literal[""]
    required: Literal[""]
    rows: str
    wrap: Literal["hard", "soft"]


class TH(Global, total=False):
    abbr: str
    colspan: str
    headers: str
    rowspan: str
    scope: Literal["col", "colgroup", "row", "rowgroup"]


class TIME(Global, total=False):
    datetime: str


class VIDEO(Global, total=False):
    autoplay: Literal[""]
    controls: Literal[""]
    height: str
    loop: Literal[""]
    muted: Literal[""]
    poster: str
    preload: Literal["auto", "metadata", "none"]
    src: str
    width: str


##### VOID #####
class AREA(Global, total=False):
    alt: str
    coords: str
    download: str
    href: str
    ping: str
    referrerpolicy: Literal[
        "no-referrer",
        "no-referrer-when-downgrade",
        "origin",
        "origin-when-cross-origin",
        "same-origin",
        "strict-origin",
        "strict-origin-when-cross-origin",
        "unsafe-url",
    ]
    rel: str
    shape: Literal["rect", "circle", "poly", "default"]
    target: str


class BASE(Global, total=False):
    href: str
    target: str


class COL(Global, total=False):
    span: str


class EMBED(Global, total=False):
    height: str
    src: str
    type: str
    width: str


class IMG(Global, total=False):
    alt: str
    crossorigin: Literal["anonymous", "use-credentials"]
    height: str
    ismap: Literal[""]
    loading: Literal["eager", "lazy"]
    longdesc: str
    referrerpolicy: Literal[
        "no-referrer",
        "no-referrer-when-downgrade",
        "origin",
        "origin-when-cross-origin",
        "unsafe-url",
    ]
    sizes: str
    src: str
    srcset: str
    usemap: str
    width: str


class INPUT(Global, total=False):
    accept: str
    alt: str
    autcomplete: Literal["on", "off"]
    autofocus: Literal[""]
    checked: Literal[""]
    dirname: str
    disabled: Literal[""]
    form: str
    formaction: str
    formenctype: Literal[
        "application/x-www-form-urlencoded",
        "multipart/form-data",
        "text/plain",
    ]
    formmethod: Literal["get", "post"]
    formnovalidate: Literal[""]
    formtarget: str
    height: str
    list: str
    max: str
    maxlength: str
    min: str
    minlength: str
    multiple: Literal[""]
    name: str
    pattern: str
    placeholder: str
    popovertarget: str
    popovertargetaction: Literal["show", "hide", "toggle"]
    readonly: Literal[""]
    required: Literal[""]
    size: str
    src: str
    step: str
    type: Literal[
        "checkbox",
        "button",
        "color",
        "date",
        "datetime-local",
        "email",
        "file",
        "hidden",
        "image",
        "month",
        "number",
        "password",
        "radio",
        "range",
        "reset",
        "search",
        "submit",
        "tel",
        "text",
        "time",
        "url",
        "week",
    ]
    value: str
    width: str


class LINK(Global, total=False):
    type: str
    rel: Literal[
        "canonical",
        "alternate",
        "stylesheet",
        "icon",
        "apple-touch-icon",
        "preconnect",
    ]
    crossorigin: Literal[
        "anonymous",
        "use-credentials",
        "",
    ]
    hreflang: str
    href: str
    stregrity: str


class META(Global, total=False):
    name: str
    content: str
    charset: str
    property: str


class PARAM(Global, total=False):
    name: str
    value: str


class SOURCE(Global, total=False):
    media: str
    sizes: str
    src: str
    srcset: str
    type: str


class TRACK(Global, total=False):
    default: Literal[""]
    kind: Literal["subtitles", "captions", "descriptions", "chapters", "metadata"]
    label: str
    src: str
    srclang: str
