# mynaveg

A privacy-focused web browser built with Python and Qt. It features a custom-built ad/tracker blocker, and secured browsing sessions (no history or cookies are saved to disk).

## Features

* **Ghost Mode:** By default, the browser runs in an "off-the-record" profile. History, cache, and cookies are wiped instantly upon closing.
* **Built-in Ad Blocker:** A native HTTP interceptor that blocks known ad networks, trackers (Google Analytics, Facebook Pixel, etc.), and telemetry domains without needing extensions.
* **Chromium Engine:** Powered by QtWebEngine (Chromium) for full support of newer web standards (HTML5, YouTube, WebGL).
* **Stealth User-Agent:** Spoofs the User-Agent string to appear as a standard Chrome browser on Windows 10, preventing fingerprinting and ensuring site compatibility.
* **Clean UI:** Tabbed browsing, load progress bar, and visual SSL security indicators.

## Installation

### Prerequisites
* Python 3.8+
* pip

### Setup
1.  Clone the repository or download the source code. (it comes with a .exe)
2.  Install the required dependencies:

```bash
pip install PyQt5 PyQtWebEngine


License & Legal
Project License
This source code is released under the MIT License. You are free to use, modify, and distribute it.

Third-Party Licenses
This software is built upon several open-source projects. If you distribute this application, you must comply with their respective licenses:

PyQt5 is licensed under the GPL v3.

Qt Project (QtWebEngine) is licensed under the LGPL v3 and GPL v3.

Chromium (the engine behind QtWebEngine) is licensed under the BSD License.

> Note: This browser is for educational and privacy purposes. It is not affiliated with Google or the Qt Company.

Created with Python 
