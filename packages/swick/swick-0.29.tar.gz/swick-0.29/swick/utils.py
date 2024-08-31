from .node import Node
from .swc import SWC


def split_swc(swc: SWC):
    """
    Splits an ``SWC`` object into one or more ``SWC`` objects, each containing
    a single root node. Node IDs are not modified by this process.

    :parameter swc:
        the ``SWC`` object to be split

    :return:
        a list of ``SWC`` objects each containing one root node
    """

    # first pass to create map from parent ID to child IDs
    root_nodes = []
    parent_id_to_child_ids = {}
    for node_id in swc.nodes:
        parent_id = swc.nodes[node_id].parent_id
        if parent_id == -1:
            root_nodes.append(node_id)
        elif parent_id in parent_id_to_child_ids:
            parent_id_to_child_ids[parent_id].append(node_id)
        else:
            parent_id_to_child_ids[parent_id] = [node_id]

    # second pass using DFS to separate connected components
    swcs = []
    for root_id in root_nodes:
        parent_id_stack = [root_id]
        nodes = {root_id: swc.nodes[root_id]}

        while parent_id_stack:
            parent_id = parent_id_stack.pop()
            if parent_id not in parent_id_to_child_ids:
                continue
            for child_id in parent_id_to_child_ids[parent_id]:
                nodes[child_id] = swc.nodes[child_id]
                parent_id_stack.append(child_id)
            parent_id_to_child_ids.pop(parent_id)

        swcs.append(SWC(nodes))

    return swcs


def combine_swcs(swcs: list[SWC]):
    r"""
    Combines each of the ``SWC`` objects in the list into a single ``SWC``.
    Node IDs for all but the first ``SWC`` in the list may be modified by
    this process in order to avoid collisions between node IDs: for each
    ``SWC`` in the list, the node IDs it contains will be offset by the
    greatest node ID in the previous ``SWC``.

    :parameter swcs:
        a list of ``SWC`` objects to be combined

    :return:
        a single ``SWC`` object containing all ``Node``\s from the input
    """

    id_offset = 0
    highest_id = 0
    new_nodes = {}

    for swc in swcs:

        # first pass to create mapping from old to new IDs
        old_id_to_new_id = {}
        for old_id in swc.nodes:
            new_id = old_id + id_offset
            old_id_to_new_id[old_id] = new_id
            if new_id > highest_id:
                highest_id = new_id

        # second pass to create modified copies of existing nodes
        for old_id in swc.nodes:
            new_id = old_id_to_new_id[old_id]
            old_node = swc.nodes[old_id]
            new_parent_id = old_node.parent_id
            if new_parent_id != -1:
                new_parent_id = old_id_to_new_id[old_node.parent_id]
            new_nodes[new_id] = Node(old_node.type, old_node.x, old_node.y,
                                     old_node.z, old_node.radius,
                                     new_parent_id)

        id_offset = highest_id

    return SWC(new_nodes)
