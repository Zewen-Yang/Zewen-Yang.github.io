---
layout: page
permalink: /publications/
title: Publications
nav: true
nav_order: 1
_styles: |
  .pub-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    margin: 0 0 1.25rem;
  }
  .pub-actions a.pub-action {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.45rem 1rem;
    border: 1px solid var(--global-theme-color);
    border-radius: 6px;
    color: var(--global-theme-color);
    font-weight: 600;
    text-decoration: none;
    transition: background-color 0.15s ease, color 0.15s ease;
  }
  .pub-actions a.pub-action:hover,
  .pub-actions a.pub-action:focus-visible {
    background-color: var(--global-theme-color);
    color: var(--global-bg-color);
  }
  .post-header .post-description {
    display: none;
  }
  p.pub-intro {
    font-size: 0.875rem;
    margin: -0.5rem 0 2rem;
  }
  #english-papers,
  #chinese-journal-papers {
    scroll-margin-top: 5rem;
  }
  h2.pub-section {
    margin-top: 3.5rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid var(--global-divider-color);
  }
  p.pub-section-note {
    color: var(--global-text-color);
    opacity: 0.75;
    font-size: 0.9rem;
  }
---

<!-- _pages/publications.md -->

<!-- These links scroll with JS instead of #anchors: bibsearch.js treats the URL hash as a filter query. -->
<p class="pub-intro">{% bibliography_count %} <a href="#" onclick="document.getElementById('english-papers').scrollIntoView({ behavior: 'smooth' }); return false;">English</a> and {% bibliography_count --file chinese %} <a href="#" onclick="document.getElementById('chinese-journal-papers').scrollIntoView({ behavior: 'smooth' }); return false;">Chinese</a> papers, in reversed chronological order.</p>

<div class="pub-actions">
  <a class="pub-action" href="https://zewen-yang.github.io/PubGallery/" target="_blank" rel="noopener">
    <i class="fa-solid fa-book-open" aria-hidden="true"></i> Explore the 3D Publication Gallery <i class="fa-solid fa-arrow-right" aria-hidden="true"></i>
  </a>
</div>

<!-- Bibsearch Feature -->

{% include bib_search.liquid %}

<div class="publications" id="english-papers">

{% bibliography %}

</div>

<h2 class="pub-section" id="chinese-journal-papers">Chinese Journal Papers</h2>
<p class="pub-section-note">Papers published in Chinese-language journals; the original Chinese title is given under each entry. <sup>†</sup> corresponding author.</p>

<div class="publications">

{% bibliography --file chinese %}

</div>
