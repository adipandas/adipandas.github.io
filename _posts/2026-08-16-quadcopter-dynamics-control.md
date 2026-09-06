---
title: 'Quadcopter Dynamics and Control'
date: 2026-08-16
permalink: /posts/2026/08/quadcopter-dynamics-control/
header:
  teaser: thumbnails/quadcopter-dynamics-control.svg
tags:
  - UAV
  - Quadcopter
  - Dynamics
  - Control
  - PID
  - Rotation
---

These are my notes on quadcopter dynamics and control from my grad school days. 

Most papers state the equations of motion and then produce a finished mixer matrix a line or two later. The steps in between are left to the reader: where the small-angle approximation gets used, why yaw is treated differently from roll and pitch, how four rotor thrusts come out of four scalar demands.

A quadcopter has six degrees of freedom and four actuators, so it is underactuated. Thrust acts along a single body axis, so horizontal acceleration is available only by tilting that axis first, which couples translation to attitude. The cascaded controller in section 5 is built around that coupling.

Below is the rigid-body model, then a cascaded position-and-attitude controller built on top of it, then the control allocation (the "mixer") for the `+` and `X` rotor layouts. Everything stays symbolic over here. I have not put in parameters for any particular airframe, so none of the gains, limits or time constants mentioned below are measured values. I hope someone finds these notes useful.

## Conventions used here

Every sign below depends on the four choices listed here, and textbooks differ on all four. Mixing conventions between two sources produces equations that look correct term by term while carrying a sign error in one axis. That error usually survives simulation and shows up on hardware as a roll or pitch loop that diverges. Read this section before comparing anything below against another reference.

<ol type="i">
  <li>The world frame is <b>z-up</b> (an ENU-style frame). Gravity therefore acts along $-z_{world}$.</li>
  <li>The body frame has $x_{b}$ forward, $y_{b}$ left, $z_{b}$ up. Total rotor thrust acts along <b>$+z_{b}$</b>.</li>
  <li>Attitude uses <b>intrinsic z-y-x Euler angles</b>: yaw $\psi$ about the current $z$, then pitch $\theta$ about the new $y$, then roll $\phi$ about the new $x$.</li>
  <li>Angular velocity $\boldsymbol\omega = (p, q, r)^{T}$ is expressed in the <b>body</b> frame; the inertia tensor is written in the body frame too, which is what makes it constant.</li>
</ol>

If you work in a NED frame (z-down, thrust along $$-z_{b}$$), a number of the signs below flip.

## Notation

| Symbol | Description |
|---|---|
| $$m$$ | mass of the quadrotor |
| $$g$$ | acceleration due to gravity |
| $$l$$ | moment arm about the body $$x$$ and $$y$$ axes (see the geometry section; it means different things in the two layouts) |
| $$k_f$$ | rotor thrust (force) coefficient |
| $$k_m$$ | rotor drag (moment) coefficient |
| $$\omega_i$$ | angular speed of rotor $$i$$ |
| $$F_i, M_i$$ | thrust and reaction moment produced by rotor $$i$$ |
| $$i_{xx}, i_{yy}, i_{zz}$$ | principal mass moments of inertia about the body $$x, y, z$$ axes |
| $$\phi, \theta, \psi$$ | roll, pitch, yaw |
| $$p, q, r$$ | body angular rates about $$x_b, y_b, z_b$$ |
| $$\mathbf{x} = (x,y,z)^T$$ | position of the center of mass in the world frame |

The state is 12-dimensional, $$(\mathbf{x}, \dot{\mathbf{x}}, \phi, \theta, \psi, p, q, r)$$, and the input is 4-dimensional, $$(\omega_1, \omega_2, \omega_3, \omega_4)$$.

# 1. Rotations

I worked through the z-y-x sequence one rotation at a time in an [earlier post on Euler angles](/posts/2020/02/euler-rotation/). This section states the two results the dynamics need.

## Body to world

With the intrinsic z-y-x sequence, the rotation matrix that takes a vector's **body-frame coordinates** to its **world-frame coordinates** is the product $$R_{z}(\psi) R_{y}(\theta) R_{x}(\phi)$$:

$$
R = R^{w}_{b} =
\left[\begin{matrix}
c_{\psi} c_{\theta} & s_\phi s_\theta c_\psi - s_\psi c_\phi & s_\phi s_\psi + s_\theta c_\phi c_\psi \\
s_{\psi} c_\theta   & s_\phi s_\psi s_\theta + c_\phi c_\psi & -s_\phi c_\psi + s_\psi s_\theta c_\phi \\
-s_\theta           & s_\phi c_\theta                        & c_\phi c_\theta
\end{matrix}\right] \tag{1}
$$

