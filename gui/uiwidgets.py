"""
UI widgets.

NB: Naming conventions follow those used in other DirectObjects (camelCasing).
"""
import direct.gui.DirectGuiGlobals as DGG
from direct.gui.DirectGui import (DirectButton, DirectEntry, DirectFrame,
                                  DirectLabel, DirectOptionMenu, DirectSlider)
from direct.gui.DirectGuiBase import DirectGuiWidget
from direct.showbase.ShowBaseGlobal import aspect2d
from direct.showutil.Rope import Rope
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import (CardMaker, NodePath, PNMImage, Point3, TextNode,
                          Texture, Vec4)

import gui.config as cfg
from gui.geom2d import make_circle


def make_box_shadow(width, height, shadowSize, darkness=.5, resol=32):
    # Create grey box
    if width > height:
        resolX = int(resol * width / height)
        resolY = resol
    else:
        resolX = resol
        resolY = int(resol * height / width)
    image = PNMImage(resolX, resolY, 1)
    image.fill(darkness)
    # Expand with black border.
    borderX = int(2 * shadowSize * resolX)
    borderY = int(2 * shadowSize * resolY)
    image.expandBorder(borderX, borderX, borderY, borderY, Vec4(0))
    # Apply blur.
    image.gaussianFilter(shadowSize * resol)
    # Transfer to alpha and make image entirely black.
    image.addAlpha()
    image.copyChannel(image, 0, 3)
    image.fill(0)
    # Remove the shadow inside the box.
    for x in range(borderX, borderX+resolX):
        for y in range(borderY, borderY+resolY):
            image.setAlpha(x, y, 0)
    # Copy to 2D box.
    cm = CardMaker('card')
    cardX = width * (1 + 2*borderX/resolX) / 2   # slightly expand the card
    cardY = height * (1 + 2*borderY/resolY) / 2  # to see the shadow
    cm.setFrame(Vec4(-cardX, cardX, -cardY, cardY))
    card = NodePath(cm.generate())
    card.setTransparency(True)
    tex = Texture()
    tex.load(image)
    card.setTexture(tex)
    return card


def add_shadow_to_frame(frame, **shadowArgs):
    left, right, bottom, top = frame['frameSize']
    width = right - left
    height = top - bottom
    shadowPos = Point3((left + right) / 2, 0, (top + bottom) / 2)
    shadow = make_box_shadow(width, height, **shadowArgs)
    shadow.setPos(shadowPos)
    shadow.reparentTo(frame)


