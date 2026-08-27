# PACT — Website

Static, RTL, Arabic-first website for PACT (Legal Advisory | Due Diligence),
built to the official brand identity (navy monochrome · Cinzel/Readex Pro · Inter/Plex Arabic).

## Structure
- `index.html`, `legal-studies.html`, `corporate-contracts.html`, `how-we-work.html`,
  `about.html`, `insights.html`, `contact.html` — page sources (fragments linking `assets/`).
- `assets/pact.css`, `assets/pact.js` — shared design system + interactions.
- `build.py` — generator. Assembles every page from shared partials (one header/footer),
  writes the source pages, and emits standalone copies to `dist/`.
- `dist/` — self-contained, deployable HTML documents (CSS + JS inlined, full RTL `<html>`).

## Build
```bash
cd website && python3 build.py
```
Edit content/partials in `build.py` and styles in `assets/pact.css`; never hand-edit
generated pages — re-run the build.

## Deploy
Serve the repo root of `website/` (source, needs the `assets/` folder alongside),
or drop the contents of `dist/` onto any static host — each file there stands alone.

## Pending (client to confirm)
- Contact email, phone, LinkedIn URL, response hours.
- Legal pages: Privacy Policy, Terms, Professional Disclaimer (need legal review before publish).
- Original logo SVG (currently reconstructed faithfully in code).
- Contact form backend endpoint (front-end validation is wired; no server yet).
