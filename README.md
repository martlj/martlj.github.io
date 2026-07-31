# Personal Website Template

A ready-to-use GitHub Pages template for a personal academic website — no
coding experience required. Everything is edited directly in your browser.

The site has three pages:

- **Bio** — your photo, a short bio, your institute, and links (email,
  socials, etc.)
- **Scientific Outputs** — your 5 most-cited publications, fetched
  automatically from an ORCID profile you provide (citation counts via
  Semantic Scholar), with a link to your full publication list
- **Outside of Work** — a free-form page for anything outside your
  research

## Get started

Click **"Use this template"** above to create your own copy, then follow
[**SETUP.md**](SETUP.md) for a full step-by-step walkthrough (about 10
minutes, no terminal needed).

## How it's built

- [Jekyll](https://jekyllrb.com/) + the [`minima`](https://github.com/jekyll/minima)
  theme, built natively by GitHub Pages — no custom build step required
  for the site itself.
- All personal details live in one file, [`_config.yml`](_config.yml).
- A scheduled [GitHub Action](.github/workflows/update-publications.yml)
  reads your publications from [ORCID](https://orcid.org) and looks up
  citation counts via [Semantic Scholar](https://www.semanticscholar.org/),
  writing the top 5 into [`_data/publications.yml`](_data/publications.yml).
  See SETUP.md for the (rare) cases this can't fully resolve, and how to
  edit the list by hand instead.
