#!/usr/bin/env python3
"""Check a RelationMap chart (JSON v1.2) and turn it into a link that opens it in the editor.

    python3 relationmap_link.py chart.json          # check, then print the link
    python3 relationmap_link.py chart.json --plain  # link without compression (for browsers older than Safari 16.4)
    python3 relationmap_link.py chart.json --check  # check only
    cat chart.json | python3 relationmap_link.py -

Errors stop with exit code 1: fix them and run again. Warnings are printed and the link is still made.
The format: https://relationmap.io/docs/data-format.md   How the link works: https://relationmap.io/docs/ai.md
Python 3 standard library only.
"""
import base64
import json
import sys
import zlib

EDITOR = "https://relationmap.io/edit/#data="
MAXIMUM_CHART_BYTES = 1024 * 1024  # the editor opens at most 1 MB of chart data from a link, counted after unpacking


def check(chart):
    errors, warnings = [], []
    if not isinstance(chart, dict):
        return ["The top level must be an object with a \"nodes\" list."], warnings
    nodes = chart.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        return ["\"nodes\" must be a list with at least one character."], warnings

    ids = set()
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            errors.append(f"nodes[{index}] is not an object.")
            continue
        if "id" not in node:
            warnings.append(f"nodes[{index}] has no \"id\"; the editor will call it \"n{index}\", and no relationship can point to it reliably.")
        node_id = str(node.get("id", f"n{index}"))
        if node_id in ids:
            errors.append(f"Two characters share the id \"{node_id}\"; the editor keeps only the first.")
        ids.add(node_id)
        if not isinstance(node.get("name"), str) or not node["name"].strip():
            errors.append(f"Character \"{node_id}\" has no \"name\".")
        if node.get("avatar"):
            warnings.append(f"Character \"{node_id}\" has an \"avatar\". Image links written by an AI often don't load; consider leaving pictures out.")

    with_position = sum(1 for node in nodes if isinstance(node, dict) and "position" in node)
    if 0 < with_position < len(nodes):
        warnings.append(f"{with_position} of {len(nodes)} characters have a \"position\". Give it to every character or to none.")

    defined = {}
    for kind in ("groups", "tags"):
        definitions = chart.get(kind, [])
        if not isinstance(definitions, list):
            errors.append(f"\"{kind}\" must be a list.")
            definitions = []
        defined[kind] = set()
        for item in definitions:
            if not isinstance(item, dict) or item.get("id") is None or item.get("name") is None:
                errors.append(f"Every entry in \"{kind}\" needs an \"id\" and a \"name\": {json.dumps(item, ensure_ascii=False)[:80]}")
                continue
            defined[kind].add(str(item["id"]))
            if not item.get("color"):
                warnings.append(f"{kind[:-1].capitalize()} \"{item['name']}\" has no \"color\"; it will be drawn without one.")
        for node in nodes:
            if isinstance(node, dict):
                for reference in node.get(kind, []) or []:
                    if str(reference) not in defined[kind]:
                        errors.append(f"Character \"{node.get('id')}\" lists {kind[:-1]} \"{reference}\", which is not defined in \"{kind}\".")

    edges = chart.get("edges", [])
    if not isinstance(edges, list):
        errors.append("\"edges\" must be a list.")
        edges = []
    edge_ids = set()
    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            errors.append(f"edges[{index}] is not an object.")
            continue
        for end in ("source", "target"):
            if str(edge.get(end)) not in ids:
                errors.append(f"edges[{index}] \"{end}\" is \"{edge.get(end)}\", which is not a character id. Use ids, not names.")
        if "id" in edge:
            if str(edge["id"]) in edge_ids:
                errors.append(f"Two relationships share the id \"{edge['id']}\".")
            edge_ids.add(str(edge["id"]))
        if "bidirectional" in edge and not isinstance(edge["bidirectional"], bool):
            errors.append(f"edges[{index}] \"bidirectional\" must be true or false.")

    meta = chart.get("meta", {})
    if isinstance(meta, dict) and meta.get("version") not in (None, "1.2"):
        warnings.append("Write \"1.2\" as meta.version.")
    if len(nodes) > 40:
        warnings.append(f"{len(nodes)} characters. It opens, but more than 40 gets crowded; consider one chart per family, faction or season.")
    return errors, warnings


def make_link(chart, plain=False):
    data = json.dumps(chart, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    if len(data) > MAXIMUM_CHART_BYTES:
        raise ValueError(f"The chart is {len(data):,} bytes; a link opens at most {MAXIMUM_CHART_BYTES:,}. "
                         "Save it as a .json file instead; the user opens it with Open in the editor.")
    packed = data if plain else zlib.compress(data, 9)
    return EDITOR + base64.urlsafe_b64encode(packed).decode("ascii").rstrip("=")


def main(arguments):
    paths = [argument for argument in arguments if not argument.startswith("--")]
    if len(paths) != 1:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    source = sys.stdin if paths[0] == "-" else open(paths[0], encoding="utf-8")
    try:
        chart = json.load(source)
    except json.JSONDecodeError as error:
        print(f"ERROR  Not valid JSON: {error}", file=sys.stderr)
        return 1
    errors, warnings = check(chart)
    for warning in warnings:
        print(f"WARN   {warning}", file=sys.stderr)
    for error in errors:
        print(f"ERROR  {error}", file=sys.stderr)
    if errors:
        return 1
    count = lambda key: len(chart.get(key) or [])
    print(f"OK     {count('nodes')} characters, {count('edges')} relationships, {count('groups')} groups, {count('tags')} tags", file=sys.stderr)
    if "--check" in arguments:
        return 0
    try:
        link = make_link(chart, plain="--plain" in arguments)
    except ValueError as error:
        print(f"ERROR  {error}", file=sys.stderr)
        return 1
    print(f"LINK   {len(link):,} characters", file=sys.stderr)
    print(link)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
