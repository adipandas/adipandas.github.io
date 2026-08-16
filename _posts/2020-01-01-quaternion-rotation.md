---
title: 'Quaternion Rotation'
date: 2020-01-01
permalink: /posts/2020/01/quaternion-rotation/
header:
  teaser: thumbnails/quaternion-rotation.svg
tags:
  - quaternion
  - quaternion-product
  - rotation
---

Quaternions are a number system that extends complex numbers. A quaternion provides a convenient mathematical notation for representing orientations and rotations of an object in three dimensions. This section discusses some of the useful properties and operations which are used in quaternion rotation.

**Conventions used here:** quaternions follow the **Hamilton** convention ($$ijk = -1$$) and are written **scalar-first**, i.e. $$q = [q_1, q_2, q_3, q_4]$$ where $$q_1$$ is the real (scalar) part. Frames are denoted with leading super/sub-scripts following Craig's notation, as used by Madgwick [1]. Be careful: many libraries (e.g. SciPy) store quaternions **scalar-last**, and some literature uses the JPL convention instead [2].

Let there be two coordinate frames in a 3-dimensional space, $$A$$ and $$B$$. Let $$\hat{r}^{A}$$ be the **unit** axis of rotation, described in frame $$A$$, as shown in the figure below.   

$$\hat{r}^{A} = (r^{A}_{x}, r^{A}_{y}, r^{A}_{z}), \qquad \lVert \hat{r}^{A} \rVert_2 = 1$$

The axis **must be normalized**; otherwise the quaternion built from it below will not be of unit length and will not represent a rotation.

Using **Quaternions** we can rotate from frame $$A$$ to $$B$$ by angle $$\theta$$ around the axis $$\hat{r}^{A}$$.
  
  
<img src="/images/quaternion_rotation/quaternion_rotation_1.png" alt="Quaternion Rotation"/>
  
  
**Quaternion describing this orientation is $$q^{A}_{B}$$**:  

$$q^{A}_{B} = [q_1, q_2, q_3, q_4] = [cos(\frac{\theta}{2}), -r^{A}_{x} sin(\frac{\theta}{2}), -r^{A}_{y} sin(\frac{\theta}{2}), -r^{A}_{z} sin(\frac{\theta}{2})]$$

$$q^{A}_{B}$$ describes the orientation of frame $$B$$ relative to frame $$A$$.

**Note the minus signs.** They are not a typo: they are what makes $$q^{A}_{B}$$ the operator that takes the *coordinates* of a vector in frame $$A$$ to its coordinates in frame $$B$$. Concretely, if $${}^{A}v$$ and $${}^{B}v$$ are the same vector expressed in the two frames (each written as a 4-element quaternion with a leading $$0$$), then

$${}^{B}v = q^{A}_{B} \bigotimes {}^{A}v \bigotimes \left( q^{A}_{B} \right)^{*}$$

Every sign and ordering convention below follows from this one equation, so it is worth fixing it in mind before reading on.

**A rotation quaternion must be of unit length.**  
Quaternion arithmetic itself works for any quaternion, but only unit quaternions represent rotations. It is therefore conventional to normalize any quaternion describing an orientation.  

$$\lVert q \rVert_2 = 1$$

**Conjugate quaternion**:  

$$\left( q^{A}_{B} \right)^{*} = q^{B}_{A} = [q_1, -q_2, -q_3, -q_4]$$

The conjugate swaps the two frames described by an orientation. For a **unit** quaternion the conjugate is also the inverse, $$q^{-1} = q^{*}$$; this is not true in general (in general $$q^{-1} = q^{*} / \lVert q \rVert_2^2$$).

**Compound orientations using quaternions**:
Let $$q^{A}_{B}$$ and $$q^{B}_{C}$$ be two quaternions.
$$q^{A}_{B}$$ - orientation of $$B$$ w.r.t. $$A$$.  
$$q^{B}_{C}$$ - orientation of $$C$$ w.r.t. $$B$$.  

The compound orientation $$q^{A}_{C}$$ is defined as:

$$q^{A}_{C} = q^{B}_{C} \bigotimes q^{A}_{B}$$  

$$q^{A}_{C}$$ - orientation of $$C$$ w.r.t. $$A$$.  
$$\bigotimes$$ represents quaternion product.

**Why the order looks reversed:** applying the rotation operation twice gives

$${}^{C}v = q^{B}_{C} \bigotimes \left( q^{A}_{B} \bigotimes {}^{A}v \bigotimes \left( q^{A}_{B} \right)^{*} \right) \bigotimes \left( q^{B}_{C} \right)^{*}$$

$${}^{C}v = \left( q^{B}_{C} \bigotimes q^{A}_{B} \right) \bigotimes {}^{A}v \bigotimes \left( q^{B}_{C} \bigotimes q^{A}_{B} \right)^{*}$$

hence $$q^{A}_{C} = q^{B}_{C} \bigotimes q^{A}_{B}$$. If you instead adopt the (nowadays more common) convention **without** the minus signs, where $$q^{A}_{B}$$ maps coordinates from $$B$$ into $$A$$, the composition reverses to $$q^{A}_{C} = q^{A}_{B} \bigotimes q^{B}_{C}$$. Mixing the two is the single most common source of errors.


**Quaternion Product** (Hamilton rule):  
Let $$p$$ and $$q$$ be two quaternions. Then the product of these two quaternions is:  

$$p \bigotimes q = [p_1, p_2, p_3, p_4] \bigotimes [q_1, q_2, q_3, q_4]$$  

$$p \bigotimes q = \begin{pmatrix}
p_1 q_1 - p_2 q_2 - p_3 q_3 - p_4 q_4 \\
p_1 q_2 + p_2 q_1 + p_3 q_4 - p_4 q_3 \\
p_1 q_3 - p_2 q_4 + p_3 q_1 + p_4 q_2 \\
p_1 q_4 + p_2 q_3 - p_3 q_2 + p_4 q_1
\end{pmatrix}^T $$  

Quaternion product is not commutative, i.e., $$p \bigotimes q \ne q \bigotimes p$$.  

**NOTE: I know there may be a lot of confusion in Quaternion mathematics. The [blogpost by Fan Zheng](https://fzheng.me/2017/11/12/quaternion_conventions_en/) provides an excellent overview of conventions used in Quaternion representations. [2]**

References
-------------
1. Madgwick, S. (2010). An efficient orientation filter for inertial and inertial/magnetic sensor arrays. Report x-io and University of Bristol (UK), 25, 113-118. [[link](https://www.x-io.co.uk/res/doc/madgwick_internal_report.pdf)]
2. Zheng, F. (2017). Quaternion Conventions: Hamilton and JPL. [[link](https://fzheng.me/2017/11/12/quaternion_conventions_en/)]

