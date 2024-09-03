from .color import Color
from .styles import STYLES
import re

_STYLES_MAP = {}
for k, v in STYLES.items():
    if isinstance(v, dict):
        for _k1, v1 in v.items():
            _STYLES_MAP[f'{v1}'] = k
    else:
        _STYLES_MAP[f'{v}'] = k


def _load0(info: tuple[str, str, str]):
    '''
    根据 regex 中的匹配结果生成 Color 对象
    '''
    if info[-1]:
        return Color(info[-1])
    style = {}
    for v in info[0].split(';'):
        if v in _STYLES_MAP:
            style[_STYLES_MAP[v]] = int(v)
    return Color(info[1], _style=style)

def _load(text: str):
    '''
    字符串中如果含有样式代码，将被解析为 Color 对象
    '''
    reg = r'\033\[(\d+(?:;\d+)*)m(.*?)\033\[0m|([^\033\[\d;]+)'
    groups = re.findall(reg, text)
    if groups:
        if len(groups) == 1:
            return _load0(groups[0])
        children = []
        for group in groups:
            children.append(_load0(group))
        return Color('', _children=children)
    else:
        return Color(text)


def color(content: str | Color):
    '''
    将一个字符串或 Color 对象转换为 Color 对象。

    若字符串含有 ANSI 转义序列，也能转换为 Color 对象
    '''
    if isinstance(content, Color):
        return content
    else:
        return _load(content)


def str_has_style(text: str):
    '''
    检查字符串是否包含 ANSI 转义序列
    '''
    return bool(re.search(r'\033\[\d+', text))
