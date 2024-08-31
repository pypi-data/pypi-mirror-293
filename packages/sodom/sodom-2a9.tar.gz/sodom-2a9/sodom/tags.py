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

from functools import partial

from sodom import literals
from sodom.elements import NormalElement, VoidElement

__all__ = [
    'a',
    'abbr',
    'acronym',
    'address',
    'article',
    'aside',
    'audio',
    'b',
    'bdi',
    'bdo',
    'big',
    'blockquote',
    'body',
    'button',
    'canvas',
    'caption',
    'center',
    'cite',
    'code',
    'colgroup',
    'data',
    'datalist',
    'dd',
    'del_',
    'details',
    'dfn',
    'dialog',
    'dir_',
    'div',
    'dl',
    'dt',
    'em',
    'fieldset',
    'figcaption',
    'figure',
    'font',
    'footer',
    'form',
    'frame',
    'frameset',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'head',
    'header',
    'hgroup',
    'html',
    'i',
    'iframe',
    'image',
    'ins',
    'kbd',
    'label',
    'legend',
    'li',
    'main',
    'map_',
    'mark',
    'marquee',
    'menu',
    'menuitem',
    'meter',
    'nav',
    'nobr',
    'noembed',
    'noframes',
    'noscript',
    'object_',
    'ol',
    'optgroup',
    'option',
    'output',
    'p',
    'picture',
    'plaintext',
    'portal',
    'pre',
    'progress',
    'q',
    'rb',
    'rp',
    'rt',
    'rtc',
    'ruby',
    's',
    'samp',
    'script',
    'search',
    'section',
    'select',
    'slot',
    'small',
    'span',
    'strike',
    'strong',
    'style',
    'sub',
    'summary',
    'sup',
    'table',
    'tbody',
    'td',
    'template',
    'textarea',
    'tfoot',
    'th',
    'thead',
    'time',
    'title',
    'tr',
    'tt',
    'u',
    'ul',
    'var',
    'video',
    'xmp',

    'area',
    'base',
    'br',
    'col',
    'embed',
    'hr',
    'img',
    'input_',
    'link',
    'meta',
    'param',
    'source',
    'track',
    'wbr',

    'input_datetime_local',
    'input_button',
    'input_checkbox',
    'input_color',
    'input_date',
    'input_email',
    'input_file',
    'input_hidden',
    'input_image',
    'input_month',
    'input_number',
    'input_password',
    'input_radio',
    'input_range',
    'input_reset',
    'input_search',
    'input_submit',
    'input_tel',
    'input_text',
    'input_time',
    'input_url',
    'input_week',
]


