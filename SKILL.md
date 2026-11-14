---
name: relationmap-chart
description: Draft a character relationship chart for a novel, TV series, film, game, anime or the user's own story in RelationMap's JSON format, check it, and hand it over as a link that opens the chart in the free editor at relationmap.io, or as a .json file. Use when the user asks for a character relationship chart, relationship map or diagram, a "who's who" of a cast, or a chart of how characters are connected that they can edit and share.
---

# RelationMap chart

Turn a cast into a chart the user can open, edit and share at relationmap.io. No account and no API key: the chart travels inside a link, or as a .json file.

The format is documented at https://relationmap.io/docs/data-format.md and the AI workflow at https://relationmap.io/docs/ai.md. Read them when this page is not enough. Don't use fields that aren't documented there.

## 1. Pick the cast

Keep a chart to about 40 characters and 80 relationships. The editor opens a chart zoomed out to show all of it: on a laptop, 40 characters with 80 relationships open at about a third of full size. For a bigger story, make one chart per family, faction or season, and say so. Write names the way the story does.

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
- A label reads from source to target: `darcy → elizabeth, "in love with"` (Darcy is in love with Elizabeth), `wickham → georgiana, "betrays"`. A noun reads "source is target's label": `mr-bennet → elizabeth, "father"`. Use `"bidirectional": true` only when the label reads both ways ("sisters", "friends"). It is what draws the second arrow; the label never does.
- Draw at most one edge between two characters. A second edge is kept, but it is drawn on top of or right next to the first, so put both relationships in one label ("husband and cousin").
- Keep each `subtitle` to about 30 characters or fewer: it is drawn on one line under the name and never wrapped. Longer notes go in `description`, which shows when the user clicks the character in the editor.
- The label picks the line color by keyword: love, enemy, father, friend, mentor, ally, rival and their relatives. Matching is a plain substring test, so some common words stay gray (married, uncle, cousin, teacher, colleague, and plurals like enemies and allies). The full list and its surprises are under "Relationship colors" in data-format.md; when a color matters, use a matching word or set `"color": "#RRGGBB"` on the edge.
- Groups are defined once in `groups` (with a `color`) and referenced by id from each node's `groups`. Tags work the same way.
- Leave out `avatar` (image links written by an AI often don't load). Leave out `position` too (the editor lays the chart out and zooms to show all of it), except in a family tree: see below.
- Optional: `"meta": { "settings": { "avatarStyle": "notionists" } }` gives characters without a picture a drawn face instead of initials. The other styles are `lorelei`, `open-peeps`, `pixel-art` and `thumbs`.

### Family trees

- One edge from each parent to each child, labeled "father" or "mother". A child with both parents in the chart gets two edges.
- One edge per marriage, from husband to wife, labeled "husband" (or wife to husband, "wife"), without `bidirectional`.
- No edges between siblings: shared parents already show them.
- Give every node a `position`: `{ "x": 0, "y": 0 }` in pixels, x to the right, y downward. One generation per row, oldest at the top, rows about 200 apart, people in a row at least 150 apart, spouses side by side. A node without one is placed by the automatic layout and can end up off screen.
- "uncle", "aunt", "cousin", "nephew", "niece" and "married" are gray; color them with `customColorRules` (data-format.md, "Words for family trees").
- Each child brings two edges, so a family tree often has 1.5 to 2 times as many relationships as people. Split a big family into branches.

A complete example is under "Family trees" in https://relationmap.io/docs/ai.md.

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

- A link carries up to 1 MB of chart data (counted after unpacking). Charts without pictures stay far below that: a 40-person chart makes a link of about 3,000 to 4,000 characters.
- Compressed links need Chrome 80, Firefox 113, Safari 16.4 or newer. `--plain` links work in any browser but are three to five times longer.
