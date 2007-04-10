#!/usr/bin/python
# -* coding: utf-8 -*-

import urwid
import urwid.raw_display
import sys

Screen = urwid.raw_display.Screen

GFX = u"×∙◀─▶←→↑↓↔↕█▌¯«»▲▼"
GFX2 = u"─│┌┐└┘├┤┬┴┼"

ASCII_TRANS = {
        u'∙':'*',
        u'◀':'<',
        u'─':'-',
        u'▶':'>',
        u'←':'<',
        u'→':'>',
        u'↑':'^',
        u'↓':'v',
        u'█':'[',
        u'▌':']',
        u'¯':' ',
        u'«':'<',
        u'»':'>',
        u'▲':'^',
        u'▼':'v',
        u'─':'-',
        u'│':'|',
        u'┌':'+',
        u'┐':'+',
        u'└':'+',
        u'┘':'+',
        u'├':'+',
        u'┤':'+',
        u'┬':'+',
        u'┴':'+',
        u'┼':'+',
        }

if len(sys.argv)>1 and sys.argv[1].startswith('a'):
        trans_table = {}
        for k, v in ASCII_TRANS.items():
                trans_table[ord(k)] = unicode(v)
        def ascii_trans(x):
                return x.translate(trans_table)
        T = ascii_trans
else:
        def nothing(x):
                return x
        T = nothing


class Blob(urwid.WidgetWrap):
        def __init__(self, dw, attr, flow=True, thin=False):
                dw = urwid.Padding( dw, ('fixed left', 2), ('fixed right', 2))
                if flow:
                        dw = urwid.Pile([urwid.Divider(), dw, urwid.Divider()])
                else:
                        dw = urwid.Filler( dw, 'middle' )
                dw = urwid.AttrWrap( dw, attr )
                dw = urwid.Padding( dw, ('fixed left', 2), ('fixed right', 2))
                if flow and not thin:
                        dw = urwid.Pile([urwid.Divider(), dw, urwid.Divider()])
                elif not thin:
                        dw = urwid.Filler( dw, ('fixed top', 0),
                                ('fixed bottom', 1))
                urwid.WidgetWrap.__init__(self, dw)

class BulletList(urwid.WidgetWrap):
        def __init__(self, items):
                l = []
                bullet = urwid.Text(T(u"∙"))
                for i in items:
                        if l: l.append( urwid.Divider() )
                        c = urwid.Columns([('fixed', 2, bullet),
                                urwid.Text( i )])
                        l.append( c )
                dw = urwid.Pile( l )
                dw = urwid.Padding( dw, ('fixed left', 2), ('fixed right', 2))
                urwid.WidgetWrap.__init__(self, dw)

class LayoutExample(urwid.WidgetWrap):
        def __init__(self, align, wrap):
                dw = urwid.Text("some interesting text", align, wrap)
                dw = urwid.AttrWrap(dw, 'raw')
                dw = urwid.Padding(dw, 'center', 12)
                urwid.WidgetWrap.__init__(self, dw)

class FakeEdit(urwid.WidgetWrap):
        def __init__(self, cap):
                dw = urwid.Edit( cap )
                urwid.WidgetWrap.__init__(self,dw)

        def keypress(self, size, key):
                return key
W3M_EXAMPLE = urwid.Padding(
        urwid.Pile([
                urwid.Text("w3m excess.org"),
                urwid.Divider("¯"),
                urwid.AttrWrap(
                        urwid.Text([
                                ('w3m icon',"excess.org"), "\n",
                                "\n",
                                "Ian Ward\n",
                                "email: first name @ my domain apt\n",
                                "archive: deb http://excess.org\n",
                                "unstable main\n",
                                "\n",
                                "Software\n",
                                ('w3m icon',"Speedometer"),
                                ('w3m link',"    info code .py"),
                                " GNU LGPL\n",
                                "                     deb: speedometer\n",
                                "Console utility to monitor network\n",
                                ('w3m bar', T(u"« ↑ ↓ Viewing <excess.org>")),
                                ], wrap='clip'),
                        'w3m normal' ),
                ]),
        'left', 38 )

