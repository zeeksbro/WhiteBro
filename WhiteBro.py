import sys
from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon, QShortcut, QKeySequence
from PySide6.QtWidgets import QApplication, QLineEdit, \
    QMainWindow, QPushButton, QToolBar
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineUrlRequestInterceptor, QWebEngineProfile
from PySide6.QtWebEngineWidgets import QWebEngineView
from adblockparser import AdblockRules
import re


class AdBlock:
    def __init__(self, filename):
        with open(filename) as f:
            raw_rules = f.readlines()
            self.rules = AdblockRules(raw_rules)
        print(self.rules)


class CheckerFast:
    def __init__(self, *args):
        regs = "|".join(["(%s)" % a for a in args])
        # print(regs)
        self.reg = re.compile(regs)

    def check(self, s):
        return self.reg.match(s) is not None


class WebEngineUrlRequestInterceptor2(QWebEngineUrlRequestInterceptor):
    def __init__(self, rules, p=None):
        QWebEngineUrlRequestInterceptor.__init__(self, p)
        self.rules = rules

    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        if self.rules.should_block(url):
            print("block::::::::::::::::::::::", url)
            info.block(True)
        else:
            print("allow::::::::::::::::::::::", url)


class WebEngineUrlRequestInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, rules, p=None):
        QWebEngineUrlRequestInterceptor.__init__(self, p)

    @staticmethod
    def check(url):
        return re.match(r"^https://(.*\.)?googlesyndication.com/", url) or \
           re.match(r"^https://(.*\.)?google-analytics.com/", url) or \
           re.match(r"^https://(.*\.)?doubleclick.net/", url) or \
           re.match(r"^https://(.*\.)?onthe.io/", url) or \
           re.match(r"^https://(.*\.)?aidata.io/", url) or \
           re.match(r"^https://(.*\.)?cdn.onesignal.com/", url) or \
           re.match(r"^https://(.*\.)?yadro.ru/", url) or \
           re.match(r"^https://(.*\.)?weborama.com/", url) or \
           re.match(r"^https://(.*\.)?static.ngs.ru/jtnews/dist/static/js/sdk/asdk", url) or \
           re.match(r"^-core-ads\.", url) or \
           re.match(r"^https://.*/ads/", url) or \
           re.match(r"^https://.*/ad/", url) or \
           re.match(r"^https://.*/banner/", url)

    def interceptRequest(self, info):
        # info.setHttpHeader("X-Frame-Options", "ALLOWALL")
        print("interceptRequest")
        if self.check(info.requestUrl().toString()):
            info.block(True)
            print('blocked', info.requestUrl())
        print('allowed', info.requestUrl())


class MyWebEngineView(QWebEngineView):
    def __init__(self, *args, **kwargs):
        QWebEngineView.__init__(self, *args, **kwargs)
        self.checker = CheckerFast(r"^file://",
                                   r"^https://uchi.ru",
                                   r"^https://resh.edu.ru",
                                   r"^http://afonino-school.ru",
                                   r"^https://ya.ru/?$",
                                   r"^https://yandex.ru/?$"
                                   r"^https://yandex.ru/search/",
                                   r"^https://google.com",
                                   r"^https://duckduckgo.com",
                                   r"^https://habr.com",
                                   r"^https://(.*\.)?stackoverflow.com",
                                   r"^https://(.*\.)?wikipedia.org",
                                   r"^https://bigenc.ru",
                                   r"^https://gufo.me/",
                                   r"^https://stepik.org",
                                   r"^https://(www\.)?coursera.org",
                                   r"^https://lingualeo.com",
                                   r"^https://duolingo.com",
                                   r"^https://royallib.com",
                                   r"^https://www.pravoslavie.ru/",
                                   r"^http://www.patriarchia.ru/",
                                   r"^https://azbyka.ru/",
                                   r"^https://foma.ru/",
                                   r"^https://islam-today.ru/",
                                   r"^https://islam.ru/",
                                   r"^https://azan.ru/",
                                   r"^https://islamqa.info/",
                                   r"^https://python.org",
                                   r"^https://(.*\.)?cppreference.com",
                                   r"^https://(www\.)?fsf.org",
                                   r"^https://(www\.)?gnu.org",
                                   r"^https://(.*\.)?ucheba.ru/",
                                   r"^https://(.*\.)?nngasu.ru/",
                                   r"^https://(.*\.)?msu.ru/",
                                   r"^https://(.*\.)?nntu.ru/",
                                   r"^https://(.*\.)?nstu.ru/",
                                   r"^https://(.*\.)?unn.ru/",
                                   r"^https://(.*\.)?nsu.ru/",
                                   r"^https://(.*\.)?mipt.ru/",
                                   r"^https://(.*\.)?hse.ru/",
                                   r"^https://lifehacker.ru",
                                   r"^https://(www\.)?nn.ru",)

    def check(self, url: QUrl):
        return self.checker.check(url.url())

    def load(self, url):
        if self.check(url):
            QWebEngineView.load(self, url)
        else:
            print(url, "not allowed")


