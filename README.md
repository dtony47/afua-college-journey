# Afua's College Journey: progress tracker

A single-page tracker for Afua's September 2027 college applications.

| File | What it is |
|---|---|
| `data.json` | **The only file you edit.** Colleges, key dates, tasks and the activity log. |
| `template.html` | Page layout, styles and script (inline CSS/JS). Rarely needs changing. |
| `build.py` | Checks `data.json` and embeds it into `index.html`. |
| `index.html` | The finished, self-contained page. This is what gets published. |
| `make_initial_data.py` | One-off script that converted the family's ChatGPT board into `data.json` on 11 Oct 2026. Re-running it **overwrites** `data.json`, so don't. |

## Add an activity log entry

Open `data.json` and add an object to the `"activity"` list (anywhere; the page sorts newest first,
and entries on the same day keep the order they appear in the file, so put the newest at the top):

```json
{"date": "2026-10-12", "who": "Grok Bot", "text": "Registered Afua on apply.tmc.ac.uk (password chosen by Afua)."},
```

Dates are always `YYYY-MM-DD`.

## Change a status

* **College**: edit its entry in `"colleges"`. Useful fields are `stage`, `appStatus` (e.g. `Not started`,
  `Preparing application`, `Submitted`, `Interview booked`, `Offer`), `visited` (e.g. `"14 Nov 2026"`, or `""` if not visited yet),
  `deadline` / `deadlineTime`, `deadlineNote` and `next`.
* **Task**: set `status` to `To do`, `In progress` or `Done`. The other fields are `owner` (`Tony`, `Afua` or `Together`), `due` and `priority`.
* **Key date**: add or edit an entry in `"events"`, with `date`, `time`, `title`, `kind` (`Open day`, `Deadline`, ...) and `status`.
  Add `"tentative": true` to keep an unconfirmed date out of the "Next up" banner. It still shows on the timeline.

Chip colours come from the wording. Done, booked, confirmed and submitted show green; in progress, preparing and provisional show amber; overdue, not booked and decision needed show red.

## Rebuild

```bash
cd /workspace/college-tracker
python3 build.py        # validates data.json and writes index.html
```

The build **refuses to run** if `data.json` looks like it contains an email address, a UK mobile number or a postcode.
Never add Afua's email, phone, date of birth, address or grades to this page.

Preview (optional):

```bash
google-chrome --headless=new --no-sandbox --hide-scrollbars --window-size=1280,5300 \
  --screenshot=$PWD/preview.png file://$PWD/index.html
```

Countdowns are worked out in the viewer's browser from today's date, so the page doesn't need rebuilding every day.
Rebuild only when the data changes. After rebuilding, redeploy `index.html` to the host. The page carries a `noindex` tag,
but anyone with the URL can still read it.
