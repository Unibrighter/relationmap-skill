---
name: relationmap-chart
description: Draft a character relationship chart for a novel, TV series, film, game, anime or the user's own story in RelationMap's JSON format, check it, and hand it over as a link that opens the chart in the free editor at relationmap.io, or as a .json file. Use when the user asks for a character relationship chart, relationship map or diagram, a "who's who" of a cast, or a chart of how characters are connected that they can edit and share.
---

# RelationMap chart

Turn a cast into a chart the user can open, edit and share at relationmap.io. No account and no API key: the chart travels inside a link, or as a .json file.

The format is documented at https://relationmap.io/docs/data-format.md and the AI workflow at https://relationmap.io/docs/ai.md. Read them when this page is not enough. Don't use fields that aren't documented there.

## 1. Pick the cast

10 to 40 characters reads well on one screen. For a bigger story, make one chart per family, faction or season, and say so. Write names the way the story does.

Only draw relationships the story states. If you are not sure about one, leave it out: readers of the story will notice a wrong line before anything else.

## 2. Write the JSON

```json
{
  "meta": { "title": "Pride and Prejudice characters", "version": "1.2" },
  "nodes": [
    { "id": "elizabeth", "name": "Elizabeth Bennet", "subtitle": "Second Bennet daughter", "groups": ["bennets"] },
    { "id": "jane", "name": "Jane Bennet", "subtitle": "Eldest Bennet daughter", "groups": ["bennets"] },
    { "id": "darcy", "name": "Fitzwilliam Darcy", "subtitle": "Master of Pemberley" }
  ],
  "edges": [
    { "id": "e1", "source": "jane", "target": "elizabeth", "label": "sisters", "bidirectional": true },
    { "id": "e2", "source": "darcy", "target": "elizabeth", "label": "in love with" }
  ],
  "groups": [
    { "id": "bennets", "name": "The Bennets", "color": "#00B894" }
  ]
}
```

The rules that matter most:

- Every node has a unique short `id` and a `name`. `source` and `target` are ids, never names.
- A label reads from source to target: `darcy → elizabeth, "in love with"` (Darcy is in love with Elizabeth), `wickham → georgiana, "betrays"`. A noun reads "source is target's label": `mr-bennet → elizabeth, "father"`. Use `"bidirectional": true` when it goes both ways (siblings, friends).
- The label picks the line color by keyword: love, enemy, father, friend, mentor, ally, rival and their relatives. Some common words stay gray (married, uncle, teacher, colleague). The full list and its surprises are under "Relationship colors" in data-format.md; when a color matters, use a matching word or set `"color": "#RRGGBB"` on the edge.
- Groups are defined once in `groups` (with a `color`) and referenced by id from each node's `groups`. Tags work the same way.
- Leave out `avatar` (image links written by an AI often don't load) and `position` (the editor lays the chart out and zooms to show all of it).

## 3. Check it and make the link

Save the JSON to a file and run the script in this skill's `scripts/` folder (Python 3, standard library only). Use its full path, or run it from the skill's folder:

```bash
python3 <this skill's folder>/scripts/relationmap_link.py chart.json
```

Errors, warnings and a one-line summary go to stderr; fix any errors and run again. The link is the only line on stdout, so `> link.txt` saves it. `--check` only checks; `--plain` makes a link without compression.

No Python? The Node version is at https://relationmap.io/docs/ai.md#3-make-the-link-in-code.

## 4. Hand it over

- Give the link with one line on what is in it, such as "11 characters, 13 relationships, 2 groups".
- Offer the JSON as a `.json` file too. It opens with **Open** in the editor, or by pasting it into the box at https://relationmap.io/edit/?paste=1 and tapping **Apply**.
- The chart opens in the user's own browser. It is saved to their account only when they save it there; if their editor already has a chart, it asks before replacing it.

If you can't run code, give the JSON in one ```json block and tell the user to paste it at https://relationmap.io/edit/?paste=1 and tap **Apply**. The box says how many characters it found before anything changes, and tells them if the JSON was cut off.

## Limits

- A link carries up to 1 MB of chart data (counted after unpacking). Charts without pictures stay far below that: 40 characters and 60 relationships make a link of about 2,100 characters.
- Compressed links need Chrome 80, Firefox 113, Safari 16.4 or newer. `--plain` links work in any browser but are three to five times longer.
