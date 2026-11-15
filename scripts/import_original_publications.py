"""One-time migration from the lab's published bibliography, retained for provenance."""
from pathlib import Path
import re
import html
import yaml

ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / 'migration/publications-source.txt').read_text(encoding='utf-8')
special = {
 '10.1109/tsg.2026.3660187': 'quantum-storage',
 '10.1109/tpwrs.2025.3645024': 'quantum-switching',
 '10.1109/oajpe.2025.3634993': 'quantum-volt-var',
 '10.1109/tsg.2024.3453649': 'llm-der-tripping',
 '10.1016/j.apenergy.2024.124753': 'task-oriented-forecasting',
 '10.1016/j.epsr.2024.110299': 'outage-augmentation',
 '10.1109/tpwrs.2022.3233735': 'adversarial-stability',
 '10.1109/tii.2023.3240939': 'koopman-control',
 '10.1016/j.ijepes.2022.108693': 'storage-planning',
 '10.1109/tpwrs.2022.3153328': 'structure-informed-graph',
 '10.1109/tpwrs.2021.3102857': 'neural-lyapunov',
}
venues = {
 '10.1109/tsg.': 'IEEE Transactions on Smart Grid',
 '10.1109/tpwrs.': 'IEEE Transactions on Power Systems',
 '10.1109/tii.': 'IEEE Transactions on Industrial Informatics',
 '10.1109/tie.': 'IEEE Transactions on Industrial Electronics',
 '10.1109/tste.': 'IEEE Transactions on Sustainable Energy',
 '10.1109/oajpe.': 'IEEE Open Access Journal of Power and Energy',
 '10.1109/access.': 'IEEE Access',
 '10.1016/j.apenergy.': 'Applied Energy',
 '10.1016/j.epsr.': 'Electric Power Systems Research',
 '10.1016/j.ijepes.': 'International Journal of Electrical Power & Energy Systems',
 '10.1016/j.segan.': 'Sustainable Energy, Grids and Networks',
 '10.1016/j.conengprac.': 'Control Engineering Practice',
 '10.1049/iet-rpg.': 'IET Renewable Power Generation',
 '10.3389/fenrg.': 'Frontiers in Energy Research',
}
conference_venues = {
 'smartgridcomm': 'IEEE International Conference on Communications, Control, and Computing Technologies for Smart Grids (SmartGridComm)',
 'qce': 'IEEE International Conference on Quantum Computing and Engineering (QCE)',
 'gridedge': 'IEEE PES Grid Edge Technologies Conference & Exposition',
 'naps': 'North American Power Symposium (NAPS)',
 'isgt-la': 'IEEE PES Innovative Smart Grid Technologies Latin America (ISGT-LA)',
 'pesgm': 'IEEE Power & Energy Society General Meeting',
 'isgt': 'IEEE Power & Energy Society Innovative Smart Grid Technologies Conference (ISGT)',
 'chicc': 'Chinese Control Conference (CCC)',
}
out = ROOT / '_publications'
out.mkdir(exist_ok=True)
records = []
category = 'Journal'
excluded = []
for line in text.splitlines():
 if 'Conference Proceeding' in line:
  category = 'Conference'
 line = html.unescape(line).replace('\xa0', ' ').strip()
 match = re.match(r'^\d+\.\s+(.+?)\((\d{4})\)\.\s*(.*?)https://doi\.org/(\S+)', line)
 if not match:
  continue
 authors, year, tail, doi = match.groups()
 doi = doi.rstrip('.,;').lower()
 if doi == '10.3934/microbiol.2025032':
  excluded.append(line)
  continue
 if any(p['doi'] == doi for p in records):
  continue
 title_match = re.match(r'(.+?)\.\s+', tail)
 title = title_match.group(1) if title_match else tail.strip().rstrip('.')
 venue = next((v for prefix,v in venues.items() if doi.startswith(prefix)), '')
 if category == 'Conference':
  suffix = doi.split('/')[-1]
  venue = next((v for key,v in conference_venues.items() if suffix.startswith(key)), venue)
 if not venue:
  raise ValueError(f'Unknown venue for {doi}')
 slug = special.get(doi) or re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:90].rstrip('-')
 tags = []
 lower = title.lower()
 for key,tag in [('quantum','Quantum computing'),('reinforcement','Reinforcement learning'),('forecast','Forecasting'),('storage','Energy storage'),('stability','Grid stability'),('microgrid','Microgrids'),('outage','Resilience'),('adversarial','Cybersecurity'),('language model','LLMs'),('lyapunov','Trustworthy AI'),('graph','Graph learning')]:
  if key in lower:
   tags.append(tag)
 citation = re.sub(r'^\d+\.\s*', '', line).strip()
 record = {'title':title, 'pub_id':slug, 'date':f'{year}-01-01', 'year':int(year), 'category':category, 'authors':authors.strip(), 'venue':venue, 'doi':doi, 'citation':citation, 'tags':tags, 'featured':slug in ['quantum-storage','llm-der-tripping','neural-lyapunov']}
 body = '---\n' + yaml.safe_dump(record, allow_unicode=True, sort_keys=False, width=110) + '---\n'
 (out / f'{year}-{slug}.md').write_text(body, encoding='utf-8')
 records.append(record)
assert len(records) == 44, f'Expected 44 imported publications, found {len(records)}'
(ROOT / 'migration/excluded-for-review.txt').write_text('Potential author-name collision: not displayed pending PI review.\n\n'+'\n'.join(excluded)+'\n', encoding='utf-8')
print(f"Imported {len(records)} publications: {sum(p['category']=='Journal' for p in records)} journal, {sum(p['category']=='Conference' for p in records)} conference. Flagged {len(excluded)} for review.")
