#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests"]
# ///
"""
TaskNotes CLI - Manage tasks via the TaskNotes plugin HTTP API.

Usage:
    uv run tasks.py list [--status STATUS] [--priority PRIORITY] [--tag TAG] [--overdue] [--limit N]
    uv run tasks.py create "Title" [--status STATUS] [--priority PRIORITY] [--due YYYY-MM-DD] [--tags tag1,tag2] [--project PROJECT] [--details TEXT]
    uv run tasks.py update "TaskNotes/Tasks/file.md" [--status STATUS] [--priority PRIORITY] [--due YYYY-MM-DD] [--title TITLE] [--details TEXT]
    uv run tasks.py complete "TaskNotes/Tasks/file.md"
    uv run tasks.py archive "TaskNotes/Tasks/file.md"
    uv run tasks.py delete "TaskNotes/Tasks/file.md"
    uv run tasks.py options

Configuration:
    TASKNOTES_API_PORT  - API port (default: 28084)
    TASKNOTES_API_KEY   - API token if auth is enabled (optional)

Status values (frontmatter): do, doing, done, waiting, none
Priority values (frontmatter): hot, spicy, bland, mild, none
"""

import argparse
import json
import os
import sys
import urllib.parse

import requests

API_PORT = os.getenv("TASKNOTES_API_PORT", "28084")
API_KEY = os.getenv("TASKNOTES_API_KEY", "")
BASE_URL = f"http://localhost:{API_PORT}/api"


def headers():
    h = {"Content-Type": "application/json"}
    if API_KEY:
        h["Authorization"] = f"Bearer {API_KEY}"
    return h


def req(method, endpoint, params=None, data=None):
    url = f"{BASE_URL}{endpoint}"
    try:
        r = requests.request(method, url, headers=headers(), params=params, json=data, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        return {"error": f"Cannot connect to TaskNotes API at port {API_PORT}. Is Obsidian open with HTTP API enabled?"}
    except requests.exceptions.HTTPError as e:
        try:
            return r.json()
        except Exception:
            return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}


def out(result):
    print(json.dumps(result, indent=2))


def build_query(status=None, priority=None, tag=None, overdue=False, limit=50):
    """Build a FilterQuery object for POST /api/tasks/query."""
    children = []
    cid = 0

    if status:
        children.append({
            "type": "condition", "id": f"c{cid}",
            "property": "status", "operator": "is", "value": status
        })
        cid += 1

    if priority:
        children.append({
            "type": "condition", "id": f"c{cid}",
            "property": "priority", "operator": "is", "value": priority
        })
        cid += 1

    if tag:
        children.append({
            "type": "condition", "id": f"c{cid}",
            "property": "tags", "operator": "contains", "value": tag
        })
        cid += 1

    if overdue:
        children.append({
            "type": "condition", "id": f"c{cid}",
            "property": "overdue", "operator": "is", "value": True
        })
        cid += 1

    query = {
        "type": "group",
        "id": "root",
        "conjunction": "and",
        "children": children,
        "limit": limit,
        "sortKey": "due",
        "sortDirection": "asc"
    }
    return query


def cmd_list(args):
    limit = args.limit or 50
    query = build_query(
        status=args.status,
        priority=args.priority,
        tag=args.tag,
        overdue=args.overdue,
        limit=limit,
    )
    result = req("POST", "/tasks/query", data=query)
    if "error" in result:
        out(result)
        return

    tasks = result.get("data", {}).get("tasks", [])
    out({
        "success": True,
        "count": len(tasks),
        "tasks": [
            {
                "id": t.get("id"),
                "title": t.get("title"),
                "status": t.get("status"),
                "priority": t.get("priority"),
                "due": t.get("due"),
                "scheduled": t.get("scheduled"),
                "tags": t.get("tags", []),
                "projects": t.get("projects", []),
            }
            for t in tasks
        ]
    })


