---
title: 'Stability of Fixed Points of High Dimensional Dynamical Systems'
date: 2021-03-04
permalink: /posts/2021/03/fixed-point-high-dim/
header:
  teaser: thumbnails/fixed-point-high-dim.svg
tags:
  - Dynamical-Systems
  - Ordinary-Differential-Equations
  - ODE
  - Calculus
  - Jacobian
  - Vector-valued-function
  - Stability
  - Eigenvalues
---

In the [previous post](https://adipandas.github.io/posts/2020/02/stable-unstable-fixed-point/), I discussed the basics regarding the stability of fixed points of a dynamical system and explained it with a simple continuous-time one-dimensional example. In this post, I will discuss fixed points for a general case of a continuous-time $n$-dimensional system.



#### Fixed point

Just to reiterate, if the ordinary differential equation (ODE) in $\eqref{eq:1}$ represents a dynamical system:


$$
\dot x = f(x)
\label{eq:1}
$$


Fixed points of this system are given by the roots of the equation $\eqref{eq:2}$:


$$
\begin{equation}
\dot x = f(x) = 0
\label{eq:2}
\end{equation}
$$



## Fixed points of Multi-dimensional system

My [previous post](https://adipandas.github.io/posts/2020/02/stable-unstable-fixed-point/) explained the definition of fixed point of dynamical system with an example of a scalar-valued dynamical system. 

Now, focusing on the multi-dimensional ODE $\eqref{eq:3}$:


$$
\mathbf{\dot x} = \mathbf{f(x)}
\label{eq:3}
$$


where $\mathbf{f}$ is a vector-valued function, $\mathbf{x}$ and  $\mathbf{\dot x}$ are $n$-dimensional vectors:


$$
\mathbf{x, \dot x} \in \mathbb{R}^{n}
\label{eq:4}
$$


We find the fixed points (a.k.a. equilibrium states) of the system by following $\eqref{eq:2}$:


$$
\mathbf{\dot x_{eq}} = \mathbf{f}(\mathbf{x_{eq}}) = \mathbf{0}
\label{eq:5}
$$


The roots of $\eqref{eq:5}$ will give us the value of $\mathbf{x_{eq}}$, i.e., fixed points of our multi-dimensional system.



## Stable and Unstable Fixed Points

Recall, in case of one-dimensional system: $x_{eq}$ is unstable fixed point when $f^{\prime}(x_{eq})>0$ and it is stable fixed point when $f^{\prime}(x_{eq})<0$.


In case of $n$-dimensional dynamical system, following the procedure similar to the case of [one-dimensional ODE](https://adipandas.github.io/posts/2020/02/stable-unstable-fixed-point/), introduce a small perturbation $\mathbf{\delta x}$ at the equilibrium condition $\mathbf{x_{eq}}$ of the system $\eqref{eq:3}$:

$$
\begin{align}
\mathbf{\dot x_{eq} + \dot {\delta x}}
&=
\mathbf{f(x_{eq}+\delta x)}
\label{eq:6}
\end{align}
$$


Using Taylor expansion on $\eqref{eq:6}$:

$$
\begin{align}
\mathbf{\dot x_{eq} + \delta \dot x} = \mathbf{f(x_{eq})} + \mathbf{f^{\prime}(x_{eq})} \mathbf{\delta x} + \text{H.O.T.} \label{eq:7}
\end{align}
$$

Here, $\text{H.O.T.}$ stands for the terms of second and higher order in $\mathbf{\delta x}$.

But, we know at fixed points, equation $\eqref{eq:5}$ holds and thus, $\eqref{eq:7}$ reduces to $\eqref{eq:8}$.

$$
\begin{align}
\mathbf{\delta \dot x} = \mathbf{f^{\prime}(x_{eq})} \mathbf{\delta x} + \text{H.O.T.} \label{eq:8}
\end{align}
$$

The higher order terms shrink faster than the linear term as $\mathbf{\delta x}$ approaches $\mathbf{0}$, so we drop them and obtain equation $\eqref{eq:9}$.

$$
\begin{align}
\mathbf{\delta \dot x = f^{\prime}(x_{eq}) \delta x \label{eq:9}}
\end{align}
$$


$\mathbf{f}^{\prime}\mathbf{(x)}$ is the Jacobian of $\mathbf{f(x)}$ at $\mathbf{x_{eq}}$, i.e., a **linear approximation** of our dynamical system $\mathbf{f(x)}$ near $\mathbf{x_{eq}}$ (you can refer [this](https://adipandas.github.io/posts/2020/03/vector-calculus/#jacobian-aka-derivative-of-vector-valued-function) for further details on Jacobian).


$$
\begin{align}
\mathbf{f}^{\prime}\mathbf{(x)}
&=
\left[
\frac{\partial\mathbf{f}}{\partial x_{1}}, \frac{\partial\mathbf{f}}{\partial x_{2}}, \dots, \frac{\partial\mathbf{f}}{\partial x_{n}}
\right] \label{eq:11}\\
\mathbf{f}^{\prime}\mathbf{(x)} &=
\begin{bmatrix}
\frac{\partial{f_{1}}}{\partial x_{1}} & \frac{\partial{f_{1}}}{\partial x_{2}} & \dots & \frac{\partial{f_{1}}}{\partial x_{n}}\\
\vdots & \ddots & \ddots & \vdots \\
\frac{\partial{f_{n}}}{\partial x_{1}} & \frac{\partial{f_{n}}}{\partial x_{2}} & \dots & \frac{\partial{f_{n}}}{\partial x_{n}}\\
\end{bmatrix} \label{eq:12}
\end{align}
$$


Using this Jacobian, equation $\eqref{eq:12}$, at our fixed point $\mathbf{x_{eq}}$ for the dynamical system under consideration, we can calculate its [**eigenvalues**](https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors) and interpret the results of the fixed point.

An eigenvalue $\lambda$ and its eigenvector $\mathbf{v} \ne \mathbf{0}$ of the Jacobian satisfy equation $\eqref{eq:13}$,


$$
\begin{align}
\mathbf{f}^{\prime}(\mathbf{x_{eq}}) \mathbf{v} = \lambda \mathbf{v} \label{eq:13}
\end{align}
$$


Note that the eigenvector $\mathbf{v}$ is a direction of perturbation, not the fixed point itself. Rearranging $\eqref{eq:13}$ as $(\mathbf{f}^{\prime}(\mathbf{x_{eq}}) - \lambda \mathbf{I})\mathbf{v} = \mathbf{0}$, a nonzero solution $\mathbf{v}$ exists only when the matrix $(\mathbf{f}^{\prime}(\mathbf{x_{eq}}) - \lambda \mathbf{I})$ is singular. This gives the characteristic equation $\eqref{eq:14}$:


$$
\begin{align}
\det \left( \mathbf{f}^{\prime}(\mathbf{x_{eq}}) - \lambda \mathbf{I} \right) = 0 \label{eq:14}
\end{align}
$$


Here, $\mathbf{I}$ is the $n \times n$ identity matrix. The roots of $\eqref{eq:14}$ are the $n$ eigenvalues of the dynamical system at the fixed point $\mathbf{x}=\mathbf{x_{eq}}$.



### Eigenvalue interpretation <a name='eigen_value_interpretation'></a>

For a continuous-time nonlinear dynamical system given by $\eqref{eq:3}$, the eigenvalues $\lambda$ that are found as roots of equation $\eqref{eq:14}$ can be interpreted as:

* If any of the eigenvalues have a real part $Re(\lambda)>0$: $\mathbf{x_{eq}}$ is an unstable fixed point.
* If all $Re(\lambda)<0$: $\mathbf{x_{eq}}$ is a stable fixed point.
* If no eigenvalue has $Re(\lambda)>0$ and at least one has $Re(\lambda)=0$: $\mathbf{x_{eq}}$ is a non-hyperbolic fixed point and the linearization is inconclusive. The linear system $\eqref{eq:9}$ is neutrally stable along the eigenvectors with $Re(\lambda)=0$, but the higher order terms dropped in $\eqref{eq:8}$ decide the stability of the nonlinear system, and they can make it either stable or unstable. Settling the question requires [Lyapunov's direct method](https://en.wikipedia.org/wiki/Lyapunov_stability), which works with the nonlinear system itself.

A fixed point where every eigenvalue has a nonzero real part is called hyperbolic. There, the [Hartman-Grobman theorem](https://en.wikipedia.org/wiki/Hartman%E2%80%93Grobman_theorem) guarantees that the flow of the nonlinear system near $\mathbf{x_{eq}}$ is topologically equivalent to the flow of its linearization, which is what licenses reading stability off the eigenvalues. The first bullet holds even without hyperbolicity, because one eigenvalue with $Re(\lambda)>0$ creates a direction along which the perturbation grows, whatever the other eigenvalues do.


### Complex eigenvalues

The three cases above are decided by $Re(\lambda)$ alone and cover every possibility. A nonzero $Im(\lambda)$ describes the shape of the trajectories rather than their stability. Since $\mathbf{f}^{\prime}(\mathbf{x_{eq}})$ is a real matrix, complex eigenvalues occur in conjugate pairs $\lambda = \alpha \pm i \beta$. Each pair contributes a rotation of angular frequency $\beta$ in the real plane spanned by the real and imaginary parts of the corresponding eigenvector:

* $\alpha<0$: trajectories spiral inward to $\mathbf{x_{eq}}$ (stable spiral).
* $\alpha>0$: trajectories spiral outward (unstable spiral).
* $\alpha=0$: the linearization predicts closed orbits around a center. This is the non-hyperbolic case, so the higher order terms decide whether the orbits stay closed, spiral in, or spiral out.



### Important points to note regarding this article

In this post, we discussed a general case of interpreting the fixed points of a dynamical system. By general, I mean $\mathbf{f(x)}$ is a non-linear, continuous-time vector-valued function representing a dynamical system. Below are certain points one should note about any non-linear dynamical system:

* We assumed that the system is non-linear and linearized it using Taylor series expansion near its fixed point (a.k.a. equilibrium).
* We evaluated the stability of a fixed point **near** the equilibrium condition by perturbing the system  ($\mathbf{x_{eq}}+\mathbf{\delta x}$).
* This approach of interpreting the stability of the system by linearizing it near the equilibrium **does not tell much** about a system's asymptotic behavior at large.
  * We only understand how the system behaves **locally** or **in the neighborhood of the fixed points**.
* In practical or real-world systems, it may not be possible to interpret the global stability characteristics of the system. Thus, the stability analysis around the neighborhood of the fixed point is useful for many practical applications such as sustaining a non-linear system's state near or at the fixed point.
* In general, global asymptotic behaviors of any non-linear dynamical system can be complex and there are no systematic methods to predict and analyze such behaviors.



### References and Further Readings:

* Deshpande, A. M. Stability of Fixed Point of a Dynamical System. [[web](https://adipandas.github.io/posts/2020/02/stable-unstable-fixed-point/)]
* Strogatz, Steven H. Nonlinear dynamics and chaos with student solutions manual: With applications to physics, biology, chemistry, and engineering. CRC press, 2018.
* Khalil, Hassan K. "Lyapunov stability." *Control Systems, Robotics and AutomatioN–Volume XII: Nonlinear, Distributed, and Time Delay Systems-I* (2009): 115.
* Bomze, Immanuel M., and Jörgen W. Weibull. "Does neutral stability imply Lyapunov stability?." *Games and Economic Behavior* 11.2 (1995): 173-192.
* Fixed point. [[web](https://mathworld.wolfram.com/FixedPoint.html)]
* Jacobian matrix [[video](https://www.youtube.com/watch?v=bohL918kXQk)]
* Stability Theory. [[web](https://en.wikipedia.org/wiki/Stability_theory)]
* Lyapunov Stability. [[web](https://en.wikipedia.org/wiki/Lyapunov_stability)]
