---
title: 'Important Notes'
date: 2020-01-01
permalink: /posts/2020/01/important-notes/
tags:
  - Quaternions
---

These are some of the important notes which I make for reference.

Quaternions
======

Let there be two coordinate frames: Frames $$A$$ and $$B$$.  
There is a vector $$r^{A}$$ defined in Frame $$A$$.   

Rotate $$A$$ to $$B$$ by rotation of angle $$\theta$$ around vector $$r^{A}$$.

Quaternion describing this orientation is $$q^{A}_{B}$$

$$q^{A}_{B} = [q_1, q_2, q_3, q_4] = [cos(\frac{\theta}{2}), -r^{A}_{x} sin(\frac{\theta}{2}), -r^{A}_{y} sin(\frac{\theta}{2}), -r^{A}_{z} sin(\frac{\theta}{2})]$$


References
------
