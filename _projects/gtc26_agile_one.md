---
layout: page
title: Agile ONE at NVIDIA GTC 2026
description: Autonomous human-robot interaction on the Agile ONE humanoid, showcased in the GTC 2026 exhibit hall and featured by NVIDIA Robotics.
img: assets/img/gtc26_agile_one_business_card.jpg
importance: 2
category: Work
related_publications: false
---

At [NVIDIA GTC 2026](https://blogs.nvidia.com/blog/gtc-2026-news/) (San Jose, March 16–19), [Agile Robots](https://www.agile-robots.com/en/) brought the **Agile ONE** humanoid to the exhibit hall, where it ran live for the whole show and was featured by [NVIDIA Robotics](https://www.linkedin.com/feed/update/urn:li:activity:7448837286852497408/).

## Autonomous human-robot interaction

Building on the Agile ONE platform, our team developed a fully autonomous human-robot interaction application running in the real world. A visitor hands the robot a business card, and Agile ONE:

- 👁️ **Perceives and localizes** the business card in an unstructured environment
- 🤖 **Plans and executes a dexterous grasp** to pick it up autonomously
- 🧠 Runs an **onboard agent** that reads the card, reasons over its content, and extracts the key information
- 💬 **Displays the person's name** on the robot's screen, creating a natural, personalized interaction moment

Our vision at Agile Robots is to bring truly intelligent humanoids into real industrial environments: robots that don't just follow fixed scripts, but perceive, reason, and act alongside humans in complex settings.

<div class="row mt-3 justify-content-sm-center align-items-center">
    <div class="col-sm-8 mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/gtc26_agile_one_business_card.jpg" title="A visitor handing a business card to Agile ONE" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm-4 mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/gtc26_jensen_agile_one.jpg" title="Jensen Huang signing Agile ONE" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Left: a visitor hands a business card to Agile ONE at the GTC 2026 exhibit hall (photo by <a href="https://www.linkedin.com/feed/update/urn:li:activity:7448837286852497408/">NVIDIA Robotics</a>).
    Right: NVIDIA CEO Jensen Huang signing our Agile ONE at the booth.
</div>

This demo was built together with Lei Zhang, Shuang Li, Jiaxin Hu, Jun Wang, and Aarushee N.

## Dexterous pick-and-place

Alongside the interaction demo, our colleagues at Agile Robots showed Agile ONE's dexterity in picking and placing everyday items. The robots are trained in simulation with NVIDIA Isaac Sim and Isaac Lab before being deployed on the real system. The demo was highlighted in NVIDIA's official GTC 2026 recap:

> In the exhibit hall, Agile Robots' Agile ONE humanoid demonstrated its dexterity in picking and placing items. The company uses Isaac Sim and Isaac Lab to train its robots in simulation.
>
> — [NVIDIA Blog, GTC 2026 News](https://blogs.nvidia.com/blog/gtc-2026-news/)

<div class="row mt-3 justify-content-sm-center">
    <div class="col-sm-10 mt-3 mt-md-0">
        {% include video.liquid path="assets/video/agile-one-gtc26.mp4" class="img-fluid rounded z-depth-1" controls=true autoplay=true muted=true loop=true %}
    </div>
</div>
<div class="caption">
    Agile ONE picking and placing items on the GTC 2026 show floor (video courtesy of <a href="https://blogs.nvidia.com/blog/gtc-2026-news/">NVIDIA</a>).
</div>
