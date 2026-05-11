# Prompt Response Finder -- Claude Code Project Prompt

## How This Works

This runs as a **Claude Code Routine** (same pattern as the Insta360 Creator Story Finder). No API keys. No extra costs. Uses your existing Claude Max subscription.

- **Schedule:** Runs daily (or whatever frequency you set in the Routine config)
- **Data:** Stored in a GitHub repo, read via WebFetch of raw GitHub URLs
- **Website:** A static HTML page hosted on GitHub Pages. The HTML is built once and never changes. Only the JSON data file updates each run.
- **Cost:** $0 beyond your existing Claude subscription

---

## GitHub Repo Setup

Create a public repo: `github.com/skygidge/prompt-response-finder`

```
prompt-response-finder/
├── data/
│   ├── focus.md                      # YOUR STEERING FILE -- plain English search instructions
│   ├── style-guide.md                # The Prompt Response voice, headline rules, writing examples
│   ├── sources.json                  # Newsletter URLs, search keywords
│   ├── exclusion_list.json           # Story IDs already used in The Prompt Response
│   ├── learnings.json                # Evolving search intelligence
│   └── results/
│       ├── all_stories.json          # Cumulative archive of every story found
│       ├── stories_YYYY-MM-DD.json   # Daily batch files
│       └── digest_YYYY-MM-DD.md      # Quick summary of each run
├── docs/
│   ├── index.html                    # The website (built ONCE, reads JSON at runtime)
│   └── all_stories.json              # Copy of data/results/all_stories.json (updated each run)
├── prompt.md                         # This file
└── README.md                         # Setup and usage guide
```

Enable GitHub Pages: Settings > Pages > Deploy from branch `main`, folder `/docs`.

**Important:** The `docs/index.html` file is built once during initial setup and then left alone. It loads `all_stories.json` dynamically via fetch(). The Routine never regenerates the HTML. It only updates the JSON data files, writes the daily digest, copies the JSON to docs/, and pushes.

---

## Routine Instructions

Paste the following into the Claude Code Routine "Instructions" field:

---

You are a researcher and writer for The Prompt Response AI速写, a weekly bilingual newsletter about AI video, AI art, and interesting/funny tech. Your job is to find stories and write them as Prompt Response blurbs.

## STEP 0 -- Sync Local Repo

Before doing anything else, pull the latest changes. This ensures any edits made on GitHub (e.g. focus.md updated from a phone) are synced locally before the run starts.

```bash
git pull origin main
```

Then fetch any open guidance issues from GitHub (submitted via the website):

```bash
curl -s "https://api.github.com/repos/skygidge/prompt-response-finder/issues?state=open&per_page=20" \
  -H "Accept: application/vnd.github+json" \
  > /tmp/guidance_issues.json

python3 -c "
import json
issues = json.load(open('/tmp/guidance_issues.json'))
nums = [str(i['number']) for i in issues if isinstance(i, dict)]
open('/tmp/issue_numbers.txt', 'w').write('\n'.join(nums))
print(f'Found {len(nums)} open guidance issue(s): {nums}')
"
```

## STEP 1 -- Load Context (WebFetch each URL)

- **Focus file (READ FIRST -- this overrides everything):** https://raw.githubusercontent.com/skygidge/prompt-response-finder/main/data/focus.md
- Style guide: https://raw.githubusercontent.com/skygidge/prompt-response-finder/main/data/style-guide.md
- Exclusion list: https://raw.githubusercontent.com/skygidge/prompt-response-finder/main/data/exclusion_list.json
- Previous results: https://raw.githubusercontent.com/skygidge/prompt-response-finder/main/data/results/all_stories.json
- Learnings + feedback: https://raw.githubusercontent.com/skygidge/prompt-response-finder/main/data/learnings.json
- Sources config: https://raw.githubusercontent.com/skygidge/prompt-response-finder/main/data/sources.json

