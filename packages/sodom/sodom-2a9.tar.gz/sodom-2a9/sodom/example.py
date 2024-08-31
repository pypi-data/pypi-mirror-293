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
