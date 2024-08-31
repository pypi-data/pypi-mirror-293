# -*- coding: utf-8 -*-

"""
  Authors: Riccardo Filomena
  Company: Manz IT
  Address: Via S. Lorenzo, 19, 40037 Sasso Marconi (BO)
  Mail: rfilomena@manz.com
  Date: 2024-01-22
"""

"""
  Project: DumpData
  
  configuration.py
  
  Created by Riccardo Filomena
  Property of MANZ ITALY S.R.L.
  Via S. Lorenzo, 19, 40037 Sasso Marconi (BO).
"""

import os
import sys
from lxml import etree as ET

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def read_xml(root, temp=None):
    """ Reading a file '.xml'.

        input:
            ----------------------------
            - root: Python tree
                subtree's root

            - temp: Python dictionary containing a part of the tree
                default value: dict()

        __output:
            ----------------------------
            - temp: Python dictionary containing all the tree read from the file '.xml'
    """

    if temp is None:
        temp = {}
    try:
        children = root.getchildren()

        if children != list():
            for i, child in enumerate(children):
                temp[child.tag] = dict()
                temp[child.tag] = read_xml(children[i], temp[child.tag])
        else:
            if root.attrib['type'] == 'int':
                return int(root.text)
            elif root.attrib['type'] == 'float':
                return float(root.text)
            elif root.attrib['type'] == 'string':
                return str(root.text)
            elif root.attrib['type'] == 'bool':
                return root.text == 'True'
            else:
                return str(root.text)

        return temp
    except Exception as e:
        print('Problem detected [read_xml]: ', str(e))
        return dict()


class Configuration:
    def __init__(self, custom_conf_path=None):
        self.__debug = False
        self.__parameters = dict()
        self.__set_parameters(custom_conf_path)

    def __set_parameters(self, custom_conf_path) -> None:
        conf_folder = 'cfg'
        conf_name = 'conf.xml'
        default_conf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), conf_folder + os.sep + conf_name))
        conf_path = custom_conf_path if custom_conf_path and os.path.isfile(custom_conf_path) else default_conf_path

        tree = ET.parse(conf_path)
        root = tree.getroot()
        dictionary = dict()

        self.__parameters = read_xml(root, dictionary)
        self.__printer_debug(self.__debug, 'Configuration read successfully!')

    @property
    def parameters(self) -> dict:
        return self.__parameters

    def __printer_debug(self, debug, *var):
        if debug:
            print(*var)


# Instantiation of the class "Configuration" to make it global.
cfg = Configuration()
