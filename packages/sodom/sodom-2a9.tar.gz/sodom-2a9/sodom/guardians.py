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

from typing import Any, TypeGuard

from sodom.elements import NormalElement, TextWrapper, VoidElement
from sodom.literals import NORMAL_TAGS, VOID_TAGS
from sodom.missing import MISSING


def is_normal_element[TAG: NORMAL_TAGS](
    element: Any,
    /, *,
    tag: TAG = MISSING,
) -> TypeGuard[NormalElement[TAG]]:
    return (
        isinstance(element, NormalElement)
        and (
            tag is MISSING
            or element.tag == tag
        )
    )


def is_void_element[TAG: VOID_TAGS](
    element: Any,
    /, *,
    tag: TAG = MISSING,
) -> TypeGuard[VoidElement[TAG]]:
    return (
        isinstance(element, VoidElement)
        and (
            tag is MISSING
            or element.tag == tag
        )
    )


def is_text_element(
    element: Any,
    /,
) -> TypeGuard[TextWrapper]:
    return isinstance(element, TextWrapper)
