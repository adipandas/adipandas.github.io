---
title: 'Random Processes'
date: 2019-09-01
excerpt: The post explains the basics of **Random Processes**. Click [here](https://adipandas.github.io/posts/2019/09/random-process/) to read further.
permalink: /posts/2019/09/random-process/
tags:
  - Random Process
  - Stochastic Process
  - Randomness
  - Probability
---

Gaussian Processes allow the incorporation of prior knowlegde about the data while making predictions. These are a very powerful tool for regression as well as classification problems. Similarly, Reinforcement Learning (RL) also has Markov Processes and Markov Decision Processes (MDP) as its fundamental components. Both the topics have a commanality of Randomness/Stochasticity. While working with a RL agent, the stochasticity in the MDP is not about a single step in agent's life, but over the entire period of time the agent performs its actions. For each episode, it may take different actions to perform the same task because of the stochasticity involved in the process. Thus, the trajectories of this agent may differ for each episode. One can also think about any real life scenario or task. The observations are made over a period of time and they may be influenced by random effects. Here, the stochasticity is not just at a single instant but throughout the time interval.

Lets start thinking about it in terms of mathematics. A random variable holds an outcome of random experiment. For example, number of people standing in front of you right now. Randomly speaking, the number can be anything from the set of natural numbers $$N \equiv {0, 1, 2, 3, ...}$$ at the instance of observation. But this random experiment is over once you observe its outcome. Lets say, you observed 3 poeple standing in from of you.
Lets complicate our experiment. *What is the number of people standing in front of you overtime in a day?* Now, the random variable which holds a value from set $$N$$ will be different at each instance of obervation. And one needs to make observation for multiple instances for the entire day. Not just that, the series of counts you make will vary each day. It will not be the same. For this experiment, if you count the people standing in front of you for each instance of today, it will just be a *single realization* of all the possiblities of observations on different days. To understand stochasticity overtime, one needs to understand the **Random Processes**.

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

One should notice that assigning a value of 1 to H is a deterministic function, i.e., whenever one gets an outcome of the coin toss as H, we will always assign it a value of 1.

Let $$X$$ be random variable for the random experiment of tossing a coin.  
Here, $$X$$ is a deterministic function that assigns a real-value to outcome of experiment of tossing a coin.
Thus, we can write it as follows:  
$$X(H) = 1$$ and $$X(T)=0$$  
$$X(\xi)=x$$ where $$x\in\{0, 1\}$$ and $$\xi\in\{T, H\}$$.

Random variable in case of the above example of random experiment can take only discrete values. Thus, $$X$$ is called a discrete random variable. It is also possible for a random variable to take continuous values. For example, it the random experiment is measuring the height of an individual, the height is not a discrete number, it can take any value in the interval $$[0, \infty)$$.

Random Process
===
Random Process depends on random variable as well as time. In an experiment, one always takes into account the occurence of an event. While one is observing the experiment, the observations are done over a course of time. Multiple observations are made at different time instances. These observations are also effected by randomness. The randomness in the experiment does not effect only a single instance of the experiment, but its effects are seen over the complete period of time. A **random process** takes this time dependence into consideration.

### Definition:
The random process is an infinite indexed collection of random variables defined over a common probability space.  
Random process: $$\{X(t): t\in T\}$$  
This can be read as $$X(t)$$ is the random variable at index $$t$$ and $$t$$ is drawn from an index set $$T$$. The index set $$T$$ can be discrete where it make take values as $$\{1, 2, 3, ...\}$$. In continuous case it may take value in a range, for example the time of the experiment may fall in the interval $$[5, 10]$$.  
Here, the index parameter is typically a variable which accounts for time. But this value can also represent an indexing of a spatial domain.

A more intutive way to understand this definition is as follows -  
Random process: $$X(\xi, t)$$   
It is a function of the outcome of a random experiment $$\xi$$ at index $$t$$.

**Example of Random Process with temporal indexing:**
1. Noise in an IMU (inertial measurement unit) sensor which is moving at a constant speed.
  * The IMU sensor if measuring acceleration, its outcome at anytime can be written as $$a_{x}(t) = X(t)$$. Since, the velocity is constant, the experiment should result in perfect zeros. But as the sensor is noisy, the value in x direction at time $$t$$ may be some non-zero random value.
2. Price of a stock recorded every day.
  * Stock prices vary every day, and the variation if observed seems random.
  

**Example of Random Process with spatial indexing:**
1. Flipping of 4 unbiased coins at 4 different locations.
  * Coins are at 4 different locations. The indices representing these locations are $$T=\{1, 2, 3, 4\}$$.
  * All the coins are unbiased and the sample space for each coin toss is $$\{H, T\}$$. Each outcome is equally probable.
  * Random process is $$X(\xi, t)$$ where $$\xi \in \{H, T\}$$ and $$t \in \{1, 2, 3, 4\}$$.
  
  



