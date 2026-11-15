(() => {
  'use strict';
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#main-navigation');
  if (toggle && nav) {
    const closeMenu = () => { toggle.setAttribute('aria-expanded', 'false'); nav.classList.remove('is-open'); };
    toggle.addEventListener('click', () => { const open = toggle.getAttribute('aria-expanded') !== 'true'; toggle.setAttribute('aria-expanded', String(open)); nav.classList.toggle('is-open', open); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && nav.classList.contains('is-open')) { closeMenu(); toggle.focus(); } });
    nav.addEventListener('click', e => { if (e.target.closest('a')) closeMenu(); });
    document.addEventListener('click', e => { if (!e.target.closest('.header-inner')) closeMenu(); });
    window.matchMedia('(min-width: 961px)').addEventListener('change', e => { if (e.matches) closeMenu(); });
  }
  const tools = document.querySelector('[data-publication-tools]');
  if (tools) {
    tools.hidden = false;
    const search = document.querySelector('#publication-search');
    const year = document.querySelector('#publication-year');
    const type = document.querySelector('#publication-type');
    const rows = [...document.querySelectorAll('[data-publication]')];
    const count = document.querySelector('#publication-count');
    const empty = document.querySelector('#no-results');
    const params = new URLSearchParams(location.search);
    search.value = params.get('q') || '';
    if ([...year.options].some(o => o.value === params.get('year'))) year.value = params.get('year');
    if ([...type.options].some(o => o.value === params.get('type'))) type.value = params.get('type');
    const filter = () => {
      const query = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
      let visible = 0;
      rows.forEach(row => {
        const text = row.dataset.search.toLocaleLowerCase();
        const match = query.every(term => text.includes(term)) && (!year.value || row.dataset.year === year.value) && (!type.value || row.dataset.type === type.value);
        row.hidden = !match;
        if (match) visible++;
      });
      count.textContent = `${visible} of ${rows.length} publications`;
      empty.hidden = visible !== 0;
      const next = new URL(location.href);
      [['q', search.value.trim()], ['year', year.value], ['type', type.value]].forEach(([key, value]) => value ? next.searchParams.set(key, value) : next.searchParams.delete(key));
      history.replaceState(null, '', next.pathname + next.search + next.hash);
    };
    search.addEventListener('input', filter); year.addEventListener('change', filter); type.addEventListener('change', filter);
    document.querySelector('#reset-filters').addEventListener('click', () => { search.value = ''; year.value = ''; type.value = ''; filter(); search.focus(); });
    filter();
  }
  document.querySelectorAll('[data-copy-previous]').forEach(button => {
    button.addEventListener('click', async () => {
      const citation = button.previousElementSibling;
      try { await navigator.clipboard.writeText(citation.textContent.trim()); button.textContent = 'Copied'; }
      catch { button.textContent = 'Select the citation to copy'; const selection = window.getSelection(); const range = document.createRange(); range.selectNodeContents(citation); selection.removeAllRanges(); selection.addRange(range); }
      setTimeout(() => { button.textContent = 'Copy citation'; }, 2400);
    });
  });
})();