DPKG_EXAMPLE = urwid.Padding(
        urwid.Pile([
                urwid.Text("dpkg-reconfigure locales"),
                urwid.Divider("¯"),
                urwid.Text([
('dpkg bl'," "),T(u"│\n"),
('dpkg bl'," "),T(u"│ Select locales to be generated.\n"),
('dpkg bl'," "),T(u"│\n"),
('dpkg bl'," "),T(u"│    "),('dpkg bl',u"[█] aa_DJ ISO-8859-1           \n"),
('dpkg bl'," "),T(u"│    "),('dpkg bl',"[ ] aa_ER UTF-8                \n"),
('dpkg bl'," "),T(u"│    "),('dpkg bl',"[ ] aa_ER@saaho UTF-8          \n"),
('dpkg bl'," "),T(u"│    "),('dpkg bl',"[ ] aa_ET UTF-8                \n"),
('dpkg bl'," "),T(u"│\n"),
('dpkg bl'," "),T(u"│\n"),
('dpkg bl'," "),T(u"│                    <Ok>\n"),
('dpkg bl'," "),T(u"│\n"),
('dpkg bl'," "),T(u"└───────────────────────────────────\n"),
('dpkg bl',"  "),('dpkg sh',"                                   \n"),
('dpkg bl',"                                     \n"),
                        ], wrap='clip'),
                ]),
        'left', 38 )


ANATOMY_EXAMPLE = urwid.Pile( [
        urwid.Columns( [
                ( 'fixed', 10, FakeEdit("\n\n\n") ),
                urwid.Text(T(
                        u"┌┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┬┐\n"
                        u"├┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┤ →\n"
                        u"├┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┤\n"
                        u"├┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┤\n"
                        u"├┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┤ →\n"
                        u"├┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┤\n"
                        u"├┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┤\n"
                        u"├┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┼┤\n"
                        u"└┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┴┘\n"
                        u"   ↓      ↓"),
                        align='left',wrap='clip'),
                ], focus_column = 0 ),
        urwid.Text("\n\nF1, SHIFT+TAB, HOME, PAGE UP, ..."),
        ], focus_item = 0)

RADIO_GROUP = []

LISTBOX_EXAMPLE = urwid.ListBox([
        urwid.Text("Urwid is a console user interface library.\n\n"
                "It includes many features useful for text "
                "console application developers including:\n"),
        BulletList([
                "Fluid interface resizing",
                "Web application display mode using Apache and CGI",
                "Support for UTF-8, simple 8-bit and CJK encodings",
                "Multiple text alignment and wrapping modes built-in",
                "Ability create user-defined text layout classes",
                "Simple markup for setting text attributes",
                "Powerful list box that handles scrolling "
                "between different widget types",
                "List box contents may be managed with a "
                "user-defined class",
                "Flexible edit box for editing many different "
                "types of text",
                "Buttons, check boxes and radio boxes",
                "Customizable layout for all widgets",
                "Easy interface for creating HTML screen shots",
                ]),
        urwid.AttrWrap(urwid.Edit(('raw',"Edit box:"),""), None, 'raw2'),
        urwid.AttrWrap(urwid.Button('Button', lambda x:None), None, 'raw2'),
        urwid.AttrWrap(urwid.CheckBox('CheckBox'), None, 'raw2'),
        urwid.AttrWrap(urwid.RadioButton(RADIO_GROUP, 'RadioButton1'),
                None, 'raw2'),
        urwid.AttrWrap(urwid.RadioButton(RADIO_GROUP, 'RadioButton2'),
                None, 'raw2'),
        ])

