import logging
from typing import Any, Dict, List, Optional, Self, Tuple, Type, Union


def try_render(item: Any, indent_level: int = 0, indent_str: str = "  ") -> str:
    if isinstance(item, str):
        return indent_str * indent_level + item

    try:
        return item.render(indent_level, indent_str)
    except Exception:
        return indent_str * indent_level + str(item)


class Tag:
    _braces: Tuple[str, str]
    _tag: str
    _content_delimiter: str
    _indent: str
    _has_closer: bool

    _settings_word_map: Dict[str, str] = {
        "class_": "class",
        "for_": "for",
        "id_": "id",
        "type_": "type",
    }
    _settings_char_map: Dict[str, str] = {"_": "-"}

    def __init__(self, *content: Any, **kwargs: Union[str, bool]) -> None:
        self.__logger: logging.Logger = logging.getLogger(self.__class__.__name__)
        self.content = list(content)
        self.kwargs: Dict[str, str | bool] = self._sanitise_settings(**kwargs)

    def __call__(self, *content: Any, **kwargs: Union[str, bool]) -> Self:
        return self.add(*content).set(**kwargs)

    def add(self, *items: Any) -> Self:
        self.content += items
        return self

    def set(self, **kwargs) -> Self:
        self.kwargs.update(self._sanitise_settings(**kwargs))
        return self

    def render(self, indent_level: int = 0, indent_str: Optional[str] = None) -> str:
        if indent_str is None:
            indent_str = self._indent
        settings: str = self._render_settings()
        opener: str = (
            f"{indent_str*indent_level}{self._braces[0]}{self._tag}"
            + f"{" " + settings if settings else ""}{self._braces[1]}"
        )

        if not self._has_closer:
            if len(self.content) > 0:
                self.__logger.warn(
                    "Tags without a closer do not support content! \nTag: {self._tag} Content: {self.content}"
                )
            return opener

        content: List[str] = [
            try_render(item, indent_level + 1, indent_str) for item in self.content
        ]

        closer: str = (
            f"{indent_str*indent_level}{self._braces[0]}/{self._tag}{self._braces[1]}"
        )

        return self._content_delimiter.join([opener] + content + [closer])

    def _sanitise_settings(self, **settings: str | bool) -> Dict[str, str | bool]:
        return {self._sanitise_key(k): v for k, v in settings.items()}

    def _sanitise_key(self, key: str) -> str:
        key = self._settings_word_map.get(key, key)
        key = "".join(self._settings_char_map.get(c, c) for c in key)
        return key

    def _render_settings(self) -> str:
        return " ".join(
            [f'{k}="{v}"' for k, v in self.kwargs.items() if not isinstance(v, bool)]
            + [k for k, v in self.kwargs.items() if v is True]
        )


def tag_factory(
    tag: str,
    braces: Tuple[str, str] = ("<", ">"),
    content_delimiter: str = "\n",
    indentation: str = "  ",
    has_closer: bool = True,
) -> Type[Tag]:
    class TagImpl(Tag):
        _braces: Tuple[str, str] = braces
        _tag: str = tag
        _content_delimiter: str = content_delimiter
        _indent: str = indentation
        _has_closer: bool = has_closer

    return TagImpl
