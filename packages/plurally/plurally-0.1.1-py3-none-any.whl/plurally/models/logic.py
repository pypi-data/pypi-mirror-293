# from plurally.models.node import Node


# class Comparison(Node): ...


# class IfNode(Node):
#     def __init__(self, name):
#         super().__init__(name)
#         self.inputs["condition"] = None
#         self.inputs["true_value"] = None
#         self.inputs["false_value"] = None
#         self.outputs["result"] = None

#     def __call__(self):
#         """Evaluate based on condition."""
#         name, handler = self.inputs["condition"]
#         condition = flow[name].outputs[handler]
#         name, handler = self.inputs["true_value"]
#         true_value = flow[name].outputs[handler]
#         name, handler = self.inputs["false_value"]
#         false_value = flow[name].outputs[handler]

#         if condition is None:
#             raise ValueError("Condition is not set in IfNode")

#         self.outputs["result"] = true_value if condition else false_value
