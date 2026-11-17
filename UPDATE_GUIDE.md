# Updating the AIRE-Q website

You can make routine updates entirely on GitHub. Open the appropriate file, click the pencil icon, edit, and choose **Commit changes**. A change on `master` automatically rebuilds the website once GitHub Pages is enabled. For a larger change, use a branch and pull request so you can review the build before merging.

## Add a news announcement

Open `_news/`, choose **Add file → Create new file**, and use a filename such as `2026-12-01-new-paper.md`. Paste:

```yaml
---
title: "A short, factual announcement title"
date: 2026-12-01
category: Publication
description: "One sentence explaining the update."
---
```

Below the second `---`, write the announcement using ordinary text or Markdown. Add a source link if appropriate. Commit the file. News automatically appears newest first, and the latest three entries appear on the homepage. The example above is only a template; it is not a published announcement.

For an activity known only by month or season, keep `date` as a sorting key and add `display_date: January 2025` with `date_value: '2025-01'`, or `display_date: Summer 2024` with `date_value: '2024'`. All news views use these fields so an unknown day is never displayed as an event date. Use the actual conference program date rather than a recording or slides upload date. A service overview may use its publication date without implying an appointment date.

## Add a publication

Create `_publications/2026-short-paper-name.md`:

```yaml
---
title: "Exact paper title"
pub_id: short-paper-name
date: 2026-01-01
year: 2026
category: Journal
authors: "Author, A., Zhao, T., & Author, B."
venue: "Exact journal name"
doi: "10.xxxx/replace-with-real-doi"
source_url: "https://publisher.example/replace-with-real-record"
source_label: "Publisher"
scholar_url: "https://scholar.google.com/citations?view_op=view_citation&user=dCbhGekAAAAJ&citation_for_view=replace-with-real-record-id"
citation: "Full citation with authors, year, title, venue, and DOI."
tags: [Power systems, Trustworthy AI]
featured: false
---
```

Use `Conference` for a conference paper. The supported categories are `Journal`, `Conference`, `Preprint`, `Presentation`, `Thesis`, and `Report`. Use `Presentation` for a conference abstract or talk that is not a conference paper. Keep the published version and any preprint clearly distinguished when reviewing duplicates; the category alone does not establish a manuscript's review or acceptance status.

Every category requires a real DOI or a valid public `source_url`, for example the publisher record, arXiv record, conference abstract, institutional thesis record, or report page. Omit `doi` when no verified DOI is available. Use `source_label` such as `Publisher`, `arXiv`, `Conference abstract`, `Thesis`, or `Report`. The website links to the DOI when present and otherwise to this source. `source_url` remains optional when a DOI is supplied. Add `scholar_url` only when you have the actual Google Scholar citation record. All categories require the full `citation`; items without a DOI should cite their source URL instead. The profile link on the publications page is separate from individual citation records.

Add `volume`, `issue`, and `pages` if known. For an article identifier or e-locator, use `article_number`; the website displays `Article N` instead of `pages` when this is present. Include the same verified volume, issue, and page range or article identifier in `citation`, which is the exact text copied by the citation button. Do not retain early-access placeholder pagination such as `1–1` after final metadata is available. Only include `paperurl` or `codeurl` when you have a real URL. Upload a shareable manuscript to `files/` and use `paperurl: /files/my-paper.pdf`. Respect publisher rights when uploading manuscripts. Replace every example URL in the template with a verified record, or omit optional fields that you do not have.

Set `featured: true` to make a paper eligible for the homepage; the three newest featured papers are shown. The `pub_id` must be unique and can also connect a paper to a research area in `_data/research.yml`. When only the year is known, `date: YEAR-01-01` is a sorting key, not a claim about the exact publication date.

## Add a member

Edit `_data/people.yml`. Under `students:`, add an entry with the same indentation as the others:

```yaml
  - name: "Student Name"
    role: Ph.D. Student
    joined: Fall 2027
    initials: SN
    email: student@mavs.uta.edu
    note: "Optional co-supervision or research note"
    photo: ''
```

To add a photo, upload it to `images/people/` and set `photo: /images/people/student-name.jpg`. A verified public HTTPS image URL also works. Use a portrait, ideally at least 600 pixels wide. The site crops the display without modifying the original. Empty `photo` fields display initials. New students appear automatically on both the homepage and People page. Move graduates into the `alumni` list when appropriate.

Screenshot-sourced portraits use `photo_crop` display classes. When replacing one with a standalone portrait, remove its `photo_crop` line so it displays normally. Keep the student's original photo unchanged.

## Update research or courses

Edit `_data/research.yml` to revise the four research directions, topics, and related paper IDs. Edit `_data/programs.yml` for research projects and their source links. Use `group: current` for the featured collaborations and `group: previous` for earlier Brookhaven work. Each record includes a short title, exact project title, description, role, timeframe where known, and source link. Keep earlier institutional contributions separate from UTA awards and describe submitted proposals as proposals if they are ever published. To add a course, copy an existing file in `_teaching/`, edit the front matter and body, and choose its `order` value. Course terms are explicit so old offerings are not presented as current enrollment information.

## Check an update

1. Open **Actions → Build and publish AIRE-Q Lab**.
2. Check that the latest build has a green check. A red build means the update was not successfully published.
3. Open the website and refresh. For a pull request, the `aireq-lab-site` build artifact is available from the workflow run.
4. GitHub's file history and **Revert** allow you to undo changes.

## Ask ChatGPT to update it

For example: “Update the AIRE-Q website in `craigzhao/X-Grid-Lab.github.io`: add this accepted paper and feature it on the homepage,” followed by the full citation, DOI, and any permitted manuscript/code links. Or: “Add [name] as a Ph.D. student who joined in Fall 2027,” with their public profile details.

The site does not discover announcements by itself. Updates are made when you edit the content or explicitly request an update.
