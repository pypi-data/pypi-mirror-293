from dataclasses import dataclass
from typing import Optional, Mapping

from hgraph._impl._builder._node_builder import PythonBaseNodeBuilder


@dataclass(frozen=True)
class PythonComponentNodeBuilder(PythonBaseNodeBuilder):
    nested_graph: Optional["GraphBuilder"] = None  # This is the generator function
    # The nodes representing the stub inputs in the nested graph.
    input_node_ids: Mapping[str, int] | None = None
    output_node_id: int | None = None  # The node representing the stub output in the nested graph.

    def make_instance(self, owning_graph_id: tuple[int, ...], node_ndx: int) -> "PythonTryExceptNodeImpl":
        from hgraph._impl._runtime._component_node import PythonComponentNodeImpl

        node = PythonComponentNodeImpl(
            node_ndx=node_ndx,
            owning_graph_id=owning_graph_id,
            signature=self.signature,
            scalars=self.scalars,
            nested_graph_builder=self.nested_graph,
            input_node_ids=self.input_node_ids,
            output_node_id=self.output_node_id,
        )

        return self._build_inputs_and_outputs(node)

    def release_instance(self, item: "PythonTryExceptNodeImpl"):
        """Nothing to be done here"""
