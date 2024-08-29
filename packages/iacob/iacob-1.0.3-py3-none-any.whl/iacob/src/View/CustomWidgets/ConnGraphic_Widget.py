import math
import math
import sys
from copy import deepcopy
from math import comb
from typing import Union

import numpy as np
import pyqtgraph as pg
import pyqtgraph.exporters as exporters
from PyQt5.QtCore import QPointF, Qt, QSize
from PyQt5.QtGui import QFont, QColor, QPainter, QTransform, QImage, QPainterPath, QFontMetrics
from PyQt5.QtWidgets import QGraphicsBlurEffect, QWidget, QVBoxLayout
from matplotlib.path import Path

from src.Model.Data_Storage.ConnGraph_Model import ConnGraph_Infos
from src.Model.Data_Storage.Filters_Model import Filters_Infos
from src.Model.Data_Storage.FiltersSave_Model import FiltersSave_Infos


class RegionLabelItem_ConnGraphic(pg.ImageItem):
    """
    A custom graphical item that displays a text label with a specified color and rotation within a graphics scene.
    """

    def __init__(self, text: str, coordinates, color: QColor = QColor(0, 0, 0), **kargs):
        """
        Initializes the RegionLabelItem_ConnGraphic instance.

        Parameters
        ----------
        text : str
            The text to be displayed on the label.
        coordinates : np.ndarray
            A 2x2 array of coordinates defining the bounding box for positioning the text.
        color : QColor, optional
            The color of the text. Default is black (QColor(0, 0, 0)).
        **kargs
            Additional keyword arguments passed to the parent class constructor.

        Raises
        ------
        ValueError
            If the coordinates parameter is not a 2x2 array.
        """

        # Init label attributes
        self.text = text
        self.coordinates = coordinates
        self.color = color
        self.shaded = False
        self.distance = 1

        size_min, size_max = 8, 12
        self.size = self.ComputeTextSize(size_min, size_max)
        self.rotation, self.anchor = self.ComputeTextRotation()

        np_image = self.InitText()
        super().__init__(np_image, **kargs)

        self.InitImage()

    def InitText(self):
        """
        Initializes the text by creating an image and drawing the text on it.

        Returns
        -------
        np.ndarray
            The NumPy array representation of the text image.
        """

        # Initialisation de la police pour calculer la taille de la zone de texte
        font = QFont("Arial", self.size, weight=QFont.Bold)
        self.text_width = QFontMetrics(font).width(self.text, len(self.text))
        self.text_height = QFontMetrics(font).height() + 6

        # width, height = self.size * len(self.text), self.size + 6
        image = QImage(self.text_width, self.text_height, QImage.Format_ARGB32)
        image.fill(Qt.transparent)

        # On utilise QPainter et QPainterPath pour afficher le texte
        painter = QPainter(image)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.setFont(font)

        path = QPainterPath()
        path.addText(0, self.size + 3, font, self.text)

        painter.fillPath(path, self.color)
        painter.end()

        # On convertit ensuite ce texte en matrice pour initialiser l'ImageItem
        np_image = self.ImageToNpArray(image)

        return np_image

    def InitImage(self):
        """
        Initializes the image by setting its position, transformation, and applying a blur effect.
        """

        self.setPos(self.ComputeTextCoordinates(self.distance))

        self.setTransform(self.ComputeTextTransform())

        blurEffect = QGraphicsBlurEffect(blurRadius=1.01)
        self.setGraphicsEffect(blurEffect)

    def ImageToNpArray(self, image: QImage):
        """
        Converts a QImage to a NumPy array.

        Parameters
        ----------
        image : QImage
            The QImage to be converted.

        Returns
        -------
        np.ndarray
            The NumPy array representation of the image.
        """

        width, height = image.width(), image.height()

        buffer = image.bits().asstring(width * height * 4)
        np_array = np.frombuffer(buffer, dtype=np.uint8).reshape((height, width, 4))

        return np_array

    def ComputeTextSize(self, size_min: int, size_max: int):
        """
        Computes the text size based on the bounding box size.

        Parameters
        ----------
        size_min : int
            The minimum allowed text size.
        size_max : int
            The maximum allowed text size.

        Returns
        -------
        int
            The computed text size, constrained between size_min and size_max.
        """

        # Compute text size based on the width of text area
        size = int(math.dist(self.coordinates[2], self.coordinates[3]))

        # To guarantee that text size is beetween given min and max size
        size = min(size_max, size)
        size = max(size_min, size)

        return size

    def ComputeTextRotation(self):
        """
        Computes the rotation angle and anchor point for the text.

        Returns
        -------
        tuple
            The rotation angle in degrees and the anchor point for the text.
        """

        if self.coordinates[2, 1] - self.coordinates[3, 1] < 0:
            x = -np.mean(self.coordinates[:, 0])
            y = -np.mean(self.coordinates[:, 1])
            anchor = (1, 0.5)
        else:
            x = np.mean(self.coordinates[:, 0])
            y = np.mean(self.coordinates[:, 1])
            anchor = (0, 0.5)

        angle = -np.arctan2(x, y)

        return np.degrees(angle), anchor

    def ComputeTextCoordinates(self, distance):
        """
        Computes the position of the text based on the distance from the bounding box.

        Parameters
        ----------
        distance : int
            The distance of the text from the bounding box.

        Returns
        -------
        QPointF
            The position of the text.
        """

        p1, p2 = self.coordinates[2], self.coordinates[3]

        # Calculate the normal vector to the longer side
        dx, dy = p2 - p1
        normal_vector = np.array([-dy, dx])
        normal_vector = normal_vector / np.linalg.norm(normal_vector) * distance

        # Determine the direction to place the point outside the region
        midpoint = (p1 + p2) / 2
        point = midpoint + normal_vector

        text_coordinates = QPointF(point[0], point[1])

        # Now the position is defined, we translate the text depending on the anchor settings

        x = text_coordinates.x()
        text_coordinates.setX(x)
        return text_coordinates

    def ComputeTextTransform(self):
        """
        Computes the transformation matrix for the text, including scaling and rotation.

        Returns
        -------
        QTransform
            The transformation matrix for the text.
        """

        tr = QTransform()
        tr.scale(0.3, 0.3)
        tr.rotate(self.rotation)

        xt = -self.anchor[1] * self.text_height
        # We use text_len to put the anchor at the end of the text if it is reversed
        yt = -self.anchor[0] * self.text_width + self.distance
        tr.translate(xt, yt)

        return tr

    """
    Si les connexions ne sont pas affichées : gris
    Si les connexions sont partiellement affichées : gris
    Si les connexions sont toutes affichées : noir
    """

    def SetTextShaded(self, shaded: bool):
        """
        Sets whether the text should be shaded and adjusts opacity accordingly.

        Parameters
        ----------
        shaded : bool
            If True, the text will be shaded. If False, the text will be fully opaque.
        """

        self.shaded = shaded
        if shaded:
            self.setOpacity(0.7)
        else:
            self.setOpacity(1)

    def IsPointInTextPolygon(self, x, y):
        """
        Checks if a given point is inside the polygon defined by the label's coordinates.

        Parameters
        ----------
        x : float
            The x-coordinate of the point.
        y : float
            The y-coordinate of the point.

        Returns
        -------
        bool
            True if the point is inside the polygon, False otherwise.
        """

        polygon = np.array([
            self.coordinates[0],
            self.coordinates[1],
            self.coordinates[2],
            self.coordinates[3]
        ])
        path = Path(polygon)

        return path.contains_point((x, y))