class DropdownMenu(DirectButton):
    def __init__(self, parent=None, **kw):
        # Define options. Why use this complicated system instead of a simple
        # list of keyword args? Some ideas:
        #  - when there is a LOT of keywords (as in e.g. matplotlib), this
        #  avoids bloating __init__ definitions while keeping the ability
        #  of defining default kw values and overriding them when inheriting.
        #  - this allows to attach each argument to a handler method in a
        #  coherent way.
        optiondefs = (
            # List of items to display on the popup menu
            ('items', [], self.setItems),
            # Background color to use to highlight popup menu items
            ('highlightColor', (.5, .5, .5, 1), None),
            # Text properties
            ('text_align', TextNode.ACenter, None),
            # Remove press effect because it looks a bit funny
            ('pressEffect', 0, DGG.INITOPT),
            # Shadow parameters
            ('shadowSize', 0, self.setShadow),
            # Make menu drop up instead of down
            ('dropUp', False, None),
        )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)
        # Initialize superclasses (the one we want here is DirectButton).
        super().__init__(parent)
        # This is created when you set the menu's items
        self.popupMenu = None
        # A big screen encompassing frame to catch the cancel clicks
        self.cancelFrame = self.createcomponent(
            'cancelframe', (), None,
            DirectFrame, (self,),
            frameSize=(-1, 1, -1, 1),
            relief=None,
            state='normal')
        # Make sure this is on top of all the other widgets
        self.cancelFrame.setBin('gui-popup', 0)
        self.cancelFrame.bind(DGG.B1PRESS, self.hidePopupMenu)
        # Default action on press is to show popup menu
        self.bind(DGG.B1PRESS, self.showPopupMenu)
        # Call option initialization functions
        # NB: calling this function in __init__ with the new subclass as an
        # argument is ESSENTIAL, yet poorly documented.
        # https://www.panda3d.org/forums/viewtopic.php?p=12111#p12111
        # NB2: for group_option-type options to be properly applied, you have
        # to create the components from that group _before_ this call.
        self.initialiseoptions(DropdownMenu)

    def _highlightItem(self, item):
        """Set frame color of highlighted item."""
        item['frameColor'] = self['highlightColor']

    def _unhighlightItem(self, item, frameColor):
        """Reset frame color of previously highlighted item."""
        item['frameColor'] = frameColor

    def hidePopupMenu(self, event=None):
        """Put away popup and cancel frame."""
        self.popupMenu.hide()
        self.cancelFrame.hide()

    def setItems(self):
        """Create new popup menu to reflect specified set of items

        Can be used via self['items'] = itemList

        """
        # Remove old component if it exits
        if self.popupMenu is not None:
            self.destroycomponent('popupMenu')
        # Create new component
        self.popupMenu = self.createcomponent(
            'popupMenu', (), None,
            DirectFrame, (self,),
            relief=self['relief'] or 'flat',
        )
        # Make sure it is on top of all the other gui widgets
        self.popupMenu.setBin('gui-popup', 0)
        if not self['items']:
            return
        # Variables to find the maximum extents of all items
        self.minX = self.minZ = float('inf')
        self.maxX = self.maxZ = -self.minX
        # Reason why we use _constructorKeywords[*] and not self[*] for all the
        # 'text_*' options: see DirectGuiBase.py's docstring.
        # In a nutshell: __getitem__ only queries _optionInfo, to which
        # '*_*'-options are not added -- they are left in _constructorKeywords
        # instead. They will be consumed as they are used, UNLESS 'component'
        # is a group name, which 'text' is, because DirectFrame says so.
        text_kw = {k: v[0] for k, v in self._constructorKeywords.items()
                   if k.startswith('text_')}
        text_kw['text_align'] = TextNode.ALeft
        # Create a new component for each item
        for ind, item in enumerate(self['items']):
            c = self.createcomponent(
                'item{}'.format(ind), (), 'item',
                DirectButton, (self.popupMenu,),
                text=item,
                pad=(.01, .01),
                command=self['command'],
                extraArgs=[item],
                relief=self['relief'] or 'flat',
                **text_kw
                )
            bounds = c.getBounds()
            if bounds[0] < self.minX:
                self.minX = bounds[0]
            if bounds[1] > self.maxX:
                self.maxX = bounds[1]
            if bounds[2] < self.minZ:
                self.minZ = bounds[2]
            if bounds[3] > self.maxZ:
                self.maxZ = bounds[3]
        # Calc max width and height
        self.maxWidth = self.maxX - self.minX
        self.maxHeight = self.maxZ - self.minZ
        # Adjust frame size for each item and bind actions to mouse events
        for i in range(ind+1):
            item = self.component('item{}'.format(i))
            # So entire extent of item's slot on popup is reactive to mouse
            item['frameSize'] = (self.minX, self.maxX, self.minZ, self.maxZ)
            # Move it to its correct position on the popup
            item.setPos(-self.minX, 0, -self.maxZ - i * self.maxHeight)
            item.bind(DGG.B1RELEASE, self.hidePopupMenu)
            # Highlight background when mouse is in item
            item.bind(
                DGG.WITHIN,
                lambda _, item=item: self._highlightItem(item)
            )
            # Restore specified color upon exiting
            fc = item['frameColor']
            item.bind(
                DGG.WITHOUT,
                lambda _, item=item, fc=fc: self._unhighlightItem(item, fc)
            )
        # Set popup menu frame size to encompass all items
        self.popupMenu['frameSize'] = (
                0, self.maxWidth, -self.maxHeight * (ind+1), 0)
        # Set initial state
        self.hidePopupMenu()

    def showPopupMenu(self, event=None):
        """Make popup visible above or below the button."""
        # Show the menu
        self.popupMenu.show()
        # Compute bounds
        b = self.getBounds()
        fb = self.popupMenu.getBounds()
        # Place the menu
        # NB: the original coordinates of the menu are such that its top left
        # corner is at the origin.
        xPos = b[0] - fb[0]
        # If you want it centered do:
        # xPos = (b[0] + b[1])/2 - (fb[1] - fb[0])/2
        self.popupMenu.setX(self, xPos)
        zPos = b[3] + (fb[3] - fb[2]) if self['dropUp'] else b[2]
        self.popupMenu.setZ(self, zPos)
        # Also display cancel frame to catch clicks outside of the popup
        self.cancelFrame.show()
        # Position and scale cancel frame to fill entire window
        self.cancelFrame.setPos(self.parent, 0, 0, 0)
        self.cancelFrame.setScale(self.parent, 1, 1, 1)

    def setShadow(self):
        if not self['shadowSize']:
            return
        if self['frameSize']:
            left, right, bottom, top = self['frameSize']
            width = right - left
            height = top - bottom
            shadowPos = Point3((left + right) / 2, 0, (top + bottom) / 2)
        elif self['geom']:
            bottomleft, topright = self['geom'].getTightBounds()
            width, _, height = topright - bottomleft
            shadowPos = (bottomleft + topright) / 2
        else:
            print("No frameSize or geom found: can't make shadow.")
            return
        shadowSize = self['shadowSize']
        shadow = make_box_shadow(width, height, shadowSize)
        shadow.setPos(shadowPos)
        shadow.reparentTo(self)


