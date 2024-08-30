"""
ColladaFileConverter.py
Description
-----------
This file contains the ColladaFileConverter class, which is responsible for converting a Collada file to an OBJ file.
"""

import xml.etree.ElementTree as ET
from typing import List

# Local Imports
from .MeshConverter import MeshConverter

class ColladaFileConverter:
    def __init__(self, dae_filename: str, obj_filename: str = None):
        """
        Description
        -----------
        Initializes the ColladaFileConverter class.
        Requires a Collada file to parse. You can also provide an output filename to write to.
        :param dae_filename:
        :param obj_filename:
        """
        self.dae_filename = dae_filename
        self.obj_filename = obj_filename

        # Input Processing / Checking
        if self.obj_filename is None:
            self.obj_filename = self.dae_filename.replace('.dae', '.obj')

        # Extra Details
        self.xmlns = "{https://www.collada.org/2005/11/COLLADASchema}"
        self.tree = ET.ElementTree(file=dae_filename)

        # FIX xmlns problem
        # http://stackoverflow.com/questions/13412496/python-elementtree-module-how-to-ignore-the-namespace-of-xml-files-to-locate-ma
        for el in self.tree.iter():
            if '}' in el.tag:
                el.tag = el.tag.split('}', 1)[1]  # strip all namespaces

        self.meshes = self.tree.findall('library_geometries/geometry/mesh')

    def get_preamble_lines(self) -> List[str]:
        """
        Description
        -----------
        This function returns the preamble lines of the obj file.
        :return: List[str]
                 A list of strings where each element of the list is a line in the obj file's preamble announcing
                 the conversion.
        """
        return [
            "# Converted from a Collada file to an OBJ file using collada2obj.\n",
            "# collada2obj was created by @georgethrax on GitHub (lixinthu).\n",
            "# It is maintained by Kwesi Rutledge and Wrench Robotics.\n",
        ]

    def get_obj_str_lines(self) -> List[str]:
        """
        Description
        -----------
        This function returns all lines in the resultant obj file as a List of strings.
        :return: List[str]
                 A list of strings where each element of the list is a line in the obj file.
        """
        # Setup

        # Add Preamble Lines
        obj_lines = self.get_preamble_lines()
        geometries = self.tree.findall('library_geometries/geometry')

        # Algorithm
        for ii, mesh_ii in enumerate(self.meshes):
            # Setup
            print(f"Processing mesh {ii} ({geometries[ii].attrib["id"]})...")
            converter_ii = MeshConverter(mesh_ii)

            # Add a line describing the current object
            obj_lines.append(f"o {geometries[ii].attrib["id"]}\n")

            obj_lines += converter_ii.get_obj_str_lines()

        # Export
        return obj_lines

    def export_obj(self, output_filename: str = None):
        """
        Description
        -----------
        Exports the obj file to the specified path.
        :param output_filename: An optional output filename. By default, we will use the obj_filename attribute.
        :return:
        """
        # Setup
        lines = self.get_obj_str_lines()

        if output_filename is None:
            output_filename = self.obj_filename

        # Export
        with open(output_filename, 'w') as f:
            f.write(''.join(lines))