# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *

from anki.hooks import addHook

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def testFunction():
    # get the number of cards in the current collection, which is stored in
    # the main window
    cardCount = mw.col.cardCount()
    # show a message box
    showInfo("Card count: %d" % cardCount)



def load():
    # create a new menu item, "test"
    action = QAction("Test", mw)
    # set it to call testFunction when it's clicked
    action.triggered.connect(testFunction)
    # and add it to the tools menu
    mw.form.menuTools.addAction(action)

    from .hooks import Editor
    from .japanese import Content

    config = mw.addonManager.getConfig(__name__)
    content = Content(config)
    editor = Editor(config, content)

    addHook('editFocusLost', editor.onFocusLost)