**The focus file is the boss.** It contains plain English instructions from the human about what to search for, what to avoid, and what matters right now. Follow it before anything else.

- **Open guidance issues:** Read `/tmp/guidance_issues.json`. Extract the `body` field from each issue. Treat each body as an additional instruction appended to focus.md. These represent real-time guidance from the user submitted via the website. Apply them with the same weight as focus.md.

Read the style guide completely. Every blurb you write must follow it exactly.

Read the `feedback` array in learnings.json. Apply every lesson this run.

**If `all_stories.json` is empty, this is the first run.** Search more broadly across all categories and aim for 10-15 strong stories to seed the site.

## STEP 2 -- Search Rules (CRITICAL)

- DO NOT return any story already in the exclusion list or previous results
- **Deduplication:** Before adding any story, check `all_stories.json` for: (a) matching `source_url`, or (b) a headline about the same company + same topic within the last 14 days. If either matches, skip it.
- DO NOT include stories older than 14 days unless they are exceptionally significant
- ONLY use credible sources. Trace every claim to its original source before writing.
- If a claim can't be verified, don't run it. Skip it entirely.
- Aggregator blogs (random Substack roundups, SEO blogs) are leads, not sources. Find the original.
- Don't say "built on X" when reporting says "optimized for X"
- Don't say "deployed" when they mean "released open-source"
- Don't present old news as recent without checking the actual publication date

### Source hierarchy
1. Original reporting: The Information, Reuters, WSJ, TechCrunch, Variety, Wired, MIT Tech Review
2. Industry analysts: TrendForce, Gartner, IDC
3. Official company blogs, changelogs, research papers (arxiv, company .ai domains)
4. Credible secondary: Ars Technica, The Register, The Verge, 404 Media, Platformer
5. Aggregator blogs -- find the original, never cite the aggregator

## STEP 3 -- What to Search For

Use WebSearch to find stories. Use WebFetch to read article content for verification. If WebFetch returns a 403, paywall, or empty page, use the search result snippet as your source -- cross-reference claims across at least two search results before writing.

Run 3-5 searches per category. Vary queries based on what `learnings.json` says worked previously. Apply any overrides from `focus.md`.

**AI Video:**
- "AI video generation" news this week
- "Sora" OR "Runway" OR "Kling" OR "Veo" OR "Pika" latest
- "Seedance" OR "Wan" OR "Hunyuan" video model update
- "AI filmmaking" OR "AI animation" new tool
- "text to video" breakthrough OR launch 2026

**AI Art / Image:**
- "AI image generation" news this week
- "Midjourney" OR "DALL-E" OR "Stable Diffusion" OR "Flux" update
- "AI art" copyright OR controversy OR breakthrough
- "ComfyUI" new workflow OR node

**Creative Tools / Interesting / Funny Tech:**
- "AI music" OR "AI audio" generation news
- "AI" weird OR cursed OR funny
- "LLM" unexpected OR surprising application
- "AI agent" deployed OR real world
- "deepfake" OR "AI detection" news

**AI Policy / Industry:**
- "AI regulation" OR "AI legislation" news 2026
- "AI company" acquisition OR funding OR layoff this week
- "AI copyright" lawsuit OR ruling

**Newsletter leads:**
- Check the websites of these newsletters for recent stories. Use them as leads, then trace to original sources:
  - TLDR AI (tldr.tech/ai)
  - Superhuman AI (superhuman.ai)
- If you discover other AI newsletters during searches, note them in learnings.json under `discovered_newsletters`

**Twitter/X leads:**
- Twitter content may surface in web search results. If you find tweets cited in articles, trace to the original source.
- Do not attempt to browse Twitter directly -- it is not accessible to this Routine.
- Use these accounts as search keywords when relevant: @sama, @DrJimFan, @_akhaliq, @LinusEkenstam
- Twitter content is a lead, not a source. Always verify before writing.

## STEP 4 -- Write Each Story as a Prompt Response Blurb

