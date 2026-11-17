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

No fabricated headshots or lab photographs are used. The PI portrait is the official UTA faculty image linked from the UTA Quantum Initiative and Electrical Engineering directory. Its public CDN URL is stored in _data/people.yml. Screenshots supplied by the PI verify Xiaofei Nie and Ji Xia joining in Fall 2026, and provide portraits for those two students and Luofei Liang. The screenshots also support Luofei's research focus in multimodality alignment and fusion. The PI explicitly approved public publication of the Xiaofei Nie, Ji Xia and Luofei Liang portraits on November 17, 2026. Their screenshot files are stored unchanged, with CSS display crops isolating each portrait. Faces and appearance have not been modified. Degree programs and email addresses for the two new members were not shown and are not inferred. Vikrampruthvira's portrait has not been supplied. See migration/people-photo-sources.json for source and prepared display-crop details. Research illustrations are editable SVGs, explicitly conceptual rather than measured plots.

## Hosting

This repository is configured for the GitHub project-site address:

`https://craigzhao.github.io/X-Grid-Lab.github.io/`

Enable GitHub Pages with **GitHub Actions** in the repository settings. The deployment workflow builds on updates to `master` or `main`, and validates pull requests and the implementation branch.

To retain `https://aireqlab.uta.edu/`, UTA must authorize the hosting/DNS arrangement. Options include deploying the static output to UTA-managed hosting or mapping the university subdomain to GitHub Pages after institutional approval. For a root custom domain, change `url` to `https://aireqlab.uta.edu`, `baseurl` to `''`, and adjust the workflow link-check flag accordingly. Add `CNAME` only after the domain has been approved and configured. No DNS or university-site changes have been made by this implementation.

## Update behavior

Routine changes are Markdown or YAML edits. The GitHub Actions workflow rebuilds and deploys commits to the default branch after Pages is enabled. No scheduled crawling or unattended import is configured. Users can make edits through GitHub or ask ChatGPT to apply updates.


## Activities and projects update, November 17, 2026

Six source-linked activity updates were added: selected IEEE task-force service, the July 20, 2026 trustworthy-AI panel, the July 30, 2025 quantum research/education panel, Grid Edge panel leadership in January 2025, summer 2024 Brookhaven school outreach, and the November 29, 2023 Resilience Week session. Conference programs establish event dates; IEEE Resource Center upload dates are not treated as event dates. Month/season-only events use display_date and date_value; the date field is only a sorting key for those entries. The service overview date is the date of this website update, not the start of an appointment.

Public IEEE sources verify the RL task-force secretary role and quantum task-force existence. The quantum co-chair role is based on the PI's own January 17, 2025 statement, with no invented appointment term or assertion that the standalone task force remains active. The 2024 PSOPE annual report describes a planned January 2025 merger into a broader working group. Proposed agentic-AI and operator-theory task forces were not represented as approved appointments.

Research now includes Genesis/GridFM, DOE advanced-transformer co-modeling, and integrated wind forecasting. The PI's supplied 2025-2026 annual research statement confirms funded 2025 wind and transformer projects and PI roles; the site uses UTA lead to distinguish consortium leadership. Internal amounts, submitted proposals, and the review document itself are not published. The partner award listing establishes funded wind-project activity but does not independently establish Zhao's role. The DOE transformer presentation supplies the October 2025-September 2027 project term. Earlier Brookhaven contributions are labeled separately and do not imply current UTA funding or project leadership.

