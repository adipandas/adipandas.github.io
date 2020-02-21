---
title: 'Rotation using Euler Angles'
date: 2020-02-10
permalink: /posts/2020/02/euler-rotation/
tags:
  - Rotation
  - Euler Angles
  - Rotation Matrix
---

I have always found rotation using euler angles confusing. This post is just a simple note to maintain my sanity while performing rigid body transformations using euler angles and rotational matrices.

# Rotation

Rotational matrices are special orthogonal matrices. I am not going to discuss any property of these matrices over here. But this post a quick reference for rotation using **z-y-x euler angles**. For further details, you can refer [this](https://en.wikipedia.org/wiki/Rotation_matrix).

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
  <li>Original Frame: $Ox_{1}y_{1}z_{1}$</li>
  <li>Target Frame: $Ox_{2}y_{2}z_{2}$</li>
  <li>Angle $\psi$ is the rotation about $Oz_{1}$.
    <ul>
      <li>This transformation takes frame $Ox_{1}y_{1}z_{1}$ to frame $Ox_{1}^{\prime}y_{1}^{\prime}z_{1}^{\prime}$</li>
      <li>$Ox_{1}$ is rotated to $Ox_{1}^{\prime}$</li>
      <li>$Oy_{1}$ is rotated to $Oy_{1}^{\prime}$</li>
      <li>$Oz_{1}$ is rotated to $Oz_{1}^{\prime}$. The axes $Oz_{1}$ and $Oz_{1}^{\prime}$ overlap on each other.</li>
      <li>One should note, $Oy_{1}^{\prime}$ now falls in the plane $Oy_{2}z_{2}$ and $Ox_{1}^{\prime}$ now falls in the plane $Ox_{2}z_{2}$. These two planes are in the <b>target</b> frame of reference.</li>
    </ul>
  </li>
  <li>Angle $\theta$ is rotation about $Oy_{1}^{\prime}$.
    <ul>
      <li>This transformation takes frame $Ox_{1}^{\prime}y_{1}^{\prime}z_{1}^{\prime}$ to frame $Ox_{1}^{\prime\prime}y_{1}^{\prime\prime}z_{1}^{\prime\prime}$.</li>
      <li>$Ox_{1}^{\prime}$ is rotated to $Ox_{1}^{\prime\prime}$.</li>
      <li>$Oy_{1}^{\prime}$ is rotated to $Oy_{1}^{\prime\prime}$. The axes $Oy_{1}^{\prime}$ and $Oy_{1}^{\prime\prime}$ overlap on each other.</li>
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


## Constrains on three euler angles:
Euler angle rotation using rotation matrices face the issue of singularity or gimbal lock. These angle rotations are constraint to avoid ambiguities. The limits are as follows:

$$-\pi \le \psi \le \pi$$

$$-\frac{\pi}{2} \le \theta \le \frac{\pi}{2}$$

$$-\pi \le \phi \le \pi$$

## Rotational Transformations

Let there be two frames defined as **start** frame and **target** frame.

* **Start Frame**: $$Ox_{1}y_{1}z_{1}$$
* **Target Frame**: $$Ox_{2}y_{2}z_{2}$$
* A point **$$p$$** is defined in start and target frames as **$$p^{1}$$** and **$$p^{2}$$** respectively.

Now, with the help of euler angles, transform the point given in **start** frame to the corresponding point in **target** frame.

**Note: Order of transformation is: (1) Angle $$\psi$$ along $$Oz_{1}$$; (2) Angle $$\theta$$ along $$Oy_{1}^{\prime}$$; (3) Angle $$\phi$$ along $$Ox_{1}^{\prime\prime}$$.**

* Rotation by $$\psi$$ along $$Oz_{1}$$
    * Transform point **$$p^{1}$$** in frame $$Ox_{1}y_{1}z_{1}$$ to point **$$p^{1\prime}$$** in frame $Ox_{1}^{\prime}y_{1}^{\prime}z_{1}^{\prime}$.

$$p^{1\prime} = R_{1}^{1\prime} p^{1}$$

$$p^{1\prime} = \begin{bmatrix}
\cos \psi & \sin \psi & 0\\
-\sin \psi & \cos \psi & 0\\
0 & 0 & 1
\end{bmatrix} p^{1}$$