where $$c_\alpha = \cos\alpha$$ and $$s_\alpha = \sin\alpha$$.

## World to body

Rotation matrices are orthogonal, so the inverse is simply the transpose:

$$
R^{b}_{w} = \left(R^{w}_{b}\right)^{-1} = \left(R^{w}_{b}\right)^{T} =
\left[\begin{matrix}
c_{\psi} c_{\theta}                    & s_{\psi} c_\theta                       & -s_\theta \\
s_\phi s_\theta c_\psi - s_\psi c_\phi & s_\phi s_\psi s_\theta + c_\phi c_\psi  & s_\phi c_\theta \\
s_\phi s_\psi + s_\theta c_\phi c_\psi & -s_\phi c_\psi + s_\psi s_\theta c_\phi & c_\phi c_\theta
\end{matrix}\right] \tag{2}
$$

Only the **third column** of $$R^{w}_{b}$$ ever appears in the translational dynamics, because thrust points along $$+z_b$$. That column,

$$\hat{z}_b = (\, s_\phi s_\psi + s_\theta c_\phi c_\psi, \;\; -s_\phi c_\psi + s_\psi s_\theta c_\phi, \;\; c_\phi c_\theta \,)^{T} \tag{3}$$

is the body $$z$$-axis written in world coordinates. The outer loop in section 5 chooses a direction for this unit vector, and the inner loop drives the airframe until $$\hat z_b$$ points that way.

## Euler rates and body rates are not the same thing

Euler rates $$(\dot\phi, \dot\theta, \dot\psi)$$ are the time derivatives of orientation angles relative to an external/inertial reference frame. Body rates $$(p,q,r)$$ are true angular velocity components measured directly around a moving object's own local axes. These are different objects, and the map between them is:


$$
\begin{pmatrix} p \\ q \\ r \end{pmatrix}
=
\underbrace{\left[\begin{matrix}
1 & 0       & -s_\theta \\
0 & c_\phi  & s_\phi c_\theta \\
0 & -s_\phi & c_\phi c_\theta
\end{matrix}\right]}_{W(\phi,\theta)}
\begin{pmatrix} \dot\phi \\ \dot\theta \\ \dot\psi \end{pmatrix} \tag{4}
$$

The inverse is the form you integrate in a simulator:

$$
\begin{pmatrix} \dot\phi \\ \dot\theta \\ \dot\psi \end{pmatrix}
=
\left[\begin{matrix}
1 & s_\phi \tan\theta & c_\phi \tan\theta \\
0 & c_\phi            & -s_\phi \\
0 & s_\phi / c_\theta & c_\phi / c_\theta
\end{matrix}\right]
\begin{pmatrix} p \\ q \\ r \end{pmatrix} \tag{5}
$$

Note the $$1/\cos\theta$$ terms: equation $$(5)$$ blows up at $$\theta = \pm\pi/2$$. This is gimbal lock. At that pitch the roll and yaw axes coincide, $$W$$ in $$(4)$$ drops to rank 2, and $$(\dot\phi, \dot\psi)$$ can no longer be recovered from $$(p,q,r)$$. The singularity is a property of the three-angle parameterization and disappears under quaternions or rotation matrices, which is what controllers written for aggressive flight use. I set out the [quaternion parameterization in a separate post](/posts/2020/01/quaternion-rotation/). Near hover $$W \approx I$$, so $$p \approx \dot\phi$$, $$q \approx \dot\theta$$ and $$r \approx \dot\psi$$. The controller in section 5 depends on that approximation quite heavily.

# 2. What a rotor produces

Before the equations of motion, a quick note on what a single rotor gives you.

Each rotor, spinning at speed $$\omega_i$$, produces a thrust along $$+z_b$$ and an aerodynamic drag moment about its own axis:

$$F_{i} = k_f \omega_{i}^2, \qquad M_{i} = k_m \omega_{i}^2, \qquad \Longrightarrow \qquad M_{i} = \frac{k_m}{k_{f}} F_{i} \tag{6}$$

The quadratic law comes from momentum theory. The coefficients $$k_f$$ and $$k_m$$ are identified experimentally on a thrust stand. Since $$F_i = k_f\omega_i^2$$, thrust can never be negative, because a fixed-pitch rotor cannot push down. That restriction matters in §6.3.

### The yaw torque and its sign

To keep rotor $$i$$ spinning against aerodynamic drag, the motor applies a torque to the rotor. By Newton's **third** law the rotor applies an equal and opposite torque to the airframe. So:

> **The reaction torque on the airframe is opposite in sense to the rotor's own spin.** A rotor turning clockwise when viewed from above (i.e. in the $$-z_b$$ sense) yaws the airframe in the $$+z_b$$ sense.

