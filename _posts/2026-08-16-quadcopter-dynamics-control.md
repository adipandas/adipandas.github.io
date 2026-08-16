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

The controller worked. That was the frustrating part.

I could fly the quadrotor and tune its gains, but *why* the control law had the shape it did stayed a mystery. The papers I turned to state the equations of motion and then jump, often in a single line, to a finished mixer matrix. The steps in between — where the small-angle approximation enters, why yaw is treated differently from roll and pitch, how four rotor thrusts fall out of four scalar demands — are left as an exercise, or omitted altogether.

So I sat down and derived the whole thing from scratch, writing out every line I had to work out for myself. This post is that derivation. I wrote it during grad school, then filed it away and never published it — so here it is, finally seeing the light of day.

A quadcopter has six degrees of freedom but only four independent actuators. That single sentence explains almost everything about how these vehicles are modelled and flown: the system is **underactuated**, so translation has to be bought with attitude. You cannot slide sideways without first tipping over.

This post derives the full rigid-body model of a quadrotor, then builds a cascaded position-and-attitude controller on top of it, and finishes with the **control allocation** (the "mixer") for both the `+` and the `X` rotor layouts.

## Conventions used here

Every sign in this post follows from the four choices below. Different textbooks pick differently, and mixing conventions is the single most common source of sign errors in quadrotor code — so it is worth fixing these in mind before reading on.

<ol type="i">
  <li>The world frame is <b>z-up</b> (an ENU-style frame). Gravity therefore acts along $-z_{world}$.</li>
  <li>The body frame has $x_{b}$ forward, $y_{b}$ left, $z_{b}$ up. Total rotor thrust acts along <b>$+z_{b}$</b>.</li>
  <li>Attitude uses <b>intrinsic z-y-x Euler angles</b>: yaw $\psi$ about the current $z$, then pitch $\theta$ about the new $y$, then roll $\phi$ about the new $x$.</li>
  <li>Angular velocity $\boldsymbol\omega = (p, q, r)^{T}$ is expressed in the <b>body</b> frame; the inertia tensor is written in the body frame too, which is what makes it constant.</li>
</ol>

If you use a NED frame (z-down, thrust along $$-z_{b}$$), several signs below flip. The physics does not change; the bookkeeping does.

## Notation

| Symbol | Description |
|---|---|
| $$m$$ | mass of the quadrotor |
| $$g$$ | acceleration due to gravity |
| $$l$$ | moment arm about the body $$x$$ and $$y$$ axes (see the geometry section — it means different things in the two layouts) |
| $$k_f$$ | rotor thrust (force) coefficient |
| $$k_m$$ | rotor drag (moment) coefficient |
| $$\omega_i$$ | angular speed of rotor $$i$$ |
| $$F_i, M_i$$ | thrust and reaction moment produced by rotor $$i$$ |
| $$i_{xx}, i_{yy}, i_{zz}$$ | principal mass moments of inertia about the body $$x, y, z$$ axes |
| $$\phi, \theta, \psi$$ | roll, pitch, yaw |
| $$p, q, r$$ | body angular rates about $$x_b, y_b, z_b$$ |
| $$\mathbf{x} = (x,y,z)^T$$ | position of the centre of mass in the world frame |

The state is 12-dimensional: $$(\mathbf{x}, \dot{\mathbf{x}}, \phi, \theta, \psi, p, q, r)$$. The input is 4-dimensional: $$(\omega_1, \omega_2, \omega_3, \omega_4)$$. The gap between 6 and 4 is the underactuation.

# 1. Rotations

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

is the body $$z$$-axis expressed in world coordinates. **Steering a quadrotor is nothing more than pointing this unit vector.**

## Euler rates and body rates are not the same thing

The Euler rates $$(\dot\phi, \dot\theta, \dot\psi)$$ are rates of three angles measured about three *different, non-orthogonal* axes; the body rates $$(p,q,r)$$ are components of one angular velocity vector in one orthogonal frame. The map between them is:

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

and its inverse, which is what you actually integrate in a simulator:

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

Note the $$1/\cos\theta$$ terms: equation $$(5)$$ blows up at $$\theta = \pm\pi/2$$. This is **gimbal lock**, and it is a defect of the Euler-angle *parameterisation*, not of the vehicle. It is the main reason aggressive-flight controllers use quaternions or rotation matrices instead. Near hover, $$W \approx I$$, so $$p \approx \dot\phi$$, $$q \approx \dot\theta$$, $$r \approx \dot\psi$$ — an approximation the controller below leans on heavily.

# 2. What a rotor produces

