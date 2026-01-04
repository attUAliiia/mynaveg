import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QToolBar, QAction, 
                             QLineEdit, QProgressBar, QTabWidget, QLabel)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage, QWebEngineSettings
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor

# --- adblocker ---
class SmartBlocker(QWebEngineUrlRequestInterceptor):
    def __init__(self):
        super().__init__()
        self.blocked_substrings = [
            "doubleclick.net", "adservice.google", "googlesyndication",
            "facebook.com/tr", "google-analytics", "adnxs.com",
            "criteo.com", "moatads.com", "hotjar.com", "outbrain.com"
        ]

    def interceptRequest(self, info):
        url = info.requestUrl().toString().lower()
        
        # i messed up on something here lmaoo 
        for forbanned in self.blocked_substrings:
            if forbanned in url:
                print(f"🚫 Blocked: {url[:30]}...") 
                info.block(True)
                return
        
        # bradar ur now un chrome LMAOOOOOOOOOOOOOOOOOOOOOOOOO (jkjk)
        info.setHttpHeader(b"User-Agent", b"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# main window
class FinalBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("mynaveg")
        self.resize(1300, 850)
        
        self.setStyleSheet("""
            QMainWindow { background-color: #121212; }
            QTabWidget::pane { border: 0px; top: -1px; }
            QTabBar::tab {
                background: #1e1e1e; color: #888; padding: 8px 20px;
                border-top-left-radius: 6px; border-top-right-radius: 6px;
                margin-right: 2px; font-family: Segoe UI;
            }
            QTabBar::tab:selected { background: #333; color: white; font-weight: bold; }
            QToolBar { background: #252526; border-bottom: 2px solid #111; padding: 5px; }
            QLineEdit { 
                background: #121212; color: white; border: 1px solid #444; 
                border-radius: 12px; padding: 6px 15px; font-size: 13px;
            }
            QLineEdit:focus { border: 1px solid #007acc; }
            QProgressBar { border: none; background: #121212; height: 3px; }
            QProgressBar::chunk { background-color: #007acc; }
        """)

        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.setHttpCacheType(QWebEngineProfile.MemoryHttpCache)
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)
        
        self.interceptor = SmartBlocker()
        self.profile.setUrlRequestInterceptor(self.interceptor)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.tab_changed)
        self.setCentralWidget(self.tabs)

        self.setup_ui()
        self.add_tab(QUrl("https://duckduckgo.com"), "Inicio")

    def setup_ui(self):
        nav = QToolBar("Nav")
        nav.setMovable(False)
        self.addToolBar(nav)

        for text, func in [("◀", self.back), ("▶", self.forward), ("↻", self.reload)]:
            act = QAction(text, self)
            act.triggered.connect(func)
            nav.addAction(act)

        nav.addSeparator()
        self.https_icon = QLabel("🔒")
        self.https_icon.setStyleSheet("color: gray; margin-right: 8px; font-size: 14px;")
        nav.addWidget(self.https_icon)

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Buscar o escribir URL...")
        self.url_bar.returnPressed.connect(self.navigate)
        nav.addWidget(self.url_bar)

        add_tab_btn = QAction(" + ", self)
        add_tab_btn.triggered.connect(lambda: self.add_tab())
        nav.addAction(add_tab_btn)

        self.progress = QProgressBar()
        self.progress.setMaximumWidth(150)
        nav.addWidget(self.progress)

    def add_tab(self, qurl=None, label="Nueva Pestaña"):
        if qurl is None: qurl = QUrl("https://duckduckgo.com")
        
        browser = QWebEngineView()
        page = QWebEnginePage(self.profile, browser)
        
        settings = page.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
        settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
        
        browser.setPage(page)
        browser.setUrl(qurl)
        
        browser.urlChanged.connect(lambda q: self.update_url(q, browser))
        browser.loadProgress.connect(lambda p: self.update_progress(p, browser))
        browser.titleChanged.connect(lambda t: self.update_title(t, browser))
        
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

    def back(self): self.tabs.currentWidget().back()
    def forward(self): self.tabs.currentWidget().forward()
    def reload(self): self.tabs.currentWidget().reload()
    def close_tab(self, i): 
        if self.tabs.count() > 1: self.tabs.removeTab(i)
    
    def tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_url(qurl, self.tabs.currentWidget())

    def update_url(self, q, browser):
        if browser != self.tabs.currentWidget(): return
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)
        if q.scheme() == "https":
            self.https_icon.setText("🔒")
            self.https_icon.setStyleSheet("color: #4caf50; font-size: 14px; margin-right: 8px;")
        else:
            self.https_icon.setText("🔓")
            self.https_icon.setStyleSheet("color: #f44336; font-size: 14px; margin-right: 8px;")

    def update_title(self, title, browser):
        if browser != self.tabs.currentWidget(): return
        self.tabs.setTabText(self.tabs.indexOf(browser), title[:15] + ".." if len(title)>15 else title)

    def update_progress(self, p, browser):
        if browser == self.tabs.currentWidget():
            self.progress.setValue(p)
            self.progress.setVisible(p < 100)

    def navigate(self):
        url = self.url_bar.text()
        if "." not in url and " " in url: url = f"https://duckduckgo.com/?q={url}"
        elif not url.startswith("http"): url = "https://" + url
        self.tabs.currentWidget().setUrl(QUrl(url))

if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    window = FinalBrowser()
    window.show()

    sys.exit(app.exec_())