This is why the spin-direction column and the yaw-torque column in the table below carry opposite signs.

| Rotor | Spin (viewed from above) | Spin sense about $$z_b$$ | Contribution to yaw torque $$\tau_z$$ |
|---|---|---|---|
| 1 | clockwise | $$-$$ | $$+M_1$$ |
| 2 | anti-clockwise | $$+$$ | $$-M_2$$ |
| 3 | clockwise | $$-$$ | $$+M_3$$ |
| 4 | anti-clockwise | $$+$$ | $$-M_4$$ |

Hence, using equation $$(6)$$,

$$\tau_z = M_1 - M_2 + M_3 - M_4 = \frac{k_m}{k_f}\left(F_1 - F_2 + F_3 - F_4\right) \tag{7}$$

Two rotors spin each way so that, in level hover with equal thrusts, the four reaction torques cancel and the vehicle does not spin up.

# 3. Geometry: `+` versus `X`

<p style="text-align:center;"><img src="/images/quadcopter_dynamics/rotor-layouts.svg" alt="Plus and X quadcopter rotor layouts"/></p>

The two layouts differ only in where the rotors sit. Everything else over here applies to both.

Rotor $$i$$ sits at body-frame position $$(x_i, y_i, 0)$$ and pushes with $$\mathbf{F}_i = (0,0,F_i)^T$$. The moment it exerts about the center of mass is

$$\mathbf{r}_i \times \mathbf{F}_i = (\, y_i F_i, \;\; -x_i F_i, \;\; 0 \,)^{T} \tag{8}$$

so roll torque $$\tau_x = \sum_i y_i F_i$$ and pitch torque $$\tau_y = -\sum_i x_i F_i$$. Substituting the rotor positions of each layout gives the two results below.

**`+` layout.** Rotors sit at $$(l,0), (0,l), (-l,0), (0,-l)$$, so here $$l$$ *is* the arm length:

$$\tau_x = l\,(F_2 - F_4), \qquad \tau_y = l\,(-F_1 + F_3) \tag{9}$$

**`X` layout.** Rotors sit at $$(l,l), (l,-l), (-l,-l), (-l,l)$$:

$$\tau_x = l\,(F_1 - F_2 - F_3 + F_4), \qquad \tau_y = l\,(-F_1 - F_2 + F_3 + F_4) \tag{10}$$

> ### Watch out
>
> In the `X` layout $$l$$ is the half-span rather than the arm length. The center-to-rotor distance is $$L = l\sqrt{2}$$. If you take a `+` frame, rotate the electronics by 45° and reuse the same $$l$$, your roll and pitch gains come out wrong by a factor of $$\sqrt 2$$.
>
> It is also worth comparing the two layouts at equal center-to-rotor distance $$L$$. Perturb each rotor by $$\Delta F$$. The `+` layout gets $$\tau_x = 2L\,\Delta F$$ out of two rotors, while `X` gets $$\tau_x = \tfrac{L}{\sqrt 2}\cdot 4\Delta F = 2\sqrt{2}\,L\,\Delta F$$ out of all four. `X` therefore has about $$1.41\times$$ the roll and pitch authority at the same frame size.

# 4. Equations of motion

This is Newton and Euler, each written in the frame that keeps the algebra simple.

Newton's second law for the center of mass, written in the world frame:

$$
m \begin{pmatrix} \ddot x \\ \ddot y \\ \ddot z \end{pmatrix}
=
\begin{pmatrix} 0 \\ 0 \\ -mg \end{pmatrix}
+ R^{w}_{b} \begin{pmatrix} 0 \\ 0 \\ \sum_{i=1}^{4} F_{i} \end{pmatrix} \tag{11}
$$

and Euler's rotational equation for a rigid body, written in the body frame, where $$I$$ is constant:

$$
I \begin{pmatrix} \dot p \\ \dot q \\ \dot r \end{pmatrix}
= \boldsymbol\tau - \boldsymbol\omega \times \left( I \boldsymbol\omega \right),
\qquad
I = \left[\begin{matrix} i_{xx} & 0 & 0 \\ 0 & i_{yy} & 0 \\ 0 & 0 & i_{zz} \end{matrix}\right] \tag{12}
$$

The $$-\boldsymbol\omega \times (I\boldsymbol\omega)$$ term appears because the equation is written in the rotating body frame, where the components of $$I\boldsymbol\omega$$ change even while angular momentum is constant in the inertial frame. It is the source of the nonlinearity in $$(12)$$ and of the coupling between the three axes.


Substituting $$(3)$$ into $$(11)$$:

