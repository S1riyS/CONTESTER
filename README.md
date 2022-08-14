![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Heroku](https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)
![JS](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

[![Tests](https://github.com/S1riyS/CONTESTER/actions/workflows/checks.yml/badge.svg?branch=master&style=flat)](https://github.com/S1riyS/CONTESTER/actions/workflows/checks.yml)
![License](https://img.shields.io/github/license/S1riyS/CONTESTER?labelColor=333a41&style=flat)
![Python quality](https://img.shields.io/lgtm/grade/python/github/S1riyS/CONTESTER?logo=LGTM&style=flat&labelColor=333a41)
![JavaScript quality](https://img.shields.io/lgtm/grade/javascript/github/S1riyS/CONTESTER?logo=LGTM&style=flat&labelColor=333a41)

     █████╗  █████╗ ███╗  ██╗████████╗███████╗ ██████╗████████╗███████╗██████╗ 
    ██╔══██╗██╔══██╗████╗ ██║╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔════╝██╔══██╗
    ██║  ╚═╝██║  ██║██╔██╗██║   ██║   █████╗  ╚█████╗    ██║   █████╗  ██████╔╝
    ██║  ██╗██║  ██║██║╚████║   ██║   ██╔══╝   ╚═══██╗   ██║   ██╔══╝  ██╔══██╗
    ╚█████╔╝╚█████╔╝██║ ╚███║   ██║   ███████╗██████╔╝   ██║   ███████╗██║  ██║
     ╚════╝  ╚════╝ ╚═╝  ╚══╝   ╚═╝   ╚══════╝╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝

## 📝 About project

**[CONTESTER](https://github.com/S1riyS/CONTESTER)** - is a system for testing students' code.

4 programming languages are supported:

* **[Python](https://www.python.org/?hl=ru)** (Python 3.8.9)
* **[C++](https://isocpp.org/)** (GNU C++ 11.1)
* **[C#](https://dotnet.microsoft.com/en-us/languages/csharp)** (C# Mono 6.12)
* **[PascalABC](http://pascalabc.net/)** (Free Pascal 3.2.0)

Also supported **[Pypy 3.7](https://www.pypy.org/)** (7.3.4)

## 🖥️ Editor

![Editor](https://i.postimg.cc/HWtxnQ2b/CONTESTER-editor.png)

### Usage:

First, lets look on Editor:

Here we have 3 buttons: `Send Code`, `Delete code` and `Copy to clipbord`. In the upper left corner of the editor there
is a drop-down menu where you can select a programming language

When you click the `Send Code` button, the server is processing sent code, and as a result you can see a response like
this:

![Response](https://i.postimg.cc/qqqRXyHJ/image.png)

Response can contain next messages: `Success`, `WrongAnswerError`,
`TimeLimitError` (sometimes works incorrect), `ExecutionError`, `ServerResponseError`

### How it works:

The editor was created using **[CodeMirror](https://codemirror.net/)**.

When user is pressing `Send Code` button, an **AJAX** request is sent to the server.

Then CONTESTER's server sends async requests to **[WandboxAPI](https://github.com/melpon/wandbox)**. The code is
executed there and then CONTESTER's server process results of execution and returns **JSON**, which is rendered into
**HTML** code

## ⬇ Installation

* Clone repository to your local machine:

  `git clone https://github.com/S1riyS/CONTESTER.git`

* Move to the root folder of the project

* Create virtual environment: `python -m venv venv`

* Activate *venv*:
    * Linux: `source venv/bin/activate`
    * Windows: `venv\Scripts\activate`

* Install all the necessary modules:

  `pip install -r requirements.txt`

Now you can start `app.py` file :

```python
from app import app

if __name__ == "__main__":
    app.run(port=5000, host='127.0.0.1', debug=True)
```

## 🎞 Preview

![Image 1](https://i.postimg.cc/6p5djWHG/CONTESTER-screenshot.png)

*Remaining description will be added later...*