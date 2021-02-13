import json
from pathlib import Path

from controllers.cti_client import client

GROUPS_COLLECTION = "groups"
TOOLS_COLLECTION = "tools"
TECHNIQUES_COLLECTION = "techniques"
GROUP_TOOLS_COLLECTION = "group_tools"
TOOL_TECHNIQUES_COLLECTION = "tool_techniques"


class Edge(object):
    def __init__(self, node_from, coll_from, node_to, coll_to):
        self.node_from = node_from
        self.coll_from = coll_from

        self.node_to = node_to
        self.coll_to = coll_to

    def json(self):
        return {
            "_from": f"{self.coll_from}/{self.node_from}",
            "_to": f"{self.coll_to}/{self.node_to}"
        }


def get_filename(filename: str):
    return Path(f"db/json/{filename}.json")


def get_groups():
    group_list = []

    group_names = client.get_groups_names()
    i = 1
    for g in group_names:
        try:
            print(f"({i}/{len(group_names)}) getting group {g}")
            group_list.append(client.get_group_by_name(g))
        except AttributeError:
            continue
        finally:
            i += 1

    return group_list


def get_tools():
    tools_list = []

    tools_name = client.get_tools_names()
    i = 1
    for t in tools_name:
        try:
            print(f"({i}/{len(tools_name)}) getting tool {t}")
            tools_list.append(client.get_tool_by_name(t))
        except AttributeError:
            continue
        finally:
            i += 1

    return tools_list


def get_techniques():
    techniques_list = []

    technique_names = client.get_techniques_names()
    i = 1
    for t in technique_names:
        try:
            print(f"({i}/{len(technique_names)}) getting technique {t}")
            techniques_list.append(client.get_technique_by_name(t))
        except AttributeError:
            continue
        finally:
            i += 1

    return techniques_list


def get_group_tools():
    edges = []
    group_names = client.get_groups_names()
    i = 1
    for group_name in group_names:
        try:
            print(f"({i}/{len(group_names)}) getting group {group_name}")
            group = client.get_group_by_name(group_name)
            tools = client.get_tools_used_by_group(group_name)
            for t in tools:
                edges.append(Edge(group.id, GROUPS_COLLECTION, t.id, TOOLS_COLLECTION))

        except Exception as e:
            print(str(e))
            continue

        finally:
            i += 1

    return edges


def get_tool_techniques():
    edges = []
    tool_names = client.get_tools_names()
    i = 1
    for tool_name in tool_names:
        try:
            print(f"{i}/{len(tool_names)} getting tool {tool_name}")
            tool = client.get_tool_by_name(tool_name)
            techniques = client.get_techniques_used_by_tool(tool_name)
            for t in techniques:
                edges.append(Edge(tool.id, TOOLS_COLLECTION, t.id, TECHNIQUES_COLLECTION))

        except Exception as e:
            print(str(e))
            continue

        finally:
            i += 1

    return edges


def write_to_file(item_list, collection):
    with get_filename(collection).open("w") as f:
        data = json.dumps([
            i.json() for i in item_list
        ], indent=4)
        f.write(data)


def main():
    # sandbox
    return


if __name__ == "__main__":
    main()
