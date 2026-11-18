---
layout: page
permalink: /patents/
title: Patents
nav: true
nav_order: 2
_styles: |
  .post-header .post-description {
    display: none;
  }
  p.pub-intro {
    font-size: 0.875rem;
    margin: -0.5rem 0 2rem;
  }
---

<!-- _pages/patents.md -->

<p class="pub-intro">{% bibliography_count --file patents %} Chinese invention and utility model patents, in reversed chronological order.</p>

<div class="publications">

{% bibliography --file patents %}

</div>
