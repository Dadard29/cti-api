from attackcti import attack_client

from models.group import Group
from models.technique import Technique
from models.tool import Tool


class CtiClient(object):
    def __init__(self):
        self._client = attack_client()

    def _get_group_by_name(self, group_name: str):
        groups = self._client.get_groups()
        for g in groups:
            if g.name == group_name:
                return g

        return None

    def _get_tool_by_name(self, tool_name):
        tools = self._client.get_software()
        for t in tools:
            if t.name == tool_name:
                return t

        return None

    # ============ GROUPS ============
    def get_group_by_id(self, group_id):
        groups = self._client.get_groups()
        for g in groups:
            if g.id == group_id:
                return Group(g)

        return None

    def get_group_by_name(self, group_name: str) -> Group:
        return Group(self._get_group_by_name(group_name))

    def get_groups_names(self) -> list:
        groups = self._client.get_groups()
        return [
            g.name for g in groups
        ]

    def get_groups_using_technique(self, technique_name):
        # todo
        return

    # ============ TECHNIQUES ============
    def get_techniques_names(self) -> list:
        techniques = self._client.get_techniques()
        return [
            t.name for t in techniques
        ]

    def get_technique_by_name(self, technique_name):
        techniques = self._client.get_techniques()
        for t in techniques:
            if t.name == technique_name:
                return Technique(t)

        return None

    def get_techniques_used_by_group(self, group_name: str):
        group = self._get_group_by_name(group_name)
        techniques = self._client.get_techniques_used_by_group(group)
        return [
            Technique(t) for t in techniques
        ]

    def get_techniques_used_by_tool(self, tool_name: str):
        tool = self._get_tool_by_name(tool_name)
        techniques = self._client.get_techniques_used_by_software(tool)

        techniques_list = []
        for t in techniques:
            try:
                tech = Technique(t)
                techniques_list.append(tech)
            except AttributeError:
                continue

        return techniques_list

    # ============ TOOLS ============
    def get_tools_names(self) -> list:
        tools = self._client.get_software()
        return [t.name for t in tools]

    def get_tool_by_name(self, tool_name):
        return Tool(self._get_tool_by_name(tool_name))

    def get_tools_used_by_group(self, group_name):
        group = self._get_group_by_name(group_name)
        tools = self._client.get_software_used_by_group(group)
        tools_list = []
        for t in tools:
            try:
                tool = Tool(t)
                tools_list.append(tool)
            except AttributeError:
                continue

        return tools_list


client = CtiClient()
