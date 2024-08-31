import math

from .node import Node


class SWC:
    r"""
    A representation of the ``.swc`` file, which contains a mapping from node
    IDs to ``Node`` objects.

    :param nodes:
        a ``dict`` mapping IDs to the ``Node``\s belonging to this ``SWC``
    """

    def __init__(self, nodes: dict[int, Node]):
        self.nodes = nodes

    def total_length(self):
        """
        Calculates and returns the sum of the Euclidean distances between each
        pair of connected nodes in this ``SWC``.

        :return:
            the sum of the distances between each pair of connected nodes in
            this ``SWC``
        """

        total_length = 0.0
        for node in self.nodes.values():
            if node.parent_id == -1:
                continue
            parent = self.nodes[node.parent_id]
            node_position = [node.x, node.y, node.z]
            parent_position = [parent.x, parent.y, parent.z]
            total_length += math.dist(node_position, parent_position)
        return total_length

    def condense_node_ids(self):
        r"""
        Modifies the IDs of the ``Node``\s contained by this ``SWC`` such that
        they form a contiguous series of natural numbers beginning at 1.
        The order of node IDs will not change, i.e. a node ID that is greater
        than another given node ID before this operation will still be
        greater afterwards.
        """

        next_id = 1
        old_id_to_new_id = {}
        new_nodes = {}

        # first pass to create mapping from old to new IDs
        for old_id in self.nodes:
            old_id_to_new_id[old_id] = next_id
            next_id += 1

        # second pass to create modified copies of existing nodes
        for old_id in self.nodes:
            if self.nodes[old_id].parent_id != -1:
                new_parent_id = old_id_to_new_id[self.nodes[old_id].parent_id]
                self.nodes[old_id].parent_id = new_parent_id
            new_id = old_id_to_new_id[old_id]
            new_nodes[new_id] = self.nodes[old_id]

        self.nodes = new_nodes