PAGE = [
        urwid.Pile( [
                urwid.Text(('program',"\nConsole User Interfaces "
                                "and Urwid\n"),
                        align='center'),
                Blob(
                        urwid.Text("Ian Ward\n\n"
                                "Ottawa Canada Linux User's Group\n\n"
                                "April 4, 2006", align='center'),
                        'bigtitle' ),
                ] ),
        urwid.Pile( [
                urwid.Text(('program',"\nTalk Outline\n\n"),
                        align='center'),
                BulletList( [
                        "Console User Interfaces",
                        "examples, weaknesses & strengths",
                        "Ncurses library",
                        "Urwid library - four really cool features",
                        ]),
                ] ),
        urwid.Pile( [
                urwid.Text(('program',"\nConsole User Interfaces\n\n"),
                        align='center'),
                BulletList( [
                        "Where do they fit?",
                        ]),
                urwid.Divider(),
                urwid.Columns([
                        Blob( urwid.Text("Command Line Interfaces (CLI)"),
                                'cli'),
                        Blob( urwid.Text("Console User Interfaces"),
                                'cui'),
                        Blob( urwid.Text("Graphical User Interfaces (GUI)"),
                                'gui'),
                        ]),
                ] ),
        urwid.Pile( [
                urwid.Text(('program',"\nWhen to use a Console User "
                                "Interfaces\n\n"),
                        align='center'),
                BulletList( [
                        "no X libraries for GUI, eg. on a secure server",
                        "slow connection to host",
                        "need character-by-character interaction "
                        "with a program",
                        ]),
                ] ),
        urwid.Pile( [
                urwid.Text(('program',"\nExamples of Console User "
                                "Interfaces\n\n"),
                        align='center'),
                urwid.Columns( [
                        BulletList( [
                                "configuration programs: modconf, "
                                        "dpkg-reconfigure",
                                "text editors: vim, vi",
                                "web browsers: w3m, lynx, links",
                                "file viewers: less, more",
                                "email clients: mutt, pine",
                                "file managers: mc",
                                "games: nethack"
                                ]),
                        W3M_EXAMPLE,
                        ] ),
                ] ),
        urwid.Pile( [
                urwid.Text(('program',"\nAnatomy of Console User "
                                "Interface\n"),
                        align='center'),
                urwid.Columns( [
                        urwid.Pile( [
                                urwid.Divider(),
                                BulletList( [
                                        "resizable grid of charater cells",
                                        "cursor",
                                        "very limited colours",
                                        "mouse, sometimes",
                                        "widely varying support for "
                                                "special keys",
                                        ] ),
                                ] ),
                        ANATOMY_EXAMPLE,
                        ], focus_column = 1 ),
                ], focus_item = 1 ),

        urwid.Pile( [
                urwid.Text(('program',"\nThe Bright Side\n\n"),
                        align='center'),
                urwid.Columns( [
                        BulletList( [
                                "widely available, all platforms",
                                "small set of standards cover majority of "
                                        "terminals",
                                "applications may be very efficient",
                                "good internationalization support",
                                "few dependencies",
                                ] ),
                        ] ),
                ]),

        urwid.Pile( [
                urwid.Columns( [
                        urwid.Pile( [
                                urwid.Text(('program',"\nGood\nConsole User "
                                        "Interfaces"), align='center'),
                                urwid.Divider(),
                                BulletList( [
                                        "should make good use of limited "
                                                "screen space",
                                        "should handle window resizing "
                                                "smoothly",
                                        ] ),
                                ] ),

                        urwid.Pile( [
                                urwid.Text(('program',"\nNot Good\nConsole "
                                        "User Interfaces"), align='center'),
                                urwid.Divider(),
                                DPKG_EXAMPLE,
                                ] ),
                        ] ),
                ]),

        urwid.Pile( [
                urwid.Text(('program',"\nNcurses Library\n\n"),
                        align='center'),
                BulletList( [
                        "fast",
                        "mature",
                        "widely available",
                        "provides scrolling regions",
                        "internationalization support",
                        ]),
                ] ),

        urwid.Pile( [
                urwid.Text(('program',"\nUrwid\n\n"),
                        align='center'),
                BulletList( [
                        "pure Python library",
                        "handles text wrapping and alignment",
                        "allows complex interface layouts",
                        "provides text entry, focus changing and scrolling",
                        "has a wide range of built-in widgets",
                        "has multiple display modules",
                        "featured on lwn.net Developer section in February/06",
                        ]),
                ] ),

        urwid.Pile( [
                urwid.Text(('program',"\nUrwid Components Covered\n"),
                        align='center'),
                urwid.Columns([
                        urwid.Pile([
                                Blob(
                                        urwid.Text("Widgets",
                                                align='center'),
                                        'widget' ),
                                Blob(
                                        urwid.Text("Text Widgets\n"
                                                "& Text Layouts",
                                                align='center'),
                                        'widget' ),
                                Blob(
                                        urwid.Text("ListBox Widgets\n"
                                                "& List Walkers",
                                                align='center'),
                                        'widget' ),
                                ]),
                        Blob(
                                urwid.Text("Display Modules",
                                        align='center'),
                                'screen' ),
                        ]),
                ]),

        urwid.Pile( [
                urwid.Text(('program',"\nWidgets\n\n"),
                        align='center'),
                BulletList( [
                        "everything on screen is a widget",
                        "widgets are simple",
                        "widgets are easy to implement",
                        ]),
                ] ),

        urwid.Pile( [
                Blob( urwid.Pile( [
                        urwid.Text("Topmost Widget"),
                        Blob( urwid.Pile( [
                                urwid.Text("Inner Widget (level 1)"),
                                urwid.Columns( [
                                        ('weight', 2, Blob( urwid.Text(
                                                "Inner Widget (level 2)"),
                                                'widget3' )),
                                        Blob( urwid.Text("\n\n\n\n"),
                                                 'widget3' ),
                                        ('weight', 3, Blob( urwid.Pile( [
                                                Blob( urwid.Text("Inner Widget "
                                                        "(level 3)"),'widget4',
                                                        thin=True),
                                                urwid.Divider(),
                                                Blob( urwid.Divider(),
                                                        'widget4', thin=True),
                                                ] ), 'widget3' )),
                                        ] ),
                                ] ), 'widget2' )
                        ] ), 'widget' ),
                ]),

        urwid.Pile( [
                urwid.Text(('program',"\nWidget Delegation\n\n"),
                        align='center'),
                urwid.Padding(
                        urwid.Pile([
                                urwid.Columns([
                                        urwid.Text(T(u"render(size)\n▼"),
                                                align='center'),
                                        urwid.Text(('return',T(u"canvas\n↑")),
                                                align='center'),
                                        ]),
                                Blob(
                                        urwid.Text("Topmost Widget",
                                                align='center'),
                                        'widget', thin=True ),
                                urwid.Columns([
                                        urwid.Text(T(u"render(size1)\n▼"),
                                                align='center'),
                                        urwid.Text(('return',T(u"canvas1\n↑")),
                                                align='center'),
                                        ]),
                                Blob(
                                        urwid.Text("Inner Widget (level 1)",
                                                align='center'),
                                        'widget', thin=True ),
                                urwid.Columns([
                                        urwid.Text(T(u"render(size2)\n▼"),
                                                align='center'),
                                        urwid.Text(('return',T(u"canvas2\n↑")),
                                                align='center'),
                                        ]),
                                Blob(
                                        urwid.Text("Inner Widget (level 2)",
                                                align='center'),
                                        'widget', thin=True ),
                                ]),

                        'center', ('relative',50)),
                ]),

        urwid.Pile( [
                urwid.Text(('program',"\nText Widgets\n\n"),
                        align='center'),
                BulletList( [
                        "flexible",
                        "support different encodings",
                        "provide different layouts",
                        ]),
                ] ),

        urwid.Pile( [
                urwid.Text(('program',"\nStandard Text Layouts\n\n"),
                        align='center'),
                urwid.Columns([
                        urwid.Pile([
                                urwid.Text("\n\n\nwrap on space\n\n\n\n\n"
                                        "wrap anywhere\n\n\n\nclipped text",
                                        align='center')
                                ]),
                        urwid.Pile([
                                urwid.Text("left alignment\n\n",
                                        align='center'),
                                LayoutExample('left','space'),
                                urwid.Divider(),
                                urwid.Divider(),
                                LayoutExample('left','any'),
                                urwid.Divider(),
                                urwid.Divider(),
                                LayoutExample('left','clip'),
                                ]),
                        urwid.Pile([
                                urwid.Text("center alignment\n\n",
                                        align='center'),
                                LayoutExample('center','space'),
                                urwid.Divider(),
                                urwid.Divider(),
                                LayoutExample('center','any'),
                                urwid.Divider(),
                                urwid.Divider(),
                                LayoutExample('center','clip'),
                                ]),
                        urwid.Pile([
                                urwid.Text("right alignment\n\n",
                                        align='center'),
                                LayoutExample('right','space'),
                                urwid.Divider(),
                                urwid.Divider(),
                                LayoutExample('right','any'),
                                urwid.Divider(),
                                urwid.Divider(),
                                LayoutExample('right','clip'),
                                ]),
                        ]),
                ] ),

        urwid.Pile( [
                urwid.Text(('program',"\nLayout Structure\n\n"),
                        align='center'),
                urwid.Padding(
                        urwid.Pile([
                                Blob(
                                        urwid.Text("Text Widget\n"
                                                '"some interesting text"',
                                                align='center'),
                                        'widget', thin=True ),
                                urwid.Columns([
                                        urwid.Pile([
                                                urwid.Text("\n"),
                                                Blob(
                                                        urwid.Text(
                                                                "Text Layout\n"
                                                                "(Standard or "
                                                                "Custom)",
                                                                align='center'),
                                                        'widget2', thin=True ),
                                                ]),
                                        urwid.Pile([
                                                urwid.Text(T(u"\n          ↓\n"
                                                        u"\n"
                                                        u" →     Layout\n"
                                                        u"     Structure\n"
                                                        u"\n          ↓\n")),
                                                LayoutExample('left','space'),
                                                ]),
                                        ]),
                                ]),
                        'center', ('relative',50)),
                ]),

        urwid.Frame(
                urwid.Columns([
                        urwid.Filler(
                                BulletList( [
                                        "scrolls vertically through widgets",
                                        "handles focus changing",
                                        "manages cursor movement between "
                                        "widgets",
                                        ])
                                , 'top'),
                        urwid.Filler(
                                urwid.Padding(
                                        urwid.AttrWrap(LISTBOX_EXAMPLE,'raw'),
                                        ('fixed left',2),('fixed right',2)),
                                ('fixed top',0),('fixed bottom',1)),
                        ], focus_column=1),
                header = urwid.Text(('program',"\nListBox Widget\n\n"),
                        align='center'),
                ),

        urwid.Pile( [
                urwid.Text(('program',"\nListBox & List Walkers\n\n"),
                        align='center'),
                urwid.Columns([
                        urwid.Pile([
                                Blob(
                                        urwid.Text("ListBox",
                                                align='center'),
                                        'widget' ),
                                BulletList( [
                                        "knows the size of the visible area",
                                        "knows the position of the focus "
                                        "widget within the visible area",
                                        ] ),
                                ]),
                        urwid.Pile([
                                Blob(
                                        urwid.Text("List Walker",
                                                align='center'),
                                        'widget2' ),
                                BulletList( [
                                        "knows which widget is in focus",
                                        "knows the arrangement of widgets "
                                        "within the ListBox",
                                        ] ),
                                ]),
                        ]),
                ] ),

        urwid.Pile( [
                urwid.Text(('program',"\nDisplay Modules\n"),
                        align='center'),
                urwid.Columns([
                        urwid.Pile([
                                Blob(
                                        urwid.Text("curses_display",
                                                align='center'),
                                        'screen' ),
                                BulletList([
                                        "run on console or terminal",
                                        "uses Ncurses library",
                                        ]),
                                ]),
                        urwid.Pile([
                                Blob(
                                        urwid.Text("raw_display",
                                                align='center'),
                                        'screen' ),
                                BulletList([
                                        "run on console or terminal",
                                        "sends escape codes directly",
                                        ]),
                                ]),
                        ]),
                urwid.Divider(),
                urwid.Columns([
                        urwid.Pile([
                                Blob(
                                        urwid.Text("web_display",
                                                align='center'),
                                        'screen' ),
                                BulletList([
                                        "run as a web application",
                                        "uses Apache and CGI",
                                        ]),
                                ]),
                        urwid.Pile([
                                Blob(
                                        urwid.Text("html_fragment",
                                                align='center'),
                                        'screen' ),
                                BulletList([
                                        "simulates user input",
                                        "generates html screen shots",
                                        ]),
                                ]),
                        ]),
                ] ),

        urwid.Columns([
                Blob( urwid.Text("Topmost Widget", align='center'), 'widget',
                        flow=False ),
                ('weight', 2, urwid.Filler(
                        urwid.Pile( [
                                urwid.Text(('program',
                                        "\nMain Loop\n\n"),
                                        align='center'),
                                urwid.Text([T(u"get_cols_rows()  ▶\n"),
                                        ('return',T(u"screen size  ←\n"))],
                                        align='right'),
                                urwid.Text([T(u"◀  render( screen size )\n"),
                                        ('return',T(u"→  canvas\n"))]),
                                urwid.Text(T(u"draw_screen( canvas )  ▶\n\n"),
                                        align='right'),
                                urwid.Text([T(u"get_input()  ▶\n"),
                                        ('return',T(u"list of keys  ←\n"))],
                                        align='right'),
                                urwid.Text(T(u"◀  keypress( key )")),
                                ] )
                        , 'top') ),
                Blob( urwid.Text("Display Module", align='center'), 'screen',
                        flow=False ),
                ], focus_column=1),

        urwid.Pile( [
                urwid.Text(('program',"\nConsole User Interfaces "
                                "and Urwid\n"),
                        align='center'),
                Blob(
                        urwid.Text("Thank You", align='center'),
                        'bigtitle' ),
                urwid.Text(('url',"\n\n\nWeb Site: http://excess.org/urwid/"),
                        align='center'),
                ] ),

        None, # signal extra slides

        urwid.Pile( [
                urwid.Text(('program',"\nWidget Types\n"),
                        align='center'),
                urwid.Columns([
                        urwid.Pile( [
                                Blob(
                                        urwid.Text("Box Widgets",
                                                align='center'),
                                        'widget' ),
                                BulletList( [
                                        "given maximum screen columns"
                                        " and rows",
                                        "must render to fit inside"
                                        " the space given",
                                        ]),
                                ] ),
                        urwid.Pile( [
                                Blob(
                                        urwid.Text("Flow Widgets",
                                                align='center'),
                                        'widget' ),
                                BulletList( [
                                        "given maximum screen columns"
                                        " only",
                                        "will calculate rows required",
                                        ]),

                                ]),
                        ] ),
                ] ),

        urwid.Pile( [
                urwid.Text(('program',"\nWidget Types Continued\n"),
                        align='center'),
                urwid.Columns([
                        urwid.Pile( [
                                Blob(
                                        urwid.Text("Composite Widgets",
                                                align='center'),
                                        'widget' ),
                                BulletList( [
                                        "contain one or more other"
                                        " widgets",
                                        "keep track of which widget"
                                        " is the focus",
                                        "combine the rendered output"
                                        " of contained widgets",
                                        ]),
                                ] ),
                        urwid.Pile( [
                                Blob(
                                        urwid.Text("Content Widgets",
                                                align='center'),
                                        'widget' ),
                                BulletList( [
                                        "responsible for own rendering",
                                        "may display cursor",
                                        ]),

                                ]),
                        ] ),
                ] ),
        urwid.Pile( [
                urwid.Text(('program',"\nStandard Urwid Widgets\n\n"),
                        align='center'),
                urwid.Columns([
                        BulletList( [
                                "Columns",
                                "Pile",
                                "GridFlow",
                                "BoxAdapter",
                                "WidgetWrap",
                                "AttrWrap",
                                "Padding",
                                ]),
                        BulletList( [
                                "Frame",
                                "Filler",
                                "ListBox",
                                "Text",
                                "Edit",
                                "IntEdit",
                                "Button",
                                ]),
                        BulletList( [
                                "CheckBox",
                                "RadioButton",
                                "Bargraph",
                                "GraphVScale",
                                "ProgressBar",
                                "Divider",
                                ]),
                        ] ),
                ] ),

        ]

