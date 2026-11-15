# AIRE-Q migration notes

## Sources

- Existing site: https://aireqlab.uta.edu/
- Research: https://aireqlab.uta.edu/research/
- Members: https://aireqlab.uta.edu/cp_school_directory/members/
- Bibliography: https://aireqlab.uta.edu/publications/
- Teaching: https://aireqlab.uta.edu/teaching/
- Opportunities: https://aireqlab.uta.edu/openings/
- UTA faculty directory: https://www.uta.edu/academics/schools-colleges/engineering/academics/departments/electrical/faculty-directory
- Genesis announcement (2026-09-28): https://www.uta.edu/news/news-releases/2026/09/28/uta-lands-second-genisis-mission-research-project
- UTA Quantum Initiative and AIRE-Q testbed: https://www.uta.edu/academics/schools-colleges/engineering/quantum
- DOE advanced-transformer collaboration: https://www.energy.gov/documents/scalable-and-flexible-meng-yue
- Foundation: the existing Academic Pages template in `craigzhao/X-Grid-Lab.github.io`, initial commit `a5b4d17c58954bce09be72d9e17875a19ab5b4c8`.

Content was reviewed on November 15, 2026. Search-index copies of the original pages were available, while direct automated retrieval was intermittent. The original homepage and navigation were also inspected in the browser. Students and course terms reflect the information displayed on the original site and should be reviewed by the PI for subsequent changes.

## Bibliography decisions

The original list has 35 journal entries and 10 conference entries. 34 journal entries and all 10 conference entries are included here. “Effects of probiotics on gut microbiota in poultry,” DOI `10.3934/microbiol.2025032`, appears unrelated to the lab and could be an author-name collision. It is preserved in `migration/excluded-for-review.txt` and excluded from public pages pending PI review. This is a review flag, not a definitive authorship finding.

IEEE and other recognizable DOI families were used to normalize journal names where the old page omitted them. Existing citation strings are preserved with each entry. Imported front matter omits unverified exact issue/page metadata; original citation strings retain the supplied values, including early-access pagination. Review and update final pagination as needed.

Publication `date` values use January 1 for year-only source records. The public pages display only the year. No specific publication day is inferred.

## Content boundaries

Content combines the public sources above with research-direction context supplied by the PI. The expanded research descriptions cover neural stability certificates, agentic AI, grid foundation models, renewable forecasting, and data-center flexibility as areas of investigation. Research proposals, collaborator lists from private planning, unpublished results, internal budgets, grant applications, and student research interests not stated on the source pages are not published.

No fabricated headshots or lab photographs are used. The PI portrait is the official UTA faculty image linked from the UTA Quantum Initiative and Electrical Engineering directory. Its public CDN URL is stored in `_data/people.yml`; initials remain for students whose verified portraits have not been supplied. Additional student names and portraits are awaiting PI input because the original members page could not be retrieved and its indexed roster contained only the two imported students. Research illustrations are editable SVGs, explicitly conceptual rather than measured plots.

## Hosting

This repository is configured for the GitHub project-site address:

`https://craigzhao.github.io/X-Grid-Lab.github.io/`

Enable GitHub Pages with **GitHub Actions** in the repository settings. The deployment workflow builds on updates to `master` or `main`, and validates pull requests and the implementation branch.

To retain `https://aireqlab.uta.edu/`, UTA must authorize the hosting/DNS arrangement. Options include deploying the static output to UTA-managed hosting or mapping the university subdomain to GitHub Pages after institutional approval. For a root custom domain, change `url` to `https://aireqlab.uta.edu`, `baseurl` to `''`, and adjust the workflow link-check flag accordingly. Add `CNAME` only after the domain has been approved and configured. No DNS or university-site changes have been made by this implementation.

## Update behavior

Routine changes are Markdown or YAML edits. The GitHub Actions workflow rebuilds and deploys commits to the default branch after Pages is enabled. No scheduled crawling or unattended import is configured. Users can make edits through GitHub or ask ChatGPT to apply updates.
