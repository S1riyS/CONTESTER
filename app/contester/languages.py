from flask import url_for

from app import app
from app.utils.singleton import SingletonBaseClass

# Dictionary with programming languages (name, compiler, CodeMirror mode)
languages_dict = {
    'cpp': {
        'name': 'C++',
        'fullname': 'GNU C++ 11.1',
        'compiler': 'gcc-11.1.0',
        'mode': 'text/x-c++src',
        'icon': 'cpp'},
    'csharp': {
        'name': 'C#',
        'fullname': 'C# Mono 6.12',
        'compiler': 'mono-6.12.0.122',
        'mode': 'text/x-csharp',
        'icon': 'csharp'},
    'python': {
        'name': 'Python 3',
        'fullname': 'Python 3.8.9',
        'compiler': 'cpython-3.8.9',
        'mode': 'text/x-python',
        'icon': 'python',
        'is_default': True},
    'pypy': {
        'name': 'Pypy 3',
        'fullname': 'Pypy 3.7 (7.3.4)',
        'compiler': 'pypy-3.7-v7.3.4',
        'mode': 'text/x-python',
        'icon': 'python'},
    'pascal': {
        'name': 'Pascal',
        'fullname': 'Free Pascal 3.2.0',
        'compiler': 'fpc-3.2.0',
        'mode': 'text/x-pascal',
        'icon': 'default'},
}


class Languages(metaclass=SingletonBaseClass):
    def __init__(self, lang_dict):
        self.languages = lang_dict

    def get_language(self, language) -> dict:
        return self.languages.get(language, None)

    def get_icon_url(self, language) -> str:
        current_language = self.get_language(language)

        if current_language:
            icon_name = current_language.get('icon', 'default')
        else:
            icon_name = 'default'

        with app.app_context(), app.test_request_context():
            return url_for('static', filename=f'images/svg/language_icons/{icon_name}.svg')

    def get_info(self, language) -> dict:
        current_language = self.get_language(language)

        fullname = current_language.get('fullname', 'Not found')
        icon = self.get_icon_url(language)

        return {'fullname': fullname, 'icon': icon}


languages = Languages(lang_dict=languages_dict)