class RegionItem_ConnGraphic:
    """
    A class that represents a graphical region item with an inner region, an inter-region, and a text label in a PyQtGraph plot.
    """

    outside: pg.PlotDataItem  # Outer line of the region
    inside: pg.FillBetweenItem  # Colored part of the region

    interRegionOutside: pg.PlotDataItem  # Outer line of the region
    interRegionInside: pg.FillBetweenItem  # InterRegional colored part (between the region and text area)

    text: RegionLabelItem_ConnGraphic  # Text label
    edgesVisible: bool = True

    def __init__(self, code: int, name: str,
                 coordinates,  # coordinates of each item : region, interRegion, label
                 circlePoints,  # 3 list of corresponding circle coords for each item
                 precision=1,
                 regionColor=QColor(255, 255, 255, 255),  # inside color of a region, white by default
                 outlineColor=QColor(0, 0, 0, 255),  # outline color of a region, black by default
                 interRegionColor=QColor(255, 255, 255, 255),  # color of an inter-region associated to a region
                 *args):
        """
        Initializes a RegionItem_ConnGraphic instance.

        Parameters
        ----------
        code : int
            The code identifier for the region.
        name : str
            The name of the region.
        coordinates : list of np.ndarray
            A list containing four 2D numpy arrays:
            - Coordinates for the region boundary.
            - Coordinates for the inter-region boundary.
            - Coordinates for the label position.
        circlePoints : list of list of np.ndarray
            A list containing three lists of numpy arrays representing circle points for each item (region, inter-region, label).
        precision : int, optional
            Precision for drawing the arc of the region boundaries. Default is 1.
        regionColor : QColor, optional
            The color used to fill the inside of the region. Default is white (QColor(255, 255, 255, 255)).
        outlineColor : QColor, optional
            The color of the region's outline. Default is black (QColor(0, 0, 0, 255)).
        interRegionColor : QColor, optional
            The color used to fill the inter-region area. Default is white (QColor(255, 255, 255, 255)).
        *args
            Additional arguments passed to the parent class constructor.

        Raises
        ------
        ValueError
            If the `coordinates` parameter is not a list of four 2D numpy arrays, or if `circlePoints` is not a list of three lists of numpy arrays.
        """

        self.code = code  # Code of the region
        self.name = name  # Name of the region
        self.coordinates = coordinates  # Coordinates of region, interRegion and label
        self.regionColor = regionColor  # Region color
        self.outlineColor = outlineColor  # Region color (outline)
        self.interRegionColor = interRegionColor  # Inter region color
        self.precision = precision  # Precision value. WARING : Greatly affect performances
        self.allCircles = circlePoints  # Circles points for drawing region, interRegion and label

        self._ComputePolygons()
        self._DrawRegion()
        self._DrawInterRegion()
        self._DrawLabel()

        super().__init__(*args)

    def _ComputePolygons(self): 
        """
        Computes the polygon coordinates for the region and inter-region based on circle points.
        """

        # Compute polygon lines
        # regions
        self.innerCoords = self.LineToCircleArc(self.allCircles[0][0], self.coordinates[0][0])
        self.outerCoords = self.LineToCircleArc(self.allCircles[0][1], self.coordinates[0][3])

        # inter regions
        self.innerInterRegCoords = self.LineToCircleArc(self.allCircles[1][0], self.coordinates[1][0])
        self.outerInterRegCoords = self.LineToCircleArc(self.allCircles[1][1], self.coordinates[1][3])

    def _DrawRegion(self):
        """
        Draws the region's outer boundary and fills the inside with the specified color.
        """

        x_coords = np.append(np.append(self.innerCoords[:, 0],
                                       self.outerCoords[::-1, 0]),
                             self.innerCoords[0, 0])

        y_coords = np.append(np.append(self.innerCoords[:, 1],
                                       self.outerCoords[::-1, 1]),
                             self.innerCoords[0, 1])

        # Draw the outline of the polygon
        self.outside = pg.PlotDataItem(x_coords, y_coords, pen=pg.mkPen(color=self.outlineColor, width=1))

        # Color the inside of the polygon
        innerLine = pg.PlotDataItem(self.innerCoords[:, 0], self.innerCoords[:, 1])
        outerLine = pg.PlotDataItem(self.outerCoords[:, 0], self.outerCoords[:, 1])

        self.inside = pg.FillBetweenItem(innerLine, outerLine, brush=pg.mkBrush(self.regionColor))

    def _DrawInterRegion(self):
        """
        Draws the inter-region's outer boundary and fills the inside with the specified color.
        """

        x_coords = np.append(np.append(self.innerInterRegCoords[:, 0],
                                       self.outerInterRegCoords[::-1, 0]),
                             self.innerInterRegCoords[0, 0])

        y_coords = np.append(np.append(self.innerInterRegCoords[:, 1],
                                       self.outerInterRegCoords[::-1, 1]),
                             self.innerInterRegCoords[0, 1])

        # Draw the outline of the polygon
        self.interRegionOutside = pg.PlotDataItem(x_coords, y_coords,
                                                  pen=pg.mkPen(color=self.interRegionColor, width=1))

        # Color the inside of the polygon
        innerLine = pg.PlotDataItem(self.innerInterRegCoords[:, 0], self.innerInterRegCoords[:, 1])
        outerLine = pg.PlotDataItem(self.outerInterRegCoords[:, 0], self.outerInterRegCoords[:, 1])

        self.interRegionInside = pg.FillBetweenItem(innerLine, outerLine, brush=pg.mkBrush(self.interRegionColor))

    def _DrawLabel(self):
        """
        Draws the text label for the region.
        """

        # Draw text next to the polygon
        self.text = RegionLabelItem_ConnGraphic(self.name, self.coordinates[2])

    # Function used for rouding region borders
    def LineToCircleArc(self, circlePoints, start):
        """
        Computes the arc of a circle from the closest point to the start.

        Parameters
        ----------
        circlePoints : np.ndarray
            Points on the circle used to compute the arc.
        start : np.ndarray
            The starting point for the arc computation.

        Returns
        -------
        np.ndarray
            The computed arc points.
        """

        # Find the two points on the circle closest to the start and end points
        startDistances = np.linalg.norm(circlePoints - start, axis=1)

        startIndex = np.argmin(startDistances)
        endIndex = startIndex + self.precision

        return circlePoints[startIndex:endIndex + 1]

    def IsPointInRegionPolygon(self, x, y):
        """
        Compute if the given point is inside the polygon region

        Parameters
        ----------
        x : int
            x coordinate of the point
        y : int
            y coordinate of the point

        Returns
        -------
        bool
            True if inside else False

        """

        # Create matplotlib Path object
        polygonPoints = np.vstack((self.innerCoords, self.outerCoords[::-1]))
        polygonPath = Path(polygonPoints)

        # Check if the point is inside the polygon
        return polygonPath.contains_point((x, y))