$$
\begin{align}
\ddot x &= \frac{\textstyle\sum_i F_i}{m}\left(s_\phi s_\psi + s_\theta c_\phi c_\psi\right) \tag{13}\\
\ddot y &= \frac{\textstyle\sum_i F_i}{m}\left(-s_\phi c_\psi + s_\psi s_\theta c_\phi\right) \tag{14}\\
\ddot z &= \frac{\textstyle\sum_i F_i}{m}\,c_\phi c_\theta \; - \; g \tag{15}
\end{align}
$$

And expanding $$(12)$$, the gyroscopic term $$\boldsymbol\omega \times I\boldsymbol\omega$$ has components $$qr(i_{zz}-i_{yy})$$, $$pr(i_{xx}-i_{zz})$$ and $$pq(i_{yy}-i_{xx})$$ along the body $$x$$, $$y$$ and $$z$$ axes:

$$
\begin{align}
i_{xx}\, \dot p &= \left(i_{yy} - i_{zz}\right) q r + \tau_x \tag{16}\\
i_{yy}\, \dot q &= \left(i_{zz} - i_{xx}\right) p r + \tau_y \tag{17}\\
i_{zz}\, \dot r &= \left(i_{xx} - i_{yy}\right) p q + \tau_z \tag{18}
\end{align}
$$

Together with the kinematics $$(5)$$, equations $$(13)$$–$$(18)$$ are the complete 12-state model.

# 5. Control architecture

<p style="text-align:center;"><img src="/images/quadcopter_dynamics/control-architecture.svg" alt="Cascaded quadcopter control architecture"/></p>

The controller is arranged as a cascade because the vehicle is underactuated. The split holds only while the attitude loop settles much faster than the position loop, which lets the outer loop treat its commanded tilt as achieved immediately. That separation is a requirement you impose when choosing the gains, not something the airframe gives you.

1. **Outer loop (slow).** A position PID converts position error into a *commanded acceleration* $$\ddot{\mathbf{x}}_c$$.
2. **Attitude/thrust extraction.** $$\ddot{\mathbf{x}}_c$$ is converted into a *desired tilt* $$(\phi_d, \theta_d)$$ and a *total thrust* $$\sum F_i$$. Yaw $$\psi_d$$ is free and commanded independently.
3. **Inner loop (fast).** An attitude PD converts attitude error into *commanded angular accelerations* $$(\dot p_c, \dot q_c, \dot r_c)$$.
4. **Allocation.** The mixer converts $$\left(\sum F_i, \dot p_c, \dot q_c, \dot r_c\right)$$ into four individual rotor thrusts, and then into motor speeds.

## 5.1 Outer loop: position PID

We want the position error $$\mathbf{e} = \mathbf{x}_d - \mathbf{x}$$ to obey a stable second-order ODE. Imposing

$$\left(\ddot{\mathbf{x}}_{d} - \ddot{\mathbf{x}}_{c}\right) + K_d \left(\dot{\mathbf{x}}_{d} - \dot{\mathbf{x}}\right) + K_p \left(\mathbf{x}_d - \mathbf{x}\right) + K_i \int \left(\mathbf{x}_d - \mathbf{x}\right) dt = \mathbf{0} \tag{19}$$

and solving for the commanded acceleration gives

$$\ddot{\mathbf{x}}_{c} = \ddot{\mathbf{x}}_{d} + K_d \left(\dot{\mathbf{x}}_{d} - \dot{\mathbf{x}}\right) + K_p \left(\mathbf{x}_d - \mathbf{x}\right) + K_i \int \left(\mathbf{x}_d - \mathbf{x}\right) dt \tag{20}$$

with diagonal gains $$K_p = \mathrm{diag}(k_{p_x}, k_{p_y}, k_{p_z})$$, and likewise $$K_d$$, $$K_i$$. For station keeping the feedforward term vanishes ($$\ddot{\mathbf{x}}_d = \mathbf{0}$$) and $$(20)$$ collapses to a plain PID. For trajectory tracking you keep $$\ddot{\mathbf{x}}_d$$ and $$\dot{\mathbf{x}}_d$$ as feedforward, which lets the vehicle follow a path instead of lagging permanently behind it.

Componentwise:

$$
\ddot{\mathbf{x}}_{c} =
\left[\begin{matrix}
k_{d_x} (\dot x_{d} - \dot x) + k_{p_x} (x_d - x) + k_{i_x} \int (x_d - x)\, dt \\
k_{d_y} (\dot y_{d} - \dot y) + k_{p_y} (y_d - y) + k_{i_y} \int (y_d - y)\, dt \\
k_{d_z} (\dot z_{d} - \dot z) + k_{p_z} (z_d - z) + k_{i_z} \int (z_d - z)\, dt
\end{matrix}\right]
=
\begin{pmatrix} \ddot x_c \\ \ddot y_c \\ \ddot z_c \end{pmatrix} \tag{21}
$$