class MainWindow(QMainWindow):

    def __init__(self, initial_url: str):
        super().__init__()

        self.setWindowTitle('Safe Browser with white list')

        self.toolBar = QToolBar()
        self.addToolBar(self.toolBar)
        self.backButton = QPushButton()
        self.backButton.setIcon(QIcon(':/qt-project.org/styles/commonstyle/images/left-32.png'))
        self.backButton.clicked.connect(self.back)
        self.toolBar.addWidget(self.backButton)
        self.forwardButton = QPushButton()
        self.forwardButton.setIcon(QIcon(':/qt-project.org/styles/commonstyle/images/right-32.png'))
        self.forwardButton.clicked.connect(self.forward)
        self.toolBar.addWidget(self.forwardButton)

        self.addressLineEdit = QLineEdit()
        self.addressLineEdit.returnPressed.connect(self.load)
        self.toolBar.addWidget(self.addressLineEdit)

        self.searchLineEdit = QLineEdit()
        self.searchLineEdit.returnPressed.connect(self.search)
        self.toolBar.addWidget(self.searchLineEdit)

        # adblock = AdBlock("easylist.txt")
        interceptor = WebEngineUrlRequestInterceptor(None, None)
        profile = QWebEngineProfile()
        profile.setUrlRequestInterceptor(interceptor)

        self.shortcut_s = QShortcut(QKeySequence("ctrl+f"), self)
        self.shortcut_s.activated.connect(lambda: self.searchLineEdit.setFocus())

        self.shortcut_g = QShortcut(QKeySequence("g"), self)
        self.shortcut_g = QShortcut(QKeySequence("ctrl+g"), self)
        self.shortcut_g.activated.connect(lambda: self.addressLineEdit.setFocus())

        self.webEngineView = MyWebEngineView()  # browser
        self.setCentralWidget(self.webEngineView)
        self.webpage = QWebEnginePage(profile, self.webEngineView)
        self.addressLineEdit.setText(initial_url)
        self.webEngineView.load(QUrl(initial_url))
        # self.webEngineView.page().titleChanged.connect(self.setWindowTitle)
        # self.webEngineView.page().urlChanged.connect(self.url_changed)
        self.webpage.titleChanged.connect(self.setWindowTitle)
        self.webpage.urlChanged.connect(self.url_changed)

    def search(self):
        s = self.searchLineEdit.text()
        self.webEngineView.page().findText(s)

    def load(self):
        def log_url(url_s: str, allowed_or_forbidden):
            try:
                with open('history.txt', 'a') as hf:
                    hf.write('%s %s\n' % (allowed_or_forbidden, url_s))
            except IOError:
                pass

        url = QUrl.fromUserInput(self.addressLineEdit.text())
        if url.isValid():
            self.webEngineView.load(url)
            log_url(url.toString(), 'allowed')
        else:
            log_url(url.toString(), 'forbidden')

    def back(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Back)

    def forward(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Forward)

    def url_changed(self, url):
        self.addressLineEdit.setText(url.toString())


def unify_url(url):
    if url.startswith('https://') or url.startswith('http://') or url.startswith('file://'):
        return url
    return 'https://' + url


if __name__ == '__main__':
    app = QApplication(sys.argv)
    URL = 'https://ya.ru/' if len(sys.argv) == 1 else unify_url(sys.argv[-1])
    mainWin = MainWindow(URL)
    availableGeometry = mainWin.screen().availableGeometry()
    mainWin.resize(availableGeometry.width() * 2 / 3, availableGeometry.height() * 5 / 6)
    mainWin.show()
    sys.exit(app.exec())
