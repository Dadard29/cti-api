from typing import List

from models.group import Group
from models.technique import Technique
from models.tool import Tool


class Node(object):
    def __init__(self, tool: Tool, techniques_used: List[Technique]):
        self.tool = tool
        self.techniques_used = techniques_used

    def json(self):
        return {
            "id": self.tool.id,
            "data": self.tool.json(),
            "children": [
                {
                    "id": t.id,
                    "data": t.json(),
                }
                for t in self.techniques_used
            ]
        }


class Tree(object):
    def __init__(self, group: Group):
        self.group = group
        self.nodes = []

    def add_node(self, tool: Tool, techniques_used: List[Technique]):
        self.nodes.append(
            Node(tool, techniques_used)
        )

    def json(self):
        return {
            "id": self.group.id,
            "data": self.group.json(),
            "children": [
                n.json() for n in self.nodes
            ]
        }
