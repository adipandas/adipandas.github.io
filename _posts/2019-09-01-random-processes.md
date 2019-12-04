---
title: 'Random Processes'
date: 2019-09-01
excerpt: The post explains the basics of **Random Processes**. Click [here](https://adipandas.github.io/posts/2019/09/random-processes/) to read further.
permalink: /posts/2019/09/random-processes/
tags:
  - Random Process
  - Stochastic Process
  - Randomness
  - Probability
  - Machine Learning
---

Gaussian Processes allow the incorporation of prior knowledge about the data while making predictions. These are a very powerful tool for regression as well as classification problems. Similarly, Reinforcement Learning (RL) also has Markov Processes and Markov Decision Processes (MDP) as its fundamental components. Both the topics have a commonality of Randomness/Stochasticity. While working with a RL agent, the stochasticity in the MDP is not about a single step in the agent’s life, but over the entire period, the agent performs its actions. For each episode, it may take different actions to perform the same task because of the stochasticity involved in the process. Thus, the trajectories of this agent may differ for each episode. One can also think about any real-life scenario or task. The observations are made a timespan and they may be influenced by random effects. Here, the stochasticity is not just at a single instant but throughout the time interval.

Let us start thinking about it in terms of mathematics. A random variable holds the outcome of a random experiment. For example, several people standing in front of you right now. Randomly speaking, the number can be anything from the set of natural numbers $$N \equiv \{0, 1, 2, 3, ...\}$$ at the instance of observation. But this random experiment is over once you observe its outcome. Let's say, you observed 3 people standing in from of you.
Let's complicate our experiment. *What is the number of people standing in front of you over time in a day?* Now, the random variable which holds a value from set $$N$$ will take different values at each instance of observation. You will need to observe multiple instances for the entire day. Not just that, the set of observations you make will vary each day. It will not be the same. If you count the people standing in front of you for each instance of today, it will just be a *single realization* of all the possibilities of observations on different days. To understand this stochasticity over time, one needs to understand the **Random Processes**.

The rest of the page formalizes the idea of Random Processes.

Random Experiment
===
An experiment whose outcome cannot be predicted with certainty is called a Random Experiment.

Examples:
1. The lifetime of a light bulb.
2. Rolling a dice.
3. A coin toss.

Random Variable
===
A random variable is a *deterministic* function that assigns a real value to an outcome of a random experiment.

Example:  
Let there be an experiment of tossing a coin. This experiment may result in two outcomes, viz., Heads ($$H$$) or Tails ($$T$$). Mathematically speaking the sample space of this experiment can be defined as $$\{H, T\}$$. We can assign a numerical value to these possible outcomes of the sample space. Lets say, we call getting $$H$$ in the coin toss as $$1$$ and getting $$T$$ as $$0$$. Therefore, we can represent the sample space in terms of numerical value as $$\{1, 0\}$$.

One should notice that assigning a value of $$1$$ to $$H$$ is a deterministic function, i.e., whenever one gets an outcome of the coin toss as $$H$$, we will always assign it a value of $$1$$.

Let $$X$$ be random variable for the random experiment of tossing a coin.  
Here, $$X$$ is a deterministic function that assigns a real-value to outcome of experiment of tossing a coin.
Thus, we can write it as follows:  
$$X(H) = 1$$ and $$X(T)=0$$  
$$X(\xi)=x$$ where $$x\in\{0, 1\}$$ and $$\xi\in\{T, H\}$$. Note, how $$\xi$$ is a parameter to the function $$X$$ and the outcome is the value $$x$$.

Random variable in case of the above example of random experiment can take only discrete values. Thus, $$X$$ is called a discrete random variable. It is also possible for a random variable to take continuous values. For example, it the random experiment is measuring the height of an individual, the height is not a discrete number, it can take any value in the interval $$[0, \infty)$$.

Once, we observe the outcome of our experiment, there is no more randomness involved. For example, we observe a $$H$$ in a coin toss and thus, we have the information of the exact state of the experiment. More formally, this is known as **realization** of the random variable. In this case $$X(H)=1$$ is one realization of the random variable $$X$$ and $$X(T)=0$$ is another.

Random Processes
===
Random Process depends on a random variable as well as an indexing variable.  
In many stochastic processes, the indexing variable which will represent some index set will be related to a temporal dimension. For example, while one is observing a random experiment, the observations are done over a interval of time. Multiple observations are made at different time instances which may have been effected by randomness. This randomness does not effect only a single observation, but its effects are seen over the duration of the experiment. **Random process** can take the time of observation as an input parameter which will be represented as an indexing variable.

### Definition:
The random process is an infinite indexed collection of random variables defined over a common probability space.  
Random process: $$\{X(t): t\in T\}$$  
This can be read as $$X(t)$$ is the random variable at index $$t$$ and $$t$$ is drawn from an index set $$T$$. The index set $$T$$ can be discrete where it make take values as $$\{1, 2, 3, ...\}$$. In continuous case it may take value in a range, for example the time of the experiment may fall in the interval $$[5, 10]$$.  
Here, the index parameter is typically a variable which accounts for time. But this value can also represent an indexing of a spatial domain.

A more intutive way to understand this definition is as follows -  
Random process: $$X(\xi, t)$$ or $$X_{t}(\xi)$$  or $$X_{t}$$  
It is a function of the outcome of a random experiment $$\xi$$ at index $$t$$. Unless otherwise stated, a random process is represented by one of the above notations. The variable $$\xi$$ is omitted and the indexing is represented as the subscript for convenience of presentation in $$X_{t}$$. This page follows one of the conventions mentioned above unless otherwise stated.  

**Example of Random Process with temporal indexing:**
1. Noise in an IMU (inertial measurement unit) sensor which is moving at a constant speed from point A to point B on a road.
  * This IMU is measuring acceleration, its outcome at anytime can be written as $$a_{x}(t) = X(t)$$. Since, the velocity is constant, the experiment should result in perfect zeros. But as the sensor is noisy, the value in x direction at time $$t$$ may be some non-zero random value.
2. Price of a stock recorded every day.
  * Stock prices vary every day, and the variation if observed seems random.
  

**Example of Random Process with spatial indexing:**
1. Flipping of 4 unbiased coins at 4 different locations.
  * Coins are at 4 different locations. The indices representing these locations are $$T=\{1, 2, 3, 4\}$$.
  * All the coins are unbiased and the sample space for each coin toss is $$\{H, T\}$$. Each outcome is equally probable.
  * Random process is $$X(\xi, t)$$ where $$\xi \in \{H, T\}$$ and $$t \in \{1, 2, 3, 4\}$$.


As explained before, random process $$X(\xi, t)$$ an be understood as a function of two variables, $$\xi \in \Xi$$ and $$t \in T$$. Here, $$\Xi$$ is the sample space of random experiment underlying this random process and $$T$$ is the index set.  




