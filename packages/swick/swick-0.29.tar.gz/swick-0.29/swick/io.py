from .node import Node
from .swc import SWC

import re


class SWCFormatError(Exception):
    """
    Exception raised during  ``.swc`` file I/O in cases in which the SWC
    format is not or cannot be properly adhered to.
    """
    pass


def parse_int(value: str,  name: str, min_value: int, file_name: str,
              line_number: int):
    """
    Attempts to interpet a given string ``value`` as an integer, returning the
    integer on success and raising an ``SWCFormatError`` on failure.

    :parameter value:
        the string value to be parsed
    :parameter name:
        the name of the field being parsed
    :parameter min_value:
        minimum valid integer value
    :parameter file_name:
        the name of the file being read
    :parameter line_number:
        the line where the value occurs

    :return:
        an integer interpretation of the value

    :raises SWCFormatError:
        if ``value`` is not a valid integer
    """

    try:
        assert value.lstrip("-").isdigit()
        int_value = int(value)
        assert int_value >= min_value
        return int_value
    except (AssertionError, ValueError):
        raise SWCFormatError(f"Could not read {file_name}. Line"
                             f" {line_number} has {name} with value"
                             f" {value!r}; expected an integer"
                             f" greater than {min_value - 1}.")


def parse_float(value: str,  name: str, file_name: str, line_number: int):
    """
    Attempts to interpet a given string ``value`` as a float, returning the
    float on success and raising an ``SWCFormatError`` on failure.

    :parameter value:
        the string value to be parsed
    :parameter name:
        the name of the field being parsed
    :parameter file_name:
        the name of the file being read
    :parameter line_number:
        the line where the value occurs

    :return:
        a float interpretation of the value

    :raises SWCFormatError:
        if ``value`` is not a float
    """

    try:
        return float(value)
    except ValueError:
        raise SWCFormatError(f"Could not read {file_name}. Line"
                             f" {line_number} has {name} with value"
                             f" {value!r}; expected a float.")


def read_swc(path: str):
    """
    Reads an ``.swc`` file to create and return an ``SWC`` object.

    :parameter path:
        the path to the ``.swc`` file to be read

    :return:
        an ``SWC`` object containing the loaded data

    :raises SWCFormatError:
        if the file does not adhere to the SWC format
    """

    with open(path, 'r') as swc_file:
        nodes = {}
        id_line_numbers = {}

        line_number = 0
        for line in swc_file:
            line_number += 1

            # TODO: consider capturing comments
            # ignore empty, white-space only, and comment lines
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            fields = re.split(r'[\t ]+', line)
            if len(fields) != 7:
                raise SWCFormatError(f"Could not read {path}. Line"
                                     f" {line_number} contains"
                                     f" {len(fields)} fields;"
                                     f" expected 7 fields.")

            id = parse_int(fields[0], "ID", 1, path, line_number)
            type = parse_int(fields[1], "type", 0, path, line_number)
            x = parse_float(fields[2], "x position", path, line_number)
            y = parse_float(fields[3], "y position", path, line_number)
            z = parse_float(fields[4], "z position", path, line_number)
            radius = parse_float(fields[5], "radius", path, line_number)
            parent_id = parse_int(fields[6], "parent ID", -1, path,
                                  line_number)

            if parent_id == id:
                raise SWCFormatError(f"Could not read {path}. Line"
                                     f" {line_number} refers to itself as the"
                                     f" parent. Root nodes should use parent "
                                     f"ID -1.")

            if id in id_line_numbers:
                raise SWCFormatError(f"Could not read {path}. Line"
                                     f" {line_number} contains an ID {id}"
                                     f" which already exists on line"
                                     f" {id_line_numbers[id]}.")
            else:
                id_line_numbers[id] = line_number

            nodes[id] = Node(type, x, y, z, radius, parent_id)

        for node in nodes.values():
            if node.parent_id != -1 and node.parent_id not in nodes:
                raise SWCFormatError(f"Could not read {path}. Line "
                                     f"{id_line_numbers[id]} refers to a "
                                     f"parent ID {node.parent_id} that does "
                                     f"not exist.")

    return SWC(nodes)


def write_swc(path: str, swc: SWC, delimeter: str = " ",
              decimal_places: int = -1):
    """
    Writes an ``SWC`` object into an ``.swc`` file.

    :parameter path:
        the path to the ``.swc`` file to be written
    :parameter swc:
        the ``SWC`` object to be written to a file
    :parameter delimeter:
        separator for fields (tabs and spaces only)
    :parameter decimal_places:
        number of decimal places written for floats; if ``-1``, uses as many as
        necessary for each field

    :return:
        an ``SWC`` object containing the data to be written

    :raises ValueError:
        if ``delimeter`` or ``decimal_places`` values are invalid

    :raises SWCFormatError:
        if the ``SWC`` object is invalid
    """

    if not delimeter:
        raise ValueError(f"Could not write {path}. Delimeter may not be an"
                         f" empty string.")
    elif re.sub(r'[\t ]+', '', delimeter) != "":
        raise ValueError(f"Could not write {path}. Delimeter may only contain"
                         f" tabs and space, but was specified as"
                         f" {delimeter!r}.")

    if decimal_places < -1:
        raise ValueError(f"Could not write {path}. {decimal_places} is not a"
                         f" valid value for number of decimal places; expected"
                         f" a value of -1 or greater.")

    with open(path, 'w') as swc_file:
        has_written_root = False
        for id in swc.nodes:
            node = swc.nodes[id]

            # check for self-referential parent IDs
            if id == node.parent_id:
                raise SWCFormatError(f"Could not write {path}. A node with ID "
                                     f"{id} refers to itself as the parent. "
                                     f"Root nodes must use parent ID -1.")

            if node.parent_id == -1:
                has_written_root = True

            if decimal_places == -1:
                swc_file.write(f"{id}{delimeter}{node.type}{delimeter}{node.x}"
                               f"{delimeter}{node.y}{delimeter}{node.z}"
                               f"{delimeter}{node.radius}{delimeter}"
                               f"{node.parent_id}\n")
            else:
                swc_file.write(f"{id}{delimeter}{node.type}{delimeter}"
                               f"{node.x:.{decimal_places}f}{delimeter}"
                               f"{node.y:.{decimal_places}f}{delimeter}"
                               f"{node.z:.{decimal_places}f}{delimeter}"
                               f"{node.radius:.{decimal_places}f}{delimeter}"
                               f"{node.parent_id}\n")

        # check for missing root node
        if not has_written_root:
            raise SWCFormatError(f"Could not write {path}. The SWC contains "
                                 f"no node with parent ID -1; SWCs must "
                                 f"contain a root node.")
