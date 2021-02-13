import json
import os

from arango import ArangoClient
from flask import Blueprint, Response, request

from controllers.arangodb import db_get_group_tools
from controllers.cti_client import client
from models.tree import Tree

cti_blueprint = Blueprint("CTI", __name__)
arangodb = ArangoClient()
db = arangodb.db(name="apt_groups", username="root", password=os.environ["ARANGO_ROOT_PASSWORD"])

INDENT = 4


def response(obj):
    resp = Response(obj)
    resp.headers['Content-Type'] = 'application/json'
    return resp


# === GROUPS ===
@cti_blueprint.route("/groups", methods=['GET'])
def get_group_list():
    cursor = db.aql.execute("""
    FOR g in groups
        RETURN g.name
    """)
    group_names = [document for document in cursor]
    return response(
        json.dumps(group_names, indent=INDENT)
    )


@cti_blueprint.route("/groups/<group_name>", methods=['GET'])
def get_group(group_name):
    cursor = db.aql.execute(f"""
    FOR g in groups
        FILTER g.name == @group_name
        RETURN g
    """, bind_vars={"group_name": group_name})
    groups = [d for d in cursor]

    return response(
        json.dumps(groups[0], indent=INDENT)
    )


@cti_blueprint.route("/groups/<group_name>/tools", methods=['GET'])
def get_group_tools(group_name):
    tools = db_get_group_tools(db, group_name)
    return response(
        json.dumps(tools, indent=INDENT)
    )


@cti_blueprint.route("/compare", methods=['GET'])
def get_tools_groups_compare():
    group_1_name = request.args['group1']
    group_1_tools = db_get_group_tools(db, group_1_name)
    group_1_tools_names = [g['name'] for g in group_1_tools]

    group_2_name = request.args['group2']
    group_2_tools = db_get_group_tools(db, group_2_name)
    group_2_tools_names = [g['name'] for g in group_2_tools]

    common_tools = list(set(group_1_tools_names).intersection(group_2_tools_names))
    common_stats = {
        'percent': round(len(common_tools) / len(group_1_tools) * 100),
        'count': len(common_tools),
        'total': len(group_1_tools)
    }

    d = {
        'stats': common_stats,
        'tools': common_tools
    }
    return response(json.dumps(d, indent=INDENT))


# === TOOLS ===
@cti_blueprint.route("/tools", methods=['GET'])
def get_tools_list():
    cursor = db.aql.execute("""
        FOR t in tools
            RETURN t.name
        """)
    tools_names = [document for document in cursor]

    return response(
        json.dumps(tools_names, indent=INDENT)
    )


@cti_blueprint.route("/tools/<tool_name>", methods=['GET'])
def get_tool(tool_name):
    cursor = db.aql.execute(f"""
        FOR t in tools
            FILTER t.name == @tool_name
            RETURN t
        """, bind_vars={'tool_name': tool_name})
    tools = [d for d in cursor]

    return response(
        json.dumps(tools[0], indent=INDENT)
    )


@cti_blueprint.route("/tools/<tool_name>/groups", methods=['GET'])
def get_tools_group(tool_name):
    cursor = db.aql.execute("""
    FOR t in tools
        FILTER t.name == @tool_name
        RETURN t
    """, bind_vars={'tool_name': tool_name})
    tool = [t for t in cursor][0]

    cursor = db.aql.execute(f"""
    FOR gt in group_tools
        FILTER gt._to == @tool_id
        RETURN DOCUMENT(gt._from)
    """, bind_vars={'tool_id': tool['_id']})
    groups = [d for d in cursor]
    return response(
        json.dumps(groups, indent=INDENT)
    )


@cti_blueprint.route("/tools/<tool_name>/techniques", methods=['GET'])
def get_tools_techniques(tool_name):
    cursor = db.aql.execute("""
        FOR t in tools
            FILTER t.name == @tool_name
            RETURN t
        """, bind_vars={'tool_name': tool_name})
    tool = [t for t in cursor][0]

    cursor = db.aql.execute(f"""
    FOR gt in tool_techniques
        FILTER gt._from == @tool_id
        RETURN DOCUMENT(gt._to)
    """, bind_vars={'tool_id': tool['_id']})
    techniques = [d for d in cursor]
    return response(
        json.dumps(techniques, indent=INDENT)
    )
