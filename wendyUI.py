#-------------------------------------------------------------------------------
# Name:        Wendy User Interface 1.0
# For Maya :   2008 - 2015
#
# Author:      Mickael Bonfill
#
# Created:     11/04/2014
# Copyright:   (c) Mickael-B 2014
# Licence:     Public License
#-------------------------------------------------------------------------------

import maya.cmds as cmds
import os
from functools import partial
#import pymel.core as pm

class wendyUI():

    def __init__(self):

        self.windowName = "wendyUI_dock"

        self.widgets = {}

        #get namespaces
        namespaces = cmds.namespaceInfo(listOnlyNamespaces = True)

        self.namespaces = []

        for name in namespaces:
            if cmds.objExists(name + ":MainC"):
                self.namespaces.append(name)

        self.createUI(self.windowName)

    def createUI(self, windowName):
        if cmds.dockControl(windowName, exists = True) :
            cmds.deleteUI(windowName)

        self.widgets["window"] = cmds.window(title = "Wendy User Interface 1.0", mnb = False, mxb = False)

        self.widgets["scrollLayout"] = cmds.scrollLayout(hst = 0)

        self.widgets["mainLayout"] = cmds.columnLayout(adj = True, parent = self.widgets["scrollLayout"])

        self.widgets["menuBarLayout"] = cmds.menuBarLayout()
        cmds.menu( label='Help', helpMenu=True )
        cmds.menuItem( label='About', c = self.aboutWindow)

        cmds.text(label = "Wendy User Interface 1.0")

        self.widgets["tabLayout"] = cmds.tabLayout()



        for name in self.namespaces:

            self.widgets[name + "_subLayout"] = cmds.columnLayout(adj = True, parent = self.widgets["tabLayout"])

            self.widgets[name + "_viewer_frameLayout"] = cmds.frameLayout(label = "Viewer", collapsable = True, parent = self.widgets[name + "_subLayout"])
            self.widgets[name + "_RigoptionMenu"] = cmds.optionMenu( label='Control Zone', changeCommand=self.changeZoneOfControl )
            cmds.menuItem( label='Face' )
            cmds.menuItem( label='Body' )


            """FACIAL ZONE"""

            self.widgets[name + "_faceViewer_mainLayout"] = cmds.formLayout(w = 512, h = 512, parent = self.widgets[name + "_viewer_frameLayout"])

            #Display Background Image
            self.widgets["faceViewer_background"] = cmds.image(i = cmds.internalVar(upd = True) + "icons/wendyUI/bg_face.jpg", w= 512, h = 512)

            #Character Rig Buttons Creation

            self.viewerButtonList = []
            ctInScene = cmds.ls(name + ':ct_*', transforms = True)
            for controler in ctInScene:
                self.viewerButtonList.append(controler)

            defaultBGC = [0, 0, 0]
            newBGC = [1, 1, 1]

            self.viewerButtonList.append(name + ":JawC")
            self.viewerButtonList.append(name + ":HeadC")
            self.viewerButtonList.append(name + ":lEyeAimC")
            self.viewerButtonList.append(name + ":EyeAimC")
            self.viewerButtonList.append(name + ":rEyeAimC")

            for viewerButton in self.viewerButtonList:


                self.widgets[viewerButton + "Button"] = cmds.button(label = "", w = 50, h = 50, bgc = self.colorAlgorithm(viewerButton), parent = self.widgets[name + "_faceViewer_mainLayout"])
                cmds.button(self.widgets[viewerButton + "Button"], edit = True, c = partial(self.selectControl, [viewerButton]))


            self.createScriptJob(self.viewerButtonList, newBGC)


            #Character Rig Button Placement

            #Right Controlers
            cmds.button(self.widgets[name + ":ct_cheek1RtButton"], edit =True, w= 50, h= 70)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_cheek1RtButton"], 'left', 108))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_cheek1RtButton"], 'top', 305))


            cmds.button(self.widgets[name + ":ct_sneer1RtButton"], edit =True, w= 40, h= 30)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_sneer1RtButton"], 'left', 160))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_sneer1RtButton"], 'top', 370))


            cmds.button(self.widgets[name + ":ct_nose1RtButton"], edit =True, w= 30, h= 30)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_nose1RtButton"], 'left', 210))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_nose1RtButton"], 'top', 306))


            cmds.button(self.widgets[name + ":ct_lidLower1RtButton"], edit =True, w= 30, h= 30)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_lidLower1RtButton"], 'left', 107))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_lidLower1RtButton"], 'top', 255))


            cmds.button(self.widgets[name + ":ct_eyeLid2RtButton"], edit =True, w= 21, h= 21)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_eyeLid2RtButton"], 'left', 46))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_eyeLid2RtButton"], 'top', 210))


            cmds.button(self.widgets[name + ":ct_eyeLid1RtButton"], edit =True, w= 21, h= 21)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_eyeLid1RtButton"], 'left', 195))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_eyeLid1RtButton"], 'top', 237))


            cmds.button(self.widgets[name + ":ct_lidUpper1RtButton"], edit =True, w= 30, h= 30)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_lidUpper1RtButton"], 'left', 105))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_lidUpper1RtButton"], 'top', 147))

            cmds.button(self.widgets[name + ":ct_eyebrow1RtButton"], edit =True, w= 30, h= 30)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_eyebrow1RtButton"], 'left', 215))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_eyebrow1RtButton"], 'top', 103))


            cmds.button(self.widgets[name + ":ct_eyebrow2RtButton"], edit =True, w= 30, h= 30)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_eyebrow2RtButton"], 'left', 102))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_eyebrow2RtButton"], 'top', 97))


            cmds.button(self.widgets[name + ":ct_eyebrow3RtButton"], edit =True, w= 30, h= 30)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_eyebrow3RtButton"], 'left', 36))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_eyebrow3RtButton"], 'top', 155))





            #Left Controlers
            cmds.button(self.widgets[name + ":ct_cheek1LtButton"], edit =True, w= 50, h= 70)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_cheek1LtButton"], 'left', (512-50-108)))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_cheek1LtButton"], 'top', 305))


            cmds.button(self.widgets[name + ":ct_sneer1LtButton"], edit =True, w= 40, h= 30)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_sneer1LtButton"], 'left', 512-40-160))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_sneer1LtButton"], 'top', 370))


            cmds.button(self.widgets[name + ":ct_nose1LtButton"], edit =True, w= 30, h= 30)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_nose1LtButton"], 'left', 512-30-210))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_nose1LtButton"], 'top', 306))


            cmds.button(self.widgets[name + ":ct_lidLower1LtButton"], edit =True, w= 30, h= 30)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_lidLower1LtButton"], 'left', 512-30-107))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_lidLower1LtButton"], 'top', 255))


            cmds.button(self.widgets[name + ":ct_eyeLid2LtButton"], edit =True, w= 21, h= 21)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_eyeLid2LtButton"], 'left', 512-21-46))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_eyeLid2LtButton"], 'top', 210))


            cmds.button(self.widgets[name + ":ct_eyeLid1LtButton"], edit =True, w= 21, h= 21)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_eyeLid1LtButton"], 'left', 512-21-195))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_eyeLid1LtButton"], 'top', 237))


            cmds.button(self.widgets[name + ":ct_lidUpper1LtButton"], edit =True, w= 30, h= 30)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_lidUpper1LtButton"], 'left', 512-30-105))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_lidUpper1LtButton"], 'top', 147))

            cmds.button(self.widgets[name + ":ct_eyebrow1LtButton"], edit =True, w= 30, h= 30)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_eyebrow1LtButton"], 'left', 512-30-215))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_eyebrow1LtButton"], 'top', 103))


            cmds.button(self.widgets[name + ":ct_eyebrow2LtButton"], edit =True, w= 30, h= 30)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_eyebrow2LtButton"], 'left', 512-30-102))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_eyebrow2LtButton"], 'top', 97))


            cmds.button(self.widgets[name + ":ct_eyebrow3LtButton"], edit =True, w= 30, h= 30)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_eyebrow3LtButton"], 'left', 512-30-36))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_eyebrow3LtButton"], 'top', 155))




            #Non-symmetrical Controlers
            cmds.button(self.widgets[name + ":ct_nose1Button"], edit =True, w= 55, h= 30)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_nose1Button"], 'left', 229))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_nose1Button"], 'top', 274))


            cmds.button(self.widgets[name + ":ct_mainUperLip1Button"], edit =True, w= 55, h= 30)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_mainUperLip1Button"], 'left', 229))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_mainUperLip1Button"], 'top', 345))


            cmds.button(self.widgets[name + ":ct_mainLowerLip1Button"], edit =True, w= 55, h= 30)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_mainLowerLip1Button"], 'left', 229))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_mainLowerLip1Button"], 'top', 411))


            cmds.button(self.widgets[name + ":ct_upperTiltHead1Button"], edit =True, w= 55, h= 15)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_upperTiltHead1Button"], 'left', 455))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_upperTiltHead1Button"], 'top', 256))


            cmds.button(self.widgets[name + ":ct_lowerTiltHead1Button"], edit =True, w= 55, h= 15)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_lowerTiltHead1Button"], 'left', 455))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_lowerTiltHead1Button"], 'top', 275))

            cmds.button(self.widgets[name + ":JawCButton"], edit =True, w= 150, h= 50)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":JawCButton"], 'left', 181))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":JawCButton"], 'top', 455))

            cmds.button(self.widgets[name + ":HeadCButton"], edit =True, w= 240, h= 50)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":HeadCButton"], 'left', 136))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":HeadCButton"], 'top', 10))



            #Right Lower Eyelid
            cmds.button(self.widgets[name + ":ct_LidLower1RtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower1RtButton"], 'left', 184))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower1RtButton"], 'top', 250))

            cmds.button(self.widgets[name + ":ct_LidLower2RtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower2RtButton"], 'left', 166))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower2RtButton"], 'top', 253))

            cmds.button(self.widgets[name + ":ct_LidLower3RtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower3RtButton"], 'left', 135))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower3RtButton"], 'top', 254))

            cmds.button(self.widgets[name + ":ct_LidLower4RtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower4RtButton"], 'left', 96))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower4RtButton"], 'top', 250))

            cmds.button(self.widgets[name + ":ct_LidLower5RtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower5RtButton"], 'left', 70))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower5RtButton"], 'top', 242))

            cmds.button(self.widgets[name + ":ct_LidLower6RtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower6RtButton"], 'left', 65))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower6RtButton"], 'top', 228))

            cmds.button(self.widgets[name + ":ct_LidLower7RtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower7RtButton"], 'left', 63))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower7RtButton"], 'top', 216))




            #Right Upper Eyelid
            cmds.button(self.widgets[name + ":ct_LidUpper1RtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper1RtButton"], 'left', 190))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper1RtButton"], 'top', 222))

            cmds.button(self.widgets[name + ":ct_LidUpper2RtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper2RtButton"], 'left', 181))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper2RtButton"], 'top', 210))

            cmds.button(self.widgets[name + ":ct_LidUpper3RtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper3RtButton"], 'left', 170))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper3RtButton"], 'top', 195))

            cmds.button(self.widgets[name + ":ct_LidUpper4RtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper4RtButton"], 'left', 155))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper4RtButton"], 'top', 182))

            cmds.button(self.widgets[name + ":ct_LidUpper5RtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper5RtButton"], 'left', 140))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper5RtButton"], 'top', 172))

            cmds.button(self.widgets[name + ":ct_LidUpper6RtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper6RtButton"], 'left', 110))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper6RtButton"], 'top', 173))

            cmds.button(self.widgets[name + ":ct_LidUpper7RtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper7RtButton"], 'left', 90))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper7RtButton"], 'top', 178))

            cmds.button(self.widgets[name + ":ct_LidUpper8RtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper8RtButton"], 'left', 77))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper8RtButton"], 'top', 190))

            cmds.button(self.widgets[name + ":ct_LidUpper9RtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper9RtButton"], 'left', 64))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper9RtButton"], 'top', 202))




            #Left Lower Eyelid
            cmds.button(self.widgets[name + ":ct_LidLower1LtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower1LtButton"], 'left', 512-13-184))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower1LtButton"], 'top', 512-13-250))

            cmds.button(self.widgets[name + ":ct_LidLower2LtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower2LtButton"], 'left', 512-13-166))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower2LtButton"], 'top', 253))

            cmds.button(self.widgets[name + ":ct_LidLower3LtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower3LtButton"], 'left', 512-13-135))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower3LtButton"], 'top', 254))

            cmds.button(self.widgets[name + ":ct_LidLower4LtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower4LtButton"], 'left', 512-13-96))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower4LtButton"], 'top', 250))

            cmds.button(self.widgets[name + ":ct_LidLower5LtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower5LtButton"], 'left', 512-13-70))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower5LtButton"], 'top', 242))

            cmds.button(self.widgets[name + ":ct_LidLower6LtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower6LtButton"], 'left', 512-13-65))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower6LtButton"], 'top', 228))

            cmds.button(self.widgets[name + ":ct_LidLower7LtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower7LtButton"], 'left', 512-13-63))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidLower7LtButton"], 'top', 216))




            #Left Upper Eyelid
            cmds.button(self.widgets[name + ":ct_LidUpper1LtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper1LtButton"], 'left', 512-13-190))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper1LtButton"], 'top', 222))

            cmds.button(self.widgets[name + ":ct_LidUpper2LtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper2LtButton"], 'left', 512-13-181))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper2LtButton"], 'top', 210))

            cmds.button(self.widgets[name + ":ct_LidUpper3LtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper3LtButton"], 'left', 512-13-170))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper3LtButton"], 'top', 195))

            cmds.button(self.widgets[name + ":ct_LidUpper4LtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper4LtButton"], 'left', 512-13-155))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper4LtButton"], 'top', 182))

            cmds.button(self.widgets[name + ":ct_LidUpper5LtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper5LtButton"], 'left', 512-13-140))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper5LtButton"], 'top', 172))

            cmds.button(self.widgets[name + ":ct_LidUpper6LtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper6LtButton"], 'left', 512-13-110))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper6LtButton"], 'top', 173))

            cmds.button(self.widgets[name + ":ct_LidUpper7LtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper7LtButton"], 'left', 512-13-90))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper7LtButton"], 'top', 178))

            cmds.button(self.widgets[name + ":ct_LidUpper8LtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper8LtButton"], 'left', 512-13-77))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper8LtButton"], 'top', 190))

            cmds.button(self.widgets[name + ":ct_LidUpper9LtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper9LtButton"], 'left', 512-13-64))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LidUpper9LtButton"], 'top', 202))




            #Lips

            cmds.button(self.widgets[name + ":ct_UpperMouth1RtButton"], edit =True, w= 10, h= 10)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_UpperMouth1RtButton"], 'left', 200))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_UpperMouth1RtButton"], 'top', 380))

            cmds.button(self.widgets[name + ":ct_UpperMouth2RtButton"], edit =True, w= 10, h= 10)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_UpperMouth2RtButton"], 'left', 210))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_UpperMouth2RtButton"], 'top', 380))

            cmds.button(self.widgets[name + ":ct_UpperMouth3RtButton"], edit =True, w= 10, h= 10)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_UpperMouth3RtButton"], 'left', 221))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_UpperMouth3RtButton"], 'top', 378))

            cmds.button(self.widgets[name + ":ct_UpperMouth4RtButton"], edit =True, w= 10, h= 10)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_UpperMouth4RtButton"], 'left', 229))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_UpperMouth4RtButton"], 'top', 377))

            cmds.button(self.widgets[name + ":ct_UpperMouth5RtButton"], edit =True, w= 10, h= 10)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_UpperMouth5RtButton"], 'left', 242))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_UpperMouth5RtButton"], 'top', 376))

            cmds.button(self.widgets[name + ":ct_UpperMouth1LtButton"], edit =True, w= 10, h= 10)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_UpperMouth1LtButton"], 'left', 512-10-200))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_UpperMouth1LtButton"], 'top', 380))

            cmds.button(self.widgets[name + ":ct_UpperMouth2LtButton"], edit =True, w= 10, h= 10)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_UpperMouth2LtButton"], 'left', 512-10-210))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_UpperMouth2LtButton"], 'top', 380))

            cmds.button(self.widgets[name + ":ct_UpperMouth3LtButton"], edit =True, w= 10, h= 10)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_UpperMouth3LtButton"], 'left', 512-10-221))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_UpperMouth3LtButton"], 'top', 378))

            cmds.button(self.widgets[name + ":ct_UpperMouth4LtButton"], edit =True, w= 10, h= 10)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_UpperMouth4LtButton"], 'left', 512-10-229))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_UpperMouth4LtButton"], 'top', 377))

            cmds.button(self.widgets[name + ":ct_UpperMouth5LtButton"], edit =True, w= 10, h= 10)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_UpperMouth5LtButton"], 'left', 512-10-242))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_UpperMouth5LtButton"], 'top', 376))


            cmds.button(self.widgets[name + ":ct_LowerMouth1RtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LowerMouth1RtButton"], 'left', 200))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LowerMouth1RtButton"], 'top', 390))

            cmds.button(self.widgets[name + ":ct_LowerMouth2RtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LowerMouth2RtButton"], 'left', 213))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LowerMouth2RtButton"], 'top', 395))

            cmds.button(self.widgets[name + ":ct_LowerMouth3RtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LowerMouth3RtButton"], 'left', 226))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LowerMouth3RtButton"], 'top', 396))

            cmds.button(self.widgets[name + ":ct_LowerMouth4RtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LowerMouth4RtButton"], 'left', 239))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LowerMouth4RtButton"], 'top', 396))

            cmds.button(self.widgets[name + ":ct_LowerMouth1LtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LowerMouth1LtButton"], 'left', 512-13-200))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LowerMouth1LtButton"], 'top', 390))

            cmds.button(self.widgets[name + ":ct_LowerMouth2LtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LowerMouth2LtButton"], 'left', 512-13-213))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LowerMouth2LtButton"], 'top', 395))

            cmds.button(self.widgets[name + ":ct_LowerMouth3LtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LowerMouth3LtButton"], 'left', 512-13-226))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LowerMouth3LtButton"], 'top', 396))

            cmds.button(self.widgets[name + ":ct_LowerMouth4LtButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LowerMouth4LtButton"], 'left', 512-13-239))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LowerMouth4LtButton"], 'top', 396))

            cmds.button(self.widgets[name + ":ct_LowerMouth1MdButton"], edit =True, w= 13, h= 13)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LowerMouth1MdButton"], 'left', 249))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_LowerMouth1MdButton"], 'top', 396))

            cmds.button(self.widgets[name + ":ct_UpperMouth1MdButton"], edit =True, w= 10, h= 10)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_UpperMouth1MdButton"], 'left', 251))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":ct_UpperMouth1MdButton"], 'top', 374))


            #Eyes direction
            cmds.button(self.widgets[name + ":EyeAimCButton"], edit =True, w= 30, h= 30)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":EyeAimCButton"], 'left', 241))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":EyeAimCButton"], 'top', 220))

            cmds.button(self.widgets[name + ":lEyeAimCButton"], edit =True, w= 30, h= 30)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":lEyeAimCButton"], 'left', 512-30-130))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":lEyeAimCButton"], 'top', 220))

            cmds.button(self.widgets[name + ":rEyeAimCButton"], edit =True, w= 30, h= 30)
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":rEyeAimCButton"], 'left', 130))
            cmds.formLayout(self.widgets[name + "_faceViewer_mainLayout"], edit = True, af = (self.widgets[name + ":rEyeAimCButton"], 'top', 220))


            """BODY ZONE"""

            self.widgets[name + "_bodyViewer_mainLayout"] = cmds.formLayout(w = 512, h = 512, parent = self.widgets[name + "_viewer_frameLayout"], visible = False)

            #Character Rig Buttons Creation

            self.viewerButtonList = []
            defaultBGC = [0, 0, 0]
            newBGC = [1, 1, 1]

            for viewerButton in self.viewerButtonList:
                self.widgets[viewerButton + "Button"] = cmds.button(label = "", w = 40, h = 40, bgc = self.colorAlgorithm(viewerButton))
                cmds.button(self.widgets[viewerButton + "Button"], edit = True, c = partial(self.selectControl, [viewerButton]))


            self.createScriptJob(self.viewerButtonList, newBGC)



            """MODIFIERS ZONE"""

            self.widgets[name + "_modifiers_frameLayout"] = cmds.frameLayout(label = "Modifiers", collapsable = True, parent = self.widgets[name + "_subLayout"])
            self.widgets[name + "_modifiers_mainLayout"] = cmds.rowColumnLayout(nc = 10)


            self.currentFaceViewer = self.widgets[name + "_faceViewer_mainLayout"]
            self.currentBodyViewer = self.widgets[name + "_bodyViewer_mainLayout"]


            self.populateModifiersButtons(name)


            """NOTES ANIMATION ZONE"""
            self.widgets[name +"_notes_frameLayout"] = cmds.frameLayout(label = "Notes for Animators", collapsable = True, parent = self.widgets[name + "_subLayout"])
            self.widgets[name + "_notes_mainLayout"] = cmds.rowColumnLayout(nc = 2)
            cmds.text(label = "Wendy User Interface 1.0", parent = self.widgets[name + "_notes_mainLayout"])

            cmds.tabLayout(self.widgets["tabLayout"], edit = True, tabLabel = ((self.widgets[name + "_subLayout"], name)))


        self.widgets["dock"] = cmds.dockControl(windowName, area = 'left', content = self.widgets["window"], allowedArea = 'left')






    #VIEWER Buttons Informations
    def selectControl(self, controls, args):

        mods = cmds.getModifiers()
        if (mods & 1) > 0:
            for i in range(len(controls)):
                cmds.select(controls[i], tgl = True)
                ++i

        elif (mods & 8) > 0:
            cmds.select(clear = True)

        else:
            cmds.select(clear = True)
            for i in range(len(controls)):
                cmds.select(controls[i], add = True)
                ++i



    def changeZoneOfControl(self, item):
        if item == "Face":
            cmds.formLayout(self.currentFaceViewer, edit = True, visible = True)
            cmds.formLayout(self.currentBodyViewer, edit = True, visible = False)
        elif item == "Body":
            cmds.formLayout(self.currentFaceViewer, edit = True, visible = False)
            cmds.formLayout(self.currentBodyViewer, edit = True, visible = True)


    #MODIFIERS Buttons Informations

    def populateModifiersButtons(self, namespace, *args):
        iconPath = cmds.internalVar(upd = True) + "icons/wendyUI/"
        icons = os.listdir(iconPath)
        for icon in icons:
            if icon.partition("_")[0] == "mod":
                niceName = icon.partition(".")[0].partition("_")[2]
                print niceName
                self.widgets[niceName + "_button"] = cmds.symbolButton(w = 50, h = 50, image = (iconPath + icon), c= partial(self.runModifier, niceName), parent = self.widgets[namespace + "_modifiers_mainLayout"])


    def runModifier(self, method, *args):
        exec("self." + method + "()")

    def setTranslateKey(self, *args):
        cmds.setKeyframe(at = 'translateX')
        cmds.setKeyframe(at = 'translateY')
        cmds.setKeyframe(at = 'translateZ')

    def setRotateKey(self, *args):
        cmds.setKeyframe(at = 'rotateX')
        cmds.setKeyframe(at = 'rotateY')
        cmds.setKeyframe(at = 'rotateZ')

    def setScaleKey(self, *args):
        cmds.setKeyframe(at = 'scaleX')
        cmds.setKeyframe(at = 'scaleY')
        cmds.setKeyframe(at = 'scaleZ')

    def setSteppedAnimation(self, *args):
        cmds.selectKey()
        cmds.keyTangent(itt = "step", ott = "step")

    def setSteppedAnimationForAll(self, *args):
        allDagObj = cmds.ls(transforms = True)
        animCurves = cmds.listConnections(allDagObj, source=True, type="animCurve")
        cmds.select(animCurves)
        cmds.selectKey()
        cmds.keyTangent(itt = "step", ott = "step")


    #VIEWER Script

    def createScriptJob(self, viewerButtonList, newBGC ):
        scriptJobNum = cmds.scriptJob(event = ["SelectionChanged", partial(self.DeselectButton, viewerButtonList, newBGC)], runOnce = False, parent = self.widgets["window"])

    def DeselectButton(self, viewerButtonList, newBGC):
        selection = cmds.ls(sl = True, transforms = True)
        for viewerButton in viewerButtonList:
            if viewerButton not in selection:
                    cmds.button(self.widgets[viewerButton + "Button"], edit = True, bgc = self.colorAlgorithm(viewerButton))
            else:
                cmds.button(self.widgets[viewerButton + "Button"], edit = True, bgc = newBGC)

    def aboutWindow(self, *args):
        if cmds.window("aboutWindowPanel", exists = True) :
            cmds.deleteUI("aboutWindowPanel")

        self.widgets["aboutPanel"] = cmds.window("aboutWindowPanel", title = "About", w = 300, h= 150, mnb = False, mxb = False)
        about_formLayout = cmds.formLayout(w=300, h=150)
        cmds.text(label = "Wendy User Interface 1.0")
        cmds.showWindow(self.widgets["aboutPanel"])

    def colorAlgorithm(self, transformObject, *args):
        objectShapes = cmds.listRelatives(transformObject)
        shapeColor = cmds.getAttr(objectShapes[0] + ".overrideColor")
        result = []
        if shapeColor == 0:
            result=[.20, .20, 1]
        elif shapeColor == 29:
            result = [.68, .78, .91]
        elif shapeColor == 31:
            result = [.84, .56, .62]
        elif shapeColor == 4:
            result = [.85, .20, .20]
        else:
            result = [.5, .5, .5]
        return result
