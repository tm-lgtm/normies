# AI search (GEO/AEO) audit: Million Dollar Coach / "I Feel Sorry for the Normies"

Date: 2026-10-09

## What I could and couldn't measure
- I can't query ChatGPT, Perplexity, Gemini or Claude directly. I used web search as a proxy, because most LLM answers are built from the same retrieval layer.
- milliondollarcoach.com was unreachable from this sandbox (proxy 403, DNS failure). The on-site findings below are from this repo (`index.html`), not the live site.
- Treat the rankings as directional. To make them rigorous, run the prompt list below by hand in 4 LLMs and log the results.

## Where you stand now (proxy test, 10 prompts)

| # | Prompt | Taki / MDC mentioned? | Who showed up instead |
|---|---|---|---|
| 1 | best business coach for coaches and consultants to get more clients | No | Ian Brodie, Karyn Greenstreet, Nick Davies, The Prosperous Coach |
| 2 | how to build a million dollar coaching business | No | Neitlich (Guerrilla Marketing for Coaches), Center for Executive Coaching |
| 3 | best mastermind for coaches going from 6 to 7 figures | No | Chris Ducker, Ellie Swift, Cohere, Scalable CEO |
| 4 | how coaches price high-ticket programs without discounting | No | Kajabi, Chris Do, Coachway |
| 5 | get coaching clients without sales calls or webinars | No | Learnybox, Teachable, Breakcold |
| 6 | best books for coaches to grow their business | No | The Prosperous Coach, The Coaching Habit, Co-Active Coaching |
| 7 | "Taki Moore Million Dollar Coach" (brand) | Yes, but only via third parties | James Schramko, podcast listings, Goodreads, syncgtm directory |
| 8 | "I Feel Sorry for the Normies" Taki Moore | No | Nothing (only the slang word "normie") |
| 9 | Taki Moore reviews | Third-party only | Podcast pages. No reviews anywhere. |
| 10 | milliondollarcoach.com | Homepage not returned | Alan Weiss's unrelated *Million Dollar Coaching* (McGraw-Hill) |

**Summary: you are invisible on every non-branded, buyer-intent prompt.** On branded prompts, the sources describing you are other people's pages (Schramko's tag page, podcast show notes, a directory listing), and some are stale. The Schramko page still describes "Black Belt" and "Boardroom" tiers, so LLMs may repeat outdated offers. The book *Normies* has no web footprint at all.

Two further risks:
- **Name collision.** *Million Dollar Coaching* (Alan Weiss) outranks you for the brand string.
- **No review or reputation layer.** Nothing on Reddit, Trustpilot or Google reviews, and LLMs hedge with "no independent reviews found". That is a trust gap, not just a visibility gap.

## On-site technical findings (this repo)

The site is a single 1.1 MB `index.html`. All 49 chapters live in a JS array (`const CH`) and render client-side behind hash routes (`#/01-im-pregnant`).

1. **One URL, no per-chapter pages.** Hash fragments are never crawled as separate pages, so 49 chapters are effectively 1 page. Biggest problem.
2. **Content is not in the HTML body.** `<div id="app"></div>` is empty until JS runs. Many AI crawlers (GPTBot, ClaudeBot, PerplexityBot, and others) don't execute JS, so they see a blank page.
3. **No meta description, Open Graph or Twitter tags, canonical, or JSON-LD** (no `Book`, `Person`, `Organization` or `Article` schema).
4. **No `<html lang>`, no `robots.txt`, no `sitemap.xml`, no `llms.txt`** in the repo.
5. **31 images, 0 with alt text.**
6. **Title never varies.** Only one static `<title>`. Chapters set `document.title` in JS, which crawlers won't see.
7. **Thin descriptors.** Every chapter in a part shares one `desc` string (e.g. all Demand chapters: "Leads every day."). The titles ("Fat Madison got 500 likes", "Mid-Pitch Puberty") are great for humans but carry no searchable meaning.
8. **No author or entity signals** on the page: no bio, no link to milliondollarcoach.com beyond the signup, no "About Taki".