Each rotor, spinning at speed $$\omega_i$$, produces a thrust along $$+z_b$$ and an aerodynamic drag moment about its own axis:

$$F_{i} = k_f \omega_{i}^2, \qquad M_{i} = k_m \omega_{i}^2, \qquad \Longrightarrow \qquad M_{i} = \frac{k_m}{k_{f}} F_{i} \tag{6}$$

The quadratic law comes from momentum theory; $$k_f$$ and $$k_m$$ are identified experimentally on a thrust stand. Because $$F_i = k_f\omega_i^2$$, thrust is always **non-negative** — a fixed-pitch rotor cannot push down. Remember this when you get to the mixer.

### The yaw torque and its sign

To keep rotor $$i$$ spinning against aerodynamic drag, the motor applies a torque to the rotor. By Newton's **third** law the rotor applies an equal and opposite torque to the airframe. So:

> **The reaction torque on the airframe is opposite in sense to the rotor's own spin.** A rotor turning clockwise when viewed from above (i.e. in the $$-z_b$$ sense) yaws the airframe in the $$+z_b$$ sense.

This is why the spin-direction column and the yaw-torque column in the table below have opposite signs. Conflating the two is a classic bug.

| Rotor | Spin (viewed from above) | Spin sense about $$z_b$$ | Contribution to yaw torque $$\tau_z$$ |
|:---:|:---|:---:|:---:|
| 1 | clockwise | $$-$$ | $$+M_1$$ |
| 2 | anti-clockwise | $$+$$ | $$-M_2$$ |
| 3 | clockwise | $$-$$ | $$+M_3$$ |
| 4 | anti-clockwise | $$+$$ | $$-M_4$$ |

Hence

$$\tau_z = M_1 - M_2 + M_3 - M_4 = \frac{k_m}{k_f}\left(F_1 - F_2 + F_3 - F_4\right) \tag{7}$$

Two rotors spin each way so that, in level hover with equal thrusts, the four reaction torques cancel and the vehicle does not spin up.

# 3. Geometry: `+` versus `X`

<p style="text-align:center;"><img src="/images/quadcopter_dynamics/rotor-layouts.svg" alt="Plus and X quadcopter rotor layouts"/></p>

Rotor $$i$$ sits at body-frame position $$(x_i, y_i, 0)$$ and pushes with $$\mathbf{F}_i = (0,0,F_i)^T$$. The moment it exerts about the centre of mass is

$$\mathbf{r}_i \times \mathbf{F}_i = (\, y_i F_i, \;\; -x_i F_i, \;\; 0 \,)^{T} \tag{8}$$

so roll torque $$\tau_x = \sum_i y_i F_i$$ and pitch torque $$\tau_y = -\sum_i x_i F_i$$. Everything else follows mechanically.

**`+` layout** — rotors at $$(l,0), (0,l), (-l,0), (0,-l)$$, so here $$l$$ *is* the arm length:

$$\tau_x = l\,(F_2 - F_4), \qquad \tau_y = l\,(-F_1 + F_3) \tag{9}$$

**`X` layout** — rotors at $$(l,l), (l,-l), (-l,-l), (-l,l)$$:

$$\tau_x = l\,(F_1 - F_2 - F_3 + F_4), \qquad \tau_y = l\,(-F_1 - F_2 + F_3 + F_4) \tag{10}$$

> ### A trap worth flagging
>
> In the `X` layout, $$l$$ is the **half-span**, *not* the arm length. The centre-to-rotor distance is $$L = l\sqrt{2}$$. If you take a `+` frame, rotate the electronics 45°, and reuse the same $$l$$, your roll and pitch gains will be off by $$\sqrt 2$$.
>
> Comparing the two layouts *at equal centre-to-rotor distance $$L$$*, and perturbing each rotor by $$\Delta F$$: the `+` layout gets $$\tau_x = 2L\,\Delta F$$ from two rotors, while the `X` layout gets $$\tau_x = \tfrac{L}{\sqrt 2}\cdot 4\Delta F = 2\sqrt{2}\,L\,\Delta F$$ from all four. The `X` layout therefore has $$\sqrt{2} \approx 1.41\times$$ more roll and pitch authority — which is exactly why almost every modern airframe flies in `X`.

# 4. Equations of motion

Two laws, no more. **Newton's second law** for the centre of mass, written in the world frame:

$$
m \begin{pmatrix} \ddot x \\ \ddot y \\ \ddot z \end{pmatrix}
=
\begin{pmatrix} 0 \\ 0 \\ -mg \end{pmatrix}
+ R^{w}_{b} \begin{pmatrix} 0 \\ 0 \\ \sum_{i=1}^{4} F_{i} \end{pmatrix} \tag{11}
$$

