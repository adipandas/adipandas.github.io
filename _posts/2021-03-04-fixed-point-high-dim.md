---
title: 'Stability of Fixed Points of a "High Dimensional" Dynamical System'
date: 2021-03-04
permalink: /posts/2021/03/fixed-point-high-dim/
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

My [previous post](https://adipandas.github.io/posts/2020/02/stable-unstable-fixed-point/) only explained the definition of fixed point and provided an example with a scalar-valued dynamical system. Now, lets discuss a case of multi-dimensional ODE.

We will start with the system given by equation $\eqref{eq:3}$:

$$
\mathbf{\dot x} = \mathbf{f(x)}
\label{eq:3}
$$

where $\mathbf{f}$ is a vector-valued function, $\mathbf{x}$ and  $\mathbf{\dot x}$ are $n$-dimensional vectors:

$$
\mathbf{x, \dot x} \in \mathcal{R}^{n}
\label{eq:4}
$$

We find the fixed points (a.k.a. equilibrium states) of the system by following $\eqref{eq:2}$:

$$
\mathbf{\dot x}_{eq} = \mathbf{f}(\mathbf{x}_{eq}) = \mathbf{0}
\label{eq:5}
$$

The roots of $\eqref{eq:5}$ will give us the value of $\mathbf{x}_{eq}$, i.e., fixed points of our multi-dimensional system.


## Stable and Unstable Fixed Points

We analyzed the system in a one-dimensional case ([here](https://adipandas.github.io/posts/2020/02/stable-unstable-fixed-point/)) using a small perturbation $\delta$ at the equilibrium condition of the system. We will follow the similar procedure here as well.

We evaluated $\mathbf{f}^{\prime}\mathbf{(x)}$ at $\mathbf{x}_{eq}$, to see if our fixed point is stable or unstable. For one-dimensional system, it was easy since $f^{\prime}(x_{eq})>0$ with unstable fixed point and $f^{\prime}(x_{eq})<0$ with a stable fixed point. In case of high-dimensional system, we cannot do this. To analyze the behavior of our $n$-dimensional system at $\mathbf{x}_{eq}$, we will introduce the perturbation $\mathbf{\delta x}$ at $\mathbf{x}_{eq}$. Thus, we end up with the following:

$$
\begin{align}
\mathbf{\dot{x}}_{eq} + \mathbf{\dot {\delta x}} &= \mathbf{f} (\mathbf{x}_{eq} + \mathbf{\delta x}) \label{eq:6}
\end{align}
$$

Using Taylor expansion on $\eqref{eq:6}$:

$$
\begin{align}
\mathbf{\dot{x}}_{eq} + \mathbf{\dot {\delta x}} = \mathbf{f}(\mathbf{x}_{eq}) + \mathbf{f}^{\prime}(\mathbf{x}_{eq}) \mathbf{{\delta x}} + \mathbf{f}^{\prime\prime}(\mathbf{x}_{eq}) \frac{\mathbf{{\delta x}}^{2}}{2!} + \dots \label{eq:7}
\end{align}
$$

But, we know at fixed points, equation $\eqref{eq:5}$ holds and thus, $\eqref{eq:7}$ reduces to $\eqref{eq:8}$.

$$
\begin{align}
\mathbf{\dot {\delta x}} 
&=
\mathbf{f}^{\prime}(\mathbf{x}_{eq}) \mathbf{{\delta x}} + \mathbf{f}^{\prime\prime}(\mathbf{x}_{eq}) \frac{\mathbf{{\delta x}}^{2}}{2!} + \dots \\
\mathbf{\dot {\delta x}} 
&=
\mathbf{f}^{\prime}(\mathbf{x}_{eq}) \mathbf{{\delta x}} + \mathbf{H.O.T.} 
\label{eq:8}
\end{align}
$$

We can ignore the higher order terms $\mathbf{H.O.T.}$ for values of $\mathbf{\delta{x}}$ close to $\mathbf{0}$, resulting in equation $\eqref{eq:9}$.

$$
\begin{align}
\mathbf{\dot {\delta x}}
&=
\mathbf{f}^{\prime}(\mathbf{x}_{eq}) \mathbf{{\delta x}} 
\label{eq:9}
\end{align}
$$

$\mathbf{f}^{\prime}\mathbf{(x)}$ is the Jacobian of $\mathbf{f(x)}$ at $\mathbf{x}_{eq}$, i.e., a **linear approximation** of our dynamical system $\mathbf{f(x)}$ near $\mathbf{x}_{eq}$ (you can refer [this](https://adipandas.github.io/posts/2020/03/vector-calculus/#jacobian-aka-derivative-of-vector-valued-function) for further details on Jacobian).

$$
\begin{align}
\mathbf{f}^{\prime}\mathbf{(x)}
&=
\left[
\frac{\partial\mathbf{f}}{\partial x_{1}}, \frac{\partial\mathbf{f}}{\partial x_{2}}, \dots, \frac{\partial\mathbf{f}}{\partial x_{n}}
\right]
\label{eq:11}\\
\mathbf{f}^{\prime}\mathbf{(x)} &=
\begin{bmatrix}
\frac{\partial{f_{1}}}{\partial x_{1}} & \frac{\partial{f_{2}}}{\partial x_{2}} & \dots & \frac{\partial{f_{n}}}{\partial x_{n}}\\
\vdots & \ddots & \ddots & \vdots \\
\frac{\partial{f_{n}}}{\partial x_{1}} & \frac{\partial{f_{n}}}{\partial x_{2}} & \dots & \frac{\partial{f_{n}}}{\partial x_{n}}\\
\end{bmatrix} \label{eq:12}
\end{align}
$$

Using this Jacobian, equation $\eqref{eq:12}$, at our fixed point $\mathbf{x}_{eq}$ for the dynamical system under consideration, we can calculate its [**eigenvalues**](https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors) and interpret the results of the fixed point.

Therefore, we find the eigenvalues for equation $\eqref{eq:13}$,

$$
\begin{align}
\mathbf{f}^{\prime}(\mathbf{x}_{eq}) \mathbf{x}_{eq} = \lambda \mathbf{x}_{eq} \label{eq:13}
\end{align}
$$

Here, $\lambda$ denotes the eigenvalue of the system. The roots of $\eqref{eq:13}$ are the eigenvalues the dynamical system at the fixed point ${\mathbf{x}=\mathbf{x}_{eq}}$.


**Eigenvalue interpretation** <a name='eigen_value_interpretation'></a>

For a continuous-time nonlinear dynamical system given by $\eqref{eq:3}$, the eigenvalues $\lambda$ that are found as roots of equation $\eqref{eq:13}$ can be interpreted as:  
* If any of the eigenvalues have a real part $Re(\lambda)>0$: $\mathbf{x}_{eq}$ is an unstable fixed point.
* If all $Re(\lambda)<0$: $\mathbf{x}_{eq}$ is a stable fixed point.
* If $\lambda=0$: $\mathbf{x}_{eq}$ is a neutral fixed point.
* If eigenvalues $\lambda$ are complex conjugates, i.e., $Im(\lambda) \ne 0$: The dynamical system has oscillatory behavior around the fixed point.



### Important points to note regarding this article

In this post, we discussed a general case of interpreting the fixed points of a dynamical system. By general, I mean $\mathbf{f(x)}$ is a non-linear, continuous-time vector-valued function representing a dynamical system. Below are certain points one should note about any non-linear dynamical system:  
* We assumed that the system is non-linear and linearized it using Taylor series expansion near its fixed point (a.k.a. equilibrium).
* We evaluated the stability of a fixed point **near** the equilibrium condition by perturbing the system  ($\mathbf{x}_{eq}+\mathbf{\delta x}$).
* This approach of interpreting the stability of the system by linearizing it near the equilibrium **does not tell much** about a system's asymptotic behavior at large.
  * We only understand how the system behaves **locally** or **in the neighborhood of the fixed points**.
* In practical or real-world systems, it may not be possible to interpret the global stability characteristics of the system. Thus, the stability analysis around the neighborhood of the fixed point is useful for many practical applications such as sustaining a non-linear system's state near or at the fixed point.
* In general, global asymptotic behaviors of any non-linear dynamical system can be complex and there are no systematic methods to predict and analyze such behaviors.



### References and Further Readings:

* Deshpande, A. M. Stablility of Fixed Point of a Dynamical System. [[web](https://adipandas.github.io/posts/2020/02/stable-unstable-fixed-point/)]
* Strogatz, Steven H. Nonlinear dynamics and chaos with student solutions manual: With applications to physics, biology, chemistry, and engineering. CRC press, 2018.
* Khalil, Hassan K. "Lyapunov stability." *Control Systems, Robotics and AutomatioN–Volume XII: Nonlinear, Distributed, and Time Delay Systems-I* (2009): 115.
* Bomze, Immanuel M., and Jörgen W. Weibull. "Does neutral stability imply Lyapunov stability?." *Games and Economic Behavior* 11.2 (1995): 173-192.
* Fixed point. [[web](https://mathworld.wolfram.com/FixedPoint.html)]
* Jacobian matrix [[video](https://www.youtube.com/watch?v=bohL918kXQk)]
* Stability Theory. [[web](https://en.wikipedia.org/wiki/Stability_theory)]
* Lyapunov Stability. [[web](https://en.wikipedia.org/wiki/Lyapunov_stability)]