Activity sources:
- https://ieee-pes.org/trending-tech/machine-learning-for-microgrids-resiliency-stability-control-and-operation/
- https://ieee-pes.org/wp-content/uploads/2025/07/Annual_Report_PSOPE_2024.pdf
- https://resourcecenter.ieee-pes.org/conferences/general-meeting/pes_cvs_gm26_080426_amps1_sld
- https://pes-gm.org/wp-content/uploads/2026/07/2026-IEEE-PES-GM-Print-Program.pdf
- https://resourcecenter.ieee-pes.org/conferences/general-meeting/pes_cvs_gm25_0727_peecpl06_sld
- https://pes-gm.org/wp-content/uploads/2025/07/7.17.25-Program-_-2025-IEEE-PES-GM-.pdf
- https://resourcecenter.ieee.org/conferences/grid-edge/pes_cvs_ge25_pl02_020325_sld
- https://pes-gridedge.org/ge-2025/
- https://www.bnl.gov/newsroom/news.php?a=221999
- https://inl.gov/content/uploads/2023/07/2023-Resilience-Week-Agenda.pdf

Additional research-project sources:
- https://www.wichita.edu/research/ResearchNewsletter/2025-06-Newsletter.php
- https://www.bnl.gov/isd/agm/index.php
- https://www.bnl.gov/isd/agm/deep-learning.php
- https://www.bnl.gov/isd/agm/wecc-clm.php
- https://doi.org/10.1038/s44172-026-00670-z
- https://www.bnl.gov/community/docs/cac/2023/2023-03-09-cac-climate-energy-presentation.pdf
- https://www.nysrc.org/wp-content/uploads/2023/06/BNL-Climate-Energy-Resilience-Kickoff-021723.pdf


## Google Scholar bibliography reconciliation, November 17, 2026

Profile: https://scholar.google.com/citations?user=dCbhGekAAAAJ&hl=en . The complete profile page returned 74 records. The source website had 44 publication records. This update adds 31 missing scholarly outputs and retains the two independently verified existing publications not listed on Scholar (the coordinated T&D state-estimation conference paper and the Frontiers editorial), producing 75 records. The BNL repository version of the NAPS dynamic-line-rating conference paper is represented by the existing conference record rather than duplicated.

The 31 additions comprise 8 journal items (including a corrigendum), 14 conference papers, 4 preprints, 3 conference presentations/abstracts, 1 technical report, and 1 doctoral thesis. Distinct conference papers on transmission switching, stochastic UC with BESS, and RL battery bidding remain separate from the related journal articles. No citation-count or h-index snapshot is displayed.

Google Scholar supplies discovery and profile-record links. Author-verified Crossref records (publisher-deposited metadata), publisher pages, arXiv, AMS programs, the University of Manchester thesis, and the BNL report establish citation details. Source records and comparison snapshots are preserved in the excluded migration directory. Journal years follow verified final issues rather than old online-first years where applicable. IEEE's placeholder pages 1-1 are omitted. The two-stage quantum switching paper now uses 2026, volume 41(3), pages 2174-2186; the quantum Volt-VAR paper uses volume 12, pages 833-844. Existing publication paths and research-link IDs are preserved.

The operator-learning preprint explicitly links arXiv:2301.12538v1, the 2023 original version coauthored by Tianqiao Zhao. The revised 2026 version has a different author list and is not attributed to him. Preprints, presentations, reports, and the thesis use separate types and source links; they are not presented as journal or conference papers. The unrelated poultry/probiotic paper remains excluded.

Additional primary sources:
- https://api.crossref.org/works?query.author=Tianqiao%20Zhao&rows=100
- https://api.crossref.org/works/10.1109/TPWRS.2025.3645024
- https://api.crossref.org/works/10.1109/OAJPE.2025.3634993
- https://api.crossref.org/works/10.1109/RWS58133.2023.10284644
- https://arxiv.org/abs/2611.08929
- https://arxiv.org/abs/2610.19565
- https://arxiv.org/abs/2607.24539
- https://arxiv.org/abs/2301.12538v1
- https://ams.confex.com/ams/104ANNUAL/webprogram/Paper440020.html
- https://ams.confex.com/ams/106ANNUAL/meetingapp.cgi/Person/316557
- https://www.bnl.gov/isd/docs/ess-final-report-jul-31-2021.pdf
- https://pure.manchester.ac.uk/ws/portalfiles/portal/87764694/FULL_TEXT.PDF
