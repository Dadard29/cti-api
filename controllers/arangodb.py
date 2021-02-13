def db_get_group_tools(db, group_name):
    cursor = db.aql.execute(f"""
        FOR g in groups
            FILTER g.name == @group_name
            RETURN g
        """, bind_vars={"group_name": group_name})
    group = [d for d in cursor][0]

    cursor = db.aql.execute(f"""
        FOR gt IN group_tools
            FILTER gt._from == @group_id
            RETURN DOCUMENT(gt._to)
        """, bind_vars={"group_id": group['_id']})
    tools = [d for d in cursor]

    return tools
