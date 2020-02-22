---
title: 'Rotation using Euler Angles'
date: 2020-02-10
permalink: /posts/2020/02/euler-rotation/
tags:
  - Rotation
  - Euler Angles
  - Rotation Matrix
---

I have always found rotation using Euler angles confusing. This post is just a simple note to maintain my sanity while performing rigid body transformations using Euler angles and rotational matrices.

# Rotation

Rotational matrices are special orthogonal matrices. I am not going to discuss any property of these matrices over here. But this post is a quick reference for rotation using **z-y-x Euler angles**. For further details, you can refer to [this](https://en.wikipedia.org/wiki/Rotation_matrix).

## Euler Angle Transformation
The most important thing you must remember before reading further about transformations using Euler angles is:  
**The order of matrix multiplication of rotational matrices is of extreme importance.**


<ol type="i">
  <li>Euler angles are used to specify the orientation of one reference frame relative to another reference frame.</li>
  <li>Euler angles are specified by the <b>three angles</b>, viz., <strong>$\psi$, $\theta$, $\phi$</strong>.</li>
  <li>Euler angles represent three consecutive rotations in the order of $\psi$, $\theta$, $\phi$ so that one coordinate axes system is made to coincide with another system.</li>
  <li>Again, the <b><i>order of rotation</i></b>, i.e., $\psi$, $\theta$, $\phi$, is very very important.</li>
  <li>Angle <strong>$\psi$</strong> - Angle to be rotated about the <i>current</i> frame's <b>Z-axis</b>.</li>
  <li>Angle <strong>$\theta$</strong> - Angle to be rotated about the <i>current</i> frame's <b>Y-axis</b>.</li>
  <li>Angle <strong>$\phi$</strong> - Angle to be rotated about the <i>current</i> frame's <b>X-axis</b>.</li>
</ol>


## Sequence of rotation of three Euler angles:
Let's say one has to go from **frame 1** to **frame 2** using Euler angle $$\psi$$, $$\theta$$, $$\phi$$. Lets start with the current frame, i.e., **frame 1**.
<ol type="i">
  <li>Original Frame: $Ox_{1}y_{1}z_{1}$</li>
  <li>Target Frame: $Ox_{2}y_{2}z_{2}$</li>
  <li>Angle $\psi$ is the rotation about $Oz_{1}$.
    <ul>
      <li>This transformation takes frame $Ox_{1}y_{1}z_{1}$ to frame $Ox_{1}^{\prime}y_{1}^{\prime}z_{1}^{\prime}$</li>
      <li>$Ox_{1}$ is rotated to $Ox_{1}^{\prime}$</li>
      <li>$Oy_{1}$ is rotated to $Oy_{1}^{\prime}$</li>
      <li>$Oz_{1}$ is rotated to $Oz_{1}^{\prime}$. The axes $Oz_{1}$ and $Oz_{1}^{\prime}$ overlap with each other.</li>
      <li>One should note, $Oy_{1}^{\prime}$ now falls in the plane $Oy_{2}z_{2}$ and $Ox_{1}^{\prime}$ now falls in the plane $Ox_{2}z_{2}$. These two planes are in the <b>target</b> frame of reference.</li>
    </ul>
  </li>
  <li>Angle $\theta$ is rotation about $Oy_{1}^{\prime}$.
    <ul>
      <li>This transformation takes frame $Ox_{1}^{\prime}y_{1}^{\prime}z_{1}^{\prime}$ to frame $Ox_{1}^{\prime\prime}y_{1}^{\prime\prime}z_{1}^{\prime\prime}$.</li>
      <li>$Ox_{1}^{\prime}$ is rotated to $Ox_{1}^{\prime\prime}$.</li>
      <li>$Oy_{1}^{\prime}$ is rotated to $Oy_{1}^{\prime\prime}$. The axes $Oy_{1}^{\prime}$ and $Oy_{1}^{\prime\prime}$ overlap with each other.</li>
      <li>$Oz_{1}^{\prime}$ is rotated to $Oz_{1}^{\prime\prime}$.</li>
      <li>$Ox_{1}^{\prime\prime}$ now coincides with the axes $Ox_{2}$ and $Oz_{1}^{\prime\prime}$ now falls in the plane $Oy_{2}z_{2}$. The axis $Ox_{2}$ and the plane $Oy_{2}z_{2}$ are in the <b>target</b> frame of reference.</li>
    </ul>
  </li>
  
  <li>Angle $\phi$ is rotation about $Ox_{1}^{\prime\prime}$.
    <ul>
      <li>This transformation takes frame $Ox_{1}^{\prime\prime}y_{1}^{\prime\prime}z_{1}^{\prime\prime}$ to frame $Ox_{1}^{\prime\prime\prime}y_{1}^{\prime\prime\prime}z_{1}^{\prime\prime\prime}$. The resulting frame $Ox_{1}^{\prime\prime\prime}y_{1}^{\prime\prime\prime}z_{1}^{\prime\prime\prime}$ is also the target frame $Ox_{2}y_{2}z_{2}$.</li>
      <li>$Ox_{1}^{\prime\prime}$ is rotated to $Ox_{1}^{\prime\prime\prime}$ ($Ox_{2}$).</li>
      <li>$Oy_{1}^{\prime\prime}$ is rotated to $Oy_{1}^{\prime\prime\prime}$ ($Oy_{2}$).</li>
      <li>$Oz_{1}^{\prime\prime}$ is rotated to $Oz_{1}^{\prime\prime\prime}$ ($Oz_{2}$).</li>
      <li>$Oy_{1}^{\prime\prime\prime}$ now coincides with the axes $Oy_{2}$ and $Oz_{1}^{\prime\prime\prime}$ coincides with the axis $Oz_{2}$. The axes $Oy_{2}$ and $Oz_{2}$ are in the <b>target</b> frame of reference.</li>
    </ul>
  </li>
  
</ol>

<p style="text-align:center;"><img src="/images/euler_rotation/euler_rotation_diagram.png" alt="euler-rotation-sequence"/></p>


## Constrains on three Euler angles:
Euler angle rotation using rotation matrices faces the issue of singularity or gimbal lock. These angle rotations are constraint to avoid ambiguities. The limits are as follows:

$$-\pi \le \psi \le \pi$$

$$-\frac{\pi}{2} \le \theta \le \frac{\pi}{2}$$

$$-\pi \le \phi \le \pi$$

## Rotational Transformations

Let there be two frames defined as **start** frame and **target** frame.

* **Start Frame**: $$Ox_{1}y_{1}z_{1}$$
* **Target Frame**: $$Ox_{2}y_{2}z_{2}$$
* A point **$$p$$** is defined in the start and target frames as **$$p^{1}$$** and **$$p^{2}$$** respectively.

Now, with the help of Euler angles, transform the point given in the **start** frame to the corresponding point in the **target** frame.

**Note: Order of transformation is: (1) Angle $$\psi$$ along $$Oz_{1}$$; (2) Angle $$\theta$$ along $$Oy_{1}^{\prime}$$; (3) Angle $$\phi$$ along $$Ox_{1}^{\prime\prime}$$.**

* Rotation by $$\psi$$ along $$Oz_{1}$$: This transforms point **$$p^{1}$$** in frame $$Ox_{1}y_{1}z_{1}$$ to point **$$p^{1^{\prime}}$$** in frame $Ox_{1}^{\prime}y_{1}^{\prime}z_{1}^{\prime}$.

<p style="text-align:center;"><img src="/images/euler_rotation/Ryaw12.gif" alt="Ryaw"/></p>

$$p^{1^{\prime}} = R_{1_{z=\psi}}^{1\prime} p^{1}$$

* The above transformation is followed by $$\theta$$ around $$Oy_{1}^{\prime}$$ and then by $$\phi$$ around $$Ox_{1}^{\prime\prime}$$.

<p style="text-align:center;"><img src="/images/euler_rotation/Rpitch12.gif" alt="Rpitch"/></p>

$$p^{1^{\prime\prime}} = R_{1^{\prime}_{y=\theta}}^{1^{\prime\prime}} p^{1^{\prime}}$$

<p style="text-align:center;"><img src="/images/euler_rotation/Rroll12.gif" alt="Rroll"/></p>

$$p^{2} = R_{1^{\prime\prime}_{x=\phi}}^{2} p^{1^{\prime\prime}}$$

Therefore, the resultant transformation matrix for going from Frame $$Ox_{1}y_{1}z_{1}$$ to Frame $$Ox_{2}y_{2}z_{2}$$ is:

$$p^{2} = R_{1^{\prime\prime}_{x=\phi}}^{2} R_{1^{\prime}_{y=\theta}}^{1^{\prime\prime}} R_{1_{z=\psi}}^{1^{\prime}} p^{1}$$

<p style="text-align:center;"><img src="/images/euler_rotation/R12_z-y-x-euler.png" alt="R-z-y-x-euler"/></p>

$$p^2 = R_1^2 p^1$$

## Code

The code for euler angle transformation is available on Google Colab: 
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Ua6puurb9OuODAlMWJmVArg8dYh8OUTH)

You can also find the corresponding notebook on github:
[![Github](https://img.shields.io/badge/GitHub-Euler-blue)](/files/_posts/code/euler-rotation/euler_rotation.ipynb)

## References
* Pamadi, B. N. (2004). Performance, stability, dynamics, and control of airplanes. American Institute of aeronautics and astronautics.