The $$z$$ integrator matters here. Neither $$m$$ nor $$k_f$$ is known exactly, and without the integral term the vehicle settles a little below its altitude setpoint and stays there.

## 5.2 From acceleration to attitude

Now invert the translational dynamics. Setting $$\ddot x = \ddot x_c$$ etc. in $$(13)$$–$$(15)$$:

$$
\begin{align}
s_\phi s_\psi + s_\theta c_\phi c_\psi &= \frac{m\, \ddot x_c}{\sum_i F_i} \tag{22}\\
-s_\phi c_\psi + s_\psi s_\theta c_\phi &= \frac{m\, \ddot y_c}{\sum_i F_i} \tag{23}
\end{align}
$$

Near hover the tilt angles are small, and the total thrust nearly balances weight:

- $$\phi \to 0$$, so $$\sin\phi \approx \phi$$ and $$\cos\phi \approx 1$$
- $$\theta \to 0$$, so $$\sin\theta \approx \theta$$ and $$\cos\theta \approx 1$$
- the rotors very nearly carry the weight, so $$\sum_i F_i \approx mg$$

> **Yaw is not linearized.** $$\psi$$ can be anything; a hovering vehicle is free to point wherever it likes, so only $$\phi$$ and $$\theta$$ are assumed small. Keeping $$\sin\psi$$ and $$\cos\psi$$ exact is what makes the result below work at any heading. If you assume $$\psi \to 0$$ as well, $$(25)$$ holds only at zero heading; at any other heading the commanded tilt comes out rotated by $$\psi$$ in the horizontal plane, and the vehicle accelerates at an angle to the direction asked for.

With that, $$(22)$$ and $$(23)$$ become linear in $$\phi, \theta$$:

$$
\left[\begin{matrix}
s_\psi & c_\psi \\
-c_\psi & s_\psi
\end{matrix}\right]
\begin{pmatrix} \phi \\ \theta \end{pmatrix}
= \frac{1}{g} \begin{pmatrix} \ddot x_c \\ \ddot y_c \end{pmatrix} \tag{24}
$$

That $$2\times2$$ matrix has determinant $$s_\psi^2 + c_\psi^2 = 1$$, so it is orthogonal and inverts by transposition. There is no singularity here:

$$
\begin{pmatrix} \phi_{d} \\ \theta_{d} \end{pmatrix}
= \frac{1}{g}
\left[\begin{matrix}
s_\psi & -c_\psi \\
c_\psi & s_\psi
\end{matrix}\right]
\begin{pmatrix} \ddot x_c \\ \ddot y_c \end{pmatrix}
= \frac{1}{g}
\begin{pmatrix} \ddot x_c \sin\psi - \ddot y_c \cos\psi \\ \ddot x_c \cos\psi + \ddot y_c \sin\psi \end{pmatrix} \tag{25}
$$

Sanity check at $$\psi = 0$$: $$\theta_d = \ddot x_c / g$$ and $$\phi_d = -\ddot y_c / g$$. Pitching about $$+y$$ tilts the body $$z$$-axis toward $$+x$$, so positive pitch buys positive $$x$$-acceleration; rolling about $$+x$$ tilts it toward $$-y$$, hence the minus sign. Both agree with $$(3)$$.

In practice, make two changes to this. Replace $$g$$ with the commanded specific thrust $$\ddot z_c + g$$, which is exact rather than a hover approximation, and whose difference from $$g$$ grows with the commanded climb rate:

$$\phi_d = \frac{\ddot x_c \sin\psi - \ddot y_c \cos\psi}{\ddot z_c + g}, \qquad \theta_d = \frac{\ddot x_c \cos\psi + \ddot y_c \sin\psi}{\ddot z_c + g} \tag{26}$$

Then saturate $$\phi_d$$ and $$\theta_d$$ at some maximum tilt. Where you put that limit is a design choice, traded against how much horizontal acceleration you are willing to give up. The small-angle inversion is the first thing to break when the controller is pushed hard, and without a clamp a large position error can command a flip.

## 5.3 Total thrust

From $$(15)$$, with $$c_\phi c_\theta \approx 1$$ near hover:

$$\sum_{i=1}^{4} F_{i} = m\left(\ddot z_c + g\right) \tag{27}$$

For larger tilts, divide by $$c_\phi c_\theta$$ instead, since a banked vehicle needs more thrust to hold altitude. This is usually called tilt compensation, and it writes $$(27)$$ as $$\sum F_i = m(\ddot z_c + g)/(c_\phi c_\theta)$$.

## 5.4 Inner loop: attitude PD

The attitude loop drives the body toward $$(\phi_d, \theta_d, \psi_d)$$ by commanding angular accelerations:

