# RelationMap chart skill

A skill that teaches Claude to draft character relationship charts in [RelationMap](https://relationmap.io)'s JSON format, check them, and hand them over as a link that opens the chart in the free editor. Ask for "a relationship chart of the main characters in *Pride and Prejudice*" and you get a link; open it, then move people around, add pictures, save, share or embed.

No account, no API key, no server. The chart travels inside the link.

## Install in Claude Code

```bash
git clone https://github.com/Unibrighter/relationmap-skill.git ~/.claude/skills/relationmap-chart
```

Claude Code reads personal skills from `~/.claude/skills/<name>/SKILL.md` and uses this one when you ask for a relationship chart. To use it in one project only, clone it into `.claude/skills/relationmap-chart` inside that project.

## Without installing

In ChatGPT, Gemini or any other chat, copy the prompt from [relationmap.io/docs/ai](https://relationmap.io/docs/ai/), fill in your story, and paste the JSON answer into [relationmap.io/edit/?paste=1](https://relationmap.io/edit/?paste=1).

## What's inside

| File | What it is |
| --- | --- |
| `SKILL.md` | The instructions: pick the cast, write the JSON, check it, hand it over. |
| `scripts/relationmap_link.py` | Checks a chart (unique ids, relationships that point to real characters, groups that exist) and prints the link. Python 3, standard library only. |
| `examples/pride-and-prejudice.json` | 11 characters, 13 relationships, 2 groups. |

Try it:

```bash
python3 scripts/relationmap_link.py examples/pride-and-prejudice.json
```

## Format

- Data format: [relationmap.io/docs/data-format](https://relationmap.io/docs/data-format/) ([Markdown](https://relationmap.io/docs/data-format.md))
- Making charts with an AI, and how the link works: [relationmap.io/docs/ai](https://relationmap.io/docs/ai/) ([Markdown](https://relationmap.io/docs/ai.md))
- All docs for AI tools: [relationmap.io/llms.txt](https://relationmap.io/llms.txt)
