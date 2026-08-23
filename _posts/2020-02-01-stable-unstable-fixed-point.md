---
title: 'Stability of Fixed Point of a Dynamical System'
date: 2020-02-01
permalink: /posts/2020/02/stable-unstable-fixed-point/
header:
  teaser: thumbnails/stable-unstable-fixed-point.svg
tags:
  - Dynamical-Systems
  - Ordinary-Differential-Equations
  - ODE
  - Calculus
---

Stability theory is used to address the stability of solutions of differential equations. A dynamical system can be represented by a differential equation. The stability of the trajectories of this system under perturbations of its initial conditions can also be addressed using the stability theory.


## Fixed Point

Consider a dynamical system given by the following ordinary differential equation (ODE):

$$\dot x = f(x)  \tag{1}$$

A **fixed point** of this system is given by:

$$\dot x = 0$$

Therefore, $$f(x) = 0$$ or roots of the function $$f(x)$$ form the fixed points of the dynamical system.

## Stable and Unstable Fixed Points

In layman's terms, you can say the following about stable and unstable fixed points.

**Stable Fixed Point**: Put a system to an initial value that is "close" to its fixed point. The trajectory of the solution of the differential equation $$\dot x = f(x)$$ will stay close to this fixed point.

**Unstable Fixed Point**: Again, start the system with initial value "close" to its fixed point. If the fixed point is unstable, there exists a solution that starts at this initial value but the trajectory of the solution will move away from this fixed point.


In other words, one can also think of a stable fixed point as the attractor and unstable fixed point as the repeller. A particle governed by $$\dot x = f(x)$$ is drawn towards a stable fixed point and pushed away from an unstable one.

### Mathematical Intuition:

For the dynamical system in equation (1), write $$x^{*}$$ for a fixed point, so that $$f(x^{*}) = 0$$. The state of the particle is $$x$$, and it starts a small distance $$\delta \gt 0$$ away from $$x^{*}$$.

Suppose $$f^{\prime}(x^{*}) \gt 0$$. Then $$f$$ is increasing as it crosses zero at $$x^{*}$$, which means $$f(x^{*} - \delta) \lt 0 \lt f(x^{*} + \delta)$$ for sufficiently small $$\delta$$.

Start the particle at $$x = x^{*} + \delta$$. Equation (1) gives $$\dot x = f(x) \gt 0$$, so $$x$$ grows and the particle moves further to the right of $$x^{*}$$. Start it instead at $$x = x^{*} - \delta$$. Now $$\dot x \lt 0$$, so $$x$$ shrinks and the particle moves further to the left. In both cases the particle leaves the neighborhood of $$x^{*}$$.

Therefore, $$f^{\prime} (x^{*}) \gt 0$$ gives an **unstable fixed point**. $$f^{\prime} (x^{*}) \lt 0$$ gives a **stable fixed point**.

**Note**: The conditions $$f^{\prime} (x^{*}) \lt 0$$ and $$f^{\prime} (x^{*}) \gt 0$$ are sufficient to guarantee stability and instability respectively. They are not necessary, i.e., it is possible to have stable and unstable fixed points where $$f^{\prime} (x^{*}) = 0$$.

## Intuitive Example:

For the differential equation $$\dot x = \sin(x)$$:

<img src="/images/stable_unstable_fixed_point/sin_x_feb2020.png" alt="Stable and Unstable fixed points on $$\dot x = sin(x)$$"/>

Using linear stability analysis, fixed points occur when $$f(x)=\sin(x)=0$$, that is at $$x^{*}=k \pi$$ where $$k$$ is an integer.

$$f^{\prime}(x^{*})=\cos(k \pi)=1$$ if $$k$$ is even and $$f^{\prime}(x^{*})=\cos(k \pi)= - 1$$ if $$k$$ is odd.

Therefore, $$x^{*}$$ is **unstable** when $$k$$ is *even*, and **stable** when $$k$$ is *odd*.


### High Dimensional Dynamical Systems

This post discussed the definition of a fixed point of a dynamical system. A simple one-dimensional dynamical system is used as an illustration to explain the concept. A more detailed discussion on general nonlinear, continuous-time, multi-dimensional dynamical systems and their fixed points is provided in my [next post](https://adipandas.github.io/posts/2021/03/fixed-point-high-dim/).

## Reference and Further Readings:

* Strogatz, S. H. (2018). Nonlinear dynamics and chaos: with applications to physics, biology, chemistry, and engineering. CRC press. [[book](http://www.hds.bme.hu/~fhegedus/Strogatz%20-%20Nonlinear%20Dynamics%20and%20Chaos.pdf)]
* Deshpande, A. M. (2021). Stability of Fixed Points of High Dimensional Dynamical Systems.[[web](https://adipandas.github.io/posts/2021/03/fixed-point-high-dim/)]