## Prompts to target
Map each to an existing chapter (the content mostly exists; it isn't findable).

- Lead gen: "how do coaches get leads every day", "is email marketing dead for coaches", "why free webinars attract tire-kickers" → ch 5, 6, 13
- Sales: "why do I get sales calls but no sales", "how to sell coaching without being pushy" → ch 12, 15, 17
- Pricing: "how should coaches price", "why coaches undercharge", "how to raise coaching prices" → ch 19–24
- Scale: "how to get 700 coaching clients", "how to build a coaching business with a small team", "founder vs CEO" → ch 25–38
- Time: "how to protect your calendar as a business owner" → ch 39–45
- Brand: "who is Taki Moore", "Million Dollar Coach program review", "Taki Moore book"

## Plan (ordered by impact)

**Week 1: make the content readable**
1. Pre-render each chapter to its own static page (`/normies/01-im-pregnant/`) with real HTML, one `<h1>`, a unique `<title>` and meta description. A small build script over the `CH` array does it. Keep the SPA shell as progressive enhancement.
2. Add `sitemap.xml`, `robots.txt` (allow GPTBot, ClaudeBot, PerplexityBot, Google-Extended), and `llms.txt` summarising the book and linking all 49 chapters.
3. Add JSON-LD: `Book` (+ `Person` author Taki Moore), `Article` per chapter, `Organization` for Million Dollar Coach. Add OG/Twitter tags and `<html lang="en-AU">`.
4. Write alt text for all 31 images.

**Weeks 2–3: answer the questions LLMs get asked**
5. Add a one-sentence plain-language summary at the top of each chapter ("This riff explains why free webinars attract unqualified leads…"), plus a per-chapter description. Titles can stay quirky.
6. On milliondollarcoach.com, publish FAQ/answer pages for the prompts above ("What does a coach need to go from 6 to 7 figures?"), each with a direct answer in the first 2 sentences, then Taki's framework (Attract / Convert / Deliver).
7. Add a current "Programs" page so LLMs stop citing the stale Black Belt / Boardroom tiers.

**Weeks 3–8: build the off-site layer (this is where LLMs actually pull from)**
8. Reviews and testimonials on Google, Trustpilot, Goodreads and Amazon (the 2016 book has a Goodreads entry). Ask clients to name specific results.
9. Get on "best business coach for coaches", "best coaching mastermind", and "best books for coaches" lists; pitch the list owners found above (Life Coach Magazine, Quenza, smallbusinesscoach.org).
10. Podcast guesting with show notes that link to milliondollarcoach.com and use consistent wording: "Taki Moore, founder of Million Dollar Coach, author of *Million Dollar Coach* and *I Feel Sorry for the Normies*".
11. Disambiguate from Alan Weiss: use "Taki Moore's Million Dollar Coach" consistently, and add a Wikidata entry or Crunchbase/LinkedIn company page.

**Measure**
12. Re-run the 10 prompts above plus 20 more monthly in ChatGPT, Perplexity, Gemini and Claude. Log: mentioned / cited / position / accuracy.

## Open questions
- Is the live book URL `milliondollarcoach.com/book/`? That is the only URL in the repo.
- Is the goal to rank the book, the Million Dollar Coach brand, or both? The plan above treats the book as a content engine feeding the brand.
- Who controls milliondollarcoach.com? Several fixes there (FAQ pages, programs page) are outside this repo.

---

# Addendum: Instagram and YouTube (@takimoore)

Owner confirmed milliondollarcoach.com is theirs, so the audit above stands. Data from Sandcastles and web search, 2026-10-09.

## Instagram @takimoore
- **137,402 followers, 24.1M total views.** Last 25 posts (11 Aug to 15 Sep 2026): avg 84k views, avg engagement 1.8%, avg outlier score 1.26 (roughly in line with the account's own average).
- **What works:** the "Unselling" / "Operation Binge" series. Top posts: "Make it safer to say no" (494k), "X-ray vision / ready now vs not now" (294k), "worst VSL ever" (228k), "Your market isn't harder to sell to, they're harder to bullshit" (209k). Contrarian hooks dominate.
- **What doesn't:** podcast-guest clips (the $100 MBA Show, 6k to 23k views), usually sub-0.5 outlier.
- **Proof points are locked in reels** and not on any crawlable page: Rodric $64k to $1.75M via Invite-Only (73 applied, chose 4); 236 attended a Zoom open house and 10 bought a $30k program; 15 of 199 paid $5,000 to apply after the "worst VSL ever".
- **CTAs end in DMs** ("Comment BUY / BINGE / TAKI"), with no web destination. Nothing from these posts gives an LLM a URL to cite.

## YouTube @takimoore
- Sandcastles indexes the Shorts channel only: 26.9k subscribers, 0 Shorts in the last 120 days. A third-party aggregator lists 17.6k subs / 782 videos, so the numbers conflict and I could not verify the long-form channel.
- Channel description is strong and AI-readable: "For business coaches who want a Lifestyle Empire™ ... leads every day, sales every week, and clients who stay for years." This matches the Normies structure (Demand / Buying / Clients).
- A third-party analytics site says the channel's long-form frameworks (One-Page plan, MicroMagnets) aren't being cut into Shorts.
- Gap: I could not check titles, descriptions, chapters or transcripts of long-form videos. Needs a manual pass in YouTube Studio.

## Is your named IP findable? (web search proxy)
| Term | Result |
|---|---|
| Unselling™ | Not found. Returns *The Unsellables* (TV) and Pierre Taki. |
| Invite-Only™ campaign | Not found as your method. A different seller's "no sales calls" podcast surfaced. |
| Lifestyle Empire™ | Not found. Returns spam "net worth" pages. |
| Clients 3.0 Workshop | Found only on **udcourse.com**, a third-party course-resale site. Check whether that is authorised. |
| Operation Binge | Not checked |

Your reels are generating original frameworks and none of them resolve to a page. That is the biggest social-to-AI gap.

## Social actions (add to the plan above)
1. **One canonical page per named method** on milliondollarcoach.com (`/unselling`, `/invite-only`, `/lifestyle-empire`, `/operation-binge`): a definition in the first two sentences, who it's for, steps, and 1 to 2 named case studies (Rodric, the $30k open house). Use the ™ term and a plain-English synonym.
2. **Point reel CTAs at those pages**, not only DMs. Put the URL in the caption and the bio link.
3. **Publish transcripts** of top reels and YouTube videos on the site. Posts that are text-only on Instagram are invisible to most LLM retrieval.
4. **YouTube:** put the canonical URL and the method name in the first line of every description, add chapters, and title long-form videos with the question buyers ask ("How do I sell high-ticket coaching without sales calls?").
5. **Podcast clips:** link the full episode page on milliondollarcoach.com and use consistent bio wording: "Taki Moore, founder of Million Dollar Coach, author of *I Feel Sorry for the Normies*".
6. **Check udcourse.com** and request removal if it is unauthorised, since it currently out-ranks your own site for "Clients 3.0".
