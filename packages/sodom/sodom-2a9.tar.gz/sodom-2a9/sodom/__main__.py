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


from operator import itemgetter

from sodom.contexts import PYCTX


if __name__ == '__main__':
    import warnings

    try:
        from lxml import etree as ETree
        from xml.etree.ElementTree import Element, ElementTree
        from typer import Typer
        from loguru import logger
    except ImportError as e:
        warnings.warn('Please install modules required for cli usage `python -m pip install sodom[cli]`')
        raise e
    else:
        from typing import cast
        from pathlib import Path
        from typing import cast

        from sodom import *
        from sodom.elements import NormalElement, VoidElement, ABCElement
        from sodom.guardians import is_normal_element
        from sodom.literals import NORMAL_TAG_STRS, VOID_TAG_STRS, NORMAL_TAGS, VOID_TAGS
        from sodom.contexts import pyctx

        cli = Typer()


        def _build_sodom_document(tree: ElementTree, include_empty_rows: bool) -> NormalElement:

            def build_sodom_element(parent: NormalElement | None, xml_elem: Element) -> ABCElement:
                html_tag = xml_elem.tag
                html_attrs = xml_elem.attrib
                text = (xml_elem.text or '').split('\n')
                text = (
                    t.strip()
                    for t in text
                )
                text = (
                    t
                    for t in text
                    if bool(t) or include_empty_rows
                )

                if html_tag in NORMAL_TAG_STRS:
                    sodom_elem = NormalElement(cast(NORMAL_TAGS, html_tag), *text, **html_attrs)
                elif html_tag in VOID_TAG_STRS:
                    sodom_elem = VoidElement(cast(VOID_TAGS, html_tag), **html_attrs)
                else:
                    raise RuntimeError(f'Unknown tag: {html_tag}')

                if parent is not None:
                    parent.add(sodom_elem)

                for xml_child in xml_elem:
                    build_sodom_element(sodom_elem, xml_child)

                return sodom_elem

            xml_root = tree.getroot()
            sodom_root = build_sodom_element(None, xml_root)

            return sodom_root


        @cli.command(
            help='test',
            short_help='Generate python code via HTML (.html) file.',
        )
        def generator(source: Path, target: Path, dialect: str = 'sodom', include_empty_rows: bool = False):
            logger.info('Parsing source: {}', source)
            tree: ElementTree = ETree.parse(
                source,
                ETree.HTMLParser(
                    remove_comments=True,
                    remove_blank_text=True,
                    collect_ids=False,
                ),
            )

            if dialect == 'sodom':
                logger.info('Building python structure via {}...', 'sodom')
                document = _build_sodom_document(tree, include_empty_rows)
                logger.info('Generating python code via {}...', 'sodom')
                code = document.render(ctx=PYCTX)
            else:
                raise ValueError(f'dialect must be {['sodom']}')

            logger.info('Writing {} target: {}', document, target)
            with open(target, 'w+') as f:
                f.write(code)
            for row in code.split('\n'):
                logger.info(row)
            logger.info('Done!')

        cli()
