
# NOTE: 
#  For using gmail you need to enable imap [link]()
#  and for enabling login from "less secure apps", enable that using: [link](https://myaccount.google.com/lesssecureapps)

from PyQt5.QtCore import QThread, QUrl, QSize, Qt, QProcess
# from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtGui import QIcon, QColor, QFont, QKeySequence, QTransform, QTextCharFormat, QRegExpValidator, QSyntaxHighlighter, QFontDatabase, QWindow
from PyQt5.QtWidgets import QPushButton, QWidget, QLineEdit, QMainWindow, QHBoxLayout, QVBoxLayout, QGridLayout, QPlainTextEdit, QSizePolicy, QTextEdit, QToolButton, QTabBar, QLabel, QSplitter, QTabWidget, QFrame, QGraphicsDropShadowEffect
try:
    from FigUI.assets.Linker import FigLinker
    from FigUI.subSystem.Email.backend import IMapMailHandler
except ImportError:
    from .backend import IMapMailHandler
    from ...assets.Linker import FigLinker

class FigEmailClient(QWidget):
    '''A simple e-mail client.'''
    def __init__(self, parent=None, imap_url: str="imap.gmail.com"):
        # dummy layout (to sort of set Central Widget)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        super(FigEmailClient, self).__init__(parent)
        # backend for mailing operations.
        print("creating mailer backend")
        self._mailer_backend = IMapMailHandler(imap_url)
        # the main view/widget of the mail client UI.
        print("created mailer backend")
        self.view = QSplitter(Qt.Horizontal)
        self.folderTree = self.initInboxes(self.view) 
        self.view.addWidget(self.folderTree)
        # self.view.addWidget(self.mailView)
        self.linker = FigLinker(__file__, "../../../assets")
        # background with gradient.
        self.bgStyle = "url('/home/atharva/GUI/FigUI/FigUI/assets/icons/email/bg_texture2.png');"
        # f"qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #292929, stop : 0.10 #484848, stop: 0.5 #505050, stop : 0.9 #484848, stop : 1 #292929);"
        # add the main view to the dummy layout.
        self.menu = self.initMailMenu()
        layout.addWidget(self.menu)
        layout.addWidget(self.view)    
        self.setLayout(layout)
        print(self.linker.icon("email/comfort_view.svg"))
        if parent:
            parent.setWindowOpacity(1)
        glowEffect = QGraphicsDropShadowEffect()
        glowEffect.setBlurRadius(50)
        glowEffect.setOffset(30,0)
        glowEffect.setColor(QColor(160, 32, 240))
        self.menu.setGraphicsEffect(glowEffect)

    @property
    def imap_url(self):
        return self._mailer_backend.imap_url

    def initInboxes(self, parent=None):
        '''return folder tree for sections of the inbox.'''
        inboxes = QWidget(parent)
        inboxes
        
        return inboxes

    def initFolderMenu(self):
        '''create folder menu.'''
        return QWidget()

    def initMailMenu(self):
        '''create the top main menu.'''
        mailMenu = QTabWidget()
        # add logo for fig mail.
        mailMenu.addTab(QWidget(), self.linker.FigIcon("sidebar/email.png"), "")
        # file menu tab.
        fileMenu = self.initFileMenu()
        mailMenu.addTab(fileMenu, "\t\t\t\t\t\tFile\t\t\t\t\t\t")
        # home menu tab.
        homeMenu = self.initHomeMenu()
        mailMenu.addTab(homeMenu, "\t\t\t\t\t\tHome\t\t\t\t\t\t")
        # folder menu tab.
        folderMenu = self.initFolderMenu()
        mailMenu.addTab(folderMenu, "\t\t\t\t\t\tFolder\t\t\t\t\t\t")
        # view layout tab.
        viewMenu = self.initViewMenu()
        mailMenu.addTab(viewMenu, "\t\t\t\t\t\tView\t\t\t\t\t\t")
        # help tab.
        helpMenu = self.initHelpMenu()
        mailMenu.addTab(helpMenu, "\t\t\t\t\t\tHelp\t\t\t\t\t\t")
        # tell me what to do.
        mailMenu.addTab(QWidget(), self.linker.FigIcon("email/help.svg"), "Tell me what you want to do")
        # mailMenu.setObjectName("MailMenu")
        mailMenu.setStyleSheet('''
            QTabWidget {
                background: #484848;
                color: #000;
                border: 0px;
            }
            QTabWidget::pane {
                background: #484848;
                border: 0px;
            }
            QTabBar {
                background: #484848;
                border: 0px;
            }
            QTabBar::tab {
                color: #fff;
                border: 0px;
                margin: 0px;
                padding: 0px;
                padding-top: 5px;
                padding-left: 9px;
                padding-right: 9px;
                padding-bottom: 5px;
                background: #292929;
            }
            QTabBar::tab:hover {
                /* background: qlineargradient(x1 : 0, y1 : 1, x2 : 0, y2 : 0, stop : 0.0 #70121c, stop : 0.6 #b31f2f, stop : 0.8 #de2336); */
                background: purple;
                color: #fff;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 2, stop : 0.0 #3f0c5e, stop : 0.99 purple); 
                color: #fff;
                /* font-weight: bold; */
                padding-top: 5px;
                padding-left: 9px;
                padding-right: 9px;
                padding-bottom: 5px;
            }
            QToolTip { 
                color: #fff;
                border: 0px;
            }''')
        # mailMenu.tabBar().setTabBackgroundColor(3, QColor(235, 235, 235, 235))
        mailMenu.setCurrentIndex(1)
        mailMenu.setFixedHeight(125)
        # mailMenu.tabBar().setTabButton(3, QTabBar.RightSide, self.helpBtn)
        return mailMenu

    @property
    def helpBtn(self):
        helpBtn = QToolButton(self)
        helpBtn.setText("Need help with something?")
        helpBtn.setStyleSheet('''
            QToolButton {
                border: 0px;
                color: #484848;
                background: #bbb; 
            }''')
        helpBtn.setIcon(self.linker.FigIcon("email/help.svg"))
        helpBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        return helpBtn 

    def initHelpMenu(self):
        return QWidget()

    def initFileMenu(self):
        '''create file menu'''
        fileMenu = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        # 
        QToolButton(fileMenu)
        
        fileMenu.setLayout(layout)

        return fileMenu

    def initHomeMenu(self):
        '''create home menu.'''
        homeMenu = QWidget()
        homeMenu.setObjectName("HomeMenu")
        homeMenu.setStyleSheet('''
            QToolButton {
                color: #fff;
                background: #292929;
                font-size: 14px;
                font-weight: bold;
            }
            QWidget#HomeMenu {
                padding-top: 5px;
                padding-bottom: 5px;
            }
            QToolButton:hover {
                border: 0px;
                background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 2, stop : 0.0 #3f0c5e, stop : 0.99 purple); 
            }
            QWidget#MiscGroup {
                background: '''+self.bgStyle+'''
                color: #000;
            }
            QWidget#NewGroup {
                background: '''+self.bgStyle+'''
                color: #000;
            }
            QWidget#NewToolbar {
                background: '''+self.bgStyle+'''
                color: #000;
            }
            QWidget#DelGroup {
                background: '''+self.bgStyle+'''
                color: #000;
            }
            QWidget#DelToolbar {
                background: '''+self.bgStyle+'''
                color: #000;
            }
            QWidget#DelRibbon {
                background: '''+self.bgStyle+'''
                color: #000;
            }
            QWidget#StretchGroup {
                background: '''+self.bgStyle+'''
                color: #000;
            }
            QWidget#RespGroup {
                background: '''+self.bgStyle+'''
                color: #000;
            }
            QWidget#FindGroup {
                background: '''+self.bgStyle+'''
                color: #000;
            }
            QWidget#UtilGroup {
                background: '''+self.bgStyle+'''
                color: #000;
            }
            QLabel {
                padding: 5px;
                background: transparent;
                font-size: 14px;
                color: violet;
            }''')
        self.transStyle = '''
            QToolButton {
                color: #fff;
                border: 0px;
                padding-top: 2px;
                padding-bottom: 2px;
                background: '''+self.bgStyle+''';
                font-size: 14px;
                font-weight: bold;
            }
            QToolButton:hover {
                background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 2, stop : 0.0 #3f0c5e, stop : 0.99 purple); 
            }
        '''
        # contains toolbar sets.
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # command groups.
        newGroup = QWidget()
        newGroup.setObjectName("NewGroup")
        newGroupLayout = QVBoxLayout()
        newGroupLayout.setSpacing(0)
        newGroupLayout.setContentsMargins(0, 0, 0, 0)
        
        delGroup = QWidget()
        delGroup.setObjectName("DelGroup")
        delGroupLayout = QVBoxLayout()
        delGroupLayout.setSpacing(0)
        delGroupLayout.setContentsMargins(0, 0, 0, 0)

        addGroup = QWidget()
        addGroup.setObjectName("AddGroup")
        addGroupLayout = QVBoxLayout()
        addGroupLayout.setSpacing(0)
        addGroupLayout.setContentsMargins(0, 0, 0, 0)

        utilGroup = QWidget()
        utilGroup.setObjectName("UtilGroup")
        utilGroupLayout = QVBoxLayout()
        utilGroupLayout.setSpacing(0)
        utilGroupLayout.setContentsMargins(0, 0, 0, 0)        

        respGroup = QWidget()
        respGroup.setObjectName("RespGroup")
        respGroupLayout = QVBoxLayout()
        respGroupLayout.setSpacing(0)
        respGroupLayout.setContentsMargins(0, 0, 0, 0)

        findGroup = QWidget()
        findGroup.setObjectName("FindGroup")
        findGroupLayout = QVBoxLayout()
        findGroupLayout.setSpacing(0)
        findGroupLayout.setContentsMargins(0, 0, 0, 0)

        miscGroup = QWidget()
        miscGroup.setObjectName("MiscGroup")
        miscGroupLayout = QGridLayout()
        miscGroupLayout.setSpacing(0)
        miscGroupLayout.setContentsMargins(0, 0, 0, 0)

        # toolbars
        newToolbar = QWidget()
        newToolbar.setObjectName("NewToolbar")
        newToolbarLayout = QHBoxLayout()
        newToolbarLayout.setSpacing(0)
        newToolbarLayout.setContentsMargins(0, 0, 0, 0)

        delToolbar = QWidget()
        delToolbar.setObjectName("DelToolbar")
        delToolbarLayout = QHBoxLayout()
        delToolbarLayout.setSpacing(0)
        delToolbarLayout.setContentsMargins(0, 0, 0, 0)

        # ribbons
        delRibbon = QWidget()
        delRibbon.setObjectName("DelRibbon")
        delRibbonLayout = QVBoxLayout()
        delRibbonLayout.setSpacing(0)
        delRibbonLayout.setContentsMargins(0, 0, 0, 0)

        newEmailBtn = QToolButton(newToolbar)
        newEmailBtn.setIcon(self.linker.FigIcon("email/new_mail.svg"))
        newEmailBtn.setIconSize(QSize(25,25))
        newEmailBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        newEmailBtn.setText("New\nEmail")
        newToolbarLayout.addWidget(newEmailBtn)

        newRulesBtn = QToolButton(newToolbar)
        newRulesBtn.setIcon(self.linker.FigIcon("email/rules_add.svg"))
        newRulesBtn.setIconSize(QSize(25,25))
        newRulesBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        newRulesBtn.setText("Add\nRule")
        newToolbarLayout.addWidget(newRulesBtn)

        newTagBtn = QToolButton(newToolbar)
        newTagBtn.setIcon(self.linker.FigIcon("email/add_tag.svg"))
        newTagBtn.setIconSize(QSize(25,25))
        newTagBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        newTagBtn.setText("Add\nTag")
        newToolbarLayout.addWidget(newTagBtn)

        remTagBtn = QToolButton(delToolbar)
        remTagBtn.setIcon(self.linker.FigIcon("email/remove_tag.svg"))
        remTagBtn.setIconSize(QSize(14,14))
        remTagBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        remTagBtn.setText(" Tag ")
        remTagBtn.setToolTip("Remove tag")
        remTagBtn.setFixedWidth(60)
        remTagBtn.setStyleSheet(self.transStyle)
        delRibbonLayout.addWidget(remTagBtn)
        # junk button to move to spam
        junkBtn = QToolButton(delToolbar) 
        junkBtn.setIcon(self.linker.FigIcon("email/email_cancel.svg"))
        junkBtn.setIconSize(QSize(14,14))
        junkBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        junkBtn.setText(" Junk")
        junkBtn.setToolTip("Move mail to spam")
        junkBtn.setFixedWidth(60)
        junkBtn.setStyleSheet(self.transStyle)
        delRibbonLayout.addWidget(junkBtn)
        # button to delete attachment.
        delAttachBtn = QToolButton(delToolbar) 
        delAttachBtn.setIcon(self.linker.FigIcon("email/remove_attachment.svg"))
        delAttachBtn.setIconSize(QSize(14,14))
        delAttachBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        delAttachBtn.setText(" File")
        delAttachBtn.setToolTip("Remove attachment/file")
        delAttachBtn.setFixedWidth(60)
        delAttachBtn.setStyleSheet(self.transStyle)
        delRibbonLayout.addWidget(delAttachBtn)
        delRibbon.setLayout(delRibbonLayout)
        delToolbarLayout.addWidget(delRibbon)

        delBtn = QToolButton(delToolbar)
        delBtn.setIcon(self.linker.FigIcon("email/delete.svg"))
        delBtn.setIconSize(QSize(25,25))
        delBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        delBtn.setText("Delete")
        delToolbarLayout.addWidget(delBtn)

        archiveBtn = QToolButton(delToolbar)
        archiveBtn.setIcon(self.linker.FigIcon("email/email_archive.svg"))
        archiveBtn.setIconSize(QSize(25,25))
        archiveBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        archiveBtn.setText("Archive")
        delToolbarLayout.addWidget(archiveBtn)

        newAttachBtn = QToolButton(newToolbar)
        newAttachBtn.setIcon(self.linker.FigIcon("email/add_attachment.svg"))
        newAttachBtn.setIconSize(QSize(25,25))
        newAttachBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        newAttachBtn.setText("Attach\nFile")
        newToolbarLayout.addWidget(newAttachBtn)
        
        replyBtn = QToolButton(respGroup)
        replyBtn.setIcon(self.linker.FigIcon("email/reply.svg"))   
        replyBtn.setIconSize(QSize(16,16))
        replyBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        replyBtn.setText(" Reply")
        replyBtn.setFixedWidth(90)
        replyBtn.setStyleSheet(self.transStyle)
        respGroupLayout.addWidget(replyBtn)

        replyAllBtn = QToolButton(respGroup)
        replyAllBtn.setIcon(self.linker.FigIcon("email/reply_all.svg"))   
        replyAllBtn.setIconSize(QSize(16,16))
        replyAllBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        replyAllBtn.setText(" Reply All")
        replyAllBtn.setFixedWidth(90)
        replyAllBtn.setStyleSheet(self.transStyle)
        respGroupLayout.addWidget(replyAllBtn)

        forwardBtn = QToolButton(respGroup)
        forwardBtn.setIcon(self.linker.FigIcon("email/forward.svg"))   
        forwardBtn.setIconSize(QSize(16,16))
        forwardBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        forwardBtn.setText(" Forward")
        forwardBtn.setFixedWidth(90)
        forwardBtn.setStyleSheet(self.transStyle)
        respGroupLayout.addWidget(forwardBtn)

        searchBar = QLineEdit(findGroup)
        searchBar.setPlaceholderText("Search People")
        searchBar.setFixedWidth(200)
        searchBar.setStyleSheet("background: #fff; color: #000;")
        searchBar.setFixedHeight(22)
        findGroupLayout.addWidget(searchBar)

        contactsBtn = QToolButton(findGroup)
        contactsBtn.setIcon(self.linker.FigIcon("email/contacts.svg"))
        contactsBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        contactsBtn.setIconSize(QSize(16,16))
        contactsBtn.setText("Address Book")
        contactsBtn.setFixedWidth(150)
        contactsBtn.setStyleSheet(self.transStyle)
        findGroupLayout.addWidget(contactsBtn)
        
        phishingBtn = QToolButton(miscGroup)
        phishingBtn.setIcon(self.linker.FigIcon("email/report_phishing.svg"))
        # phishingBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        phishingBtn.setIconSize(QSize(20,20))
        # phishingBtn.setText("Phishing")

        starBtn = QToolButton(miscGroup)
        starBtn.setIcon(self.linker.FigIcon("email/star.svg"))
        starBtn.setIconSize(QSize(20,20))

        spamBtn = QToolButton(miscGroup)
        spamBtn.setIcon(self.linker.FigIcon("email/report_spam.svg"))
        # spamBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        spamBtn.setIconSize(QSize(20,20))
        # spamBtn.setText("Spam")
        importantBtn = QToolButton(miscGroup)
        importantBtn.setIcon(self.linker.FigIcon("email/important.svg"))
        # importantBtn.setToolButtonStyle(sQt.ToolButtonTextUnderIcon)
        importantBtn.setIconSize(QSize(20,20))
        # importantBtn.setText("Important")
        flagBtn = QToolButton(miscGroup)
        flagBtn.setIcon(self.linker.FigIcon("email/mark_follow_up.svg"))
        flagBtn.setIconSize(QSize(20,20))
        # flagBtn.setToolButtonStyle(Qt.ToolBsuttonTextUnderIcon)
        # flagBtn.setText("Follow Up")
        unflagBtn = QToolButton(miscGroup)
        unflagBtn.setIcon(self.linker.FigIcon("email/unmark_follow_up.svg"))
        unflagBtn.setIconSize(QSize(20,20))
        # unflagBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        # unflagBtn.setText("Follow Up")
        miscGroupLayout.addWidget(phishingBtn, 0, 0)
        miscGroupLayout.addWidget(spamBtn, 0, 1)
        miscGroupLayout.addWidget(starBtn, 1, 0)
        miscGroupLayout.addWidget(importantBtn, 1, 1)
        miscGroupLayout.addWidget(flagBtn, 2, 0)
        miscGroupLayout.addWidget(unflagBtn, 2, 1)

        templateBtn = QToolButton(utilGroup)
        templateBtn.setIcon(self.linker.FigIcon("email/template.svg"))
        templateBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        templateBtn.setIconSize(QSize(18,18))
        templateBtn.setText("Template")
        templateBtn.setFixedWidth(70)
        templateBtn.setStyleSheet(self.transStyle)
        utilGroupLayout.addWidget(templateBtn)

        ruleBtn = QToolButton(utilGroup)
        ruleBtn.setIcon(self.linker.FigIcon("email/rules.svg"))
        ruleBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        ruleBtn.setIconSize(QSize(18,18))
        ruleBtn.setText("Rules")
        ruleBtn.setFixedWidth(70)
        ruleBtn.setStyleSheet(self.transStyle)
        utilGroupLayout.addWidget(ruleBtn)

        filterBar = self.initFilterBar()
        findGroupLayout.addWidget(filterBar)

        # set toolbar layouts.
        newToolbar.setLayout(newToolbarLayout)
        delToolbar.setLayout(delToolbarLayout)

        # build tool groups.
        newGroupLayout.addWidget(newToolbar)
        newGroupLabel = QLabel("new", parent=newGroup)
        newGroupLabel.setAlignment(Qt.AlignCenter)
        newGroupLayout.addWidget(newGroupLabel)

        delGroupLayout.addWidget(delToolbar)
        delGroupLabel = QLabel("delete", parent=delGroup)
        delGroupLabel.setAlignment(Qt.AlignCenter)
        delGroupLayout.addWidget(delGroupLabel)
        
        respGroupLabel = QLabel("respond", parent=respGroup)
        respGroupLabel.setAlignment(Qt.AlignCenter)
        respGroupLayout.addWidget(respGroupLabel)

        findGroupLabel = QLabel("find", parent=findGroup)
        findGroupLabel.setAlignment(Qt.AlignCenter)
        findGroupLayout.addWidget(findGroupLabel)

        utilGroupLabel = QLabel("", parent=utilGroup)
        utilGroupLayout.setAlignment(Qt.AlignCenter)
        # utilGroupLayout.addWidget(utilGroupLabel)
        # set container layouts.
        newGroup.setLayout(newGroupLayout)
        newGroup.setFixedWidth(200)
        delGroup.setLayout(delGroupLayout)
        delGroup.setFixedWidth(190)
        respGroup.setLayout(respGroupLayout)
        respGroup.setFixedWidth(90)
        findGroup.setLayout(findGroupLayout)
        findGroup.setFixedWidth(200)
        utilGroup.setLayout(utilGroupLayout)
        utilGroup.setFixedWidth(70)
        miscGroup.setLayout(miscGroupLayout)
        miscGroup.setFixedWidth(65)
        stretchGroup = QWidget()
        stretchGroup.setObjectName("StretchGroup")
        emailGroup = self.initEmailPanel()
        # emailGroup.setFixedWidth(200)
        stretchGroup.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # build menu layout.
        layout.addWidget(newGroup)
        layout.addWidget(self.addSpacer(10))
        layout.addWidget(delGroup)
        layout.addWidget(self.addSpacer(10))
        layout.addWidget(respGroup)
        layout.addWidget(self.addSpacer(10))
        layout.addWidget(findGroup)
        layout.addWidget(self.addSpacer(10))
        layout.addWidget(utilGroup)
        layout.addWidget(self.addSpacer(10))
        layout.addWidget(miscGroup)
        layout.addWidget(self.addSpacer(10))
        layout.addWidget(emailGroup)
        layout.addWidget(stretchGroup)
        # set menu layout.
        homeMenu.setLayout(layout)

        return homeMenu

    def initFilterBar(self):
        '''create filter bar.'''
        filterBar = QWidget()
        filterBar.setObjectName("FilterBar")
        
        filterBarLayout = QHBoxLayout()
        filterBarLayout.setSpacing(0)
        filterBarLayout.setContentsMargins(0, 0, 0, 0)

        filterBar.setStyleSheet('''
            QToolButton {
                color: #fff;
                background: #292929;
                font-size: 14px;
                font-weight: bold;
            }
            QWidget#FilterBar {
                padding-top: 5px;
                padding-bottom: 5px;
                background: '''+self.bgStyle+'''
            }
            QToolButton:hover {
                border: 0px;
                background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 2, stop : 0.0 #3f0c5e, stop : 0.99 purple); 
            }''')
        btnSize = QSize(18,18)
        filtBtn = QToolButton(self)
        filtBtn.setIcon(self.linker.FigIcon("email/filter.svg"))
        filtBtn.setIconSize(btnSize)
        filtBtn.setToolTip("apply filters")
        filtBtn.setStyleSheet(self.transStyle)
        filterBarLayout.addWidget(filtBtn)

        filtAddBtn = QToolButton(self)
        filtAddBtn.setIcon(self.linker.FigIcon("email/filter_add.svg"))
        filtAddBtn.setIconSize(btnSize)
        filtAddBtn.setToolTip("add filter")
        filtAddBtn.setStyleSheet(self.transStyle)
        filterBarLayout.addWidget(filtAddBtn)

        filtNegBtn = QToolButton(self)
        filtNegBtn.setIcon(self.linker.FigIcon("email/filter_negate.svg"))
        filtNegBtn.setIconSize(btnSize)
        filtNegBtn.setToolTip("negate filter")
        filtNegBtn.setStyleSheet(self.transStyle)
        filterBarLayout.addWidget(filtNegBtn)

        filtEditBtn = QToolButton(self)
        filtEditBtn.setIcon(self.linker.FigIcon("email/filter_edit.svg"))
        filtEditBtn.setIconSize(btnSize)
        filtEditBtn.setToolTip("edit filter")
        filtEditBtn.setStyleSheet(self.transStyle)
        filterBarLayout.addWidget(filtEditBtn)

        filtDelBtn = QToolButton(self)
        filtDelBtn.setIcon(self.linker.FigIcon("email/filter_delete.svg"))
        filtDelBtn.setIconSize(btnSize)
        filtDelBtn.setToolTip("remove all filters")
        filtDelBtn.setStyleSheet(self.transStyle)
        filterBarLayout.addWidget(filtDelBtn)

        filtReadBtn = QToolButton(self)
        filtReadBtn.setIcon(self.linker.FigIcon("email/filter_read.svg"))
        filtReadBtn.setIconSize(btnSize)
        filtReadBtn.setToolTip("filter read emails")
        filtReadBtn.setStyleSheet(self.transStyle)
        filterBarLayout.addWidget(filtReadBtn)

        filtImpBtn = QToolButton(self)
        filtImpBtn.setIcon(self.linker.FigIcon("email/filter_important.svg"))
        filtImpBtn.setIconSize(btnSize)
        filtImpBtn.setToolTip("filter important emails")
        filtImpBtn.setStyleSheet(self.transStyle)
        filterBarLayout.addWidget(filtImpBtn)

        filtFavBtn = QToolButton(self)
        filtFavBtn.setIcon(self.linker.FigIcon("email/filter_favourite.svg"))
        filtFavBtn.setIconSize(btnSize)
        filtFavBtn.setToolTip("filter favourited emails")
        filtFavBtn.setStyleSheet(self.transStyle)
        filterBarLayout.addWidget(filtFavBtn)

        filterBar.setLayout(filterBarLayout)

        return filterBar

    def initViewMenu(self):
        '''create mail view menu.'''
        viewMenu = QWidget()
        viewMenu.setObjectName("ViewMenu")
        viewMenu.setStyleSheet('''
            QToolButton {
                color: #fff;
                background: #292929;
                font-size: 14px;
                font-weight: bold;
            }
            QWidget#ViewMenu {
                padding-top: 5px;
                padding-bottom: 5px;
            }
            QToolButton:hover {
                border: 0px;
                background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 2, stop : 0.0 #3f0c5e, stop : 0.99 purple); 
            }
            QWidget#ViewContainer {
                background: '''+self.bgStyle+'''
                color: #000;
            }
            QWidget#SplitContainer {
                background: '''+self.bgStyle+'''
                color: #000;
            }
            QWidget#AttachContainer {
                background: '''+self.bgStyle+'''
                color: #000;
            }
            QWidget#SplitToolbar {
                background: '''+self.bgStyle+'''
                color: #000;
            }
            QWidget#ViewToolbar {
                background: '''+self.bgStyle+'''
                color: #000;
            }
            QWidget#StretchContainer {
                background: '''+self.bgStyle+'''
                color: #000;
            }
            QWidget#SortContainer {
                background: '''+self.bgStyle+'''
                color: #000;
            }
            QLabel {
                padding: 5px;
                background: transparent;
                font-size: 14px;
                color: violet;
            }''')
        # contains toolbar sets.
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # containers 
        viewContainer = QWidget()
        viewContainer.setObjectName("ViewContainer")
        viewContainerLayout = QVBoxLayout()
        viewContainerLayout.setSpacing(0)
        viewContainerLayout.setContentsMargins(0, 0, 0, 0)
        
        sortContainer = QWidget()
        sortContainer.setObjectName("SortContainer")
        sortContainerLayout = QVBoxLayout()
        sortContainerLayout.setSpacing(0)
        sortContainerLayout.setContentsMargins(0, 0, 0, 0)
        
        attachContainer = QWidget()
        attachContainer.setObjectName("AttachContainer")
        attachContainerLayout = QVBoxLayout()
        attachContainerLayout.setSpacing(0)
        attachContainerLayout.setContentsMargins(0, 0, 0, 0)

        splitContainer = QWidget()
        splitContainer.setObjectName("SplitContainer")
        splitContainerLayout = QVBoxLayout()
        splitContainerLayout.setSpacing(0)
        splitContainerLayout.setContentsMargins(0, 0, 0, 0)

        # toolbars
        viewToolbar = QWidget()
        viewToolbar.setObjectName("ViewToolbar")
        viewToolbarLayout = QHBoxLayout()
        viewToolbarLayout.setSpacing(0)
        viewToolbarLayout.setContentsMargins(0, 0, 0, 0)

        splitToolbar = QWidget()
        splitToolbar.setObjectName("SplitToolbar")
        splitToolbarLayout = QHBoxLayout()
        splitToolbarLayout.setSpacing(0)
        splitToolbarLayout.setContentsMargins(0, 0, 0, 0)

        comfortBtn = QToolButton(viewToolbar)
        comfortBtn.setIcon(self.linker.FigIcon("email/comfort_view.svg"))
        comfortBtn.setIconSize(QSize(25,25))
        comfortBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        comfortBtn.setText("comfort")
        viewToolbarLayout.addWidget(comfortBtn)
        
        defaultBtn = QToolButton(viewToolbar)
        defaultBtn.setIcon(self.linker.FigIcon("email/default_view.svg"))
        defaultBtn.setIconSize(QSize(25,25))
        defaultBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        defaultBtn.setText("default")
        viewToolbarLayout.addWidget(defaultBtn)
        
        compactBtn = QToolButton(viewToolbar)
        compactBtn.setIcon(self.linker.FigIcon("email/compact_view.svg"))
        compactBtn.setIconSize(QSize(25,25))
        compactBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        compactBtn.setText("compact")
        viewToolbarLayout.addWidget(compactBtn)

        sortUpBtn = QToolButton(sortContainer)
        sortUpBtn.setIcon(self.linker.FigIcon("email/sort_ascending.svg"))
        sortUpBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        sortUpBtn.setIconSize(QSize(18,18))
        sortUpBtn.setText("A to Z")

        sortDownBtn = QToolButton(sortContainer)
        sortDownBtn.setIcon(self.linker.FigIcon("email/sort_descending.svg"))
        sortDownBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        sortDownBtn.setIconSize(QSize(18,18))
        sortDownBtn.setText("Z to A")
        
        splitViewBtn = QToolButton(splitToolbar) 
        splitViewBtn.setIcon(self.linker.FigIcon("email/split_view.svg"))
        splitViewBtn.setIconSize(QSize(25,25))
        splitViewBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        splitViewBtn.setText("split")
        splitToolbarLayout.addWidget(splitViewBtn)

        splitVerticalBtn = QToolButton(splitToolbar) 
        splitVerticalBtn.setIcon(self.linker.FigIcon("email/vertical_split.svg"))
        splitVerticalBtn.setIconSize(QSize(25,25))
        splitVerticalBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        splitVerticalBtn.setText("vertical")
        splitToolbarLayout.addWidget(splitVerticalBtn)

        splitHorizontalBtn = QToolButton(splitToolbar) 
        splitHorizontalBtn.setIcon(self.linker.FigIcon("email/horizontal_split.svg"))
        splitHorizontalBtn.setIconSize(QSize(25,25))
        splitHorizontalBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        splitHorizontalBtn.setText("horizontal")
        splitToolbarLayout.addWidget(splitHorizontalBtn)

        viewTagsBtn = QToolButton(attachContainer)
        viewTagsBtn.setIcon(self.linker.FigIcon("email/view_tags.svg"))
        viewTagsBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        viewTagsBtn.setIconSize(QSize(18,18))
        viewTagsBtn.setText("tags")

        viewAttachBtn = QToolButton(attachContainer)
        viewAttachBtn.setIcon(self.linker.FigIcon("email/view_attachments.svg"))
        viewAttachBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        viewAttachBtn.setIconSize(QSize(18,18))
        viewAttachBtn.setText("attachments")

        # set toolbar layouts.
        viewToolbar.setLayout(viewToolbarLayout)
        splitToolbar.setLayout(splitToolbarLayout)

        # build container layouts.
        viewContainerLayout.addWidget(viewToolbar)
        viewContainerLabel = QLabel("view layouts", parent=viewContainer)
        viewContainerLabel.setAlignment(Qt.AlignCenter)
        viewContainerLayout.addWidget(viewContainerLabel)

        sortContainerLayout.addWidget(sortUpBtn)
        sortContainerLayout.addWidget(sortDownBtn)
        sortContainerLabel = QLabel("sort mail", parent=sortContainer)
        sortContainerLabel.setAlignment(Qt.AlignCenter)
        sortContainerLayout.addWidget(sortContainerLabel)
        
        splitContainerLayout.addWidget(splitToolbar)
        splitContainerLabel = QLabel("split views", parent=splitContainer)
        splitContainerLabel.setAlignment(Qt.AlignCenter)
        splitContainerLayout.addWidget(splitContainerLabel)
        
        attachContainerLayout.addWidget(viewTagsBtn)
        attachContainerLayout.addWidget(viewAttachBtn)
        attachContainerLabel = QLabel("artefacts", parent=attachContainer)
        attachContainerLabel.setAlignment(Qt.AlignCenter)
        attachContainerLayout.addWidget(attachContainerLabel)

        # set container layouts.
        viewContainer.setLayout(viewContainerLayout)
        viewContainer.setFixedWidth(200)
        sortContainer.setLayout(sortContainerLayout)
        sortContainer.setFixedWidth(80)
        splitContainer.setLayout(splitContainerLayout)
        splitContainer.setFixedWidth(200)
        attachContainer.setLayout(attachContainerLayout)
        attachContainer.setFixedWidth(140)
        stretchContainer = QWidget()
        stretchContainer.setObjectName("StretchContainer")
        stretchContainer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # build menu layout.
        layout.addWidget(viewContainer)
        layout.addWidget(self.addSpacer(10))
        layout.addWidget(sortContainer)
        layout.addWidget(self.addSpacer(10))
        layout.addWidget(splitContainer)
        layout.addWidget(self.addSpacer(10))
        layout.addWidget(attachContainer)
        layout.addWidget(stretchContainer)
        # set menu layout.
        viewMenu.setLayout(layout)

        return viewMenu

    def initEmailPanel(self):
        emailPanel = QWidget()
        emailPanel.setStyleSheet('''
            QToolButton {
                color: #fff;
                background: #292929;
                font-size: 14px;
                font-weight: bold;
            }
            QWidget {
                background: '''+self.bgStyle+'''
                padding-top: 5px;
                padding-bottom: 5px;
            }
            QToolButton:hover {
                border: 0px;
                background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 2, stop : 0.0 #3f0c5e, stop : 0.99 purple); 
            }''')
        panelLayout = QVBoxLayout()
        panelLayout.setContentsMargins(0, 0, 0, 0)
        panelLayout.setSpacing(0)
        # top and bottom ribbons.
        topRibbon = QWidget()
        topLayout = QHBoxLayout()
        topLayout.setSpacing(0)
        topLayout.setContentsMargins(0, 0, 0, 0)
        bottomRibbon = QWidget()
        bottomLayout = QHBoxLayout()
        bottomLayout.setSpacing(0)
        bottomLayout.setContentsMargins(0, 0, 0, 0)
        # set style of top and bootm ribbons. 
        topRibbon.setLayout(topLayout)
        bottomRibbon.setLayout(bottomLayout)
        panelLayout.addWidget(topRibbon)
        panelLayout.addWidget(bottomRibbon)
        emailPanel.setLayout(panelLayout)

        return emailPanel

    def addSpacer(self, width=10, background=None):
        if background is None: 
            background = self.bgStyle
        spacer = QFrame(self)
        spacer.setStyleSheet('''
            QFrame {
                border: 0px;
                background: '''+background+''';
            }
            QFrame::VLine{
                border: 1px;
            }''')
        spacer.setFrameShape(QFrame.VLine)
        spacer.setFrameShadow(QFrame.Sunken)
        spacer.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        spacer.setFixedWidth(width)

        return spacer

    def postMail(self):
        pass

    def loadMail(self):
        pass


if __name__ == '__main__':
    pass