$$
\begin{pmatrix} \dot p_c \\ \dot q_c \\ \dot r_c \end{pmatrix}
=
K_{p}^{att} \begin{pmatrix} \phi_{d}-\phi \\ \theta_{d} - \theta \\ \psi_{d} - \psi \end{pmatrix}
+ K_{d}^{att} \begin{pmatrix} p_{d}-p \\ q_{d} - q \\ r_{d} - r \end{pmatrix} \tag{28}
$$

with $$K_p^{att}$$ and $$K_d^{att}$$ diagonal. Equation $$(28)$$ pairs Euler-angle errors with body-rate errors. That is only legitimate because $$W \approx I$$ near hover, where $$p \approx \dot\phi$$, $$q \approx \dot\theta$$ and $$r \approx \dot\psi$$, so $$(28)$$ really is a PD law on each angle. At large tilt the pairing loses its meaning, and you then have to map the desired Euler rates through $$W$$ from $$(4)$$, or drop Euler angles and use a geometric $$SO(3)$$ controller.

Also wrap $$\psi_d - \psi$$ to $$(-\pi, \pi]$$. If you forget, a yaw setpoint that crosses $$\pm\pi$$ will send the vehicle spinning the long way round.

## 5.5 Simplifying the rotational dynamics

To turn $$(\dot p_c, \dot q_c, \dot r_c)$$ into torques, we use $$(16)$$–$$(18)$$. Near hover two things hold:

- The yaw rate is small, $$r \approx 0$$.
- The airframe is symmetric about the body $$x$$ and $$y$$ axes, $$i_{xx} \approx i_{yy}$$.

The first removes the $$qr$$ and $$pr$$ terms in $$(16)$$ and $$(17)$$, the second removes the $$pq$$ term in $$(18)$$. The gyroscopic coupling drops out, and three decoupled axes are left:

$$\tau_x \approx i_{xx}\,\dot p_c, \qquad \tau_y \approx i_{yy}\,\dot q_c, \qquad \tau_z \approx i_{zz}\,\dot r_c \tag{29}$$

(If you need the model to hold at high yaw rates, keep the full $$(16)$$–$$(18)$$ and add the gyroscopic terms back as feedforward. They are known exactly from the measured $$p, q, r$$.)

# 6. Control allocation (the mixer)

This is the step I could never find written out anywhere, so here it is in full.

We now have four scalar demands. Combining $$(9)$$/$$(10)$$, $$(7)$$, $$(27)$$ and $$(29)$$, and writing $$M_i = \tfrac{k_m}{k_f}F_i$$:

$$
\mathbf{u} =
\begin{pmatrix} u_1 \\ u_2 \\ u_3 \\ u_4 \end{pmatrix}
=
\begin{pmatrix}
\text{total thrust} \\ \text{roll} \\ \text{pitch} \\ \text{yaw}
\end{pmatrix}
=
\left[\begin{matrix}
m\left(\ddot z_c + g\right) \\[2pt]
\dfrac{i_{xx}\, \dot p_c}{l} \\[6pt]
\dfrac{i_{yy}\, \dot q_c}{l} \\[6pt]
\dfrac{k_{f}\, i_{zz}\, \dot r_c}{k_{m}}
\end{matrix}\right] \tag{30}
$$

and the four thrusts relate to $$\mathbf{u}$$ through a constant mixer matrix $$\mathcal{M}$$, with $$\mathcal{M}\,\mathbf{F} = \mathbf{u}$$ and $$\mathbf{F} = \mathcal{M}^{-1}\mathbf{u}$$. Only $$\mathcal{M}$$ changes between layouts.

## 6.1 `+` layout

$$
\underbrace{\left[\begin{matrix}
1 & 1 & 1 & 1 \\
0 & 1 & 0 & -1 \\
-1 & 0 & 1 & 0 \\
1 & -1 & 1 & -1
\end{matrix}\right]}_{\mathcal{M}_{+}}
\begin{pmatrix} F_{1}\\ F_{2} \\ F_{3}\\ F_{4} \end{pmatrix}
= \mathbf{u},
\qquad
\mathcal{M}_{+}^{-1} =
\left[\begin{matrix}
\tfrac{1}{4} & 0            & -\tfrac{1}{2} & \tfrac{1}{4}\\
\tfrac{1}{4} & \tfrac{1}{2} & 0             & -\tfrac{1}{4}\\
\tfrac{1}{4} & 0            & \tfrac{1}{2}  & \tfrac{1}{4}\\
\tfrac{1}{4} & -\tfrac{1}{2}& 0             & -\tfrac{1}{4}
\end{matrix}\right] \tag{31}
$$

