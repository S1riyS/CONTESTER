import typing as t
from dataclasses import dataclass

from flask import current_app as app
from flask import url_for

from app.utils.singleton import SingletonBaseClass


@dataclass(frozen=True)
class Language:
    name: str
    fullname: str
    compiler: str
    mode: str
    icon_name: str = 'default'
    is_default: bool = False

    @property
    def icon_url(self) -> str:
        with app.app_context(), app.test_request_context():
            return url_for('static', filename=f'images/svg/language_icons/{self.icon_name}.svg')


@dataclass(frozen=True)
class Languages(metaclass=SingletonBaseClass):
    # Dictionary with programming languages (name, compiler, CodeMirror mode)
    dictionary = {
        'cpp': Language(
            name='C++',
            fullname='GNU C++ 11.1',
            compiler='gcc-11.1.0',
            mode='text/x-c++src',
            icon_name='cpp'
        ),
        'csharp': Language(
            name='C#',
            fullname='C# Mono 6.12',
            compiler='mono-6.12.0.122',
            mode='text/x-csharp',
            icon_name='csharp'
        ),
        'python': Language(
            name='Python 3',
            fullname='Python 3.8.9',
            compiler='cpython-3.8.9',
            mode='text/x-python',
            icon_name='python',
            is_default=True
        ),
        'pypy': Language(
            name='Pypy 3',
            fullname='Pypy 3.7 (7.3.4)',
            compiler='pypy-3.7-v7.3.4',
            mode='text/x-python',
            icon_name='python'
        ),
        'pascal': Language(
            name='Pascal',
            fullname='Free Pascal 3.2.0',
            compiler='fpc-3.2.0',
            mode='text/x-pascal',
        )}

    _language_not_found = Language(
        name='Not found',
        fullname='Not found',
        compiler='Not found',
        mode='Not found'
    )

    def get_language(self, language: str, object_only: t.Optional[bool] = False) -> t.Union[dict, Language]:
        current_language = self.dictionary.get(language, None)

        if current_language is None:
            success = False
            language_object = self._language_not_found
        else:
            success = True
            language_object = current_language

        if object_only:
            return language_object
        return {
            'success': success,
            'language': language_object
        }


languages = Languages()
try:
    app.jinja_env.globals['languages'] = languages
except RuntimeError:
    print('Cannot set jinja2 global variable')
