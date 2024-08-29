import mistune.renderers.markdown
import re
import logging
from typing import Dict, Any
from mistune.core import BlockState

log = logging.getLogger(__name__)


_strip_end_re = re.compile(r'\n\s+$')

def strip_end(src: str):
    return _strip_end_re.sub('\n', src)

def render_list(renderer, token, state) -> str:
    attrs = token['attrs']
    if attrs['ordered']:
        children = _render_ordered_list(renderer, token, state)
    else:
        children = _render_unordered_list(renderer, token, state)

    text = ''.join(children)
    parent = token.get('parent')
    if parent:
        if parent['tight']:
            return text
        return text + '\n'
    return strip_end(text) + '\n'


def _render_list_item(renderer, parent, item, state):
    leading = parent['leading']
    text = ''
    for tok in item['children']:
        if tok['type'] == 'list':
            tok['parent'] = parent
        elif tok['type'] == 'blank_line':
            continue
        text += renderer.render_token(tok, state)

    lines = text.splitlines()
    text = (lines[0] if lines else '') + '\n'
    prefix = ' ' * len(leading)
    for line in lines[1:]:
        if line:
            text += prefix + line + '\n'
        else:
            text += '\n'
    return leading + text


def _render_ordered_list(renderer, token, state):
    attrs = token['attrs']
    start = attrs.get('start', 1)
    for item in token['children']:
        leading = str(start) + token['bullet'] + ' '
        parent = {
            'leading': leading,
            'tight': token['tight'],
        }
        yield _render_list_item(renderer, parent, item, state)
        start += 1


def _render_unordered_list(renderer, token, state):
    parent = {
        'leading': '-' + ' ',
        'tight': token['tight'],
    }
    for item in token['children']:
        yield _render_list_item(renderer, parent, item, state)


class TypstRenderer(mistune.renderers.markdown.MarkdownRenderer):
    NAME = 'typst'
    IS_TREE = False
    ordered = False
    escape_text = False

    list_depth=1

    def escape(self, text):
        ''' Escape the given text for display in Typst output

        :param text: a plain text message
        :return: the message escaped to appear correctly in Typst
        '''
        conv = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '[': r'\[',
            ']': r'\]',
            '@': r'\@',
            '*': r'\*',
            '\\': r'\\',
            '<':'\<',
            '>':'\>'
        }
        regex = re.compile('|'.join(re.escape(str(key)) for key in sorted(
            conv.keys(), key=lambda item: - len(item))))
        return regex.sub(lambda match: conv[match.group()], text)



    def __init__(self, escape=True):
        super(TypstRenderer, self).__init__()
        self.escape_text = escape

    def text(self, token: Dict[str, Any], state: BlockState) -> str:
        return self.escape(token['raw'])

    def link(self, token: Dict[str, Any], state: BlockState) -> str:
        label = token.get('label')
        text = self.render_children(token, state)

        attrs = token['attrs']
        url = attrs['url']
        title = attrs.get('title')

        if title:
            return f'#link("{url}")'
        else:
            return f'#link("{url}")[{text}]'

    def image(self, token: Dict[str, Any], state: BlockState) -> str:
        label = token.get('label')
        text = self.render_children(token, state)

        attrs = token['attrs']
        url = attrs['url']
        title = attrs.get('title')

        if title:
            return f'#figure(image("{url}"), caption: [{text}])'
        else:
            return f'#image("{url}")'
        

    def emphasis(self, token: Dict[str, Any], state: BlockState) -> str:
        return '_' + self.render_children(token, state) + '_'

    def strong(self, token: Dict[str, Any], state: BlockState) -> str:
        return '*' + self.render_children(token, state) + '*'
    
    def thematic_break(self, token: Dict[str, Any], state: BlockState) -> str:
        return '\n\n'

    def heading(self, token: Dict[str, Any], state: BlockState) -> str:
        level = token['attrs']['level']
        marker = '=' * level
        text = self.render_children(token, state)
        if text[-6:] == ' \{-\}':
            text = text[:-6]
        return marker + ' ' + text + '\n\n'
    
    def list(self, token: Dict[str, Any], state: BlockState) -> str:
        return render_list(self, token, state)

