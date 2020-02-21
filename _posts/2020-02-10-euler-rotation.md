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


<ol type="i">
  <li>Euler angles are used to specify the orientation of one reference frame relative to another reference frame.</li>
  <li>Euler angles are specified by the <b>three angles</b>, viz., <strong>$\psi$, $\theta$, $\phi$</strong>.</li>
  <li>Euler angles represent three consecutive rotations in the order of $\psi$, $\theta$, $\phi$ so that one coordinate axes system is made to coincide with another system.</li>
  <li>Again, the <b><i>order of rotation</i></b>, i.e., $\psi$, $\theta$, $\phi$, is very very important.</li>
  <li>Angle <strong>$\psi$</strong> - Angle to be rotated about <i>current</i> frame's <b>Z-axis</b>.</li>
  <li>Angle <strong>$\theta$</strong> - Angle to be rotated about <i>current</i> frame's <b>Y-axis</b>.</li>
  <li>Angle <strong>$\phi$</strong> - Angle to be rotated about <i>current</i> frame's <b>X-axis</b>.</li>
</ol>


### Sequence of rotation of three euler angles:
Lets say one has to go from **frame 1** to **frame 2** using euler angle $$\psi$$, $$\theta$$, $$\phi$$. Lets start with current frame, i.e., **frame 1**.
<ol type="i">
  <li>Original Frame: $Ox_{1}y_{1}z_{1}$<li>
  <li>Target Frame: $Ox_{2}y_{2}z_{2}$<li>
  <li>Angle <strong>$\psi$</strong> is the rotation about <b>$Oz_{1}$</b>.
    <ul>
      <li>This transformation takes frame $Ox_{1}y_{1}z_{1}$ to frame $Ox_{1}^{\prime}y_{1}^{\prime}z_{1}^{\prime}$</li>
      <li>$Ox_{1}$ is rotated to $Ox_{1}^{\prime}$</li>
      <li>$Oy_{1}$ is rotated to $Oy_{1}^{\prime}$</li>
      <li>One should note, $Oy_{1}^{\prime}$ now falls in the plane $Oy_{2}z_{2}$ and $Ox_{1}^{\prime}$ now falls in the plane $Ox_{2}z_{2}$. These two planes are in the <b>target</b> frame of reference.</li>
    </ul>
  </li>
  <li>Euler angles represent three consecutive rotations in the order of <equation-inline><b>$\psi$, $\theta$, $\phi$</b></equation-inline> so that one coordinate axes system is made to coincide with another system.</li>
  <li>Again, the <b><i>order of rotation</i></b>, i.e., $\psi$, $\theta$, $\phi$, is very very important.</li>
</ol>