class ButtonMenu(DirectOptionMenu):
    """Simple menu with buttons."""
    def __init__(self, parent=None, **kw):
        optiondefs = (
            # List of items to display on the menu
            ('items', [], self.setItems),
            # Background color to use to highlight popup menu items
            ('highlightColor', (.5, .5, .5, 1), None),
            # Extra scale to use on highlight popup menu items
            ('highlightScale', (1, 1), None),
            # Command to be called on button click
            ('command',        None,       None),
            ('extraArgs',      [],         None),
            # Whether menu should be horizontal or vertical
            ('layout', 'horizontal', DGG.INITOPT),
            # Padding around the buttons
            ('pad', (.1, .1), DGG.INITOPT),
            # Shadow parameters
            ('shadowSize', 0, None),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)
        # Initialize the relevant superclass
        DirectFrame.__init__(self, parent)
        # Call option initialization functions
        self.initialiseoptions(ButtonMenu)

    def setItems(self):
        if not self['items']:
            return
        # Create a new component for each item
        # Find the maximum extents of all items
        itemIndex = 0
        self.minX = self.maxX = self.minZ = self.maxZ = None
        # Reason why we use _constructorKeywords[*] and not self[*] for all the
        # 'text_*' options: see DirectGuiBase.py's docstring.
        # In a nutshell: __getitem__ only queries _optionInfo, to which
        # '*_*'-options are not added -- they are left in _constructorKeywords
        # instead, and consumed as they are used, UNLESS 'component' is a group
        # name, which 'text' is, because DirectFrame says so.
        for item in self['items']:
            c = self.createcomponent(
                'item{}'.format(itemIndex), (), 'item',
                DirectButton, (self,),
                text=item, text_align=TextNode.ACenter,
                text_font=self._constructorKeywords['text_font'][0],
                text_scale=self._constructorKeywords['text_scale'][0],
                #  text_fg=self._constructorKeywords['text_fg'][0],
                pad=(.3, .2),
                command=lambda i=itemIndex: self.set(i),
                relief=self['relief'] or 'flat',
                borderWidth=(.01, .01),
                frameColor=self['frameColor'],
                )
            bounds = c.getBounds()
            if self.minX is None:
                self.minX = bounds[0]
            elif bounds[0] < self.minX:
                self.minX = bounds[0]
            if self.maxX is None:
                self.maxX = bounds[1]
            elif bounds[1] > self.maxX:
                self.maxX = bounds[1]
            if self.minZ is None:
                self.minZ = bounds[2]
            elif bounds[2] < self.minZ:
                self.minZ = bounds[2]
            if self.maxZ is None:
                self.maxZ = bounds[3]
            elif bounds[3] > self.maxZ:
                self.maxZ = bounds[3]
            itemIndex += 1
        # Calc max width and height
        self.maxWidth = self.maxX - self.minX
        self.maxHeight = self.maxZ - self.minZ
        # Adjust frame size for each item and bind actions to mouse events
        for i in range(itemIndex):
            item = self.component('item{}'.format(i))
            # So entire extent of item's slot on popup is reactive to mouse
            item['frameSize'] = (self.minX, self.maxX, self.minZ, self.maxZ)
            # Move it to its correct position in the menu
            if self['layout'] == 'vertical':
                item.setPos(-self.minX, 0, -self.maxZ - i * self.maxHeight)
            else:
                item.setPos(-self.minX + i * self.maxWidth, 0, -self.maxZ)
            # Highlight background when mouse is in item
            item.bind(DGG.WITHIN,
                      lambda x, i=i, item=item: self._highlightItem(item, i))
            # Restore specified color upon exiting
            fc = item['frameColor']
            item.bind(DGG.WITHOUT,
                      lambda x, item=item, fc=fc: self._unhighlightItem(
                          item, fc))
        # Set popup menu frame size to encompass all items
        px, py = self['pad']
        self['frameSize'] = (
                -px, self.maxWidth * itemIndex + px, -self.maxHeight - py, py)
        # Make shadow if need be
        self.setShadow()

    def setShadow(self):
        shadowSize = self['shadowSize']
        if not shadowSize:
            return
        frameSize = self['frameSize']
        px, py = self['pad']
        width = frameSize[1] - frameSize[0]
        height = frameSize[3] - frameSize[2]
        shadow = make_box_shadow(width, height, shadowSize)
        shadow.reparentTo(self)
        shadow.setX(width / 2 - px)
        shadow.setZ(-(height / 2 - py))

    def set(self, index, fCommand=True):
        """Set the new selected item.

        Parameters
        ----------
        index : int or string
            Index or label of the selected option.
        fCommand : bool, optional
            Whether to fire the selection callback or not. Default is True.
        """
        # Item was selected, record item and call command if any
        newIndex = self.index(index)
        if newIndex is not None:
            self.selectedIndex = newIndex
            item = self['items'][self.selectedIndex]
            if fCommand and self['command']:
                # Pass any extra args to command
                self['command'](*[item] + self['extraArgs'])