and **Euler's rotational equation** for a rigid body, written in the body frame (where $$I$$ is constant):

$$
I \begin{pmatrix} \dot p \\ \dot q \\ \dot r \end{pmatrix}
= \boldsymbol\tau - \boldsymbol\omega \times \left( I \boldsymbol\omega \right),
\qquad
I = \left[\begin{matrix} i_{xx} & 0 & 0 \\ 0 & i_{yy} & 0 \\ 0 & 0 & i_{zz} \end{matrix}\right] \tag{12}
$$

The $$-\boldsymbol\omega \times (I\boldsymbol\omega)$$ term is not a torque; it is the price of writing Newton's law in a rotating frame. It is what makes the rotational dynamics nonlinear and coupled.

*(A common slip is to attribute the equations of motion to Newton's third law. The third law shows up only in the rotor reaction torque of §2 — the equations themselves are the second law plus Euler's equation.)*

## Expanded, in scalars

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

Because the vehicle is underactuated, control is organised as a **cascade** that exploits a natural timescale separation — attitude responds far faster than position:

1. **Outer loop (slow).** A position PID converts position error into a *commanded acceleration* $$\ddot{\mathbf{x}}_c$$.
2. **Attitude/thrust extraction.** $$\ddot{\mathbf{x}}_c$$ is converted into a *desired tilt* $$(\phi_d, \theta_d)$$ and a *total thrust* $$\sum F_i$$. Yaw $$\psi_d$$ is free and commanded independently.
3. **Inner loop (fast).** An attitude PD converts attitude error into *commanded angular accelerations* $$(\dot p_c, \dot q_c, \dot r_c)$$.
4. **Allocation.** The mixer converts $$\left(\sum F_i, \dot p_c, \dot q_c, \dot r_c\right)$$ into four individual rotor thrusts, and then into motor speeds.

## 5.1 Outer loop: position PID

We want the position error $$\mathbf{e} = \mathbf{x}_d - \mathbf{x}$$ to obey a stable second-order ODE. Imposing

$$\left(\ddot{\mathbf{x}}_{d} - \ddot{\mathbf{x}}_{c}\right) + K_d \left(\dot{\mathbf{x}}_{d} - \dot{\mathbf{x}}\right) + K_p \left(\mathbf{x}_d - \mathbf{x}\right) + K_i \int \left(\mathbf{x}_d - \mathbf{x}\right) dt = \mathbf{0} \tag{19}$$

and solving for the commanded acceleration gives

$$\ddot{\mathbf{x}}_{c} = \ddot{\mathbf{x}}_{d} + K_d \left(\dot{\mathbf{x}}_{d} - \dot{\mathbf{x}}\right) + K_p \left(\mathbf{x}_d - \mathbf{x}\right) + K_i \int \left(\mathbf{x}_d - \mathbf{x}\right) dt \tag{20}$$

with diagonal gains $$K_p = \mathrm{diag}(k_{p_x}, k_{p_y}, k_{p_z})$$, and likewise $$K_d$$, $$K_i$$. For **station keeping** the feedforward term vanishes ($$\ddot{\mathbf{x}}_d = \mathbf{0}$$) and $$(20)$$ reduces to a plain PID; for **trajectory tracking** you keep $$\ddot{\mathbf{x}}_d$$ and $$\dot{\mathbf{x}}_d$$ as feedforward, which is what makes tracking accurate rather than merely stable.

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

The $$z$$ integrator is doing real work here: it absorbs the unavoidable error in $$m$$ and $$k_f$$ so the vehicle does not sit permanently below its altitude setpoint.

## 5.2 From acceleration to attitude

Now invert the translational dynamics. Setting $$\ddot x = \ddot x_c$$ etc. in $$(13)$$–$$(15)$$:

$$
\begin{align}
s_\phi s_\psi + s_\theta c_\phi c_\psi &= \frac{m\, \ddot x_c}{\sum_i F_i} \tag{22}\\
-s_\phi c_\psi + s_\psi s_\theta c_\phi &= \frac{m\, \ddot y_c}{\sum_i F_i} \tag{23}
\end{align}
$$

Near hover the **tilt** angles are small, and the total thrust nearly balances weight:

- $$\phi \to 0$$, so $$\sin\phi \approx \phi$$ and $$\cos\phi \approx 1$$
- $$\theta \to 0$$, so $$\sin\theta \approx \theta$$ and $$\cos\theta \approx 1$$
- the rotors very nearly carry the weight, so $$\sum_i F_i \approx mg$$