$$
\begin{pmatrix} F_{1}\\ F_{2} \\ F_{3}\\ F_{4} \end{pmatrix}
=
\left[\begin{matrix}
\frac{m(\ddot z_c + g)}{4} - \frac{i_{yy} \dot q_c}{2l} + \frac{k_{f} i_{zz} \dot r_c}{4 k_{m}} \\[4pt]
\frac{m(\ddot z_c + g)}{4} + \frac{i_{xx} \dot p_c}{2l} - \frac{k_{f} i_{zz} \dot r_c}{4 k_{m}} \\[4pt]
\frac{m(\ddot z_c + g)}{4} + \frac{i_{yy} \dot q_c}{2l} + \frac{k_{f} i_{zz} \dot r_c}{4 k_{m}} \\[4pt]
\frac{m(\ddot z_c + g)}{4} - \frac{i_{xx} \dot p_c}{2l} - \frac{k_{f} i_{zz} \dot r_c}{4 k_{m}}
\end{matrix}\right] \tag{32}
$$

The structure can be read straight off the inverse. Rotors 2 and 4 sit on the $$y$$-axis, so they carry all of the roll authority at weight $$\tfrac{1}{2}$$ and contribute nothing to pitch; rotors 1 and 3 do the same for pitch. Roll and pitch are each produced by two motors instead of four, which is what limits the control authority of this layout.

## 6.2 `X` layout

$$
\underbrace{\left[\begin{matrix}
1 & 1 & 1 & 1 \\
1 & -1 & -1 & 1 \\
-1 & -1 & 1 & 1 \\
1 & -1 & 1 & -1
\end{matrix}\right]}_{\mathcal{M}_{X}}
\begin{pmatrix} F_{1}\\ F_{2} \\ F_{3}\\ F_{4} \end{pmatrix}
= \mathbf{u} \tag{33}
$$

The rows of $$\mathcal{M}_{X}$$ are mutually orthogonal and each has norm $$2$$. The matrix is therefore $$2 \times$$ an orthogonal matrix (a $$\pm 1$$ Hadamard-type matrix), and the inverse is the scaled transpose, $$\mathcal{M}_{X}^{-1} = \tfrac{1}{4}\mathcal{M}_{X}^{T}$$:

$$
\mathcal{M}_{X}^{-1} =
\frac{1}{4}\left[\begin{matrix}
1 & 1 & -1 & 1\\
1 & -1 & -1 & -1\\
1 & -1 & 1 & 1\\
1 & 1 & 1 & -1
\end{matrix}\right] \tag{34}
$$

$$
\begin{pmatrix} F_{1}\\ F_{2} \\ F_{3}\\ F_{4} \end{pmatrix}
=
\left[\begin{matrix}
\frac{m}{4} & \frac{i_{xx}}{4l}  & -\frac{i_{yy}}{4l} & \frac{k_{f} i_{zz}}{4 k_{m}} \\[4pt]
\frac{m}{4} & -\frac{i_{xx}}{4l} & -\frac{i_{yy}}{4l} & -\frac{k_{f} i_{zz}}{4 k_{m}}\\[4pt]
\frac{m}{4} & -\frac{i_{xx}}{4l} & \frac{i_{yy}}{4l}  & \frac{k_{f} i_{zz}}{4 k_{m}}\\[4pt]
\frac{m}{4} & \frac{i_{xx}}{4l}  & \frac{i_{yy}}{4l}  & -\frac{k_{f} i_{zz}}{4 k_{m}}
\end{matrix}\right]
\begin{pmatrix} \ddot z_c + g \\ \dot p_c \\ \dot q_c \\ \dot r_c \end{pmatrix} \tag{35}
$$

Every rotor contributes to every channel at the same weight $$\tfrac{1}{4}$$, which is the row orthogonality above appearing in the inverse. Control effort is distributed equally over the four motors, so none of them reaches saturation ahead of the others.

Since $$\mathcal{M}$$ is constant, both mixers cost four multiply-accumulates per rotor and can run at the inner-loop rate.

## 6.3 From thrusts to motor commands

Finally, invert $$(6)$$:

$$\omega_i = \sqrt{\frac{F_i}{k_f}} \tag{36}$$

Clip $$F_i$$ at both ends before taking the square root:

- Clip to $$F_i \ge 0$$. A fixed-pitch rotor cannot produce negative thrust, but $$(32)$$ and $$(35)$$ will ask for it during an aggressive maneuver.
- Clip to $$F_i \le F_{max}$$, and take care over how. Saturating each motor independently rotates the resulting torque vector away from the commanded direction, so the vehicle still flies and the symptom is a sluggish or cross-coupled response rather than an outright failure. The usual fix is to rank the channels: roll and pitch first, because they keep the vehicle upright, then yaw, and let total thrust absorb what is left.

