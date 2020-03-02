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
The function which maps one vector space to another vector space.

$$f: \Re^n \rightarrow \Re^m \label{eq4}$$

$$ \mathbf{y} = f(\mathbf{x}) \label{eq5}$$

Equation \eqref{eq4} maps an $$n$$-dimensional vector to a vector of $$m$$-dimensions. It is a *vector-valued function*. The output value $$\mathbf{y}$$ in \eqref{eq5} is of $$m$$-dimensions and the corresponding input value $$\mathbf{x}$$ is of $$n$$-dimensions.

## Gradient
Gradient of scalar-valued differentiable function is a vector field or vector-valued function.

$$\bigtriangledown f: \Re^n \rightarrow \Re^n \label{eq-grad1}$$

Gradient of vector-valued function at a point $$\mathbf{x}$$ in domain $$\mathit{X} \in \Re^n$$ is:

$$\bigtriangledown f(\mathbf{x}) =  \begin{bmatrix}
\frac{\partial f}{\partial x_{1}} \\ 
\frac{\partial f}{\partial x_{2}} \\ 
\vdots \\
\frac{\partial f}{\partial x_{n}}
\end{bmatrix}\label{eq-grad2}$$

At each point of a scalar-valued function, the gardient is a tangent vector, which represents an **infinitesimal change** in vector input. Notice that the gradient is represented as a column vector.

## Derivative

Derivative at each point of scalar-valued function is a co-tangent vector, a linear form which expresses how much the scalar output of a function changes for a given infinitesimal change in input vector. Derivative of a scalar valued function is represented as a row vector.

$$df(\mathbf{x}) = \begin{bmatrix}
\frac{\partial f}{\partial x_{1}} && \frac{\partial f}{\partial x_{2}} && \cdots && \frac{\partial f}{\partial x_{n}}
\end{bmatrix} \label{eq-derivative1}$$


$$df(\mathbf{x}) = \begin{bmatrix}
\frac{\partial f}{\partial x_{1}} \& \frac{\partial f}{\partial x_{2}} \& \cdots \& \frac{\partial f}{\partial x_{n}}
\end{bmatrix} \label{eq-derivative1}$$

<p style="text-align:center;"><img src="/images/vector_calculus/derivative_f.png" alt="derivative of f"/></p>


**Note: derivative is just a transpose of gradient.**

$$df(\mathbf{x}) = \bigtriangledown f(\mathbf{x})^{T} \label{eq-derivative2}$$


## Linear approximation of a scalar-valued function

Linear approximation of a function $$f(\mathbf{x})$$ at a point $$\mathbf{x_{0}} \in \Re^{n}$$:

$$f(\mathbf{x}) \approx f(\mathbf{x_0}) + (\bigtriangledown f)_{\mathbf{x_0}} (\mathbf{x} - \mathbf{x_0})$$







