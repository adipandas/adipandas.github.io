---
title: 'Notes on Vector Calculus'
date: 2020-03-01
permalink: /posts/2020/03/vector-calculus/
header:
  teaser: thumbnails/vector-calculus.svg
tags:
  - Vector Calculus
  - Notes
  - Geometry
  - Calculus
  - Gradient
  - Jacobian
  - Hessian
---

This post contains some of the important notes which come in handy while working with vector-calculus.


## Vector Space
A vector space is a collection of objects called vectors, which may be added together and multiplied/scaled by scalars. Scalars are often taken to be real numbers.

$$\mathbf{x} =  \begin{bmatrix}
 x_{1} \\ 
x_{2} \\ 
\vdots \\
x_{n}
\end{bmatrix}$$

$$\mathbf{x}$$ is a vector of $$n$$ dimensions.

## Function
A function is a relationship between two sets. It associates each element of the first set to exactly one element of the second set.

$$f: \mathit{X} \rightarrow \mathit{Y} \label{eq1}$$

$$\mathbf{x} \mapsto	f(\mathbf{x}) \label{eq2}$$

In equation \eqref{eq1}, the set represented by $$\mathit{X}$$ is called **domain** of function $$f$$ and $$\mathit{Y}$$ is called **codomain** of function $$f$$. This notation can be read as '*the function $$f$$ mapping elements of set $$\mathit{X}$$ to elements of set $$\mathit{Y}$$*'. Similarly, \eqref{eq2} can be read as '*$$f$$ maps $$\mathbf{x}$$ to $$f(\mathbf{x})$$*'.

## Scalar-valued function or Scalar field
The function which maps a vector to a scalar value.

$$f:\mathbb{R}^n \rightarrow \mathbb{R} \label{eq3}$$

$$ y = f(\mathbf{x}) \label{scalar-func}$$

Equation \eqref{eq3} maps an $$n$$-dimensional vector to a scalar value. It is a *scalar-valued function*. $$y$$ is a scalar and $$\mathbf{x}$$ is a vector of $$n$$-dimensions in \eqref{scalar-func}.

## Vector-valued function
A **vector-valued function** maps one vector space to another vector space.

$$\mathbf{f}: \mathbb{R}^n \rightarrow \mathbb{R}^m \label{eq4}$$

$$ \mathbf{y} = \mathbf{f}(\mathbf{x}) \label{eq5}$$

Equation \eqref{eq4} maps an $$n$$-dimensional vector to a vector of $$m$$-dimensions. It is a *vector-valued function*. The output value $$\mathbf{y}$$ in \eqref{eq5} is of $$m$$-dimensions and the corresponding input value $$\mathbf{x}$$ is of $$n$$-dimensions.

## Gradient
The **gradient** of a differentiable scalar-valued function is a vector field, i.e. it assigns a vector to every point of the domain.

$$\nabla f: \mathbb{R}^n \rightarrow \mathbb{R}^n \label{eq-grad1}$$

Gradient of a scalar-valued function at a point $$\mathbf{x}$$ of its domain $$\mathit{X} \subseteq \mathbb{R}^n$$ is:

$$\nabla f(\mathbf{x}) =  \begin{bmatrix}
\frac{\partial f}{\partial x_{1}} \\ 
\frac{\partial f}{\partial x_{2}} \\ 
\vdots \\
\frac{\partial f}{\partial x_{n}}
\end{bmatrix}\label{eq-grad2}$$

At each point of a scalar-valued function, a gradient is a tangent vector representing an **infinitesimal change** in vector input. Notice that here a column vector is used to represent the gradient of the function at point $$x$$.

## Derivative

Derivative at each point of the scalar-valued function is a co-tangent vector, a linear form that expresses how much the scalar output of a function changes for a given infinitesimal change in the input vector. Notice, we represent the derivative of a scalar-valued function as a row vector. This is unlike the gradient vector (that used column vector).

$$df(\mathbf{x}) =  \begin{bmatrix}
\frac{\partial f}{\partial x_{1}} & \frac{\partial f}{\partial x_{2}} & \cdots & \frac{\partial f}{\partial x_{n}}
\end{bmatrix} \label{eq-derivative1}$$

**Note: the derivative is just the transpose of the gradient.**

$$df(\mathbf{x}) = \nabla f(\mathbf{x})^{T} \label{eq-derivative2}$$

## Linear approximation of a scalar-valued function

Linear approximation of a function $$f(\mathbf{x})$$ at a point $$\mathbf{x_{0}} \in \mathbb{R}^{n}$$:

