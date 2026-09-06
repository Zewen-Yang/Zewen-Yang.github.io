---
layout: page
title: Humanoid-Operated Production at Hannover Messe 2026
description: Two Agile ONE humanoids working side by side in a live production demo, combining classical 3D vision with diffusion policies. Visited by German Chancellor Friedrich Merz.
img: assets/img/hm26_merz_agile_robots_booth.jpg
importance: 1
category: Work
related_publications: false
---

At [Hannover Messe 2026](https://www.hannovermesse.de/) (Hanover, April 20–24), [Agile Robots](https://www.agile-robots.com/en/) showed a **humanoid-operated production demo** on the **Agile ONE** platform. Two humanoids shared one workcell and ran live for the whole week at the booth in Hall 27, Stand J72. On the opening day, German Chancellor **Friedrich Merz** and Federal Minister for Economic Affairs **Katherina Reiche** visited the booth and watched the demo up close ([press release](https://www.agile-robots.com/en/news/detail/humanoid-agile-one-embodies-physical-ai-at-hannover-messe-2026/)).

<div class="row mt-3 justify-content-sm-center align-items-center">
    <div class="col-sm-8 mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/hm26_merz_agile_robots_booth.jpg" title="Chancellor Friedrich Merz at the Agile Robots booth" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm-4 mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/hm26_merz_handshake.jpg" title="Chancellor Friedrich Merz greeting the team" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    German Chancellor Friedrich Merz and Federal Minister Katherina Reiche at the Agile Robots booth, with Agile ONE in the background (left), and greeting the team in front of the production demo (right).
</div>

## Two humanoids, one production line

The demo puts two Agile ONE humanoids side by side in a shared assembly workcell. Both robots handle parts and hand over work in a common workspace, so the core challenge was making the interaction smooth: perceive the scene, coordinate the two arms and two bodies, and never collide. To get there, the team combined a wide range of methods, from classical 3D vision to learned policies:

- 👁️ **Classical 3D vision** for perceiving and localizing parts and the other robot in the workcell
- 🧠 **Diffusion policies** for the contact-rich manipulation skills that are hard to script by hand
- 🤝 **Coordination between the two humanoids** so they can work in the same space without colliding

A fun detail: the two robots ran **completely different software stacks**. One Agile ONE was built on **ROS 2**, the other on **AgileCore**, our internal software platform. Both worked reliably throughout the fair.

## My contribution: the diffusion policy pipeline

I owned the **diffusion policy** part of the demo end to end:

- **Data collection** — teleoperated demonstrations of the manipulation skills on the real Agile ONE
- **Data cleaning** — filtering, segmenting and curating the demonstrations into a training-ready dataset
- **Model training** — training and iterating on the diffusion policy for the target skills
- **Deployment & testing** — running the policy on the robot in real time and validating it on hardware
- **Pipeline integration** — integrating the learned policy with the perception and coordination modules and testing the complete production flow

<div class="row mt-3 justify-content-sm-center">
    <div class="col-sm-10 mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/hm26_team_photo.jpg" title="The Agile ONE team at Hannover Messe 2026" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    The team in front of the Agile ONE production demo at Hannover Messe 2026.
</div>

This demo was built together with Nehil Danis, Olga Aleksandrova, Chang Qin, Chunyu Hu, Evgenii Neruchek, Stefan Profanter, Ana Elvira Huezo Martin, Ben Fradin, Sen Wang, Christoph Jähne-Schon, and many other colleagues at Agile Robots.