class EdgeItem_ConnGraphic(pg.PlotCurveItem):
    """
    A class that represents a graphical edge item with a Bezier curve in a PyQtGraph plot.
    """

    value = 0
    node1: int
    node2: int
    typeFiltered: bool
    regionFiltered: bool
    weightRankFiltered: bool

    def __init__(self, node1, node2, value, node1_x, node1_y, node2_x, node2_y,
                 color: QColor = QColor(0, 0, 0), width=1, precision=20, plotRadius=0.0,
                 *args, **kargs):
        """
        Initializes an EdgeItem_ConnGraphic instance.

        Parameters
        ----------
        node1 : int
            Identifier for the first node connected by the edge.
        node2 : int
            Identifier for the second node connected by the edge.
        value : float
            The value associated with the edge.
        node1_x : float
            The x-coordinate of the first node.
        node1_y : float
            The y-coordinate of the first node.
        node2_x : float
            The x-coordinate of the second node.
        node2_y : float
            The y-coordinate of the second node.
        color : QColor, optional
            The color of the edge line. Default is black (QColor(0, 0, 0)).
        width : float, optional
            The width of the edge line. Default is 1.
        precision : int, optional
            The number of points used to approximate the Bezier curve. Default is 20.
        plotRadius : float, optional
            The radius used to adjust the curvature of the Bezier curve. Default is 0.0.
        *args
            Additional arguments passed to the parent class constructor.
        **kargs
            Additional keyword arguments passed to the parent class constructor.

        Raises
        ------
        ValueError
            If the `precision` parameter is less than 1.
        """

        self.node1 = node1
        self.node2 = node2
        self.node1_x = node1_x
        self.node1_y = node1_y
        self.node2_x = node2_x
        self.node2_y = node2_y
        self.precision = precision
        self.value = value
        self.typeFiltered = False
        self.regionFiltered = False
        self.weightRankFiltered = False

        # For drawing
        self.color = color
        self.width = width

        x, y = self.computeBezierCurve(plotRadius)

        pen = pg.mkPen(color=self.color, width=self.width)

        super().__init__(x=x, y=y, pen=pen, *args, **kargs)

    def computeBezierCurve(self, plotRadius=0.0):
        """
        Computes the Bezier curve points between the two nodes.

        Parameters
        ----------
        plotRadius : float, optional
            The radius used to adjust the curvature of the Bezier curve. Default is 0.0.

        Returns
        -------
        tuple of np.ndarray
            x and y coordinates of the Bezier curve points.
        """

        p0 = np.array([self.node1_x, self.node1_y])
        p1 = np.array([self.node2_x, self.node2_y])
        midpoint = (p0 + p1) / 2

        dist = np.linalg.norm(p1 - p0)

        curvatureFactor = (plotRadius - dist) / plotRadius if plotRadius > 0.0 else 0.0

        controlPoint = curvatureFactor * midpoint

        controlPoints = np.array([p0, controlPoint, p1])
        n = len(controlPoints) - 1

        values = np.linspace(0, 1, self.precision)
        bezierPoints = np.array(
            [sum(comb(n, i) * (t ** i) * ((1 - t) ** (n - i)) * controlPoints[i]
                 for i in range(n + 1)) for t in values])

        return bezierPoints[:, 0], bezierPoints[:, 1]

    def SetColor(self, color: QColor):
        """
        Sets the color of the edge and updates its appearance.

        Parameters
        ----------
        color : QColor
            The new color for the edge line.
        """
        self.color = color
        pen = pg.mkPen(color=color, width=self.width)
        self.setPen(pen)

    def SetWidth(self, width: float):
        """
        Sets the width of the edge and updates its appearance.

        Parameters
        ----------
        width : float
            The new width for the edge line.
        """

        self.width = width
        pen = pg.mkPen(color=self.color, width=width)
        self.setPen(pen)

    def updateVisible(self):
        """
        Updates the visibility of the edge based on its filter status.
        """
        
        visible = not self.typeFiltered or not self.regionFiltered or not self.weightRankFiltered
        super().setVisible(visible)

    def setVisible(self, visible):
        """
        Sets the visibility of the edge based on its filter status and the provided visibility flag.

        Parameters
        ----------
        visible : bool
            A flag indicating whether the edge should be visible.
        """

        filtered = self.typeFiltered or self.regionFiltered or self.weightRankFiltered
        visible = visible and not filtered  # Can be true only if the edge is not filtered

        super().setVisible(visible)

    def forceVisible(self, visible):
        """
        Forces the visibility of the edge, overriding any filters.

        Parameters
        ----------
        visible : bool
            A flag indicating whether the edge should be visible.
        """

        super().setVisible(visible)