> **Yaw is *not* linearised.** $$\psi$$ can be anything — the vehicle is free to point wherever it likes while hovering. Only $$\phi$$ and $$\theta$$ are assumed small. Keeping $$\sin\psi$$ and $$\cos\psi$$ exact is precisely what makes the result below yaw-aware, and assuming $$\psi \to 0$$ as well would silently break it.

With that, $$(22)$$ and $$(23)$$ become linear in $$\phi, \theta$$:

$$
\left[\begin{matrix}
s_\psi & c_\psi \\
-c_\psi & s_\psi
\end{matrix}\right]
\begin{pmatrix} \phi \\ \theta \end{pmatrix}
= \frac{1}{g} \begin{pmatrix} \ddot x_c \\ \ddot y_c \end{pmatrix} \tag{24}
$$

That $$2\times2$$ matrix is a rotation-like matrix with determinant $$s_\psi^2 + c_\psi^2 = 1$$, so it is orthogonal and inverts by transposition — no singularity, ever:

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

**Two practical refinements.** First, replace $$g$$ by the *commanded* specific thrust $$\ddot z_c + g$$, which is exact rather than a hover approximation and noticeably improves behaviour during climbs and descents:

$$\phi_d = \frac{\ddot x_c \sin\psi - \ddot y_c \cos\psi}{\ddot z_c + g}, \qquad \theta_d = \frac{\ddot x_c \cos\psi + \ddot y_c \sin\psi}{\ddot z_c + g} \tag{26}$$

Second, **saturate** $$\phi_d$$ and $$\theta_d$$ (typically to $$25$$–$$35°$$). The small-angle inversion is what breaks first when a controller is pushed hard, and clamping the tilt is what stops a large position error from commanding a flip.

## 5.3 Total thrust

From $$(15)$$, with $$c_\phi c_\theta \approx 1$$ near hover:

$$\sum_{i=1}^{4} F_{i} = m\left(\ddot z_c + g\right) \tag{27}$$

For larger tilts, divide by $$c_\phi c_\theta$$ instead — the vehicle needs more thrust to hold altitude while banked, and this "tilt compensation" is why $$(27)$$ is usually written as $$\sum F_i = m(\ddot z_c + g)/(c_\phi c_\theta)$$ in real firmware.

## 5.4 Inner loop: attitude PD

The attitude loop drives the body toward $$(\phi_d, \theta_d, \psi_d)$$ by commanding angular accelerations:

$$
\begin{pmatrix} \dot p_c \\ \dot q_c \\ \dot r_c \end{pmatrix}
=
K_{p}^{att} \begin{pmatrix} \phi_{d}-\phi \\ \theta_{d} - \theta \\ \psi_{d} - \psi \end{pmatrix}
+ K_{d}^{att} \begin{pmatrix} p_{d}-p \\ q_{d} - q \\ r_{d} - r \end{pmatrix} \tag{28}
$$

with $$K_p^{att}$$ and $$K_d^{att}$$ diagonal. Note carefully what $$(28)$$ does: it pairs *Euler-angle* errors with *body-rate* errors. That is only legitimate because $$W \approx I$$ near hover, so $$p \approx \dot\phi$$, $$q \approx \dot\theta$$, $$r \approx \dot\psi$$, and $$(28)$$ really is a PD law on each angle. At large tilt this pairing stops being meaningful, and you should map the desired Euler rates through $$W$$ from $$(4)$$ — or drop Euler angles entirely in favour of a geometric $$SO(3)$$ controller.

Also, $$\psi_d - \psi$$ must be **wrapped** to $$(-\pi, \pi]$$. Without it, a yaw setpoint crossing $$\pm\pi$$ commands a full-circle spin the long way round.

## 5.5 Simplifying the rotational dynamics

To turn $$(\dot p_c, \dot q_c, \dot r_c)$$ into torques, we use $$(16)$$–$$(18)$$. Near hover two things hold:

- The yaw rate is small, $$r \approx 0$$.
- The airframe is symmetric about the body $$x$$ and $$y$$ axes, $$i_{xx} \approx i_{yy}$$.

The first kills the $$qr$$ and $$pr$$ terms in $$(16)$$ and $$(17)$$; the second kills the $$pq$$ term in $$(18)$$. The gyroscopic coupling drops out entirely and the three axes decouple:

$$\tau_x \approx i_{xx}\,\dot p_c, \qquad \tau_y \approx i_{yy}\,\dot q_c, \qquad \tau_z \approx i_{zz}\,\dot r_c \tag{29}$$

(If you want the model to hold at high yaw rates, keep the full $$(16)$$–$$(18)$$ and simply *add back* the gyroscopic terms as feedforward — they are exactly known from the measured $$p, q, r$$.)