class PageHeader(urwid.WidgetWrap):
        def __init__(self, max_page):
                self.max_page = max_page
                urwid.WidgetWrap( None )

        def set_page(self, page):
                l = []
                for i in range( self.max_page ):
                        if i != page:
                                l.append( ('notpage', T(u"█▌")) )
                        else:
                                l.append( T(u"█▌") )
                l.append(('pageno'," %2d" % (page+1)))
                dw = urwid.Columns([
                        ('fixed', 12, urwid.Text( "OCLUG Apr/06")),
                        urwid.Text( l, align='right' ),
                        ])
                dw = urwid.AttrWrap( dw, 'header' )
                dw = urwid.Pile( [dw,
                        urwid.AttrWrap( urwid.Divider( T(u"¯") ), 'headerline') ] )
                self.w = dw


class PresentDisplay:
        palette = [
                ('body','black','light gray', 'standout'),
                ('widget','black','dark cyan'),
                ('widget2','white','dark blue'),
                ('widget3','black','dark cyan'),
                ('widget4','white','dark blue'),
                ('screen','black','dark green'),
                ('program','dark blue','light gray'),
                ('return','dark red','light gray'),
                ('header','white','dark blue'),
                ('headerline','black','light gray'),
                ('notpage','light blue','dark blue'),
                ('pageno','light blue','dark blue'),
                ('bigtitle','white','black'),
                ('raw','light cyan','black'),
                ('raw2','black','dark cyan'),
                ('url','dark red','light gray'),
                ('cli','light gray','black'),
                ('cui','black','dark cyan'),
                ('gui','white','dark blue'),

                ('w3m bar','black','light gray'),
                ('w3m icon','dark green','black'),
                ('w3m link','dark blue','black'),
                ('w3m normal','light gray','black'),

                ('dpkg bl','yellow','dark blue'),
                ('dpkg sh','light gray','black'),
                ]

        def __init__(self):
                pass

        def main(self):
                self.ui = Screen()
                self.ui.register_palette( self.palette )
                self.ui.set_mouse_tracking()
                self.ui.run_wrapper( self.run )

        def run(self):
                top = left = right = 0
                max_page = PAGE.index(None)
                hdr = PageHeader( max_page )
                page = 0
                size = self.ui.get_cols_rows()
                while 1:
                        hdr.set_page(page)
                        view = PAGE[page]
                        if isinstance( view, urwid.Pile ):
                                view = urwid.Filler( view, 'top' )
                        view = urwid.AttrWrap( view, 'body' )
                        view = urwid.Frame( view, hdr )
                        if left or right:
                                view = urwid.Padding( view,
                                        ('fixed left',left),
                                        ('fixed right',right) )
                        if top:
                                view = urwid.Filler( view,
                                        ('fixed top',top),
                                        ('fixed bottom',0) )
                        canvas = view.render( size, focus=1 )
                        self.ui.draw_screen( size, canvas )
                        keys = None
                        while not keys:
                                keys = self.ui.get_input()
                        for k in keys:
                                if k == 'window resize':
                                        size = self.ui.get_cols_rows()
                                elif k == 'f8':
                                        return

                                if urwid.is_mouse_event( k ):
                                        ign, b, ign, ign = k
                                        if b==1:
                                                k = ' '
                                        elif b==3:
                                                k = 'backspace'
                                        else:
                                                continue
                                elif view.selectable():
                                        k = view.keypress( size, k )

                                if k == ' ':
                                        page = (page + 1) % len(PAGE)
                                        if PAGE[page] is None:
                                                page = (page + 1) % len(PAGE)
                                elif k == 'backspace':
                                        page = (page - 1) % len(PAGE)
                                        if PAGE[page] is None:
                                                page = (page - 1) % len(PAGE)
                                elif k == 'a':
                                        left = max(0, left-1)
                                elif k == 's':
                                        left = left + 1
                                elif k == 'e':
                                        top = max(0, top-1)
                                elif k == 'w':
                                        top = top +1
                                elif k == 'f':
                                        right = max(0, right-1)
                                elif k == 'd':
                                        right = right +1


def main():
        PresentDisplay().main()

if '__main__'==__name__:
        main()