class PlayerControls(DirectFrame):
    def __init__(self, parent=None, **kw):
        optiondefs = (
            ('currentFrame', 1, None),
            ('numFrames', 2*cfg.VIDEO_FRAME_RATE, None),
            ('framerate', cfg.VIDEO_FRAME_RATE, None),
            ('command', None, None),
            ('shadowSize', 0, self.setShadow),
        )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs,
                           dynamicGroups=('button', 'label', 'slider'))
        # Initialize the relevant superclass
        super().__init__(parent)
        # Create components
        self._create_slider()
        self._create_text()
        self._create_buttons()
        # Call option initialization functions
        self.initialiseoptions(PlayerControls)

    def _create_buttons(self):
        fs = self['frameSize']
        button_data = (
            ("start", "|<<"),
            ("prev", " <<"),
            ("pp", " > "),
            ("next", ">> "),
            ("end", ">>|"),
        )
        for i, (label, symbol) in enumerate(button_data):
            name = label + "Button"
            self.createcomponent(
                name, (), 'button',
                DirectButton, (self,),
                command=self['command'],
                extraArgs=[name],
                pos=(fs[1] * (.1 + .15*(i + 1)), 0, fs[2]*.7),
                frameSize=(fs[0]*.06, fs[1]*.06, fs[0]*.02, fs[1]*.08),
                text=symbol,
                text_align=TextNode.ACenter,
                text_scale=.05,
                relief='flat',
                # borderWidth=(.01, .01),
            )

    def _create_slider(self):
        fs = self['frameSize']
        name = "timelineSlider"
        self.createcomponent(
            name, (), None,
            DirectSlider, (self,),
            command=self['command'],
            extraArgs=[name],
            frameSize=(fs[0]*.95, fs[1]*.95, fs[2]*.2, fs[3]*.2),
            pos=(0, 0, fs[3]/2),
            # DirectSlider-specific
            value=self['currentFrame'],
            range=(1, self['numFrames']),
            pageSize=1,
            thumb_relief='flat',
            thumb_frameColor=cfg.BUTTON_COLOR_1,
            thumb_frameSize=(fs[0]*.05, fs[1]*.05, fs[2]*.3, fs[3]*.3),
        )

    def _create_text(self):
        fs = self['frameSize']
        label_data = (
            {
                'componentName': "currentFrameLabel",
                'text': str(int(self['currentFrame'])),
                'pos': (fs[0]*.85, 0, fs[2]*.7),
                'textMayChange': True
            },
            {
                'componentName': "numFramesLabel",
                'text': "/" + str(self['numFrames']),
                'pos': (fs[0]*.65, 0, fs[2]*.7),
                'textMayChange': False
            },
        )
        for kw in label_data:
            name = kw.pop('componentName')
            self.createcomponent(
                name, (), 'label', DirectLabel, (self,),
                text_scale=.05, relief=None, **kw
            )

    def togglePlayPause(self, play=True):
        button = self.component("ppButton")
        button['text'] = "| |" if play else " > "
        button.setText()

    def updateCurrentFrame(self, value):
        timeline = self.component("timelineSlider")
        # Check value equality to avoid infinite recursion. Be careful to round
        # the stored value to avoid precision issues.
        if value != round(timeline['value']):
            timeline['value'] = value
        label = self.component("currentFrameLabel")
        label['text'] = str(int(value))

    def setShadow(self):
        if not self['shadowSize']:
            return
        add_shadow_to_frame(self, shadowSize=self['shadowSize'])


