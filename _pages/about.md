---
permalink: /
title: "Aditya M. Deshpande"
excerpt: "Scientist, R&D at Procter & Gamble"
author_profile: true
redirect_from:
  - /about/
  - /about.html
---

I'm a scientist and R&D leader at Procter & Gamble, working on AI and embedded systems for consumer products — robotics-inspired grooming systems and sensor-driven devices.

Most of the work is about making things run under real constraints: a model on a microcontroller, within a cost target, for people who will use the product however they want to. Day to day that means some mix of technical strategy, evaluating architectures, sensor integration, firmware, and getting vision models to hold up on edge hardware.

Before this I did a PhD in Mechanical Engineering at the [University of Cincinnati](https://www.uc.edu/) with Profs. [Manish Kumar](https://researchdirectory.uc.edu/p/kumarmu) and [Ali A. Minai](https://eecs.ceas.uc.edu/~aminai/), on embodied intelligence — how a robot's morphology and physics shape what it can learn. In practice: central pattern generators for locomotion, developmental curricula for training, and swarms that coordinate through local rules.

**Work in:** edge computer vision · embedded firmware (C/C++, FreeRTOS) · control systems and robotics · sensor integration · product architecture

Curriculum Vitae: [PDF](https://adipandas.github.io/files/aditya-cv-web.pdf) &nbsp;·&nbsp; Email: deshpaad [at] mail [dot] uc [dot] edu

<!-- <div style="width:200px; margin-left: 30px;">
  <script type="text/javascript" id="clstr_globe" src="//clustrmaps.com/globe.js?d=RomffCBzeTvdhyrehWJhIAqA83-h6kNUj-rSlcO6ryE"></script>
</div> -->

## Research

Mostly from the PhD years.

**Robot learning and control**
* **DeepCPG Policies for Robot Locomotion** — central pattern generators combined with deep RL for legged locomotion.  
  [[arxiv](https://arxiv.org/abs/2302.13191)][[paper](https://doi.org/10.1109/TCDS.2023.3250393)][[Media](https://youtu.be/QHT_sm7OgWY)]
* **Robust deep reinforcement learning for quadcopter control** — policies that hold up under disturbances and model mismatch.  
  [[arxiv](https://arxiv.org/abs/2111.03915)][[paper](https://doi.org/10.1016/j.ifacol.2021.11.158)][[code](https://github.com/adipandas/gym_multirotor)]
* **Developmental RL for a quadcopter with thrust vectoring rotors** — training the task in stages rather than all at once.  
  [[arxiv](https://arxiv.org/abs/2007.07793)][[paper](https://asmedigitalcollection.asme.org/DSCC/proceedings/DSCC2020/84287/V002T36A011/1096589)][[code](https://github.com/adipandas/gym_multirotor)]

**Swarms and optimization**
* **Self-organized circle formation around an unknown target** — a multi-robot swarm surrounds a target using local communication only.  
  [[paper](https://ieeexplore.ieee.org/abstract/document/8431109)]
* **Area coverage inspired by ant foraging** — adaptive switching between Brownian motion and Lévy flight.  
  [[paper](https://proceedings.asmedigitalcollection.asme.org/proceeding.aspx?articleid=2663543)]
* **Constraint handling in the firefly algorithm**  
  [[paper](https://ieeexplore.ieee.org/document/6617447)]

**Computer vision**
* **One-shot recognition of manufacturing defects in steel surfaces** — identifying a defect type from a single labeled example.  
  [[website](https://adipandas.github.io/one-shot-steel-surfaces/)][[code](https://github.com/adipandas/one-shot-steel-surfaces)][[arxiv](https://arxiv.org/abs/2005.05815)][[paper](https://www.sciencedirect.com/science/article/pii/S2351978920315985?via%3Dihub)]
* **Computer vision toolkit for non-invasive monitoring of factory floor artifacts** — monitoring shop floor activity without instrumenting the equipment.  
  [[paper](https://www.sciencedirect.com/science/article/pii/S2351978920315936)]


## Teaching
* Spring 2019: MECH5132/MECH6032 — Robot Control Design, University of Cincinnati

## Projects

* **``pyneat``** — NeuroEvolution of Augmenting Topologies (NEAT). [[GitHub](https://github.com/adipandas/pyneat)]
* **``torch_shnet``** — stacked hourglass networks for human pose estimation, in PyTorch. [[GitHub](https://github.com/adipandas/torch_shnet)]
* **Multi-object trackers in Python** — a set of trackers that work with any detector. [[webpage](https://adipandas.github.io/multi-object-tracker/)]
* **``indoor_bot``** — a simple autonomous indoor robot. [[webpage](https://adipandas.github.io/indoor_bot/)]
* **Autonomous flying robot** [[webpage](https://adipandas.github.io/portfolio/flyingrobot/)]
