# Email archive & YouTube planner

`normies-email-archive-yt-planner.pdf` is all 49 emails from *I Feel Sorry for the Normies*. Each one is tagged with:

- an estimated send date (worked out from clues in the email and from dated screenshots, plus a confidence level)
- email format (story, case study, framework/plan, philosophy, update)
- topics
- the big idea, plus the proof and assets it contains
- a YouTube potential rating (1–5), a suggested video format, a working title and a cold-open hook

The PDF also includes a top-16 shortlist and suggested playlists.

To rebuild after editing `meta.py`:

```sh
python3 yt-planner/build.py          # writes yt-planner/normies-archive.html
chromium --headless --no-pdf-header-footer --allow-file-access-from-files \
  --print-to-pdf=yt-planner/normies-email-archive-yt-planner.pdf yt-planner/normies-archive.html
```