$$f(\mathbf{x}) \approx f(\mathbf{x_0}) + (\nabla f)_{\mathbf{x_0}}^{T} (\mathbf{x} - \mathbf{x_0}) \label{eq-linear-approx}$$

The transpose turns the column-vector gradient into the row-vector derivative, so that the correction term $$(\nabla f)_{\mathbf{x_0}}^{T} (\mathbf{x} - \mathbf{x_0})$$ is a scalar.


## Jacobian (a.k.a. derivative of Vector-valued Function)
<a name="jacobian"></a>

Derivative of $$\mathbf{f}$$ in equation \eqref{eq5} linearly maps the tangent space $$T_{\mathbf{x}}$$ to the tangent space $$T_{\mathbf{y}}$$.

First-order partial derivatives of a vector-valued function form the **Jacobian** matrix. We will denote the Jacobian by the notation $$\mathbf{J}$$.

$$\mathbf{J} = \begin{bmatrix}
\frac{\partial \mathbf{f}}{\partial x_{1}} & \frac{\partial \mathbf{f}}{\partial x_{2}} & \cdots & \frac{\partial \mathbf{f}}{\partial x_{n}}
\end{bmatrix} \label{eq-jacobian1}$$

$$\mathbf{J} = \begin{bmatrix}
\frac{\partial f_{1}}{\partial x_{1}} & \frac{\partial f_{1}}{\partial x_{2}} & \cdots & \frac{\partial f_{1}}{\partial x_{n}} \\
\vdots & \vdots & \ddots & \vdots \\
\frac{\partial f_{m}}{\partial x_{1}} & \frac{\partial f_{m}}{\partial x_{2}} & \cdots & \frac{\partial f_{m}}{\partial x_{n}}
\end{bmatrix} \label{eq-jacobian2}$$

**Note: Jacobian has the dimensions of $$m \times n$$.**

A Jacobian is the vertical stack of derivative vectors corresponding to each output element of vector $$\mathbf{y}$$ (i.e., row of the Jacobian matrix). This definition makes sense, and we can relate it to the derivative of a scalar-valued function defined above. The derivative of a scalar-valued function, $$m=1$$, is a row vector.

## Hessian matrix

Hessian matrix for scalar-valued function or scalar field given by \eqref{scalar-func} is a square matrix of **second order partial derivatives** of this scalar-valued function.

$$\mathbf{H} = \begin{bmatrix}
\frac{\partial^{2} f}{\partial x_{1}^{2}} & \frac{\partial^{2} f}{\partial x_{1} \partial x_{2}} & \cdots & \frac{\partial^{2} f}{\partial x_{1} \partial x_{n}} \\
\frac{\partial^{2} f}{\partial x_{2} \partial x_{1}} & \frac{\partial^{2} f}{\partial x_{2}^{2}} & \cdots & \frac{\partial^{2} f}{\partial x_{2} \partial x_{n}} \\
\vdots & \vdots & \ddots & \vdots \\
\frac{\partial^{2} f}{\partial x_{n} \partial x_{1}} & \frac{\partial^{2} f}{\partial x_{n} \partial x_{2}} & \cdots & \frac{\partial^{2} f}{\partial x_{n}^{2}}
\end{bmatrix} \label{eq-hessian}$$

**Note: Hessian has the dimensions of $$n \times n$$.**

### Symmetry of the Hessian

If the second-order partial derivatives of $$f$$ are continuous in a neighbourhood of $$\mathbf{x}$$, then by *Schwarz's theorem* the order of differentiation does not matter:

$$\frac{\partial^{2} f}{\partial x_{i} \partial x_{j}} = \frac{\partial^{2} f}{\partial x_{j} \partial x_{i}} \label{eq-schwarz}$$

So the Hessian is **symmetric**, $$\mathbf{H} = \mathbf{H}^{T}$$, and it is exactly the Jacobian of the gradient:

$$\mathbf{H} = \mathbf{J}(\nabla f) \label{eq-hessian-jacobian}$$

Symmetry is what makes the Hessian convenient in practice: a symmetric matrix has real eigenvalues and an orthogonal set of eigenvectors, so the *definiteness* of $$\mathbf{H}$$ classifies a stationary point (a point where $$\nabla f = \mathbf{0}$$):

* $$\mathbf{H}$$ positive definite $$\rightarrow$$ local minimum,
* $$\mathbf{H}$$ negative definite $$\rightarrow$$ local maximum,
* $$\mathbf{H}$$ indefinite $$\rightarrow$$ saddle point.

It also means only $$n(n+1)/2$$ of the $$n^{2}$$ entries need to be stored or estimated, which is why second-order and quasi-Newton methods keep symmetric approximations of $$\mathbf{H}$$.




