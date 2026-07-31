# Setup guide

This guide assumes no coding experience. Every step below can be done in
your web browser — you do not need to install anything or use a terminal.

It should take about 10 minutes.

## 1. Create your own copy of this repository

1. At the top of this repository's page on GitHub, click the green
   **"Use this template"** button, then **"Create a new repository"**.
2. Choose an owner (your GitHub account) and a name for your new
   repository. If you want your site at `https://yourusername.github.io`
   (no extra path), name the repository exactly `yourusername.github.io`.
   Any other name works too — your site will just live at
   `https://yourusername.github.io/repository-name/`.
3. Click **"Create repository"**.

## 2. Turn on GitHub Pages

1. In your new repository, click **Settings** (top menu).
2. In the left sidebar, click **Pages**.
3. Under "Build and deployment" → "Source", choose **"Deploy from a
   branch"**.
4. Under "Branch", choose **main** and folder **/(root)**, then click
   **Save**.
5. Wait a minute or two, then refresh this page — a box will appear at
   the top saying "Your site is live at ...". That's your website's
   address. Bookmark it.

## 3. Personalize your site

1. In your repository's file list, click **`_config.yml`**.
2. Click the pencil icon (✏️) in the top right to edit it.
3. Fill in your details:
   - `title`: your name
   - `bio`: a couple of sentences about yourself
   - `institute`: your institution's name and website
   - `links`: your email, GitHub, social media, etc. (add or delete
     entries as needed)
   - `orcid.id`: your ORCID iD (see step 5 below for how to find it)
4. Scroll down and click **"Commit changes..."**, then **"Commit
   changes"** again in the popup.
5. Your site will automatically rebuild — check back in a minute or two.

**Formatting tip:** this file uses YAML, where spacing matters. Keep the
same indentation as the existing lines, and if a value contains a colon
(`:`), wrap it in quotes, e.g. `"9:00 seminar"`.

## 4. Add your photo

1. Go into the `assets/images/` folder in your repository.
2. Click **"Add file"** → **"Upload files"**, and upload your photo
   (e.g. `profile.jpg`).
3. Go back to `_config.yml`, edit it again, and change the `photo:` line
   to point to your uploaded file, e.g.:
   ```yaml
   photo: "/assets/images/profile.jpg"
   ```
4. Commit the change.

## 5. Set up the Scientific Outputs page

This page uses your **ORCID iD** — a free, standard researcher identifier
(if you don't already have one, sign up at
[orcid.org/register](https://orcid.org/register), and add your
publications to it if you haven't already).

1. Go to [orcid.org](https://orcid.org), log in, and copy your ORCID iD
   from your profile — it looks like `0000-0002-1825-0097` (the full
   profile URL works too).
2. Paste it into `orcid.id` in `_config.yml` (see step 3 above).
3. A GitHub Action automatically checks your ORCID profile every
   **Monday**, looks up citation counts for each publication via
   [Semantic Scholar](https://www.semanticscholar.org/), and updates the
   "Scientific Outputs" page with your 5 most-cited publications.
4. To update it immediately instead of waiting: click the **Actions**
   tab → **"Update Publications from ORCID + Semantic Scholar"** (left
   sidebar) → **"Run workflow"** button → **"Run workflow"**.

**A note on reliability:** ORCID and Semantic Scholar are both official,
public APIs designed for this kind of automated use, so this is much more
reliable than scraping a page. There are two situations where it still
won't produce a full list:
- A publication has no DOI, PMID, or arXiv ID recorded on ORCID — there's
  no way to look up a citation count for it, so it's left out of the
  ranking.
- Semantic Scholar occasionally rate-limits automated requests; if a run
  fails for this reason, your existing list is left untouched and you can
  just try **"Run workflow"** again a little later.

Either way, nothing breaks — you can always edit `_data/publications.yml`
directly and type in publications by hand, following the same format as
the placeholder entry already there.

## 6. Edit the "Outside of Work" page

1. Click **`outside-of-work.md`** in your repository.
2. Click the pencil icon to edit it, replace the placeholder text with
   whatever you'd like to share, and commit your changes.

## Troubleshooting

- **My site isn't showing my changes.** Click the **Actions** tab — if
  the most recent run has a red ✗, click into it to see what went wrong
  (this is usually a formatting mistake in `_config.yml`, like a missing
  quote or wrong indentation).
- **Settings → Pages doesn't show a link yet.** Make sure you selected
  branch `main` and folder `/(root)`, then wait a minute and refresh.
- **The page looks broken / unstyled.** Double check `_config.yml`
  wasn't accidentally saved with broken YAML — compare your edits
  against the original structure.