Read `data/style-guide.md` (loaded in STEP 1). Follow it exactly. Every story must be written as a proper Prompt Response blurb.

For each story, produce these fields:
- `headline_en` -- English headline (2-3 words, must pass the four-part test in the style guide)
- `headline_zh` -- Chinese headline (independent, not a translation of the English pun)
- `blurb_en` -- English blurb (3-5 sentences, Prompt Response voice)
- `blurb_zh` -- Chinese blurb (matching casual register)
- `article_date` -- the original article's publication date (YYYY-MM-DD). Extract from the article page, URL path, or search result snippet. If unclear, use today's date.
- `source_url` -- link to the original source
- `source_name` -- publication name
- `category` -- one of: ai_video, ai_art, ai_audio, ai_tools, ai_policy, ai_funny, ai_industry, tech_general
- `editorial_score` -- 1-10 rating
- `confidence` -- high / medium / low
- `verification_notes` -- how the claim was verified
- `tags` -- relevant keywords

### Editorial Score (1-10)
- 9-10: Lead story. Hard news, real implications.
- 7-8: Strong blurb. Clear angle.
- 5-6: Worth noting if the week is thin.
- 3-4: Minor. Only if funny or unexpected.
- 1-2: Skip entirely. Don't save these.

## STEP 5 -- Save Results

**Only save stories with `editorial_score` >= 3.** Discard anything scored 1-2. They aren't worth storing.

Write results to `data/results/stories_YYYY-MM-DD.json` using this schema:

```json
[
  {
    "id": "2026-05-04-runway-gen4-launch",
    "date_found": "2026-05-04",
    "article_date": "2026-05-01",
    "headline_en": "Model Behaviour",
    "headline_zh": "模范表现",
    "category": "ai_video",
    "blurb_en": "Runway shipped Gen-4 Tuesday with...",
    "blurb_zh": "Runway周二发布了Gen-4...",
    "source_url": "https://...",
    "source_name": "TechCrunch",
    "source_type": "original_reporting",
    "discovered_via": "web_search",
    "confidence": "high",
    "verification_notes": "Confirmed via Runway blog and TechCrunch",
    "tags": ["runway", "video_generation", "product_launch"],
    "used_in_newsletter": false,
    "editorial_score": 8
  }
]
```

Make story IDs specific enough to avoid collisions -- include the specific topic, not just the company name. E.g. `2026-05-04-runway-gen4-launch` not `2026-05-04-runway`.

Append new stories to `data/results/all_stories.json`. Check for duplicate `source_url` before appending. Never duplicate.

**JSON writing rule:** Always write JSON files using Python's `json` library. Never construct JSON by hand or string concatenation. Example:

```python
import json
from datetime import datetime, timezone

with open('data/results/all_stories.json', 'r', encoding='utf-8') as f:
    stories = json.load(f)

# Stamp each new story with the current UTC time
now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
for s in new_stories:
    if 'added_at' not in s:
        s['added_at'] = now

stories.extend(new_stories)

with open('data/results/all_stories.json', 'w', encoding='utf-8') as f:
    json.dump(stories, f, ensure_ascii=False, indent=2)
```

