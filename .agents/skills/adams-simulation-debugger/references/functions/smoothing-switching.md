# Functions: Smoothing, Switching, and Impact

## STEP(x, x0, h0, x1, h1)
Cubic polynomial smooth transition from h0 to h1 over [x0, x1].
- **x:** independent variable; **x0, x1:** transition start/end; **h0, h1:** output start/end values
- **Returns:** h0 for x ≤ x0; h1 for x ≥ x1; cubic interpolation between
- **Continuity:** C¹ — second derivative discontinuous at x0 and x1
- **Use for:** velocity-level motions, force ramps, ON/OFF switching
- **Avoid for:** displacement-level MOTION (use STEP5 instead — second derivative discontinuity causes extra integrator work)

## STEP5(x, x0, h0, x1, h1)
Quintic polynomial smooth transition from h0 to h1.
- Same arguments as STEP.
- **Returns:** Same structure as STEP
- **Continuity:** C² — third derivative discontinuous at x0 and x1
- **Use for:** displacement-level MOTION definitions (smoother than STEP at integration level)
- **Preferred over STEP** when the motion profile feeds into an inertia load calculation

## HAVSIN(x, x0, h0, x1, h1)
Haversine smooth transition from h0 to h1.
- Same arguments as STEP.
- **Formula:** `(h0+h1)/2 - (h1-h0)/2 * COS(π*(x-x0)/(x1-x0))`
- **Continuity:** C¹ — second derivative discontinuous
- **Notes:** Often used for velocity-level inputs. Derivative shape is sinusoidal (smooth bell curve), which is natural for cam follower profiles.

## BISTOP(x, ẋ, x1, x2, k, e, cmax, d)
Two-sided gap contact force (gap between x1 and x2).
- **x:** displacement variable; **ẋ:** time derivative of x (must be matched)
- **x1:** lower bound; **x2:** upper bound (`x1 < x2`)
- **k:** contact stiffness; **e:** force-deformation exponent
- **cmax:** maximum damping coefficient; **d:** penetration depth for full damping onset
- **Returns:** 0 for `x1 < x < x2` (free zone); positive when `x < x1` (lower contact); negative when `x > x2` (upper contact)
- **Damping:** ramps via cubic STEP from 0 at zero penetration to cmax at depth d
- **Notes:** `e < 1` creates slope discontinuity at contact onset — difficult for integrator. Recommended: `e ≥ 1.5`. Use `DM()` and `VR()` for 3D contact in SFORCE expressions.

## IMPACT(x, ẋ, x1, k, e, cmax, d)
One-sided contact (impact) force. Active when `x < x1`.
- **x:** distance variable; **ẋ:** time derivative of x
- **x1:** contact limit (contact activates when `x < x1`, i.e., penetration = `x1 - x`)
- **k, e, cmax, d:** same as BISTOP
- **Returns:** ≥ 0; zero when `x ≥ x1`
- **Notes:** Recommended `e > 2.1` for hard contact. Damping ramps from 0 at zero penetration to cmax over depth d. For unit-system differences: `k_entry = k_physical × (length_conversion)^e`.
- **Typical usage:** `IMPACT(DZ(i,j,j), VZ(i,j,j,j), gap, 1e5, 2.2, 100, 0.1)` for a Z-axis impact.
