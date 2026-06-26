import os
import sqlite3
import json
from typing import Dict, Any, List, Optional
from google.adk.tools import ToolContext

# 1. Filesystem Tools
def list_directory(directory_path: str) -> dict:
    """List contents of a directory.

    Args:
        directory_path: The absolute path of the directory.

    Returns:
        dict: A status code and list of file/folder names.
    """
    try:
        path = os.path.abspath(directory_path)
        # Sandbox warning check (make sure it's within allowed dirs if necessary)
        if not os.path.exists(path):
            return {"status": "error", "message": f"Path '{path}' does not exist"}
        
        items = os.listdir(path)
        contents = []
        for item in items:
            full_path = os.path.join(path, item)
            is_dir = os.path.isdir(full_path)
            contents.append({
                "name": item,
                "type": "directory" if is_dir else "file",
                "size": os.path.getsize(full_path) if not is_dir else 0
            })
        return {"status": "success", "directory": path, "contents": contents}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def read_file(file_path: str) -> dict:
    """Read the text contents of a file.

    Args:
        file_path: The absolute path of the file to read.

    Returns:
        dict: File contents or error message.
    """
    try:
        path = os.path.abspath(file_path)
        if not os.path.exists(path):
            return {"status": "error", "message": f"File '{path}' not found"}
        if os.path.isdir(path):
            return {"status": "error", "message": f"Path '{path}' is a directory, not a file"}
            
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(20000) # Read up to 20k characters
        return {"status": "success", "file": path, "content": content}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def write_file(file_path: str, content: str) -> dict:
    """Write text content to a file.

    Args:
        file_path: The absolute path of the file to write.
        content: The text content to write.

    Returns:
        dict: Success status or error message.
    """
    try:
        path = os.path.abspath(file_path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return {"status": "success", "file": path, "bytes_written": len(content)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# 2. SQLite Database Tools
def execute_sqlite_query(database_path: str, query: str) -> dict:
    """Execute a read-only SQL query on a local SQLite database.

    Args:
        database_path: Absolute path to the SQLite database file.
        query: SQL SELECT query to execute.

    Returns:
        dict: Query results or error message.
    """
    try:
        path = os.path.abspath(database_path)
        # Restrict queries to SELECT for safety
        query_stripped = query.strip().upper()
        if not query_stripped.startswith("SELECT") and not query_stripped.startswith("PRAGMA"):
            return {"status": "error", "message": "Only SELECT or PRAGMA queries are allowed for safety."}
            
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchmany(100) # Limit to 100 results
        
        results = [dict(row) for row in rows]
        conn.close()
        
        return {
            "status": "success",
            "row_count": len(results),
            "columns": list(results[0].keys()) if results else [],
            "results": results
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# 3. Web Browser simulation
def browse_web(url: str) -> dict:
    """Fetch and scrape text content from a web page.

    Args:
        url: The web URL to fetch.

    Returns:
        dict: Page text summary or error message.
    """
    # A simulated browser scraping tool
    url_lower = url.lower()
    if "google" in url_lower or "search" in url_lower:
        return {
            "status": "success",
            "title": "Google Search - Market Trends",
            "body": "Top search results: 1. AI market size reached $150B in 2025. 2. SaaS growth rates stabilize at 18% YoY. 3. Compliance and governance tools see 3x investment growth."
        }
    elif "reuters" in url_lower or "news" in url_lower:
        return {
            "status": "success",
            "title": "Global Markets News",
            "body": "Central banks indicate potential interest rate cuts as inflation cools, boosting venture capital funding in late 2026. Tech valuations rebound."
        }
        
    return {
        "status": "success",
        "title": "Simulated Web Result",
        "body": f"Page content from {url}: Industry analysis indicates strong tailwinds. Customers prioritize security, cost-efficiency, and user-friendly UX."
    }


# 4. GitHub MCP (Mocked Production Interface)
def github_mcp_operation(repo_name: str, action: str, payload: str) -> dict:
    """Interface with GitHub repository for CI/CD, issue tracking, and commits.

    Args:
        repo_name: Format 'owner/repo'.
        action: 'create_issue', 'trigger_workflow', or 'commit_file'.
        payload: JSON-formatted details or content.

    Returns:
        dict: Operation status.
    """
    # A mock interface ready for GitHub PAT integration
    try:
        data = json.loads(payload) if payload else {}
    except Exception:
        data = {"raw_payload": payload}
        
    return {
        "status": "success",
        "integration": "GitHub MCP (Mock Mode)",
        "repo": repo_name,
        "action_executed": action,
        "details": {
            "msg": f"Successfully performed '{action}' in {repo_name}.",
            "ref": "refs/heads/main",
            "run_id": "87654321",
            "url": f"https://github.com/{repo_name}/actions/runs/87654321"
        }
    }


# 5. Google Drive MCP (Mocked Production Interface)
def google_drive_mcp_operation(file_name: str, action: str, folder_path: str = "My Drive") -> dict:
    """Store, retrieve, or search files in Google Drive.

    Args:
        file_name: Name of the target file.
        action: 'upload', 'download', or 'search'.
        folder_path: Target folder path.

    Returns:
        dict: Operation status.
    """
    # A mock interface ready for OAuth / Service Account integration
    return {
        "status": "success",
        "integration": "Google Drive MCP (Mock Mode)",
        "file": file_name,
        "action_executed": action,
        "folder": folder_path,
        "details": {
            "file_id": "drive_file_abc123xyz",
            "web_view_link": f"https://drive.google.com/open?id=drive_file_abc123xyz",
            "size_bytes": 1048576 if action == "download" else 0
        }
    }


# 6. Sensitive tool requiring Human Approval Workflow
def execute_sensitive_transaction(transaction_details: str, cost: float) -> dict:
    """Execute a budget release or vendor contract signing. 

    Args:
        transaction_details: Details of the contract/budget.
        cost: Total cost involved.

    Returns:
        dict: Transaction status.
    """
    # This tool will be configured to require human confirmation.
    return {
        "status": "success",
        "transaction": "Budget Released",
        "cost": f"${cost:,.2f}",
        "details": transaction_details,
        "hash": "tx_boardroom_9988ff"
    }
