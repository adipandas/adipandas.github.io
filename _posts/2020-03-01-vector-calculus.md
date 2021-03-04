---
title: 'Notes on Vector Calculus'
date: 2020-03-01
permalink: /posts/2020/03/vector-calculus/
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
A function is relationship between two sets. It associates an element from frist set to exactly one element of second set.

$$f: \mathit{X} \rightarrow \mathit{Y} \label{eq1}$$

$$\mathbf{x} \mapsto	f(\mathbf{x}) \label{eq2}$$

In equation \eqref{eq1}, the set represented by $$\mathit{X}$$ is called **domain** of function $$f$$ and $$\mathit{Y}$$ is called **codomain** of function $$f$$. This notation can be read as '*the function $$f$$ mapping elements of set $$\mathit{X}$$ to elements of set $$\mathit{Y}$$*'. Similarly, \eqref{eq2} can be read as '*$$f$$ maps $$\mathbf{x}$$ to $$f(\mathbf{x})$$*'.

## Scalar-valued function or Scalar field
The function which maps a vector to a scalar value.

$$f:\Re^n \rightarrow \Re \label{eq3}$$

$$ y = f(\mathbf{x}) \label{scalar-func}$$

Equation \eqref{eq3} maps an $$n$$-dimensional vector to a scalar value. It is a *scalar-valued function*. $$y$$ is a scalar and $$\mathbf{x}$$ is a vector of $$n$$-dimensions in \eqref{scalar-func}.

## Vector-valued function
A **vector-valued function** maps one vector space to another vector space.

$$\mathbf{f}: \Re^n \rightarrow \Re^m \label{eq4}$$

$$ \mathbf{y} = \mathbf{f}(\mathbf{x}) \label{eq5}$$

Equation \eqref{eq4} maps an $$n$$-dimensional vector to a vector of $$m$$-dimensions. It is a *vector-valued function*. The output value $$\mathbf{y}$$ in \eqref{eq5} is of $$m$$-dimensions and the corresponding input value $$\mathbf{x}$$ is of $$n$$-dimensions.

## Gradient
The **gradient** of a scalar-valued differentiable function is also referred to as vector field or vector-valued function.

$$\bigtriangledown f: \Re^n \rightarrow \Re^n \label{eq-grad1}$$

Gradient of vector-valued function at a point $$\mathbf{x}$$ in domain $$\mathit{X} \in \Re^n$$ is:

$$\bigtriangledown f(\mathbf{x}) =  \begin{bmatrix}
\frac{\partial f}{\partial x_{1}} \\ 
\frac{\partial f}{\partial x_{2}} \\ 
\vdots \\
\frac{\partial f}{\partial x_{n}}
\end{bmatrix}\label{eq-grad2}$$

At each point of a scalar-valued function, a gradient is a tangent vector representing an **infinitesimal change** in vector input. Notice that here a column vector is used to represent the gradient of the function at point $$x$$.

## Derivative

Derivative at each point of the scalar-valued function is a co-tangent vector, a linear form that expresses how much the scalar output of a function changes for a given infinitesimal change in the input vector. Notice, we represent the derivative of a scalar-valued function as a row vector. This is unlike the gradient vector (that used column vector).

<p style="text-align:center;"><img src="/images/vector_calculus/derivative_f.png" alt="derivative of f"/></p> $$ \label{eq-derivative1}$$


**Note: derivative is just a transpose of gradient.**

$$df(\mathbf{x}) = \bigtriangledown f(\mathbf{x})^{T} \label{eq-derivative2}$$

## Linear approximation of a scalar-valued function

Linear approximation of a function $$f(\mathbf{x})$$ at a point $$\mathbf{x_{0}} \in \Re^{n}$$:

$$f(\mathbf{x}) \approx f(\mathbf{x_0}) + (\bigtriangledown f)_{\mathbf{x_0}} (\mathbf{x} - \mathbf{x_0})$$


## Derivative of Vector-valued Function (Jacobian)

Derivative of $$\mathbf{f}$$ in equation \eqref{eq5} linearly maps tangent space $$T_{\mathbf(x)}$$ to tanget space $$T_{\mathbf(y)}$$.

First order-partial derivative of vector-valued function forms the **Jacobian** matrix. We will denote the Jacobian by the notation $$\mathbf{J}$$

