import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon, QKeySequence, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QShortcut,
    QTabWidget,
    QWidget,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView


class Browser(QMainWindow):
    def __init__(self):
        super(Browser, self).__init__()

        # Destruction parent, children when close
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        # Show each page in each tab
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        # self.tabs.setStyleSheet(
        #     "QTabBar::close-button { image: url(images/close.png); subcontrol-position: right; }"
        #     "QTabBar::close-button:hover { background: #aaaaaa }"
        # )
        self.tabs.tabCloseRequested.connect(self.closeTab)

        self.page1 = QWidget()

        # Store all webview
        self.tabWebView = []

        # Store all url
        self.lNameLine = []

        # Add initial page with label "New Tab" to tab
        self.tabs.addTab(self.page1, "Google")

        self.tab1UI(self.page1)

        self.setWindowTitle("NBrowser")
        self.setCentralWidget(self.tabs)
        self.showMaximized()

        QShortcut(QKeySequence("Ctrl+T"), self, self.addTab)

    def addTab(self):
        newPage = QWidget()
        self.tabs.addTab(newPage, "Google")
        self.tab1UI(newPage)

        index = self.tabs.currentIndex()
        self.tabs.setCurrentIndex(index + 1)

    def closeTab(self, tabId):
        del self.lNameLine[tabId]
        del self.tabWebView[tabId]

        # Close window when close the last tab
        if self.tabs.count() == 1:
            self.close()
        else:
            self.tabs.removeTab(tabId)

    def goBack(self):
        index = self.tabs.currentIndex()
        self.tabWebView[index].back()

    def goNext(self):
        index = self.tabs.currentIndex()
        self.tabWebView[index].forward()

    def goRefresh(self):
        index = self.tabs.currentIndex()
        self.tabWebView[index].reload()

    def changePage(self):
        index = self.tabs.currentIndex()
        pageTitle = self.sender().title()[:15]
        self.tabs.setTabText(index, pageTitle)
        self.lNameLine[self.tabs.currentIndex()].setText(self.sender().url().url())

    def tab1UI(self, tabName):
        backButton = QPushButton("")
        backIcon = QIcon()
        backIcon.addPixmap(QPixmap("images/back.svg"))
        backButton.setIcon(backIcon)
        backButton.setFlat(True)
        backButton.clicked.connect(self.goBack)

        nextButton = QPushButton("")
        nextIcon = QIcon()
        nextIcon.addPixmap(QPixmap("images/next.svg"))
        nextButton.setIcon(nextIcon)
        nextButton.setFlat(True)
        nextButton.clicked.connect(self.goNext)

        refreshButton = QPushButton("")
        refreshIcon = QIcon()
        refreshIcon.addPixmap(QPixmap("images/refresh.svg"))
        refreshButton.setIcon(refreshIcon)
        refreshButton.setFlat(True)
        refreshButton.clicked.connect(self.goRefresh)

        # newTabButton = QToolButton()
        # newTabButton.setText("+")

        urlLine = QLineEdit()
        urlLine.returnPressed.connect(self.requestUrl)

        tabGrid = QGridLayout()
        tabGrid.setContentsMargins(0, 0, 0, 0)

        navigationFrame = QWidget()
        navigationFrame.setMaximumHeight(32)

        navigationGrid = QGridLayout(navigationFrame)
        navigationGrid.setSpacing(0)
        navigationGrid.setContentsMargins(0, 0, 0, 0)
        navigationGrid.addWidget(backButton, 0, 1)
        navigationGrid.addWidget(nextButton, 0, 2)
        navigationGrid.addWidget(refreshButton, 0, 3)
        navigationGrid.addWidget(urlLine, 0, 4)

        tabGrid.addWidget(navigationFrame)

        # htmlHead = (
        #     "<head><style>body{ background-color: #fff; }</style></head><body></body>"
        # )

        webView = QWebEngineView()
        # webView.setHtml(htmlHead)
        googleUrl = QUrl("https://www.google.com")
        webView.setUrl(googleUrl)
        webView.loadFinished.connect(self.changePage)

        frame = QFrame()
        frame.setFrameStyle(QFrame.Panel)

        gridLayout = QGridLayout(frame)
        gridLayout.setContentsMargins(0, 0, 0, 0)
        gridLayout.addWidget(webView, 0, 0, 1, 1)

        frame.setLayout(gridLayout)

        self.tabWebView.append(webView)

        self.tabWidget = QTabWidget()
        self.tabWidget.setCurrentWidget(webView)
        self.lNameLine.append(urlLine)

        tabGrid.addWidget(frame)
        tabName.setLayout(tabGrid)

    def requestUrl(self):
        if self.tabs.currentIndex() != -1:
            urlText = self.lNameLine[self.tabs.currentIndex()].text()

            if "http" not in urlText:
                self.lNameLine[self.tabs.currentIndex()].setText("https://" + urlText)

            url = QUrl(self.lNameLine[self.tabs.currentIndex()].text())

            if url.isValid():
                self.tabWebView[self.tabs.currentIndex()].load(url)
            else:
                print("Url not valid")
        else:
            print("No tabs open, open one first.")


def main():
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
