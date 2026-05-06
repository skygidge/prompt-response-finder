import json

with open('data/learnings.json', 'r', encoding='utf-8') as f:
    learnings = json.load(f)

# Update run metadata
learnings['total_runs'] = 3
learnings['last_run'] = '2026-05-06'

# Append new queries that produced results
new_productive = [
    "Anthropic $900 billion valuation $50 billion round TechCrunch April 2026",
    "GPT-5.5 OpenAI April 23 2026 features TechCrunch CNBC",
    "this is fine creator KC Green Artisan AI subway ad stolen art May 2026",
    "Sierra AI Bret Taylor $950 million funding May 2026 CNBC",
    "podslop AI podcast generated feeds streaming May 2026",
    "AI industry funding acquisition news May 2026",
    "AI funny weird tech news May 2026"
]
for q in new_productive:
    if q not in learnings['queries_that_produced_results']:
        learnings['queries_that_produced_results'].append(q)

# Append new queries that found nothing (or were unreliable)
new_nothing = [
    "Kling AI video model update new features May 2026 (Kling 3.0 launched Feb 5 2026 -- well outside window; VO3 AI Blog falsely dated it April 24)",
    "Runway AI video generation news May 2026 (Gen-4 was March 2025, Gen-4.5 December 2025; VO3 AI Blog again reported as new -- skip this aggregator entirely)",
    "Seedance ByteDance AI video model launch May 2026 (Seedance 2.0 launched Feb 12 2026 -- outside window)",
    "HunyuanVideo 1.5 Tencent GitHub release date open source (original model Nov 2025; May 4 entry was a weights update, not a model launch -- skip)",
    "Connecticut SB5 Governor Lamont signed AI employment disclosure May 2026 (governor indicated intention to sign but not yet signed as of May 6)",
    "Flux AI image model update Stable Diffusion May 2026 (no fresh news in window)",
    "Wan video model Alibaba update release May 2026 (Wan 2.7 was March 2026 -- outside window; Wan 3.0 expected mid-2026)",
    "Runway GWM-1 world model robotics avatars 2026 (launched December 11 2025 -- outside window)",
    "Runway NVIDIA Rubin platform partnership 2026 (announced January 5 2026 -- outside window)",
]
for q in new_nothing:
    if q not in learnings['queries_that_produced_nothing']:
        learnings['queries_that_produced_nothing'].append(q)

# Append new best source domains
new_domains = [
    "axios.com",
    "bloomberg.com",
    "decrypt.co (good for AI/crypto intersection, art theft stories)",
    "futurism.com (good for AI slop/podcast stories)",
    "podnews.net (podcast industry data)",
    "digitalmusicnews.com",
]
for d in new_domains:
    if d not in learnings['best_source_domains']:
        learnings['best_source_domains'].append(d)

# Append new patterns
new_patterns = [
    "VO3 AI Blog is confirmed unreliable for MULTIPLE models -- it has falsely reported Runway Gen-4 AND Kling 3.0 as current-week releases when both launched months earlier. Treat any date from this source as unverified until cross-checked against official GitHub, HuggingFace, or company blog.",
    "Chinese AI video models (Kling, Seedance, Wan, Hunyuan) all launched their major 2026 updates in February-March -- they are now outside the 14-day window. Next cycle: watch for Wan 3.0 (expected mid-2026), Kling 3.1/4.0 updates.",
    "GPT-5.5 (April 23) was missed in Run 2. OpenAI is shipping major model versions roughly monthly in 2026 -- always run a dedicated 'OpenAI model release' search each run.",
    "Anthropic $900B round: revenue growth from $9B (end 2025) to $30B ARR in ~4 months is the key data point. Coding tools (Claude Code) are the driver. IPO expected October 2026 -- watch for board decision and round closure.",
    "Enterprise AI agents (Sierra, and the broader category) are the growth story of 2026 Q2. $950M at $15.8B with 40% Fortune 50 penetration signals the call center replacement thesis is now fundable at scale.",
    "The 'This is Fine' meme theft is a model ai_funny story: real legal stakes, clear irony (AI company stealing art), strong sourcing, and a punchline that writes itself. Look for similar AI-company-misusing-creator-IP patterns.",
    "Podslop (AI podcast flooding) is a strong recurring beat. The category is: AI-generated content overwhelming platform moderation. Same pattern applies to music (covered), video (coming), and now podcasts. Run this search each cycle.",
    "DALL-E API shuts down May 12 -- developer fallout stories may appear immediately after. Run 'DALL-E migration developer impact May 12 2026' next run.",
    "Connecticut SB5 still not signed as of May 6 -- check next run. If signed, it becomes a milestone policy story.",
    "Suno Series D still closing -- check next run for confirmation and final valuation.",
]
for p in new_patterns:
    if p not in learnings['patterns']:
        learnings['patterns'].append(p)

# Append feedback
new_feedback = "Run 3 complete (2026-05-06). 5 new stories added. Top pick: Anthropic $900B valuation round (score 9). Strong industry/funding week. GPT-5.5 (April 23) was missed in previous run -- confirmed lesson to always search OpenAI model releases explicitly. Best ai_funny yet: KC Green vs Artisan AI meme theft (real sourcing, real stakes, irony built in). Sierra $950M establishes enterprise AI agents as 2026's growth category. Podslop gives audio a funny/real beat. No new AI video stories -- all Chinese models launched Feb-March, outside 14-day window. Suggestions for next run: check DALL-E API shutdown fallout (May 12), check Connecticut SB5 signature, check Suno Series D closure, check Anthropic round closure, look for Wan 3.0 announcement, run explicit OpenAI model release search."
learnings['feedback'].append(new_feedback)

with open('data/learnings.json', 'w', encoding='utf-8') as f:
    json.dump(learnings, f, ensure_ascii=False, indent=2)
print("learnings.json updated")
print(f"  total_runs: {learnings['total_runs']}")
print(f"  last_run: {learnings['last_run']}")
print(f"  feedback entries: {len(learnings['feedback'])}")
print(f"  productive queries: {len(learnings['queries_that_produced_results'])}")
