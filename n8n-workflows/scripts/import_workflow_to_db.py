#!/usr/bin/env python3
"""
Import n8n workflow directly to database
"""

import json
import sys
import uuid
from datetime import datetime
import subprocess

# Database connection details
DB_HOST = "n8n-db"
DB_USER = "n8n"
DB_NAME = "n8n"
DB_PASSWORD = "y3Acdik71HDw/e4VCDtQXbUSn1oDA/oM"

def run_sql(sql):
    """Execute SQL via docker exec"""
    cmd = [
        "docker", "exec", "n8n-db",
        "psql", "-U", DB_USER, "-d", DB_NAME,
        "-t", "-c", sql
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"SQL Error: {result.stderr}", file=sys.stderr)
        return None
    return result.stdout.strip()

def get_user_id():
    """Get first user ID from database"""
    sql = 'SELECT id FROM "user" LIMIT 1;'
    user_id = run_sql(sql)
    return user_id.strip() if user_id else None

def load_workflow(file_path):
    """Load workflow from JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def import_workflow(workflow_file):
    """Import workflow to n8n database"""

    # Load workflow
    print(f"📂 Loading workflow from: {workflow_file}")
    workflow = load_workflow(workflow_file)

    # Generate IDs
    workflow_id = str(uuid.uuid4())
    version_id = str(uuid.uuid4())

    # Get user ID
    user_id = get_user_id()
    if not user_id:
        print("❌ Error: Could not get user ID")
        return False

    print(f"✅ User ID: {user_id}")
    print(f"✅ Workflow ID: {workflow_id}")
    print(f"✅ Version ID: {version_id}")

    # Prepare workflow data
    name = workflow.get('name', 'Imported Workflow')
    nodes = json.dumps(workflow.get('nodes', []))
    connections = json.dumps(workflow.get('connections', {}))
    settings = json.dumps(workflow.get('settings', {}))
    static_data = json.dumps(workflow.get('staticData', None))
    trigger_count = workflow.get('triggerCount', 1)

    # Escape single quotes for SQL
    name_escaped = name.replace("'", "''")
    nodes_escaped = nodes.replace("'", "''")
    connections_escaped = connections.replace("'", "''")
    settings_escaped = settings.replace("'", "''")
    static_data_escaped = static_data.replace("'", "''") if static_data != 'null' else 'NULL'

    # Insert workflow
    print(f"\n📤 Inserting workflow: {name}")

    sql_workflow = f"""
    INSERT INTO workflow_entity
    (id, name, active, nodes, connections, settings, "staticData", "versionId", "triggerCount", "createdAt", "updatedAt")
    VALUES
    ('{workflow_id}', '{name_escaped}', false, '{nodes_escaped}'::json, '{connections_escaped}'::json,
     '{settings_escaped}'::json, {static_data_escaped if static_data_escaped != 'NULL' else 'NULL'},
     '{version_id}', {trigger_count}, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    """

    result = run_sql(sql_workflow)
    if result is None:
        print("❌ Error: Failed to insert workflow")
        return False

    print("✅ Workflow inserted")

    # Get role ID for owner
    sql_role = "SELECT id FROM role WHERE name = 'owner' AND scope = 'workflow' LIMIT 1;"
    role_id = run_sql(sql_role)
    if not role_id:
        print("❌ Error: Could not get role ID")
        return False

    role_id = role_id.strip()
    print(f"✅ Role ID: {role_id}")

    # Share workflow with user
    print("\n📤 Sharing workflow with user...")

    sql_share = f"""
    INSERT INTO shared_workflow
    ("workflowId", "userId", "roleId", "createdAt", "updatedAt")
    VALUES
    ('{workflow_id}', '{user_id}', '{role_id}', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    """

    result = run_sql(sql_share)
    if result is None:
        print("❌ Error: Failed to share workflow")
        return False

    print("✅ Workflow shared")

    print(f"\n🎉 Success! Workflow imported:")
    print(f"   ID: {workflow_id}")
    print(f"   Name: {name}")
    print(f"   URL: https://n8n.szybkie-kursiki.pl/workflow/{workflow_id}")

    return True

if __name__ == '__main__':
    workflow_file = '/home/deploy/szybkie-kursiki/n8n-workflows/course-generator-workflow.json'

    if len(sys.argv) > 1:
        workflow_file = sys.argv[1]

    success = import_workflow(workflow_file)
    sys.exit(0 if success else 1)
