"""
Functions to export the various layout specifications to a printable format.

"""
import os

import cairosvg
import svgwrite


class VectorFile:

    def __init__(self, filename, dims_cm, stroke_width=.05):
        self.filename = filename
        width = str(dims_cm[0])
        height = str(dims_cm[1])
        self.stroke_width = stroke_width
        # Define viewBox with the same dimensions as 'size' to get units in cm
        # https://mpetroff.net/2013/08/analysis-of-svg-units/
        self.cont = svgwrite.Drawing(
                filename, size=(width + 'cm', height + 'cm'),
                viewBox='0 0 ' + width + ' ' + height)

    def add_circles(self, positions, radii, linecolor='black'):
        cont = self.cont
        group = cont.add(cont.g(fill='none', stroke=linecolor,
                         stroke_width=self.stroke_width))
        for pos, radius in zip(positions, radii):
            circle = cont.circle(center=(pos[0], pos[1]), r=radius)
            group.add(circle)

    def add_rectangles(self, positions, angles, sizes, linecolor='black'):
        cont = self.cont
        group = cont.add(cont.g(fill='none', stroke=linecolor,
                         stroke_width=self.stroke_width))
        for pos, angle, size in zip(positions, angles, sizes):
            rect = cont.rect(insert=(pos[0]-size[0]/2, pos[1]-size[1]/2),
                             size=size)
            rect.rotate(angle, pos)
            group.add(rect)

    def add_polyline(self, points, linecolor='black'):
        cont = self.cont
        cont.add(cont.polyline(
            points=points, fill='none', stroke=linecolor,
            stroke_width=self.stroke_width
        ))

    def add_text(self, text, position):
        cont = self.cont
        cont.add(cont.text(text, insert=position, style="font-size:1%"))

    def save(self):
        outname = os.path.splitext(self.filename)[0] + ".pdf"
        cairosvg.svg2pdf(self.cont.tostring(), write_to=outname)