class ConnGraphicView(pg.ViewBox):
    """
    A graphical view class for displaying and interacting with a network graph.
    """
    
    graph_info: ConnGraph_Infos
    filters: Filters_Infos
    filtersSave: FiltersSave_Infos
    regions: list[Union[RegionItem_ConnGraphic, None]]  # Can contain both None or RegionItem_ConnGraphic
    colors: list[QColor]
    edges: list[EdgeItem_ConnGraphic]
    radius: float  # Used to compute edges curvature
    edgesVisible: bool
    graphicFilter: bool  # True if a region is highlighted or hidden by a click on the chart
    highlightedRegions: bool

    def __init__(self, colorSet: list[QColor], parent=None):
        """
        Initializes the ConnGraphicView instance.
        
        Parameters
        ----------
        colorSet : list[QColor]
            List of colors used for edge coloring.
        parent : optional
            Parent widget or None.
        """
        
        super().__init__(parent)

        self.graph_info = ConnGraph_Infos()
        self.filters = Filters_Infos()

        numPoints = len(self.graph_info.areasOrder) + 2  # For blank at begin and end

        # Init regions and edges list
        self.regions = [None for i in range(numPoints)]
        self.edges = []
        self.edgesVisible = True
        self.highlightedRegions = False

        # Init class attributes

        self.filtersSave = FiltersSave_Infos()  # Save the current state of the filter
        self.filtersSave.LoadCurrentFilters(self.filters.SaveCurrentFilters())

        self.graphicFilter = False
        self.numPoints = numPoints
        self.maxAbsConnValue = self.graph_info.absMinMax[1]
        self.edgeThicknessFactor = 5
        self.colorSet = colorSet

        # Image exporter
        self.imageExporter = None

        # Zoom
        self.XRange = self.YRange = 100

        self._InitViewSettings()
        self._InitGraphSettings()
        self._GenerateGraphValues()
        self._InitGraph_Regions()
        self._InitGraph_Edges()
        
    def _InitViewSettings(self):
        """
        Initializes the view settings for the graph.
        
        Sets the background color and view range for the graph.
        """
        
        self.disableAutoRange()
        #self.setMouseEnabled(False, False)  # Disable mouse interactions
        self.setBackgroundColor("w")

        self.setRange(xRange=(-self.XRange, self.XRange), yRange=(-self.YRange, self.YRange))

    def ResetZoom(self):
        """
        Resets the zoom level of the graph to the initial range.
        """
        
        self.setRange(xRange=(-self.XRange, self.XRange), yRange=(-self.YRange, self.YRange))

    def _InitGraphSettings(self):
        """
        Initializes graph-specific settings including radius, thickness, and font.
        
        Sets parameters related to the appearance and smoothing of the graph.
        """
        
        self.radius = 50  # Radius in pyqtgraph unit of the text on the plot
        self.regionThickness = 300 / self.numPoints  # The more regions on the graph, the less the thickness of the donut will be
        self.interRegionThickness = self.regionThickness / 2
        self.interRegionDistance = self.regionThickness + 1  # Distance between region item and interRegion polygon
        self.textDistance = self.interRegionDistance + self.interRegionThickness + 0  # Distance between interRegion polygon and regionLabel item
        self.textLength = 20  # Lenght in pyqtgraph unit of the text on the plot

        # IMPORTANT : GREATLY AFFECT PERFORMANCES, but improves edge and region smoothing
        self.precision = 20  # Nb of lines which compose an edge

        # Changing the font can make the text too long and go outside the plotting area
        self.font = QFont("Arial", pointSize=25, weight=QFont.ExtraBold)

    def _GenerateGraphValues(self):
        """
        Generates the coordinate values for regions, edges, and labels in the graph.
        
        Computes positions for drawing regions and edges, as well as text labels.
        """
            
        angles = np.linspace(0.5 * np.pi, 2.5 * np.pi, self.numPoints, endpoint=False)

        # coordinates of each region
        self.innerPoints = (np.vstack((np.cos(angles), np.sin(angles))).T
                            * self.radius)
        self.innerPoints = np.concatenate((self.innerPoints, [self.innerPoints[0]]))

        self.outerPoints = (np.vstack((np.cos(angles), np.sin(angles))).T
                            * (self.radius + self.regionThickness))
        self.outerPoints = np.concatenate((self.outerPoints, [self.outerPoints[0]]))

        # coordinates of each interRegion polygon
        self.interRegionInnerPoints = (np.vstack((np.cos(angles), np.sin(angles))).T
                                       * (self.radius + self.interRegionDistance))
        self.interRegionInnerPoints = np.concatenate((self.interRegionInnerPoints, [self.interRegionInnerPoints[0]]))

        self.interRegionOuterPoints = (np.vstack((np.cos(angles), np.sin(angles))).T
                                       * (self.radius + self.interRegionDistance + self.interRegionThickness))
        self.interRegionOuterPoints = np.concatenate((self.interRegionOuterPoints, [self.interRegionOuterPoints[0]]))

        # coordinates of each label
        self.innerTextPoints = (np.vstack((np.cos(angles), np.sin(angles))).T
                                * (self.radius + self.textDistance))
        self.innerTextPoints = np.concatenate((self.innerTextPoints, [self.innerTextPoints[0]]))

        self.outerTextPoints = (np.vstack((np.cos(angles), np.sin(angles))).T
                                * (self.radius + self.textDistance + self.textLength))
        self.outerTextPoints = np.concatenate((self.outerTextPoints, [self.outerTextPoints[0]]))

        # create two circle for the inner and outer line of the donut
        circleAngle = np.linspace(0.5 * np.pi, 2.5 * np.pi, self.numPoints * self.precision, endpoint=False)
        circleAngle = np.append(circleAngle, circleAngle[0])

        circlesPoints = np.vstack((np.cos(circleAngle), np.sin(circleAngle))).T

        # Region item circles
        innerRegionCirclePoints = circlesPoints * self.radius
        outerRegionCirclePoints = circlesPoints * (self.radius + self.regionThickness)

        # InterRegion polygon circles
        innerInterRegionCirclePoints = circlesPoints * (self.radius + self.interRegionDistance)
        outerInterRegionCirclePoints = circlesPoints * (
                    self.radius + self.interRegionDistance + self.interRegionThickness)

        # Text circles
        innerCircleTextPoints = circlesPoints * (self.radius + self.textDistance)
        outerCircleTextPoints = circlesPoints * (self.radius + self.textDistance + self.textLength)

        self.allCircles = ((innerRegionCirclePoints, outerRegionCirclePoints),
                           (innerInterRegionCirclePoints, outerInterRegionCirclePoints),
                           (innerCircleTextPoints, outerCircleTextPoints))

    def _InitGraph_Regions(self):
        """
        Initializes the regions of the graph based on `graph_info`.
        
        Creates and adds region items to the graph view.
        """
        
        pos = 1
        for region in self.graph_info.areasOrder:
            pos += 1

            region_name = region[0]
            if region_name == "xxxx":
                continue

            region_info = self.graph_info.areaInfos[region_name]

            interRegionColor = self.graph_info.colorMajorRegions[region_info["MajorRegion"]]
            interRegionColor = [int(color * 255) for color in interRegionColor]

            self.CreateRegionOnGraph(self.graph_info.GetRegionIDWithName(region_name),
                                     region_name, region_info["RGBA"], interRegionColor, pos)

    def _InitGraph_Edges(self):
        """
        Initializes the edges of the graph based on `graph_info`.
        
        Creates and adds edge items to the graph view.
        """
        
        edges = []

        for nodes, value in self.graph_info.edgesValues_withoutDuplicata.items():
            node1, node2 = nodes[0], nodes[1]

            edges.append([value, node1, node2])

        # For layering edges based on their absolute values
        edges.sort(key=lambda edge: abs(edge[0]))
        for edge in edges:
            self.CreateEdge(edge[1], edge[2], edge[0])

    def GetRegion(self, code):
        """
        Retrieves a region from the graph by its code.
        
        Parameters
        ----------
        code : int
            The code identifying the region.
        
        Returns
        -------
        RegionItem_ConnGraphic or None
            The region item if found, otherwise None.
        """

        for region in self.regions:
            if region is not None:
                if region.code == code:
                    return region
        return None

    def CreateEdge(self, node1, node2, value):
        """
        Creates an edge between two nodes and adds it to the graph.
        
        Parameters
        ----------
        node1 : int
            The code for the first node.
        node2 : int
            The code for the second node.
        value : float
            The value representing the weight of the edge.
        """
        
        region1 = self.GetRegion(node1)
        region2 = self.GetRegion(node2)

        # Standardize edge value with the absolute value
        maxAbsConnValue = self.graph_info.plotMinMax[1]

        if region1 is not None and region2 is not None:

            # Compute edge ends
            region1Coordinates = region1.coordinates[0]
            region2Coordinates = region2.coordinates[0]

            color = self.ComputeEdgeColor(value)

            edgeW = abs(value / maxAbsConnValue * self.edgeThicknessFactor)

            # Get coordinate of each region border
            x1 = np.mean([region1Coordinates[2, 0], region1Coordinates[3, 0]])
            y1 = np.mean([region1Coordinates[2, 1], region1Coordinates[3, 1]])
            x2 = np.mean([region2Coordinates[2, 0], region2Coordinates[3, 0]])
            y2 = np.mean([region2Coordinates[2, 1], region2Coordinates[3, 1]])

            # Create the Edge
            edge = EdgeItem_ConnGraphic(node1, node2,
                                        value,
                                        x1, y1,
                                        x2, y2,
                                        color,
                                        width=edgeW,
                                        precision=self.precision,
                                        plotRadius=self.radius)

            self.AddEdge(edge)

    def ComputeEdgeColor(self, value):
        """
        Computes the color of an edge based on its value and color set.
        
        Parameters
        ----------
        value : float
            The value to determine the edge color.
        
        Returns
        -------
        QColor
            The computed color of the edge.
        """
        
        color_count = len(self.colorSet)
        bornes = self.graph_info.absMinMax[1]
        
        # Normalize the value to a ratio between 0 and 1
        ratio = abs(value) / bornes
        ratio = max(0, min(ratio, 1))  # Clamp ratio between 0 and 1

        def interpolate_color(c1, c2, ratio):
            r = int(c1.red() + (c2.red() - c1.red()) * ratio)
            g = int(c1.green() + (c2.green() - c1.green()) * ratio)
            b = int(c1.blue() + (c2.blue() - c1.blue()) * ratio)
            return QColor(r, g, b)

        if color_count == 2:
            # Interpolate between two colors
            return interpolate_color(self.colorSet[0], self.colorSet[1], ratio)
        
        elif color_count == 3:
            # Interpolate between three colors
            if value < 0:
                return interpolate_color(self.colorSet[1], self.colorSet[0], ratio)
            else:
                return interpolate_color(self.colorSet[1], self.colorSet[2], ratio)
        
        elif color_count == 7:
            if value < 0:
                # Negative value range
                segment = (-value / bornes) * 3  # Map to the range [0, 3]
                lower_index = int(segment)
                upper_index = min(lower_index + 1, 3)
                segment_ratio = segment - lower_index

                # Clamp indices to be within valid range
                lower_index = max(0, min(3, lower_index))
                upper_index = max(0, min(3, upper_index))
                lower_color_index = 3 - lower_index
                upper_color_index = 3 - upper_index
                # Ensure indices do not exceed the bounds of colorSet
                lower_color_index = max(0, min(6, lower_color_index))
                upper_color_index = max(0, min(6, upper_color_index))
                return interpolate_color(self.colorSet[lower_color_index], self.colorSet[upper_color_index], segment_ratio)
            else:
                # Positive value range
                segment = (value / bornes) * 3  # Map to the range [0, 3]
                lower_index = int(segment)
                upper_index = min(lower_index + 1, 3)
                segment_ratio = segment - lower_index

                # Clamp indices to be within valid range
                lower_index = max(0, min(3, lower_index))
                upper_index = max(0, min(3, upper_index))
                lower_color_index = 4 + lower_index
                upper_color_index = 4 + upper_index
                # Ensure indices do not exceed the bounds of colorSet
                lower_color_index = max(0, min(6, lower_color_index))
                upper_color_index = max(0, min(6, upper_color_index))
                return interpolate_color(self.colorSet[lower_color_index], self.colorSet[upper_color_index], segment_ratio)

        # Handle cases where color_count is not recognized
        return QColor(0, 0, 0)  # Default color or error handling

    def UpdateEdgesColorSet(self, colorSet : list[QColor]):
        """
        Updates the color set for edges and refreshes their colors.
        
        Parameters
        ----------
        colorSet : list[QColor]
            New list of colors for the edges.
        """

        self.colorSet = colorSet

        for edge in self.edges:
            if edge:
                color = self.ComputeEdgeColor(edge.value)
                edge.SetColor(color)


    # ---------- Accessors ----------

    def CreateRegionOnGraph(self, code, name, regionColor, interRegionColor, pos):
        """
        Creates and adds a new region to the graph at a specified position.
        
        Parameters
        ----------
        code : int
            The code identifying the region.
        name : str
            The name of the region.
        regionColor : list[int]
            RGB color values for the region.
        interRegionColor : list[int]
            RGB color values for the inter-region area.
        pos : int
            Position in the list of regions.
        
        Raises
        ------
        ValueError
            If position is out of bounds or color values are invalid.
        """
        
        pos -= 1

        # Get coordinates on the inner/outer circle of the graph
        regionCoordinates = np.array([
            [self.outerPoints[pos][0], self.outerPoints[pos][1]],
            [self.outerPoints[pos + 1][0], self.outerPoints[pos + 1][1]],
            [self.innerPoints[pos + 1][0], self.innerPoints[pos + 1][1]],
            [self.innerPoints[pos][0], self.innerPoints[pos][1]]
        ])

        interRegionCoordinates = np.array([
            [self.interRegionOuterPoints[pos][0], self.interRegionOuterPoints[pos][1]],
            [self.interRegionOuterPoints[pos + 1][0], self.interRegionOuterPoints[pos + 1][1]],
            [self.interRegionInnerPoints[pos + 1][0], self.interRegionInnerPoints[pos + 1][1]],
            [self.interRegionInnerPoints[pos][0], self.interRegionInnerPoints[pos][1]]
        ])

        textCoordinates = np.array([
            [self.outerTextPoints[pos][0], self.outerTextPoints[pos][1]],
            [self.outerTextPoints[pos + 1][0], self.outerTextPoints[pos + 1][1]],
            [self.innerTextPoints[pos + 1][0], self.innerTextPoints[pos + 1][1]],
            [self.innerTextPoints[pos][0], self.innerTextPoints[pos][1]]
        ])

        allCoordinates = (regionCoordinates, interRegionCoordinates, textCoordinates)

        # Create region

        # Convert RGB color values to QColor object
        regionColor = QColor(regionColor[0], regionColor[1], regionColor[2])
        interRegionColor = QColor(interRegionColor[0], interRegionColor[1], interRegionColor[2])

        #outlineColor = QColor(color[2], color[1], color[0])
        self.regions[pos] = RegionItem_ConnGraphic(code, name,
                                                   allCoordinates,
                                                   self.allCircles,
                                                   precision=self.precision,
                                                   regionColor=regionColor,
                                                   interRegionColor=interRegionColor)
        self.AddRegion(self.regions[pos], pos)

    def AddRegion(self, region: RegionItem_ConnGraphic, pos=None):
        """
        Adds a region to the graph at a specified position or appends it.
        
        Parameters
        ----------
        region : RegionItem_ConnGraphic
            The region to add.
        pos : int, optional
            The position to insert the region. If None, appends the region.
        """
        
        if pos is None:
            self.regions.append(region)
        else:
            self.regions[pos] = region

        # Add region polygon the connGraphicView
        self.addItem(region.inside)
        self.addItem(region.outside)

        # Add interRegion polygon to the connGraphicView
        self.addItem(region.interRegionInside)
        self.addItem(region.interRegionOutside)

        # Add label to the connGraphicView
        self.addItem(region.text)

    def AddEdge(self, edge: EdgeItem_ConnGraphic):
        """
        Adds an edge to the graph.
        
        Parameters
        ----------
        edge : EdgeItem_ConnGraphic
            The edge to add.
        """
        
        if edge is not None:
            self.edges.append(edge)

            # Add edge to the connGraphicView
            self.addItem(edge)

    def GetEdge(self, node1, node2):
        """
        Retrieves an edge between two nodes.
        
        Parameters
        ----------
        node1 : int
            The code for the first node.
        node2 : int
            The code for the second node.
        
        Returns
        -------
        EdgeItem_ConnGraphic or None
            The edge item if found, otherwise None.
        """
        
        for edge in self.edges:
            if edge is not None:
                if edge.node1 == node1 and edge.node2 == node2:
                    return edge
        return None

    def GetRegionEdges(self, code):
        """
        Retrieves all edges connected to a specific region.
        
        Parameters
        ----------
        code : int
            The code identifying the region.
        
        Returns
        -------
        list[EdgeItem_ConnGraphic]
            List of edges connected to the region.
        """

        edges = []
        for edge in self.edges:
            if edge is not None:
                if edge.node1 == code or edge.node2 == code:
                    edges.append(edge)
        return edges

    def GetSortedEdgeList(self, reverse: bool):
        """
        Returns a sorted list of edges based on their absolute values.
        
        Parameters
        ----------
        reverse : bool
            If True, sorts in descending order; otherwise, ascending order.
        
        Returns
        -------
        list[EdgeItem_ConnGraphic]
            Sorted list of edges.
        """

        # True mean descending, False mean ascending
        return sorted(self.edges, key=lambda edge: abs(edge.value), reverse=reverse)

    def GetVisibleEdgesInfos(self):
        """
        Retrieves information about visible edges in the graph.
        
        Returns
        -------
        dict[tuple[int, int], dict[str, bool]]
            Dictionary with edge node pairs as keys and visibility information as values.
        """
        
        edges = {}

        for edge in self.edges:
            infos = {"visible": edge.isVisible(), "value": edge.value}
            edges[(edge.node1, edge.node2)] = infos

        return edges


    # ---------- Click methods ----------

    def mouseClickEvent(self, ev):
        """
        Handles mouse click events to interact with regions in the graph.
        
        Parameters
        ----------
        ev : QMouseEvent
            The mouse event.
        """
        
        #super().mouseClickEvent(ev) open context menu with right click, so we need to override it
        if ev.button() == Qt.MouseButton.LeftButton or ev.button() == Qt.MouseButton.RightButton:
            # Convert pixel position into scene position
            p = self.mapSceneToView(ev.scenePos())  # QPointF

            # Search for a region under clicked point
            for region in self.regions:
                if region is not None and (region.IsPointInRegionPolygon(p.x(), p.y()) or
                                           region.text.IsPointInTextPolygon(p.x(), p.y())):
                    ev.accept()  # Indicate that the event will be handled so the parent won't receive it
                    self.RegionClickEvent(ev, region)
                    break

    def RegionClickEvent(self, ev, region):
        """
        Handles click events on a specific region.
        
        Parameters
        ----------
        ev : QMouseEvent
            The mouse event.
        region : RegionItem_ConnGraphic
            The region that was clicked.
        """
        
        if ev.button() == Qt.MouseButton.LeftButton and not region.edgesVisible:
            self.graphicFilter = True
            self.SetRegionEdgesVisible(region, True)
        elif ev.button() == Qt.MouseButton.LeftButton and region.edgesVisible:
            self.graphicFilter = True
            self.HighlightRegionEdges(region)
        elif ev.button() == Qt.MouseButton.RightButton:
            self.graphicFilter = True
            self.SetRegionEdgesVisible(region, False)

    def ShowExportDialog(self):
        """
        Shows a dialog to export the current view as an image.
        """
            
        if self.imageExporter is None:
            self.imageExporter = exporters.ImageExporter(self)

            dpi = 300
            current_size = self.imageExporter.parameters()['width']
            scaling_factor = dpi / 72.0
            self.imageExporter.parameters()['width'] = current_size * scaling_factor

            self.imageExporter.export()


    # ---------- Filter methods ----------

    def Filter(self):

        """
        Applies filters to the graph edges based on current filter settings.

        Actually, there are 4 filter applicable to the edges :
        - Connexion type
        - Inter-regional connexion type
        - Weight
        - Absolute weight
        - Rank of the edges

        Updates edge visibility and attributes according to the filters applied.
        """

        if not (self.filters.discardWeight or self.filters.discardAbsWeight or self.filters.discardRank):
            for edge in self.edges:
                edge.weightRankFiltered = False
            self.ToggleAllEdges(True)

        newFiltersDiscard = [self.filters.discardWeight, self.filters.discardAbsWeight, self.filters.discardRank]
        oldFiltersDiscard = [self.filtersSave.discardWeight, self.filtersSave.discardAbsWeight, self.filtersSave.discardRank]
        forceChange = not (newFiltersDiscard == oldFiltersDiscard)

        # Weight filter
        if self.filters.discardWeight:
            if self.filtersSave.weightBetween_threshold != self.filters.weightBetween_threshold or forceChange:
                self.KeepEdgesBetweenWeight(self.filters.WeightMin(), self.filters.WeightMax())

        # Absolute weight filter
        if self.filters.discardAbsWeight:
            if self.filtersSave.absWeightBetween_threshold != self.filters.absWeightBetween_threshold or forceChange:
                self.KeepAbsEdgesBetweenWeight(self.filters.AbsWeightMin(), self.filters.AbsWeightMax())

        if self.filters.discardRank:
            if self.filtersSave.rankBetween_threshold != self.filters.rankBetween_threshold or forceChange:
                self.KeepEdgesBetweenRank(self.filters.RankMin(), self.filters.RankMax())

        # Connexion type filter
        if self.filtersSave.contralateral_connType != self.filters.contralateral_connType:
            self.ToggleConnType("Contralateral", self.filters.contralateral_connType)

        if self.filtersSave.homotopic_connType != self.filters.homotopic_connType:
            self.ToggleConnType("Homotopic", self.filters.homotopic_connType)

        if self.filtersSave.ipsilateral_connType != self.filters.ipsilateral_connType:
            self.ToggleConnType("Ipsilateral", self.filters.ipsilateral_connType)

        if self.filtersSave.other_connType != self.filters.other_connType:
            self.ToggleConnType("Other", self.filters.other_connType)

        # Inter-regional connexion type filter
        for (name1, name2), visible in self.filters.discardInterRegConn.items():
            # Check if the state have changed since the last call of Filter function
            if self.filtersSave.InterRegConnEnabled(name1, name2) != visible:
                self.FilterBetweenAreas()
                break

        if self.filtersSave.coefWidthEdges != self.filters.coefWidthEdges:
            self.ToggleCoefWithEdges(self.filters.coefWidthEdges)

        if self.filtersSave.colorEdges != self.filters.colorEdges:
            self.UpdateEdgesColorSet(self.filters.colorEdges)

        self.UpdateRegionsEdgesVisibleState()

        # As soon a filter is detected, turn off the graphic filter
        if self.graphicFilter:
            self.ResetGraphicFilter()

        # Save the current state of the filter
        self.filtersSave.LoadCurrentFilters(self.filters.SaveCurrentFilters())

    def ToggleAllRegions(self, visible: bool):
        """
        Toggles the visibility of all regions in the graph.
        
        Parameters
        ----------
        visible : bool
            If True, makes all regions visible; otherwise, hides them.
        """
        
        for region in self.regions:
            self.SetRegionEdgesVisible(region, visible)

    def ToggleAllEdges(self, visible: bool, force: bool = False):
        """
        Toggles the visibility of all edges in the graph.
        
        Parameters
        ----------
        visible : bool
            If True, makes all edges visible; otherwise, hides them.
        force : bool, optional
            If True, forces the visibility change regardless of current state.
        """
        
        self.ResetGraphicFilter()

        # Toggle edges
        for edge in self.edges:
            if edge is not None:
                if force:
                    edge.forceVisible(visible)
                else:
                    edge.setVisible(visible)

        # Update edgesVisible state and text color
        for region in self.regions:
            if region is not None:
                region.edgesVisible = visible
                region.text.SetTextShaded(not visible)

        self.edgesVisible = visible

    def ResetFilter(self):
        """
        Resets all filters applied to the edges by making all edges visible.
        
        This method ensures that all edges are shown by calling `ToggleAllEdges` with `visible=True` and `force=True`.
        """
        
        self.ToggleAllEdges(True, True)

    def ResetGraphicFilter(self):
        """
        Resets the graphical filter state by making all region edges visible and resetting zoom.
        
        This method hides graphical filtering effects by setting `graphicFilter` to `False`, 
        making all edges of regions visible, and resetting the zoom level.
        """

        self.graphicFilter = False
        for region in self.regions:
            if region is not None:
                if region.text.shaded:
                    self.SetRegionEdgesVisible(region, True)

        self.ResetZoom()

        self.highlightedRegions = False

    def SetRegionEdgesVisible(self, region, visible):
        """
        Sets the visibility of edges connected to a specific region and updates the region's shaded text state.
        
        Parameters
        ----------
        region : RegionItem_ConnGraphic
            The region whose edges' visibility will be updated.
        visible : bool
            If True, makes the edges visible; otherwise, hides them.
        """
        
        if region is not None:
            edges = self.GetRegionEdges(region.code)

            # Toggle edges
            for edge in edges:
                edge.setVisible(visible)

            region.text.SetTextShaded(not visible)

            region.edgesVisible = visible

    def UpdateRegionsEdgesVisibleState(self):
        """
        Updates the visibility state of edges for each region.
        
        Sets `region.edgesVisible` to `False` if all edges connected to the region are hidden. 
        Otherwise, sets it to `True`.
        """
        
        for region in self.regions:
            if region is not None:
                edges = self.GetRegionEdges(region.code)
                region.edgesVisible = False

                for edge in edges:
                    if edge.isVisible():
                        region.edgesVisible = True
                        break

    def HighlightRegionEdges(self, region):
        """
        Highlights the edges of a specific region and ensures regions are hidden if no edges are highlighted.
        
        Parameters
        ----------
        region : RegionItem_ConnGraphic
            The region whose edges are to be highlighted.
        """
        
        if region is not None:
            if not self.highlightedRegions:
                self.highlightedRegions = True
                self.ToggleAllRegions(False)

            self.SetRegionEdgesVisible(region, True)

    def FilterBetweenAreas(self):
        """
        Filters edges based on the areas of the connected regions.
        
        Edges are filtered according to whether the connection between their regions is enabled 
        in the current filter settings.
        """
        
        filters = Filters_Infos()
        for edge in self.edges:

            # Get edge areas names
            edgeRegion1 = self.GetRegion(edge.node1).name
            edgeRegion2 = self.GetRegion(edge.node2).name
            edgeArea1 = self.graph_info.areaInfos[edgeRegion1]["MajorRegion"]
            edgeArea2 = self.graph_info.areaInfos[edgeRegion2]["MajorRegion"]

            visible = filters.InterRegConnEnabled(edgeArea1, edgeArea2)

            edge.regionFiltered = not visible
            edge.setVisible(visible)

    def ToggleConnType(self, connType, visible):
        """
        Toggles the visibility of edges based on their connection type.
        
        Parameters
        ----------
        connType : str
            The type of connection to filter.
        visible : bool
            If True, makes edges of the specified type visible; otherwise, hides them.
        """
        
        for edge in self.edges:
            edgeType = self.graph_info.edgesTypeConnexion[edge.node1][edge.node2]
            if edgeType == connType:
                edge.typeFiltered = not visible
                edge.setVisible(visible)
       
    def ToggleCoefWithEdges(self, newWidthCoef):
        """
        Adjusts the width of edges based on a new coefficient.
        
        Parameters
        ----------
        newWidthCoef : float
            The new coefficient to adjust edge thickness.
        """
        
        self.edgeThicknessFactor = newWidthCoef

        for edge in self.edges:
            newWidth = abs(edge.value / self.graph_info.plotMinMax[1] * self.edgeThicknessFactor)
            edge.SetWidth(newWidth)

    def KeepEdgesBetweenWeight(self, inf, sup):
        """
        Filters edges to keep only those within a specified weight range.
        
        Parameters
        ----------
        inf : float
            The minimum weight of edges to keep.
        sup : float
            The maximum weight of edges to keep.
        """
        
        # Hide each edge outside weight range
        for edge in self.edges:
            if edge is not None:
                visible = inf <= edge.value <= sup  # Boolean

                edge.weightRankFiltered = not visible
                edge.setVisible(visible)

    def KeepAbsEdgesBetweenWeight(self, inf, sup):
        """
        Filters edges to keep only those with absolute weights within a specified range.
        
        Parameters
        ----------
        inf : float
            The minimum absolute weight of edges to keep.
        sup : float
            The maximum absolute weight of edges to keep.
        """
        
        # Hide each edge outside weight range
        for edge in self.edges:
            if edge is not None:
                visible = inf <= abs(edge.value) <= sup

                edge.weightRankFiltered = not visible
                edge.setVisible(visible)

    def KeepEdgesBetweenRank(self, inf, sup):
        """
        Filters edges based on their rank within a specified range.
        
        Parameters
        ----------
        inf : int
            The minimum rank of edges to keep.
        sup : int
            The maximum rank of edges to keep.
        """
        
        edges = self.GetSortedEdgeList(True)

        for i in range(0, len(edges)):
            visible = inf <= i < sup

            edges[i].weightRankFiltered = not visible
            edges[i].setVisible(visible)