def cmd_create(args):
    data = {"title": args.title}
    if args.status:
        data["status"] = args.status
    if args.priority:
        data["priority"] = args.priority
    if args.due:
        data["due"] = args.due
    if args.scheduled:
        data["scheduled"] = args.scheduled

    # Build tag list — always include "task"
    if args.tags:
        tag_list = [t.strip() for t in args.tags.split(",")]
        if "task" not in tag_list:
            tag_list = ["task"] + tag_list
    else:
        tag_list = ["task"]
    data["tags"] = tag_list

    if args.project:
        project = args.project
        if not project.startswith("[["):
            project = f"[[{project}]]"
        data["projects"] = [project]

    if args.details:
        data["details"] = args.details

    out(req("POST", "/tasks", data=data))


def cmd_update(args):
    task_id = urllib.parse.quote(args.task_id, safe="")
    data = {}
    if args.status:
        data["status"] = args.status
    if args.priority:
        data["priority"] = args.priority
    if args.due:
        data["due"] = args.due
    if args.title:
        data["title"] = args.title
    if args.details:
        data["details"] = args.details
    if not data:
        out({"error": "No fields to update"})
        return
    out(req("PUT", f"/tasks/{task_id}", data=data))


def cmd_complete(args):
    task_id = urllib.parse.quote(args.task_id, safe="")
    out(req("PUT", f"/tasks/{task_id}", data={"status": "done"}))


def cmd_archive(args):
    task_id = urllib.parse.quote(args.task_id, safe="")
    out(req("POST", f"/tasks/{task_id}/archive"))


def cmd_delete(args):
    task_id = urllib.parse.quote(args.task_id, safe="")
    out(req("DELETE", f"/tasks/{task_id}"))


def cmd_options(args):
    result = req("GET", "/filter-options")
    if "error" in result:
        out(result)
        return
    data = result.get("data", {})
    out({
        "statuses": [{"value": s.get("value"), "label": s.get("label"), "completed": s.get("isCompleted")} for s in data.get("statuses", [])],
        "priorities": [{"value": p.get("value"), "label": p.get("label")} for p in data.get("priorities", [])],
    })


def main():
    p = argparse.ArgumentParser(description="TaskNotes HTTP API CLI")
    sub = p.add_subparsers(dest="command", required=True)

    ls = sub.add_parser("list", help="List/filter tasks")
    ls.add_argument("--status")
    ls.add_argument("--priority")
    ls.add_argument("--tag")
    ls.add_argument("--overdue", action="store_true")
    ls.add_argument("--limit", type=int)

    cr = sub.add_parser("create", help="Create a task with explicit fields (no NLP)")
    cr.add_argument("title")
    cr.add_argument("--status", default="do")
    cr.add_argument("--priority", default="bland")
    cr.add_argument("--due", help="YYYY-MM-DD")
    cr.add_argument("--scheduled", help="YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS")
    cr.add_argument("--tags", help="Comma-separated (task always added)")
    cr.add_argument("--project", help="Project note name (wikilink added automatically)")
    cr.add_argument("--details", help="Body text / description")

    up = sub.add_parser("update", help="Update task fields")
    up.add_argument("task_id", help="Task file path e.g. TaskNotes/Tasks/My task.md")
    up.add_argument("--status")
    up.add_argument("--priority")
    up.add_argument("--due", help="YYYY-MM-DD")
    up.add_argument("--title")
    up.add_argument("--details")

    co = sub.add_parser("complete", help="Mark a task done")
    co.add_argument("task_id")

    ar = sub.add_parser("archive", help="Archive a task")
    ar.add_argument("task_id")

    dl = sub.add_parser("delete", help="Delete a task")
    dl.add_argument("task_id")

    sub.add_parser("options", help="Show available status/priority values")

    args = p.parse_args()
    {
        "list": cmd_list,
        "create": cmd_create,
        "update": cmd_update,
        "complete": cmd_complete,
        "archive": cmd_archive,
        "delete": cmd_delete,
        "options": cmd_options,
    }[args.command](args)


if __name__ == "__main__":
    main()