##### NORMAL #####
a = partial(NormalElement[literals.A], 'a')
abbr = partial(NormalElement[literals.ABBR], 'abbr')
acronym = partial(NormalElement[literals.ACRONYM], 'acronym')
address = partial(NormalElement[literals.ADDRESS], 'address')
article = partial(NormalElement[literals.ARTICLE], 'article')
aside = partial(NormalElement[literals.ASIDE], 'aside')
audio = partial(NormalElement[literals.AUDIO], 'audio')
b = partial(NormalElement[literals.B], 'b')
bdi = partial(NormalElement[literals.BDI], 'bdi')
bdo = partial(NormalElement[literals.BDO], 'bdo')
big = partial(NormalElement[literals.BIG], 'big')
blockquote = partial(NormalElement[literals.BLOCKQUOTE], 'blockquote')
body = partial(NormalElement[literals.BODY], 'body')
button = partial(NormalElement[literals.BUTTON], 'button')
canvas = partial(NormalElement[literals.CANVAS], 'canvas')
caption = partial(NormalElement[literals.CAPTION], 'caption')
center = partial(NormalElement[literals.CENTER], 'center')
cite = partial(NormalElement[literals.CITE], 'cite')
code = partial(NormalElement[literals.CODE], 'code')
colgroup = partial(NormalElement[literals.COLGROUP], 'colgroup')
data = partial(NormalElement[literals.DATA], 'data')
datalist = partial(NormalElement[literals.DATALIST], 'datalist')
dd = partial(NormalElement[literals.DD], 'dd')
del_ = partial(NormalElement[literals.DEL], 'del')
details = partial(NormalElement[literals.DETAILS], 'details')
dfn = partial(NormalElement[literals.DFN], 'dfn')
dialog = partial(NormalElement[literals.DIALOG], 'dialog')
dir_ = partial(NormalElement[literals.DIR], 'dir')
div = partial(NormalElement[literals.DIV], 'div')
dl = partial(NormalElement[literals.DL], 'dl')
dt = partial(NormalElement[literals.DT], 'dt')
em = partial(NormalElement[literals.EM], 'em')
fieldset = partial(NormalElement[literals.FIELDSET], 'fieldset')
figcaption = partial(NormalElement[literals.FIGCAPTION], 'figcaption')
figure = partial(NormalElement[literals.FIGURE], 'figure')
font = partial(NormalElement[literals.FONT], 'font')
footer = partial(NormalElement[literals.FOOTER], 'footer')
form = partial(NormalElement[literals.FORM], 'form')
frame = partial(NormalElement[literals.FRAME], 'frame')
frameset = partial(NormalElement[literals.FRAMESET], 'frameset')
h1 = partial(NormalElement[literals.H1], 'h1')
h2 = partial(NormalElement[literals.H2], 'h2')
h3 = partial(NormalElement[literals.H3], 'h3')
h4 = partial(NormalElement[literals.H4], 'h4')
h5 = partial(NormalElement[literals.H5], 'h5')
h6 = partial(NormalElement[literals.H6], 'h6')
head = partial(NormalElement[literals.HEAD], 'head')
header = partial(NormalElement[literals.HEADER], 'header')
hgroup = partial(NormalElement[literals.HGROUP], 'hgroup')
html = partial(NormalElement[literals.HTML], 'html')
i = partial(NormalElement[literals.I], 'i')
iframe = partial(NormalElement[literals.IFRAME], 'iframe')
image = partial(NormalElement[literals.IMAGE], 'image')
ins = partial(NormalElement[literals.INS], 'ins')
kbd = partial(NormalElement[literals.KBD], 'kbd')
label = partial(NormalElement[literals.LABEL], 'label')
legend = partial(NormalElement[literals.LEGEND], 'legend')
li = partial(NormalElement[literals.LI], 'li')
main = partial(NormalElement[literals.MAIN], 'main')
map_ = partial(NormalElement[literals.MAP], 'map')
mark = partial(NormalElement[literals.MARK], 'mark')
marquee = partial(NormalElement[literals.MARQUEE], 'marquee')
menu = partial(NormalElement[literals.MENU], 'menu')
menuitem = partial(NormalElement[literals.MENUITEM], 'menuitem')
meter = partial(NormalElement[literals.METER], 'meter')
nav = partial(NormalElement[literals.NAV], 'nav')
nobr = partial(NormalElement[literals.NOBR], 'nobr')
noembed = partial(NormalElement[literals.NOEMBED], 'noembed')
noframes = partial(NormalElement[literals.NOFRAMES], 'noframes')
noscript = partial(NormalElement[literals.NOSCRIPT], 'noscript')
object_ = partial(NormalElement[literals.OBJECT], 'object')
ol = partial(NormalElement[literals.OL], 'ol')
optgroup = partial(NormalElement[literals.OPTGROUP], 'optgroup')
option = partial(NormalElement[literals.OPTION], 'option')
output = partial(NormalElement[literals.OUTPUT], 'output')
p = partial(NormalElement[literals.P], 'p')
picture = partial(NormalElement[literals.PICTURE], 'picture')
plaintext = partial(NormalElement[literals.PLAINTEXT], 'plaintext')
portal = partial(NormalElement[literals.PORTAL], 'portal')
pre = partial(NormalElement[literals.PRE], 'pre')
progress = partial(NormalElement[literals.PROGRESS], 'progress')
q = partial(NormalElement[literals.Q], 'q')
rb = partial(NormalElement[literals.RB], 'rb')
rp = partial(NormalElement[literals.RP], 'rp')
rt = partial(NormalElement[literals.RT], 'rt')
rtc = partial(NormalElement[literals.RTC], 'rtc')
ruby = partial(NormalElement[literals.RUBY], 'ruby')
s = partial(NormalElement[literals.S], 's')
samp = partial(NormalElement[literals.SAMP], 'samp')
script = partial(NormalElement[literals.SCRIPT], 'script')
search = partial(NormalElement[literals.SEARCH], 'search')
section = partial(NormalElement[literals.SECTION], 'section')
select = partial(NormalElement[literals.SELECT], 'select')
slot = partial(NormalElement[literals.SLOT], 'slot')
small = partial(NormalElement[literals.SMALL], 'small')
span = partial(NormalElement[literals.SPAN], 'span')
strike = partial(NormalElement[literals.STRIKE], 'strike')
strong = partial(NormalElement[literals.STRONG], 'strong')
style = partial(NormalElement[literals.STYLE], 'style')
sub = partial(NormalElement[literals.SUB], 'sub')
summary = partial(NormalElement[literals.SUMMARY], 'summary')
sup = partial(NormalElement[literals.SUP], 'sup')
table = partial(NormalElement[literals.TABLE], 'table')
tbody = partial(NormalElement[literals.TBODY], 'tbody')
td = partial(NormalElement[literals.TD], 'td')
template = partial(NormalElement[literals.TEMPLATE], 'template')
textarea = partial(NormalElement[literals.TEXTAREA], 'textarea')
tfoot = partial(NormalElement[literals.TFOOT], 'tfoot')
th = partial(NormalElement[literals.TH], 'th')
thead = partial(NormalElement[literals.THEAD], 'thead')
time = partial(NormalElement[literals.TIME], 'time')
title = partial(NormalElement[literals.TITLE], 'title')
tr = partial(NormalElement[literals.TR], 'tr')
tt = partial(NormalElement[literals.TT], 'tt')
u = partial(NormalElement[literals.U], 'u')
ul = partial(NormalElement[literals.UL], 'ul')
var = partial(NormalElement[literals.VAR], 'var')
video = partial(NormalElement[literals.VIDEO], 'video')
xmp = partial(NormalElement[literals.XMP], 'xmp')