<p style="text-align:center;">
<img src="https://latex.codecogs.com/png.latex?\inline&space;\dpi{150}&space;\large&space;\mathbf{J}&space;=&space;\begin{bmatrix}&space;\frac{\partial&space;\mathbf{f}}{\partial&space;x_{1}}&space;&&space;\frac{\partial&space;\mathbf{f}}{\partial&space;x_{2}}&space;&&space;\cdots&space;&&space;\frac{\partial&space;\mathbf{f}}{\partial&space;x_{n}}&space;\end{bmatrix}" title="\large \mathbf{J} = \begin{bmatrix} \frac{\partial \mathbf{f}}{\partial x_{1}} & \frac{\partial \mathbf{f}}{\partial x_{2}} & \cdots & \frac{\partial \mathbf{f}}{\partial x_{n}} \end{bmatrix}" /></p>

<p style="text-align:center;">
<img src="https://latex.codecogs.com/png.latex?\inline&space;\dpi{150}&space;\large&space;\mathbf{J}&space;=&space;\begin{bmatrix}&space;\frac{\partial&space;f_{1}}{\partial&space;x_{1}}&space;&&space;\frac{\partial&space;f_{1}}{\partial&space;x_{2}}&space;&&space;\cdots&space;&&space;\frac{\partial&space;f_{1}}{\partial&space;x_{n}}\\&space;\vdots&space;&&space;\vdots&space;&&space;\ddots&space;&&space;\vdots\\&space;\frac{\partial&space;f_{m}}{\partial&space;x_{1}}&space;&&space;\frac{\partial&space;f_{m}}{\partial&space;x_{2}}&space;&&space;\cdots&space;&&space;\frac{\partial&space;f_{m}}{\partial&space;x_{n}}&space;\end{bmatrix}" title="\large \mathbf{J} = \begin{bmatrix} \frac{\partial f_{1}}{\partial x_{1}} & \frac{\partial f_{1}}{\partial x_{2}} & \cdots & \frac{\partial f_{1}}{\partial x_{n}}\\ \vdots & \vdots & \ddots & \vdots\\ \frac{\partial f_{m}}{\partial x_{1}} & \frac{\partial f_{m}}{\partial x_{2}} & \cdots & \frac{\partial f_{m}}{\partial x_{n}} \end{bmatrix}" /> </p>

Note: Jacobian has the dimensions of $$m \times n$$.

## Hessian matrix

Hessian matrix for scalar-valued function or scalar field given by \eqref{scalar-func} is a square matrix of **second order partial derivatives** of this scalar-valued function.

<p style="text-align:center;">
<img src="https://latex.codecogs.com/png.latex?\inline&space;\dpi{150}&space;\large&space;\mathbf{H}&space;=&space;\begin{bmatrix}&space;\frac{\partial&space;^{2}&space;f&space;}{\partial&space;x_{1}^2}&&space;\frac{\partial&space;^{2}&space;f&space;}{\partial&space;x_{1}&space;x_{2}}&space;&&space;\cdots&space;&&space;\frac{\partial&space;^{2}&space;f&space;}{\partial&space;x_{1}&space;x_{n}}\\&space;\frac{\partial&space;^{2}&space;f&space;}{\partial&space;x_{2}x_{1}}&&space;\frac{\partial&space;^{2}&space;f&space;}{\partial&space;x_{2}^2}&space;&&space;\cdots&space;&&space;\frac{\partial&space;^{2}&space;f&space;}{\partial&space;x_{2}&space;x_{n}}\\&space;\vdots&space;&&space;\vdots&space;&&space;\ddots&space;&&space;\vdots&space;\\&space;\frac{\partial&space;^{2}&space;f&space;}{\partial&space;x_{n}x_{1}}&space;&&space;\frac{\partial&space;^{2}&space;f&space;}{\partial&space;x_{n}&space;x_{2}}&space;&&space;\cdots&space;&&space;\frac{\partial&space;^{2}&space;f&space;}{\partial&space;x_{n}^2}&space;\end{bmatrix}" title="\large \mathbf{H} = \begin{bmatrix} \frac{\partial ^{2} f }{\partial x_{1}^2}& \frac{\partial ^{2} f }{\partial x_{1} x_{2}} & \cdots & \frac{\partial ^{2} f }{\partial x_{1} x_{n}}\\ \frac{\partial ^{2} f }{\partial x_{2}x_{1}}& \frac{\partial ^{2} f }{\partial x_{2}^2} & \cdots & \frac{\partial ^{2} f }{\partial x_{2} x_{n}}\\ \vdots & \vdots & \ddots & \vdots \\ \frac{\partial ^{2} f }{\partial x_{n}x_{1}} & \frac{\partial ^{2} f }{\partial x_{n} x_{2}} & \cdots & \frac{\partial ^{2} f }{\partial x_{n}^2} \end{bmatrix}" /></p>




