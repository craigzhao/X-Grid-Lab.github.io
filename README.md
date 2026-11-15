# AIRE-Q Lab

The website for **AI & Quantum for Resilient Energy**, led by Prof. Tianqiao Zhao at The University of Texas at Arlington.

This site customizes the open-source [Academic Pages](https://github.com/academicpages/academicpages.github.io) template already present in this repository. It retains Jekyll, Markdown collections, YAML data, and the original MIT license. The AIRE-Q layouts and styles are isolated in `_layouts/lab*`, `_includes/lab`, `assets/css/lab.css`, and `assets/lab.js`.

## What is included

- Home, research, people, publications, teaching, news, opportunities, and contact pages.
- 44 imported publications (34 journal articles and 10 conference papers), with search, year/type filters, citation copying, and individual publication pages.
- Faculty and student profiles sourced from the original lab website. Add local photographs through `_data/people.yml` when available.
- A verified September 28, 2026 Genesis Mission announcement.
- Responsive navigation, keyboard access, reduced-motion support, metadata, a sitemap, and redirects for the original members/openings paths.
- Automatic Jekyll build and internal-link verification in GitHub Actions.

## Publish on GitHub Pages

1. Merge the AIRE-Q implementation branch into `master`.
2. In **Settings → Pages → Build and deployment → Source**, select **GitHub Actions**.
3. Run **Actions → Build and publish AIRE-Q Lab → Run workflow** if the merge workflow completed before Pages was enabled.
4. The default address for this repository is `https://craigzhao.github.io/X-Grid-Lab.github.io/`.

The repository name ends in `.github.io`, but because it is not `craigzhao.github.io`, GitHub treats it as a project site. The configured `baseurl` accounts for that.

For the existing university address, coordinate hosting/DNS with UTA. Do not add a `CNAME` or change DNS until UTA approves the hosting arrangement. See `MIGRATION_NOTES.md`.

## Make updates

You can edit files using GitHub's pencil button and commit through the website. No local software is required for routine content updates. Each commit to `master` triggers a rebuild and deployment after GitHub Pages is enabled.

| Update | Edit or add |
|---|---|
| Lab description and contact | `_data/lab.yml` |
| PI, students, alumni, photographs | `_data/people.yml` |
| Research areas | `_data/research.yml` |
| Publications | One Markdown file per paper in `_publications/` |
| News | One Markdown file per update in `_news/` |
| Courses | One Markdown file per course in `_teaching/` |
| Menu | `_data/navigation.yml` |

See **[UPDATE_GUIDE.md](UPDATE_GUIDE.md)** for copy-and-paste examples. You can also give ChatGPT a new publication, member, or announcement and ask it to update this repository. No unattended news scraping or automatic publication import is configured.

## Local development

Install Ruby 3.3 and Bundler, then run:

```sh
bundle install
bundle exec jekyll serve --baseurl ''
```

Visit `http://localhost:4000/`. The authoritative production build is:

```sh
JEKYLL_ENV=production bundle exec jekyll build --destination dist
python scripts/check_site.py dist --baseurl /X-Grid-Lab.github.io
```

If Ruby is unavailable, `python scripts/preview.py` builds a local approximation using the same authored templates and content (requires PyYAML and Jinja2). It supports only the Liquid features used by this lab; GitHub CI remains the authoritative Jekyll build.

## Provenance and content review

Migrated content is documented in `MIGRATION_NOTES.md`. Publication years are preserved. January 1 in a publication's `date` field is a sorting key when only the year was supplied; it does not assert the paper's publication day. No unpublished proposals or private project budgets are included. The unrelated microbiology citation from the old website is preserved in `migration/excluded-for-review.txt` for PI review and is not displayed.

## License

The underlying Academic Pages / Minimal Mistakes template is MIT licensed, copyright 2016 Michael Rose. See `LICENSE`. Academic content and personal photographs retain their respective owners' rights.