# 7. What the model leaves out

This is the standard model, and it holds up well for hover and gentle flight. It also leaves out a fair amount:

- Rotor gyroscopic torque. The rotors carry angular momentum of their own, so a body rotation produces $$-J_r \Omega_r\,\boldsymbol\omega \times \hat z_b$$, where $$J_r$$ is the rotor polar inertia and $$\Omega_r$$ is the net rotor spin resolved along $$+z_b$$. Under the convention used here, rotors 1 and 3 turn in the $$-z_b$$ sense and rotors 2 and 4 in the $$+z_b$$ sense, so $$\Omega_r = -\omega_1 + \omega_2 - \omega_3 + \omega_4$$. Much of the literature writes this with the signs reversed, which corresponds to the opposite spin assignment; note that $$\Omega_r$$ is opposite in sign to the yaw-torque pattern in $$(7)$$, since the reaction torque opposes the spin. The term scales with body rate, so it is small at hover and matters mainly during fast rolls.
- Motor dynamics. $$\omega_i$$ is treated as something you can set instantly. A real ESC and motor have a finite rise time, and that time constant puts a ceiling on inner-loop bandwidth.
- Aerodynamics: body drag, blade flapping, induced velocity, ground effect. Blade flapping produces a velocity-dependent pitching moment for which the model above has no term at all, so I would expect it to be the omission that matters first as airspeed rises.
- Off-diagonal inertia, i.e. the assumption that the body axes are the principal axes.
- Frame flex. Vibration from the arms couples into the gyros, and is usually filtered rather than modeled.
- Battery sag, which drifts $$k_f$$ as the voltage drops. The altitude integrator absorbs most of this.

# Summary

| Quantity | Result |
|---|---|
| Body $$z$$-axis in world frame | $$(s_\phi s_\psi + s_\theta c_\phi c_\psi,\; -s_\phi c_\psi + s_\psi s_\theta c_\phi,\; c_\phi c_\theta)$$ |
| Translation | $$m\ddot{\mathbf{x}} = -mg\hat{z}_w + R^{w}_{b}(0,0,\textstyle\sum F_i)^T$$ |
| Rotation | $$I\dot{\boldsymbol\omega} = \boldsymbol\tau - \boldsymbol\omega \times I\boldsymbol\omega$$ |
| Desired tilt | $$\phi_d = \frac{\ddot x_c s_\psi - \ddot y_c c_\psi}{\ddot z_c + g}$$, $$\;\theta_d = \frac{\ddot x_c c_\psi + \ddot y_c s_\psi}{\ddot z_c + g}$$ |
| Total thrust | $$\sum F_i = m(\ddot z_c + g)$$ |
| `+` mixer, eq. $$(31)$$ | rows $$(1,1,1,1)$$, $$(0,1,0,-1)$$, $$(-1,0,1,0)$$, $$(1,-1,1,-1)$$; $$\det = -8$$ |
| `X` mixer, eq. $$(33)$$ | rows $$(1,1,1,1)$$, $$(1,-1,-1,1)$$, $$(-1,-1,1,1)$$, $$(1,-1,1,-1)$$; $$\mathcal{M}_X^{-1} = \tfrac{1}{4}\mathcal{M}_X^{T}$$ |
| Motor command | $$\omega_i = \sqrt{F_i / k_f}$$, after clipping $$F_i$$ to $$[0, F_{max}]$$ |

Thrust acts only along $$+z_b$$, so horizontal motion requires tilt. The outer loop chooses a direction for $$\hat z_b$$, the inner loop drives the airframe to the attitude that achieves it, and the mixer distributes the four resulting demands over four rotors subject to $$F_i \ge 0$$.

#### Note
If you come across any errors, please let me know. I will be happy to fix it.  
Happy reading!! :smiley:

## References

1. R. Mahony, V. Kumar and P. Corke, "Multirotor Aerial Vehicles: Modeling, Estimation, and Control of Quadrotor," *IEEE Robotics & Automation Magazine*, vol. 19, no. 3, pp. 20–32, 2012.
2. D. Mellinger and V. Kumar, "Minimum snap trajectory generation and control for quadrotors," *IEEE ICRA*, 2011.
3. T. Lee, M. Leok and N. H. McClamroch, "Geometric tracking control of a quadrotor UAV on SE(3)," *IEEE CDC*, 2010.
4. F. Hover and M. Triantafyllou, "System Design for Uncertainty," MIT OCW 2.017J, [chapter on rotations](https://ocw.mit.edu/courses/mechanical-engineering/2-017j-design-of-electromechanical-robotic-systems-fall-2009/course-text/MIT2_017JF09_ch09.pdf).
