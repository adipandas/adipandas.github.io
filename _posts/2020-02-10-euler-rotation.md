---
title: 'Rotation using Euler Angles'
date: 2020-02-10
permalink: /posts/2020/02/euler-rotation/
tags:
  - Rotation
  - Euler Angles
  - Rotation Matrix
---

I have always found rotation using euler angles confusing. The following is just a simple note to maintain my sanity while performing rigid body transformations using rotational matrices.

# Rotation

Rotational matrices are special orthogonal matrices. I am not going to discuss any property of these matrices over here. But this post is just a snippet for quick reference. For further details, you can refer [this](https://en.wikipedia.org/wiki/Rotation_matrix).

## Euler Angle Transformation
The most important thing you must remember before reading further about transformations using euler angles is:  
**The order of matrix multiplication of rotational matrices is of extreme importance.**

i. Euler angles are used to specify the orientation of one reference frame relative to another reference frame.  
ii. Euler angles are specified by the **three angles**, viz., **$$\psi$$, $$\theta$$, $$\phi$$**.  
iii. Euler angles represent three consecutive rotations in the order of **$$\psi$$, $$\theta$$, $$\phi$$** so that one coordinate axes system is made to coincide with another system.  



