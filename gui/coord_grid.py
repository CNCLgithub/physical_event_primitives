#  -*- coding: utf-8 -*-
"""
Source: https://www.panda3d.org/forums/viewtopic.php?t=4784
(see _ext/coord_grid.py for the original).

"""
from numpy import arange
from panda3d.core import VBase4, LineSegs, NodePath, AntialiasAttrib


class ThreeAxisGrid:
    def __init__(self, xsize=50, ysize=50, zsize=50, gridstep=10, subdiv=10):

        # Init passed variables
        self.XSize = xsize
        self.YSize = ysize
        self.ZSize = zsize
        self.gridStep = gridstep
        self.subdiv = subdiv

        # Init default variables

        # Plane and end cap line visibility (1 is show, 0 is hide)
        self.XYPlaneShow = 1
        self.XZPlaneShow = 1
        self.YZPlaneShow = 1
        self.endCapLinesShow = 1

        # Alpha variables for each plane
        # self.XYPlaneAlpha = 1
        # self.XZPlaneAlpha = 1
        # self.YZPlaneAlpha = 1

        # Colors (RGBA passed as a VBase4 object)
        self.XAxisColor = VBase4(1, 0, 0, 1)
        self.YAxisColor = VBase4(0, 1, 0, 1)
        self.ZAxisColor = VBase4(0, 0, 1, 1)
        self.gridColor = VBase4(0, 0, 0, 1)
        self.subdivColor = VBase4(.35, .35, .35, 1)

        # Line thicknesses (in pixels)
        self.axisThickness = 1
        self.gridThickness = 1
        self.subdivThickness = 1

        # Axis, grid, and subdiv lines must be seperate LineSeg
        # objects in order to allow different thicknesses.
        # The parentNode groups them together for convenience.
        # All may be accessed individually if necessary.
        self.parentNode = None
        self.parentNodePath = None
        self.axisLinesNode = None
        self.axisLinesNodePath = None
        self.gridLinesNode = None
        self.gridLinesNodePath = None
        self.subdivLinesNode = None
        self.subdivLinesNodePath = None

        # Create line objects
        self.axisLines = LineSegs()
        self.gridLines = LineSegs()
        self.subdivLines = LineSegs()

    def create(self):

        # Set line thicknesses
        self.axisLines.setThickness(self.axisThickness)
        self.gridLines.setThickness(self.gridThickness)
        self.subdivLines.setThickness(self.subdivThickness)

        if(self.XSize != 0):
            # Draw X axis line
            self.axisLines.setColor(self.XAxisColor)
            self.axisLines.moveTo(-(self.XSize), 0, 0)
            self.axisLines.drawTo(self.XSize, 0, 0)

        if(self.YSize != 0):
            # Draw Y axis line
            self.axisLines.setColor(self.YAxisColor)
            self.axisLines.moveTo(0, -(self.YSize), 0)
            self.axisLines.drawTo(0, self.YSize, 0)

        if(self.ZSize != 0):
            # Draw Z axis line
            self.axisLines.setColor(self.ZAxisColor)
            self.axisLines.moveTo(0, 0, -(self.ZSize))
            self.axisLines.drawTo(0, 0, self.ZSize)

        # Check to see if primary grid lines should be drawn at all
        if(self.gridStep != 0):

            # Draw primary grid lines
            self.gridLines.setColor(self.gridColor)

            # Draw primary grid lines metering x axis if any x-length
            if(self.XSize != 0):

                if((self.YSize != 0) and (self.XYPlaneShow != 0)):
                    # Draw y lines across x axis starting from center moving
                    # out XY Plane
                    for x in arange(0, self.XSize, self.gridStep):
                        self.gridLines.moveTo(x, -(self.YSize), 0)
                        self.gridLines.drawTo(x, self.YSize, 0)
                        self.gridLines.moveTo(-x, -(self.YSize), 0)
                        self.gridLines.drawTo(-x, self.YSize, 0)

                    if(self.endCapLinesShow != 0):
                        # Draw endcap lines
                        self.gridLines.moveTo(self.XSize, -(self.YSize), 0)
                        self.gridLines.drawTo(self.XSize, self.YSize, 0)
                        self.gridLines.moveTo(-(self.XSize), -(self.YSize), 0)
                        self.gridLines.drawTo(-(self.XSize), self.YSize, 0)

                if((self.ZSize != 0) and (self.XZPlaneShow != 0)):
                    # Draw z lines across x axis starting from center moving
                    # out XZ Plane
                    for x in arange(0, self.XSize, self.gridStep):
                        self.gridLines.moveTo(x, 0, -(self.ZSize))
                        self.gridLines.drawTo(x, 0, self.ZSize)
                        self.gridLines.moveTo(-x, 0, -(self.ZSize))
                        self.gridLines.drawTo(-x, 0, self.ZSize)

                    if(self.endCapLinesShow != 0):
                        # Draw endcap lines
                        self.gridLines.moveTo(self.XSize, 0, -(self.ZSize))
                        self.gridLines.drawTo(self.XSize, 0, self.ZSize)
                        self.gridLines.moveTo(-(self.XSize), 0, -(self.ZSize))
                        self.gridLines.drawTo(-(self.XSize), 0, self.ZSize)

            # Draw primary grid lines metering y axis if any y-length
            if(self.YSize != 0):

                if((self.YSize != 0) and (self.XYPlaneShow != 0)):
                    # Draw x lines across y axis
                    # XY Plane
                    for y in arange(0, self.YSize, self.gridStep):
                        self.gridLines.moveTo(-(self.XSize), y, 0)
                        self.gridLines.drawTo(self.XSize, y, 0)
                        self.gridLines.moveTo(-(self.XSize), -y, 0)
                        self.gridLines.drawTo(self.XSize, -y, 0)

                    if(self.endCapLinesShow != 0):
                        # Draw endcap lines
                        self.gridLines.moveTo(-(self.XSize), self.YSize, 0)
                        self.gridLines.drawTo(self.XSize, self.YSize, 0)
                        self.gridLines.moveTo(-(self.XSize), -(self.YSize), 0)
                        self.gridLines.drawTo(self.XSize, -(self.YSize), 0)

                if((self.ZSize != 0) and (self.YZPlaneShow != 0)):
                    # Draw z lines across y axis
                    # YZ Plane
                    for y in arange(0, self.YSize, self.gridStep):
                        self.gridLines.moveTo(0, y, -(self.ZSize))
                        self.gridLines.drawTo(0, y, self.ZSize)
                        self.gridLines.moveTo(0, -y, -(self.ZSize))
                        self.gridLines.drawTo(0, -y, self.ZSize)

                    if(self.endCapLinesShow != 0):
                        # Draw endcap lines
                        self.gridLines.moveTo(0, self.YSize, -(self.ZSize))
                        self.gridLines.drawTo(0, self.YSize, self.ZSize)
                        self.gridLines.moveTo(0, -(self.YSize), -(self.ZSize))
                        self.gridLines.drawTo(0, -(self.YSize), self.ZSize)

            # Draw primary grid lines metering z axis if any z-length
            if(self.ZSize != 0):

                if((self.XSize != 0) and (self.XZPlaneShow != 0)):
                    # Draw x lines across z axis
                    # XZ Plane
                    for z in arange(0, self.ZSize, self.gridStep):
                        self.gridLines.moveTo(-(self.XSize), 0, z)
                        self.gridLines.drawTo(self.XSize, 0, z)
                        self.gridLines.moveTo(-(self.XSize), 0, -z)
                        self.gridLines.drawTo(self.XSize, 0, -z)

                    if(self.endCapLinesShow != 0):
                        # Draw endcap lines
                        self.gridLines.moveTo(-(self.XSize), 0, self.ZSize)
                        self.gridLines.drawTo(self.XSize, 0, self.ZSize)
                        self.gridLines.moveTo(-(self.XSize), 0, -(self.ZSize))
                        self.gridLines.drawTo(self.XSize, 0, -(self.ZSize))

                if((self.YSize != 0) and (self.YZPlaneShow != 0)):
                    # Draw y lines across z axis
                    # YZ Plane
                    for z in arange(0, self.ZSize, self.gridStep):
                        self.gridLines.moveTo(0, -(self.YSize), z)
                        self.gridLines.drawTo(0, self.YSize, z)
                        self.gridLines.moveTo(0, -(self.YSize), -z)
                        self.gridLines.drawTo(0, self.YSize, -z)

                    if(self.endCapLinesShow != 0):
                        # Draw endcap lines
                        self.gridLines.moveTo(0, -(self.YSize), self.ZSize)
                        self.gridLines.drawTo(0, self.YSize, self.ZSize)
                        self.gridLines.moveTo(0, -(self.YSize), -(self.ZSize))
                        self.gridLines.drawTo(0, self.YSize, -(self.ZSize))

        # Check to see if secondary grid lines should be drawn
        if(self.subdiv != 0):

            # Draw secondary grid lines
            self.subdivLines.setColor(self.subdivColor)

            if(self.XSize != 0):
                adjustedstep = self.gridStep / self.subdiv

                if((self.YSize != 0) and (self.XYPlaneShow != 0)):
                    # Draw y lines across x axis starting from center moving
                    # out XY
                    for x in arange(0, self.XSize, adjustedstep):
                        self.subdivLines.moveTo(x, -(self.YSize), 0)
                        self.subdivLines.drawTo(x, self.YSize, 0)
                        self.subdivLines.moveTo(-x, -(self.YSize), 0)
                        self.subdivLines.drawTo(-x, self.YSize, 0)

                if((self.ZSize != 0) and (self.XZPlaneShow != 0)):
                    # Draw z lines across x axis starting from center moving
                    # out XZ
                    for x in arange(0, self.XSize, adjustedstep):
                        self.subdivLines.moveTo(x, 0, -(self.ZSize))
                        self.subdivLines.drawTo(x, 0, self.ZSize)
                        self.subdivLines.moveTo(-x, 0, -(self.ZSize))
                        self.subdivLines.drawTo(-x, 0, self.ZSize)

            if(self.YSize != 0):

                if((self.YSize != 0) and (self.XYPlaneShow != 0)):
                    # Draw x lines across y axis
                    # XY
                    for y in arange(0, self.YSize, adjustedstep):
                        self.subdivLines.moveTo(-(self.XSize), y, 0)
                        self.subdivLines.drawTo(self.XSize, y, 0)
                        self.subdivLines.moveTo(-(self.XSize), -y, 0)
                        self.subdivLines.drawTo(self.XSize, -y, 0)

                if((self.ZSize != 0) and (self.YZPlaneShow != 0)):
                    # Draw z lines across y axis
                    # YZ
                    for y in arange(0, self.YSize, adjustedstep):
                        self.subdivLines.moveTo(0, y, -(self.ZSize))
                        self.subdivLines.drawTo(0, y, self.ZSize)
                        self.subdivLines.moveTo(0, -y, -(self.ZSize))
                        self.subdivLines.drawTo(0, -y, self.ZSize)

            if(self.ZSize != 0):

                if((self.XSize != 0) and (self.XZPlaneShow != 0)):
                    # Draw x lines across z axis
                    # XZ
                    for z in arange(0, self.ZSize, adjustedstep):
                        self.subdivLines.moveTo(-(self.XSize), 0, z)
                        self.subdivLines.drawTo(self.XSize, 0, z)
                        self.subdivLines.moveTo(-(self.XSize), 0, -z)
                        self.subdivLines.drawTo(self.XSize, 0, -z)

                if((self.YSize != 0) and (self.YZPlaneShow != 0)):
                    # Draw y lines across z axis
                    # YZ
                    for z in arange(0, self.ZSize, adjustedstep):
                        self.subdivLines.moveTo(0, -(self.YSize), z)
                        self.subdivLines.drawTo(0, self.YSize, z)
                        self.subdivLines.moveTo(0, -(self.YSize), -z)
                        self.subdivLines.drawTo(0, self.YSize, -z)

        # Create ThreeAxisGrid nodes and nodepaths
        # Create parent node and path
        self.parentNodePath = NodePath("threeaxisgrid-parentnode")

        # Create axis lines node and path, then reparent
        self.axisLinesNode = self.axisLines.create()
        self.axisLinesNodePath = NodePath(self.axisLinesNode)
        self.axisLinesNodePath.reparentTo(self.parentNodePath)

        # Create grid lines node and path, then reparent
        self.gridLinesNode = self.gridLines.create()
        self.gridLinesNodePath = NodePath(self.gridLinesNode)
        self.gridLinesNodePath.reparentTo(self.parentNodePath)

        # Create subdivision lines node and path then reparent
        self.subdivLinesNode = self.subdivLines.create()
        self.subdivLinesNodePath = NodePath(self.subdivLinesNode)
        self.subdivLinesNodePath.reparentTo(self.parentNodePath)

        #  Set antialiasing
        self.parentNodePath.setAntialias(AntialiasAttrib.MLine)

        return self.parentNodePath
