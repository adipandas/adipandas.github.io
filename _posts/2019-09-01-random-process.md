---
title: 'Random Process'
date: 2019-09-01
permalink: /posts/2019/09/random-process/
tags:
  - Random Process
  - Randomness
  - Probability
---

To understand a random process is very important to study Gaussian Processes and Markov Processes. This page explains the basics of what is Random Process.

Random Experiment
===
An experiment whose outcome cannot be predicted with certainty is called a Random Experiment.

Examples:
1. Life time of light bulb.
2. Rolling a dice.
3. A coin toss.

Random Variable
===
Random variable is a *deterministic* function that assigns a real value to an outcome of a random experiment.

Example:  
Let there be an experiment of tossing a coin. This experiment may result in two outcomes, viz., Heads (H) or Tails (T). Mathematically speaking the sample space of this experiment can be defined as {H, T}. We can assign a numerical value to these possible outcomes of the sample space. Lets say, we call getting H in coin toss as 1 and getting T as 0. Therefore, we can represent the sample space in terms of numerical value as {1, 0}.

One should notice that assigning a value if 1 to H is a deterministic function, i.e., whenever one gets an outcome of the coin toss as H, we will always assign it a value of 1.

Let $$X$$ be random variable for the random experiment of tossing a coin.  
$$X$$ is a deterministic function that assigns a real-value to outcome of random experiment.
Thus, we can write it as follows:  
$$X(H) = 1$$ and $$X(T)=0$$  
$$X(\xi)=x$$ where $$x\in\{0, 1\}$$ and $$\xi\in\{T, H\}$$.


Random variable in case of the above example of random experiment can take only discrete values. Thus, $$X$$ is called a discrete random variable. It is also possible for a random variable to take continuous values. For example, it the random experiment is measuring the height of an individual, the height is not a discrete number, it can take any value in the interval $$\[0, \infty)$$