# 6. Control allocation (the mixer)

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

and the four thrusts are related to $$\mathbf{u}$$ by a constant **mixer matrix** $$\mathcal{M}$$, so that $$\mathcal{M}\,\mathbf{F} = \mathbf{u}$$ and $$\mathbf{F} = \mathcal{M}^{-1}\mathbf{u}$$. Only $$\mathcal{M}$$ changes between layouts.

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

Read the structure off directly: rotors 2 and 4 (on the $$y$$-axis) carry **all** the roll authority with a $$\tfrac{1}{2}$$ weight and contribute nothing to pitch; rotors 1 and 3 do the mirror image. Roll and pitch are each produced by only half the fleet.

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

The matrix $$\mathcal{M}_{X}$$ has a rather pleasant property: its rows are mutually orthogonal and each has norm $$2$$. It is $$2 \times$$ an orthogonal matrix (a $$\pm 1$$ Hadamard-type matrix), so the inverse is just the scaled transpose, $$\mathcal{M}_{X}^{-1} = \tfrac{1}{4}\mathcal{M}_{X}^{T}$$:

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

Here **every** rotor contributes to **every** channel with equal weight $$\tfrac{1}{4}$$ — the orthogonality made visible, and the reason the `X` layout spreads control effort so evenly.

Because $$\mathcal{M}$$ is constant and invertible, both mixers are just four multiply-accumulates per rotor. This is the cheapest part of the whole controller and it runs at the innermost loop rate.

## 6.3 From thrusts to motor commands

Finally, invert $$(6)$$:

$$\omega_i = \sqrt{\frac{F_i}{k_f}} \tag{36}$$

Two things must happen before that square root:

- **Clip to $$F_i \ge 0$$.** A fixed-pitch rotor cannot produce negative thrust; $$(32)$$ and $$(35)$$ happily ask for it during aggressive manoeuvres.
- **Clip to $$F_i \le F_{max}$$**, and think about *how* you clip. Naive per-motor saturation silently distorts the commanded torque direction. The usual fix is to prioritise the channels: preserve roll and pitch first (they keep you upright), then yaw, and let total thrust absorb the remainder. A quadrotor recovers from a momentary altitude error; it does not recover from an unintended flip.

# 7. What this model leaves out

The model above is standard and works well for hover and gentle flight. It is honest to be explicit about what it discards:

- **Rotor gyroscopic torque.** The spinning rotors have their own angular momentum; a body rotation produces $$-J_r\,\boldsymbol\omega \times \hat z_b\, \Omega_r$$ with $$\Omega_r = \omega_1 - \omega_2 + \omega_3 - \omega_4$$. Small, but real during fast rolls.
- **Motor dynamics.** $$\omega_i$$ is treated as an instantaneous input. Real ESC + motor combinations have a time constant of tens of milliseconds, which sets a hard ceiling on inner-loop bandwidth.
- **Aerodynamics.** Body drag (quadratic in airspeed), blade flapping, induced-velocity effects, and ground effect are all ignored. Blade flapping in particular produces a real velocity-dependent pitching moment in fast forward flight.
- **Off-diagonal inertia.** $$I$$ is assumed diagonal, i.e. the body axes are the principal axes.
- **Rigidity.** Frame flex and rotor–arm vibration couple into the gyro measurements and are usually dealt with by filtering rather than modelling.
- **Battery sag.** $$k_f$$ effectively drifts as voltage drops, which the altitude integrator quietly compensates for.

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

The thread running through all of it: **thrust can only point along one body axis, so all horizontal motion is bought by tilting.** The outer loop decides where to point, the inner loop points there, and the mixer distributes the request across four rotors that can each only push one way.

## References

1. R. Mahony, V. Kumar and P. Corke, "Multirotor Aerial Vehicles: Modeling, Estimation, and Control of Quadrotor," *IEEE Robotics & Automation Magazine*, vol. 19, no. 3, pp. 20–32, 2012.
2. D. Mellinger and V. Kumar, "Minimum snap trajectory generation and control for quadrotors," *IEEE ICRA*, 2011.
3. T. Lee, M. Leok and N. H. McClamroch, "Geometric tracking control of a quadrotor UAV on SE(3)," *IEEE CDC*, 2010.
4. F. Hover and M. Triantafyllou, "System Design for Uncertainty," MIT OCW 2.017J — [chapter on rotations](https://ocw.mit.edu/courses/mechanical-engineering/2-017j-design-of-electromechanical-robotic-systems-fall-2009/course-text/MIT2_017JF09_ch09.pdf).
