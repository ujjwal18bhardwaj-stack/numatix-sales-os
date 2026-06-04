---
name: firecrawl
description: >
  Use this skill for any web scraping, crawling, or extraction task: scraping a URL,
  crawling a website, mapping site structure, extracting structured data from a page,
  batch-scraping multiple URLs, open-ended web research, monitoring a page for changes,
  or any task involving the words "scrape", "crawl", "extract from URL", "map a website",
  "web research", or "watch a page".
---

# Firecrawl Skill

Firecrawl exposes a set of `firecrawl_*` MCP tools. Pick the right one using the decision
tree below, then follow the hard rules to avoid token overflow and wasted credits.

---

## Tool Selection Decision Tree

```
What do you need?
│
├─ Single known URL → firecrawl_scrape
│     └─ prefer JSON format + schema; markdown only if full prose is needed
│
├─ Multiple known URLs → firecrawl_batch_scrape
│     └─ then poll firecrawl_check_batch_status until complete
│
├─ Discover URLs on a site → firecrawl_map
│     └─ returns URL list; pipe into firecrawl_batch_scrape for content
│
├─ Open-ended web question → firecrawl_search
│     └─ ALWAYS follow with firecrawl_search_feedback (rating + missingContent)
│           → refunds a credit and improves future result quality
│
├─ Complex multi-source research → firecrawl_agent (async)
│     └─ poll firecrawl_agent_status until done
│
├─ Whole site / section extraction → firecrawl_crawl
│     └─ ALWAYS set limit + maxDepth (token overflow risk without them)
│     └─ poll firecrawl_check_crawl_status until complete
│     └─ prefer map + batch_scrape when you need fine control
│
├─ Extract structured fields → firecrawl_extract
│     └─ provide schema + prompt for best accuracy
│
└─ Watch a page over time → firecrawl_monitor_create
      └─ provide page URL + plain-English goal describing what change to detect
```

---

## Hard Rules

1. **Default to JSON + schema.** Only use `format: "markdown"` when full page prose is
   genuinely needed. JSON schemas keep responses small and structured.

2. **Never crawl without limits.** Always pass `limit` and `maxDepth` to `firecrawl_crawl`.
   Uncapped crawls will overflow context. When in doubt, use `firecrawl_map` +
   `firecrawl_batch_scrape` instead for precise control.

3. **Use batch_scrape for URL lists.** Calling `firecrawl_scrape` in a loop wastes credits
   and ignores parallelism. Pass the full list to `firecrawl_batch_scrape`.

4. **Don't use crawl/map for open-ended questions.** Use `firecrawl_search` — it queries
   the web rather than spidering a single origin.

5. **Always call firecrawl_search_feedback after search.** Pass a `rating` (1–5) and
   `missingContent` string. This refunds one credit and tunes future results.

---

## Copy-Paste Examples

### 1. Scrape a single URL with a JSON schema

```json
{
  "tool": "firecrawl_scrape",
  "arguments": {
    "url": "https://example.com/pricing",
    "formats": ["json"],
    "jsonOptions": {
      "schema": {
        "type": "object",
        "properties": {
          "plans":  { "type": "array", "items": { "type": "string" } },
          "prices": { "type": "array", "items": { "type": "string" } }
        },
        "required": ["plans", "prices"]
      },
      "prompt": "Extract all pricing plan names and their monthly prices."
    }
  }
}
```

### 2. Batch scrape multiple URLs

```json
{
  "tool": "firecrawl_batch_scrape",
  "arguments": {
    "urls": [
      "https://example.com/page1",
      "https://example.com/page2",
      "https://example.com/page3"
    ],
    "formats": ["json"],
    "jsonOptions": {
      "schema": {
        "type": "object",
        "properties": {
          "title":   { "type": "string" },
          "summary": { "type": "string" }
        }
      }
    }
  }
}
```
Then poll status with:
```json
{ "tool": "firecrawl_check_batch_status", "arguments": { "id": "<batch_id>" } }
```

### 3. Search with scrapeOptions

```json
{
  "tool": "firecrawl_search",
  "arguments": {
    "query": "best open-source vector databases 2025",
    "limit": 5,
    "scrapeOptions": {
      "formats": ["json"],
      "jsonOptions": {
        "schema": {
          "type": "object",
          "properties": {
            "name":        { "type": "string" },
            "description": { "type": "string" },
            "githubStars": { "type": "number" }
          }
        }
      }
    }
  }
}
```
Always follow with:
```json
{
  "tool": "firecrawl_search_feedback",
  "arguments": {
    "searchId": "<search_id>",
    "rating": 4,
    "missingContent": "Benchmark comparisons were not included"
  }
}
```

### 4. Extract structured fields from a page

```json
{
  "tool": "firecrawl_extract",
  "arguments": {
    "urls": ["https://example.com/team"],
    "prompt": "Extract the name, title, and LinkedIn URL for each team member.",
    "schema": {
      "type": "object",
      "properties": {
        "team": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name":     { "type": "string" },
              "title":    { "type": "string" },
              "linkedin": { "type": "string" }
            },
            "required": ["name", "title"]
          }
        }
      }
    }
  }
}
```

---

## Quick Reference Table

| Task | Tool | Return type | Notes |
|---|---|---|---|
| Scrape one URL | `firecrawl_scrape` | JSON or markdown | Use JSON + schema by default |
| Scrape many URLs | `firecrawl_batch_scrape` | Batch job ID → results | Poll `check_batch_status` |
| Discover URLs on a site | `firecrawl_map` | URL list | Combine with `batch_scrape` |
| Web Q&A / open research | `firecrawl_search` | Search results | Follow with `search_feedback` |
| Multi-source deep research | `firecrawl_agent` | Agent job ID → report | Poll `agent_status` |
| Full site extraction | `firecrawl_crawl` | Crawl job ID → pages | Requires `limit` + `maxDepth` |
| Structured field extraction | `firecrawl_extract` | Structured JSON | Provide schema + prompt |
| Monitor page for changes | `firecrawl_monitor_create` | Monitor ID | Use plain-English goal |

---

## One-Line Test Command

Verify the MCP server is connected and scrape a sample URL:

```
Use firecrawl_scrape on https://firecrawl.dev with formats: ["markdown"] to confirm the tool is working.
```

Or as a structured call:
```json
{ "tool": "firecrawl_scrape", "arguments": { "url": "https://firecrawl.dev", "formats": ["markdown"] } }
```