class ParameterEditor(DirectGuiWidget):
    """Generic parameter editor, displayed as a list of (name, field) lines.

    NB: To resize the fields, use 'param_scale' rather than 'param_frameSize'.

    """
    def __init__(self, parent=None, **kw):
        optiondefs = (
            ('paramData', [], None),
            ('command', None, None),
            ('shadowSize', 0, self.setShadow),
        )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs, dynamicGroups=('title', 'param'))
        # Initialize the relevant superclass
        super().__init__(parent)
        # Components
        fs = self['frameSize']
        title = self.createcomponent(
            "editorTitle", (), 'title', DirectLabel, (self,),
            frameSize=(fs[0], fs[1], -.02, .05),
            pos=Point3(0, 0, fs[3]+.02),
            textMayChange=False,
        )
        self.createcomponent(
            "closeButton", (), 'close', DirectButton, (title,),
            pos=Point3(fs[1]*.8, 0, 0),
            text='x', textMayChange=False,
            command=self.click_close_button,
        )
        for i, (paramName, paramValue) in enumerate(self['paramData']):
            pos = Point3(fs[0]*.9, 0, fs[3] - (i+1)*.1)
            self.createcomponent(
                paramName+"Label", (), 'param',
                DirectLabel, (self,),
                text=paramName,
                text_align=TextNode.ALeft,
                relief=None,
                pos=pos,
            )
            pos[0] = fs[1] * .1
            self.createcomponent(
                paramName+"Entry", (), 'entry',
                DirectEntry, (self,),
                command=self['command'],
                extraArgs=[paramName],
                pos=pos,
                # DirectEntry-specific args
                initialText=str(paramValue),
                numLines=1,
            )
        # Call option initialization functions
        self.initialiseoptions(ParameterEditor)

    def click_close_button(self):
        self.hide()

    def setShadow(self):
        if not self['shadowSize']:
            return
        add_shadow_to_frame(self, shadowSize=self['shadowSize'])