class ConnGraphic_Widget(QWidget):
    connGraphicView: ConnGraphicView
    graph_info: ConnGraph_Infos

    def __init__(self, parent=None):
        """
        Initialize the ConnGraphic_Widget instance.
        
        Sets up the widget with zero content margins and a black border.
        Initializes a ConnGraphicView instance with a predefined color set.
        Configures a GraphicsView to use the ConnGraphicView as its central item.
        Sets up a vertical box layout and adds the GraphicsView to it.
        
        Parameters
        ----------
        parent : QWidget, optional
            The parent widget for this instance. Defaults to None.
        """

        super().__init__(parent)

        self.graph_info = ConnGraph_Infos()

        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("border: 1px solid black")

        # red, white, blue
        colorSet = [QColor(255, 0, 0), QColor(200, 200, 200), QColor(0, 0, 255)]
        self.connGraphicView = ConnGraphicView(colorSet)

        self.graphic = pg.GraphicsView()
        self.graphic.setCentralItem(self.connGraphicView)

        QVBoxLayout(self)
        self.layout().addWidget(self.graphic)

    # To force the widget to stay square
    def resizeEvent(self, event):
        """
        Handle the resize event to maintain a square aspect ratio for the widget.

        Adjusts the widget's size to be a square, based on the smaller dimension 
        of the width or height from the resize event.

        Parameters
        ----------
        event : QResizeEvent
            The resize event containing the new size dimensions.
        """
        
        size = min(event.size().width(), event.size().height())

        self.resize(QSize(size, size))


# Print iterations progress
# (from https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters)
def PrintProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
    Call in a loop to create a terminal progress bar.

    Parameters
    ----------
    iteration : int
        The current iteration (must be an integer).
    total : int
        The total number of iterations (must be an integer).
    prefix : str, optional
        The prefix string (default is an empty string).
    suffix : str, optional
        The suffix string (default is an empty string).
    decimals : int, optional
        The number of decimals in the percentage complete (default is 1).
    length : int, optional
        The character length of the progress bar (default is 100).
    fill : str, optional
        The character used to fill the progress bar (default is '█').

    Notes
    -----
    This function prints a progress bar to the terminal, which updates with each call.
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    # Print New Line on Complete
    if iteration == total:
        print()
