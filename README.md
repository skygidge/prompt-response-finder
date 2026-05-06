# Prompt Response Finder

Automated story research for The Prompt Response AI速写 newsletter. Finds AI video, AI art, and interesting tech stories, writes them as Prompt Response blurbs, and publishes to a website.

Runs as a Claude Code Routine. No API keys. No extra cost.

## Website

https://skygidge.github.io/prompt-response-finder/

## How It Works

A Claude Code Routine runs on a schedule (daily, 8:45 AM PDT). Each run:
1. Pulls the latest repo changes (so edits made on GitHub are synced)
2. Reads your focus file to see what you want searched
3. Loads previous data so it doesn't find the same stories twice
4. Searches the web for new AI/tech stories using WebSearch + WebFetch
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

- **This Week** section at the top shows the last 7 days, sorted newest-found first
- **Archive** section below (collapsed) has everything older
- **Filter by category** using the colored pills (AI Video, AI Art, Tools, Funny, etc.)
- **Toggle language** with EN/中文 to swap which language appears first
- **Star** marks stories scored 8+ (lead story candidates)
- **Checkbox** on each story marks it as "used" (orange border appears). Persists across page reloads.
- **NEW badge** appears on stories you haven't seen before. Clears after your first visit.

Each story shows the article's original publication date (not the discovery date), and displays exactly like a Prompt Response article: English headline and blurb, then Chinese headline and blurb, separated by a horizontal rule.

## Story Fields

Each story in `all_stories.json` has:

| Field | Description |
|-------|-------------|
| `id` | Unique slug (e.g. `round-numbers-2026-05-06`) |
| `date_found` | Date the routine found it |
| `article_date` | Original article publication date (falls back to `date_found`) |
| `source_url` | Link to the original article |
| `source_name` | Publication name |
| `category` | One of: AI Video, AI Art, AI Tools, AI Business, AI Music, Funny, Other |
| `editorial_score` | 1–10, newsletter-worthiness |
| `en_headline` / `zh_headline` | English and Chinese headlines |
| `en_blurb` / `zh_blurb` | Full bilingual blurbs |

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

**Website not updating after a routine run:** Hard-refresh the browser (Cmd+Shift+R on Mac). The site fetches fresh JSON with cache-busting, but the HTML page itself may be cached. If stories are still missing, check `data/results/digest_YYYY-MM-DD.md` to confirm the run actually found something.

**Routine ran but found no stories:** Check that the run completed without errors in the Routines panel. Common cause: the search returned no results for the current focus. Try broadening focus.md.

**NEW badges show on stories I've already seen:** Clear localStorage for the site in your browser's DevTools (Application > Local Storage > Delete `known_stories`). Badges will reset.

**Stories are low quality:** Add feedback to learnings.json or update focus.md with clearer instructions about what you want.

**Duplicate stories appearing:** The system deduplicates by URL and by headline similarity. If duplicates still slip through, note it in focus.md: "I'm seeing duplicate Runway stories, be stricter about dedup."

**Want to run it now:** Click "Run now" in the Routines panel.

**Article dates look wrong:** Most dates are extracted from the source URL (e.g. `techcrunch.com/2026/04/29/...`). For sites without dates in their URLs, it falls back to the date the routine found the story. If a date is consistently wrong for a specific source, note it in focus.md.

**Site loading slowly:** After ~6 months of daily runs, `all_stories.json` may get large. Archive stories older than 90 days by moving them to a separate file. (A future update could automate this.)