class EventWidget(DirectFrame):
    def __init__(self, parent=None, **kw):
        optiondefs = (
            # Make frame clickable
            ('state', DGG.NORMAL, None),
            # Event data
            ('eventName', "", None),
            ('objectList', [], None),
            ('numObjects', 0, None),
        )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)
        # Initialize the relevant superclass
        super().__init__(parent)
        # Call option initialization functions
        self.initialiseoptions(EventWidget)
        # Move behavior
        self.bind(DGG.B1PRESS, self.setMove, [True])
        self.bind(DGG.B1RELEASE, self.setMove, [False])
        # Components
        fs = self['frameSize']
        self.createcomponent(
            "eventNameLabel", (), None, DirectLabel, (self,),
            text=self['eventName'],
            text_scale=.08,
            text_fg=(1, 1, 1, 1),
            frameSize=(fs[0], fs[1], fs[2]*.15, fs[3]*.35),
            frameColor=(.2, .2, .2, 1),
            pos=(0, 0, fs[3]*.65),
            textMayChange=False,
        )
        inPort = self.createcomponent(
            "inPort", (), None,
            DirectFrame, (self,),
            frameSize=(fs[0]*.1, fs[1]*.1, fs[2], fs[3]),
            frameColor=(.8, .8, .8, .8),
            pos=(fs[0]*1.1, 0, 0),
            state=DGG.NORMAL,
        )
        inPort.bind(DGG.WITHIN, self._highlightPort, [True, "inPort"])
        inPort.bind(DGG.WITHOUT, self._highlightPort, [False, "inPort"])
        outPort = self.createcomponent(
            "outPort", (), None,
            DirectFrame, (self,),
            frameSize=(fs[0]*.1, fs[1]*.1, fs[2], fs[3]),
            frameColor=(.8, .8, .8, .8),
            pos=(fs[1]*1.1, 0, 0),
            state=DGG.NORMAL,
        )
        outPort.bind(DGG.B1PRESS, self.setLink, [True])
        outPort.bind(DGG.B1RELEASE, self.setLink, [False])
        outPort.bind(DGG.WITHIN, self._highlightPort, [True, "outPort"])
        outPort.bind(DGG.WITHOUT, self._highlightPort, [False, "outPort"])
        for i in range(self['numObjects']):
            self.createcomponent(
                "objectSelector{}".format(i+1), (), None,
                DirectOptionMenu, (self,),
                scale=.08,
                text_fg=Vec4(1),
                item_text_fg=Vec4(1),
                frameColor=(.2, .2, .2, .8),
                item_frameColor=(.2, .2, .2, 1),
                highlightColor=(.25, .25, .25, 1),
                pos=(fs[0]*.9, 0, fs[2]*.7*i),
                item_pad=(.1, .1),
                relief='flat',
                popupMarker_relief='flat',
                item_relief='flat',
                items=self['objectList'],
            )
        # Shadow
        width = (fs[1] - fs[0])*1.2
        height = fs[3] - fs[2]
        shadowSize = .2
        shadow = make_box_shadow(width, height, shadowSize)
        shadow.setZ((fs[2] + fs[3]) / 2)
        shadow.reparentTo(self)
        # Useful pointers
        self.parent.setPythonTag('activeLink', None)
        self.parent.setPythonTag('activeLinkTarget', None)
        self.parent.setPythonTag('highlightedPort', None)
        self.mouseWatcher = aspect2d.node().getMouseWatcher()

    def _highlightPort(self, highlight, portName, event):
        port = self.component(portName)
        fc = port['frameColor']
        if highlight:
            port['frameColor'] = (fc[0]*2, fc[1]*2, fc[2]*2, .8)
            self.parent.setPythonTag('highlightedPort', (portName, port))
        else:
            port['frameColor'] = (fc[0]/2, fc[1]/2, fc[2]/2, .8)
            self.parent.setPythonTag('highlightedPort', None)

    def setLink(self, link, event):
        if link:
            outPort = self.component("outPort")
            # Create the link
            activeLinkTarget = outPort.attachNewNode(
                make_circle("activeLink", .02)
            )
            activeLink = Rope("link")
            activeLink.setup(
                3,
                ((outPort, 0),
                 (outPort, (.1, 0, 0)),
                 (activeLinkTarget, (-.1, 0, 0)),
                 (activeLinkTarget, 0),
                 )
            )
            activeLink.reparentTo(outPort)
            # Set pointers
            self.parent.setPythonTag('activeLink', activeLink)
            self.parent.setPythonTag('activeLinkTarget', activeLinkTarget)
            # Start task
            taskMgr.add(self.runLinkTask, "run_link_task")
        else:
            hp = self.parent.getPythonTag('highlightedPort')
            selfIn = self.component("inPort")
            if hp is None or hp[0].startswith("out") or hp[1] is selfIn:
                self.parent.getPythonTag('activeLink').removeNode()
                self.parent.getPythonTag('activeLinkTarget').removeNode()
            else:
                activeLinkTarget = self.parent.getPythonTag('activeLinkTarget')
                activeLinkTarget.reparentTo(hp[1])
                activeLinkTarget.setPos(0)
            # Clean up pointers
            self.parent.setPythonTag('activeLink', None)
            self.parent.setPythonTag('activeLinkTarget', None)
            # Stop task
            taskMgr.remove("run_link_task")

    def runLinkTask(self, task):
        mw = self.mouseWatcher
        if mw.hasMouse():
            mousePos = Point3(mw.getMouseX(), 0, mw.getMouseY())
            render2d = self.parent.getParent()
            outPort = self.component("outPort")
            mousePos = outPort.getRelativePoint(render2d, mousePos)
            activeLinkTarget = self.parent.getPythonTag('activeLinkTarget')
            activeLinkTarget.setPos(mousePos)
        return task.cont

    def setMove(self, move, event):
        if move:
            mousePos = Point3(event.getMouse()[0], 0, event.getMouse()[1])
            render2d = self.parent.getParent()
            mousePos = self.parent.getRelativePoint(render2d, mousePos)
            self._moveOffset = mousePos - self.getPos()
            # Rendering trick to bring the event to the front:
            self.reparentTo(self.parent)
            taskMgr.add(self.runMoveTask, "run_move_task")
        else:
            taskMgr.remove("run_move_task")

    def runMoveTask(self, task):
        mw = self.mouseWatcher
        if mw.hasMouse():
            mousePos = Point3(mw.getMouseX(), 0, mw.getMouseY())
            render2d = self.parent.getParent()
            mousePos = self.parent.getRelativePoint(render2d, mousePos)
            newPos = mousePos - self._moveOffset
            self.setPos(newPos)
        return task.cont
