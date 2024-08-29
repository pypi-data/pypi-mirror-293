import uuid
from copy import deepcopy
from typing import Any, Dict, Union

import networkx as nx

from plurally import models
from plurally.models.node import Node


class Flow:
    def __init__(self, name: str = "") -> None:
        self._flow_id = f"fl-{str(uuid.uuid4())}"
        self.name = name
        self.graph = nx.MultiDiGraph()

    def __contains__(self, node: Node):
        assert isinstance(node, Node)
        return node in self.graph

    def add_node(
        self,
        node: Node,
    ) -> Node:
        if node in self:
            raise ValueError(f"Node with {node.node_id=} already registered")
        self.graph.add_node(node)
        return node

    def update_node(
        self,
        node: Node,
    ) -> Node:
        if node not in self:
            raise ValueError(f"Node with {node.node_id=} not found")
        # self.graph.
        return node

    def get_node(self, node_id: str) -> Node:
        for node in self.graph.nodes:
            if node.node_id == node_id:
                return node
        raise ValueError(f"Node with {node_id=} not found")

    def connect_nodes(
        self,
        src_node: Union[str, "Node"],
        src_handle: str,
        tgt_node: Union[str, "Node"],
        tgt_handle: str,
    ):
        """Connect this node's output to another node's input."""
        if isinstance(src_node, str):
            src_node = self.get_node(src_node)
        if isinstance(tgt_node, str):
            tgt_node = self.get_node(tgt_node)

        if src_node is tgt_node:
            raise ValueError(f"Cannot connect node with itself: {src_node}")

        outputs_annots = src_node.OutputSchema.__annotations__
        if src_handle not in outputs_annots:
            raise ValueError(
                f"Output {src_handle} not found in node {src_node}, options are {list(outputs_annots)}"
            )
        if src_node not in self:
            raise ValueError(f"{src_node} was not added to {self}")

        inputs_annots = tgt_node.InputSchema.__annotations__
        if tgt_handle not in inputs_annots:
            raise ValueError(
                f"Output {tgt_handle} not found in node {tgt_node}, options are {list(inputs_annots)}"
            )

        if not tgt_node.validate_connection(src_node, src_handle, tgt_handle):
            raise ValueError(f"Connection between {src_node} and {tgt_node} is invalid")

        key = f"{src_handle}_{tgt_handle}"
        if (src_node, tgt_node, key) in self.graph.edges:
            raise ValueError(
                f"Connection between {src_node} and {tgt_node} with {src_handle=} and {tgt_handle=} already exists"
            )

        self.graph.add_edge(
            src_node,
            tgt_node,
            src_handle=src_handle,
            tgt_handle=tgt_handle,
            key=key,
        )

    def disconnect_nodes(
        self,
        src_node: Union[str, "Node"],
        src_handle: str,
        tgt_node: Union[str, "Node"],
        tgt_handle: str,
    ):
        """Disconnect this node connection."""
        if isinstance(src_node, str):
            src_node = self.get_node(src_node)
        if isinstance(tgt_node, str):
            tgt_node = self.get_node(tgt_node)
        if src_node is tgt_node:
            raise ValueError(f"Cannot connect node with itself: {src_node}")
        try:
            self.graph.remove_edge(src_node, tgt_node, key=f"{src_handle}_{tgt_handle}")
        except nx.NetworkXError:
            raise ValueError(
                f"Connection between {src_node} and {tgt_node} with {src_handle=} and {tgt_handle=} not found"
            )

    def delete_node(self, node: Union[str, "Node"]):
        """Remove a node from the flow."""
        if isinstance(node, str):
            node = self.get_node(node)
        self.graph.remove_node(node)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        for item in nx.topological_sort(self.graph):
            if not isinstance(item, Node):
                break
            kwargs = {}
            for src_node, _, attrs in self.graph.in_edges(item, True):
                kwargs[attrs["tgt_handle"]] = src_node.outputs[attrs["src_handle"]]
            item(**kwargs)

    def clear(self):
        for node in self.graph.nodes:
            node.outputs.clear()

    def __str__(self) -> str:
        return f"{type(self).__name__}(name={self.name}, id={self._flow_id[:7]})"

    def serialize(self) -> Dict:
        s = nx.node_link_data(self.graph)
        s["nodes"] = [{**n, "id": n["id"].serialize()} for n in s["nodes"]]
        s["links"] = [
            {**link, "source": link["source"].node_id, "target": link["target"].node_id}
            for link in s["links"]
        ]
        return s

    @classmethod
    def parse(cls, data: Dict) -> "Flow":
        data = deepcopy(data)

        flow = cls()
        nodes = {}
        nodes_list = []
        for n in data["nodes"]:
            node = models.create_node(**n["id"])
            nodes[node.node_id] = node
            nodes_list.append(node)
        data["nodes"] = [{**n, "id": nodes[n["id"]["_node_id"]]} for n in data["nodes"]]
        data["links"] = [
            {**link, "source": nodes[link["source"]], "target": nodes[link["target"]]}
            for link in data["links"]
        ]
        flow.graph = nx.node_link_graph(data)
        return flow

    def __eq__(self, other: "Flow") -> bool:
        return (
            isinstance(other, Flow)
            and self.graph.nodes == other.graph.nodes
            and self.graph.edges == other.graph.edges
        )
