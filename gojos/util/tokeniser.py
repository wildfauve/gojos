from typing import List
import re

from gojos.util import fn

special_char_set = [("-", "_"), (" ", "_"), ("'", "")]
dot_splitter = re.compile(r'\.')
sp_splitter = re.compile('r\s')

def string_tokeniser(in_str: str, str_splitter: re.Pattern, char_replacers: List) -> str:
    return fn.multi_replace(str_splitter.split(in_str)[-1], char_replacers)