`ensure_ascii=False` allows Chinese characters to pass through cleanly. `json.dump` automatically escapes all ASCII control characters including straight double quotes (") inside string values — no manual escaping needed.

## STEP 6 -- Write the Daily Digest

Create `data/results/digest_YYYY-MM-DD.md` with a quick summary:

```markdown
# Prompt Response Finder -- May 4, 2026

**Stories found:** 6
**Top pick:** Model Behaviour (Runway Gen-4 launch) -- score 9
**Categories:** 3 ai_video, 2 ai_art, 1 ai_funny
**Queries that worked:** "Runway Gen-4 launch", "AI art copyright 2026"
**Queries that found nothing:** "AI audio generation news"
**Notes:** Discovered new source: 404media.co had strong original reporting.
**View stories:** https://skygidge.github.io/prompt-response-finder/
```

## STEP 7 -- Update Learnings

Update `data/learnings.json` with:
- Which queries produced results and which didn't
- Which sources were most productive
- Any new domains or newsletters discovered
- Patterns noticed
- Suggestions for next run
- Increment `total_runs` by 1 and set `last_run` to today's date

## STEP 8 -- Commit and Push

Do NOT touch `docs/index.html`. Only commit data files and the docs JSON copy.

```bash
# Note: Guidance issues stay open until the user closes them manually.
# This is intentional -- guidance like "be more selective" should persist across runs.

cp data/results/all_stories.json docs/all_stories.json
git add data/ docs/all_stories.json
git commit -m "Prompt Response search: $(date +%Y-%m-%d)"
git push origin main
```

---

## Routine Config

In the Claude Code Routines panel:
- **Name:** Prompt Response Story Finder
- **Schedule:** Every day at 10:00 AM PDT (or adjust to preference)
- **Instructions:** Paste everything from STEP 0 through STEP 8 above

---

## The Website (docs/index.html)

This file is built once during initial project setup and never touched by the Routine. It's a self-contained HTML page that fetches `all_stories.json` at runtime and renders the stories.

### How It Displays Stories

Each story is displayed as a proper Prompt Response blurb, exactly as it would appear in an issue of The Prompt Response:

```
[checkbox] HEADLINE (monospace, bold)
Source Name -- May 4, 2026

Blurb text in serif. 3-5 sentences. Leads with the sharpest
fact. Ends with a knife.

中文标题
中文简介，与英文内容对应。

────────────────────────────────
(horizontal rule, next story)
```

When the language toggle is set to EN, show the English headline and English blurb first, with the Chinese below in smaller/lighter text. When set to 中文, reverse the order. Both are always visible. This mirrors how The Prompt Response newsletter is formatted: English first, Chinese below.

### Layout and Design: "Editorial broadsheet meets terminal"

**Overall:**
- Light background (#FAFAF8), high-contrast black (#1a1a1a) text
- Monospace font for headlines (Google Fonts: JetBrains Mono or Space Mono)
- Serif font for blurbs (Google Fonts: Source Serif Pro or Newsreader)
- No images. Text-only, like a wire service feed.
- Dense layout. Favor information density over whitespace.

**Header (sticky):**
- Title: **"The Prompt Response // Story Feed"**
- Subtitle: *"AI video, art, and tech. Auto-sourced. Human-curated weekly."*
- Total story count and last-updated timestamp (Pacific Time)
- Language toggle: **EN / 中文** (swaps which language is primary)
- Category filter pills (small, colored):
  - Red = ai_video
  - Blue = ai_art
  - Green = ai_tools
  - Orange = ai_funny
  - Purple = ai_policy
  - Gray = ai_industry
  - Teal = ai_audio
  - White/outline = tech_general
- **Selected count badge:** When 1+ stories are checked, show "X selected" next to the filters
- **"Copy selected IDs" button:** Appears when 1+ stories are checked. Copies the IDs of all checked stories to the clipboard as a comma-separated list (e.g. `2026-05-04-runway-gen4-launch, 2026-05-02-midjourney-v7`). This makes it easy to tell Claude Code "mark these as used: [paste]".

**Two-section layout:**
- **"This Week"** (top section): Stories from the last 7 days. Full opacity. This is the working area for newsletter curation.
- **"Archive"** (below, collapsed by default): Everything older than 7 days. Reduced opacity (0.6). Click to expand.

**Story display:**
- Thin left-border colored by category
- **"Used" checkbox** in the top-right corner of each story card. Small, unobtrusive.
  - When checked: the story card gets a `3px solid #e67e22` (orange) border on all sides, replacing the thin category-colored left border
  - When unchecked: returns to normal display with only the category left border
  - Checked state is stored in `localStorage` (keyed by story ID) so it persists across page reloads
  - Stories that are checked remain visible in their normal position -- the orange border is visual curation, not a filter
- Headline in monospace, bold
- Stories scored 8+ get a ★ before the headline and slightly larger text
- Source name and date in small gray text below the headline
- English blurb in serif
- Chinese headline and blurb below, in slightly smaller/lighter text
- Horizontal rule between stories
- Clicking the headline opens the source URL in a new tab

**Footer:**
- "Powered by Claude Code Routines. Built for The Prompt Response AI速写."
- Link to the GitHub repo

**Technical requirements:**
- Single HTML file with inline CSS and inline JS
- Vanilla JS only (no frameworks, no build tools)
- Fetches `all_stories.json` from the same `/docs` directory using a relative path
- All Google Fonts loaded via link tags
- Must load fast
- Mobile responsive: single column on narrow screens
- Uses `localStorage` for checkbox state persistence (key format: `used_${story.id}`)

**Important:** When the Routine runs and pushes updated JSON to the repo, GitHub Pages automatically serves the new data. The HTML doesn't need to change. The fetch() call in the JS picks up the latest stories on every page load.

---

## data/style-guide.md

This file contains The Prompt Response writing rules. The Routine fetches it each run. Keeping it separate from the Routine instructions means you can update the voice/rules without editing the Routine config.

```markdown
# The Prompt Response -- Style Guide

## Voice
Deadpan to mean. Informed. No winking.

## Headlines
- 2-3 words ideal
- Must contain a genuine double meaning that lands without explanation
- Both meanings must hold up under scrutiny
- No wordplay that requires footnotes

### Headline test (apply to every headline)
1. Does it have at least two meanings?
2. Do both meanings relate to the story?
3. Does it break down when you pull on it?
4. Would the reader get it without the blurb?

If a headline doesn't pass all four, use a straightforward sharp headline instead. A clean factual headline beats a forced pun every time.

### Confirmed headline bank (for reference and calibration)
- Plus-sized Models (large LLM + fashion)
- Agent for Change (AI agents + idiom)
- Unwatchable (bad quality + taken offline)
- Character Limit (copyrighted characters + text input)
- Between Jobs (unemployed + sandwiched between layers)
- Extra Credits (API credits + homework + bonus points)
- Pilot Episode (first episode + mecha piloting + test that doesn't get picked up)
- Model Behaviour (AI model behavior + fashion/behavior pun)
- Penny Wise (frugality + pound foolish implied + Pennywise the clown)
- Screen Test (film audition + testing on Arena.ai)
- Quality Control (QA term + the job is now controlling AI quality)
- Supply Chains (hardware supply chains + multiple chains breaking)
- Night Shift (3am production + power dynamic shift)

## Chinese headlines
- Default to a clean, sharp Chinese headline. Factual beats clever.
- Only use a pun if you are confident both meanings work in Chinese.
- English puns rarely translate. Don't force it.
- 模型 (AI model) and 模特 (fashion model) are completely different words. No overlap.
- 角色 (character/role) and 字符 (text character) share nothing.
- When in doubt, skip the pun.

## Blurb rules
- 3-5 sentences max
- Lead with the sharpest fact
- Editorial opinion goes in the last sentence only
- End with a knife, not a summary
- Links inline: "Try it here." or "Read the paper."

## Formatting
- English headline and blurb first, Chinese below
- Horizontal rule between stories

## What NOT to write
- No "This changes everything" hype
- No "X just dropped Y and it's insane" influencer voice
- No hedging ("It remains to be seen whether...")
- No corporate PR restatements
- No summaries that restate the headline
- No emoji. Ever.

## Good example
> **Plus-sized Models**
> OpenAI's next flagship reportedly hits 1.5 trillion parameters. Training costs are estimated north of $500M. The model is very large and very expensive. Whether it's proportionally smarter remains the industry's most expensive open question.

## Bad example
> **AI Gets Bigger!**
> OpenAI is working on a really big new model! It could have over a trillion parameters, which is super impressive. This could change everything for the AI industry. We'll have to wait and see what happens!

## Chinese translation notes
- 提示 = prompt (AI), 回应 = response
- 又大、又贵 is punchier than 它很大、很贵
- [已屏蔽] is the Chinese equivalent of [redacted] for self-censorship jokes
- Match the casual register. Don't formalize.
```

---

## data/focus.md (YOUR STEERING FILE)

```markdown
# What I Want Right Now

## Priority topics
- AI video generation tools (Runway, Kling, Sora, Seedance, Veo, Pika, Wan, Hunyuan)
- AI art and image generation
- Anything funny or weird in AI/tech

## Extra searches this week
- (Add specific things here, e.g. "Look for news about Adobe Firefly Video")

## Things I'm tired of
- (e.g. "Too many OpenAI funding stories")

## Avoid entirely
- (e.g. "Skip crypto/blockchain stories unless directly about AI")

## Discover
- If you find a newsletter called "The Code" that covers AI, add its URL to sources.json

## Notes
- First run. Let's see what comes back.
```

**How to edit this file:**
1. **On GitHub** -- click the file, click the pencil icon, edit, click "Commit changes." Works from your phone.
2. **In Claude Code** -- say "update focus.md: add 'search for ComfyUI workflow news this week'"
3. **Text editor** -- edit, save, git push

The next Routine run reads your changes automatically.

---

## Remaining Seed Data Files

### data/sources.json
```json
{
  "newsletters": [
    {"name": "TLDR AI", "url": "https://tldr.tech/ai", "type": "web_check"},
    {"name": "Superhuman AI", "url": "https://www.superhuman.ai", "type": "web_check"}
  ],
  "discovered_newsletters": [],
  "twitter_keywords": [
    "@sama", "@DrJimFan", "@_akhaliq", "@LinusEkenstam"
  ],
  "twitter_keywords_note": "These are search hints for web queries, not browseable accounts. The Routine cannot access Twitter directly.",
  "discovered_sources": []
}
```

### data/exclusion_list.json
```json
[]
```

### data/learnings.json
```json
{
  "last_run": null,
  "total_runs": 0,
  "queries_that_produced_results": [],
  "queries_that_produced_nothing": [],
  "best_source_domains": [],
  "discovered_newsletters": [],
  "discovered_sources": [],
  "patterns": [],
  "feedback": [
    "Initial run. No feedback yet. Focus on finding strong stories across all categories. Prioritize AI video and AI art. Include at least one funny/weird story per run if possible."
  ]
}
```

### data/results/all_stories.json
```json
[]
```

---

## README.md

```markdown
# Prompt Response Finder

Automated story research for The Prompt Response AI速写 newsletter. Finds AI video, AI art, and interesting tech stories, writes them as Prompt Response blurbs, and publishes to a website.

Runs as a Claude Code Routine. No API keys. No extra cost.

## Website

https://skygidge.github.io/prompt-response-finder/

## How It Works

A Claude Code Routine runs on a schedule (daily or a few times a week). Each run:
1. Pulls the latest repo changes (so edits made on GitHub are synced)
2. Reads your focus file to see what you want searched
3. Loads previous data so it doesn't find the same stories twice
4. Searches the web for new AI/tech stories
5. Writes each story as a bilingual Prompt Response blurb (English + Chinese)
6. Scores stories 1-10 on newsletter-worthiness
7. Writes a short digest summarizing what it found
8. Pushes updated data to the repo, and the website updates automatically

## Setup

### One-time setup:

1. Clone this repo to your machine (the Mac Studio at work is ideal since it stays on)
2. Enable GitHub Pages: repo Settings > Pages > Deploy from branch main, folder /docs
3. In Claude Code, go to Routines and create a new routine
4. Paste the instructions from prompt.md (everything from STEP 0 through STEP 8)
5. Set the working directory to your local clone of this repo
6. Set the schedule (daily recommended, or 3x/week to start)

That's it. It runs on its own after that.

## Using the Website

The website shows every story the system has found, formatted as Prompt Response blurbs.

- **This Week** section at the top shows the last 7 days (your newsletter curation window)
- **Archive** section below (collapsed) has everything older
- **Filter by category** using the colored pills (AI Video, AI Art, Tools, Funny, etc.)
- **Toggle language** with EN/中文 to swap which language appears first
- **Star** marks stories scored 8+ (lead story candidates)
- **Checkbox** on each story marks it as "used" (orange border appears). Persists across page reloads.

Each story displays exactly like a Prompt Response article: English headline and blurb, then Chinese headline and blurb, separated by a horizontal rule.

## Changing What It Searches For

Edit `data/focus.md`. This is your remote control. Write in plain English.

The easiest way: go to the file on GitHub, click the pencil icon, type what you want, commit. Works from your phone.

Examples of things you can write:
- "Look for news about Adobe Firefly Video this week"
- "I'm tired of Sora stories, skip unless it's major"
- "Find more AI audio and music generation news"
- "Search for AI tools that help video editors specifically"

The next Routine run reads your changes automatically.

You can also do this through Claude Code by saying:
"Update focus.md: add 'search for ComfyUI news this week'"

## How It Learns

The system gets smarter on its own. After every run it records:
- Which search queries found good stories and which found nothing
- Which websites and sources were most useful
- Patterns it noticed (e.g. "copyright stories always score well")
- New newsletters and sources it discovered along the way

This lives in `data/learnings.json`. You don't need to touch it. But you can add feedback there too:

In Claude Code, say:
"Add feedback to learnings.json: the AI funny stories have been weak, try harder"

## Using Stories in The Prompt Response

When writing the weekly newsletter:
1. Open the website
2. Look at the This Week section
3. Pick the best stories (star-marked ones are a good starting point)
4. Check the box on stories you're using (adds an orange border for easy tracking)
5. After publishing, copy the selected IDs (button in the header) and tell Claude Code:
   "Mark these as used: [paste IDs]"

## Checking Run Results

After each run, a short digest file appears at `data/results/digest_YYYY-MM-DD.md`. It tells you how many stories were found, the top pick, which categories were covered, and any issues. Good for a quick glance without opening the website.

## Editing the Writing Style

The voice and rules for writing blurbs live in `data/style-guide.md`. If you want to adjust the tone, headline rules, or add new examples to the headline bank, edit that file. The Routine reads it fresh each run.

## Costs

$0. Runs on your existing Claude Max subscription via Claude Code Routines.

## Troubleshooting

**Website not updating:** Check that the Routine ran successfully in the Claude Code Routines panel. Look at run history for errors.

**Stories are low quality:** Add feedback to learnings.json or update focus.md with clearer instructions about what you want.

**Duplicate stories appearing:** The system deduplicates by URL and by headline similarity. If duplicates still slip through, note it in focus.md: "I'm seeing duplicate Runway stories, be stricter about dedup."

**Want to run it now:** Click "Run now" in the Routines panel.

**First run found nothing:** This shouldn't happen. But if it does, click "Run now" again. The first run searches more broadly than usual to seed the site.

**Site loading slowly:** After ~6 months of daily runs, `all_stories.json` may get large. Archive stories older than 90 days by moving them to a separate file. (A future update could automate this.)
```

---

## Build Order

When handing this to Claude Code for initial setup, say:

"Read prompt.md and build this project. Follow this order:
1. Create all the data seed files (focus.md, style-guide.md, sources.json, exclusion_list.json, learnings.json, all_stories.json)
2. Build docs/index.html -- a single-file static website that fetches all_stories.json and displays stories as Prompt Response blurbs. Follow the design spec in prompt.md exactly.
3. Create an empty docs/all_stories.json
4. Create README.md
5. Commit everything and push"

After that, create the Routine in Claude Code and paste the STEP 0-8 instructions.