##### VOID #####
area = partial(VoidElement[literals.AREA], 'area')
base = partial(VoidElement[literals.BASE], 'base')
br = partial(VoidElement[literals.BR], 'br')
col = partial(VoidElement[literals.COL], 'col')
embed = partial(VoidElement[literals.EMBED], 'embed')
hr = partial(VoidElement[literals.HR], 'hr')
img = partial(VoidElement[literals.IMG], 'img')
input_ = partial(VoidElement[literals.INPUT], 'input')
link = partial(VoidElement[literals.LINK], 'link')
meta = partial(VoidElement[literals.META], 'meta')
param = partial(VoidElement[literals.PARAM], 'param')
source = partial(VoidElement[literals.SOURCE], 'source')
track = partial(VoidElement[literals.TRACK], 'track')
wbr = partial(VoidElement[literals.WBR], 'wbr')


##### INPUT #####
input_datetime_local = partial(input_, type='datetime-local')
input_button = partial(input_, type='button')
input_checkbox = partial(input_, type='checkbox')
input_color = partial(input_, type='color')
input_date = partial(input_, type='date')
input_email = partial(input_, type='email')
input_file = partial(input_, type='file')
input_hidden = partial(input_, type='hidden')
input_image = partial(input_, type='image')
input_month = partial(input_, type='month')
input_number = partial(input_, type='number')
input_password = partial(input_, type='password')
input_radio = partial(input_, type='radio')
input_range = partial(input_, type='range')
input_reset = partial(input_, type='reset')
input_search = partial(input_, type='search')
input_submit = partial(input_, type='submit')
input_tel = partial(input_, type='tel')
input_text = partial(input_, type='text')
input_time = partial(input_, type='time')
input_url = partial(input_, type='url')
input_week = partial(input_, type='week')
