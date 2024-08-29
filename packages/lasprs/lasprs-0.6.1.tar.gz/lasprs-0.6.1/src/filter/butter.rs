//! We implement
//! [Pieter's Pages](https://tttapa.github.io/Pages/Mathematics/Systems-and-Control-Theory/Analog-Filters/Butterworth-Filters.html)
//! is a fine source to understand the theory presented here.
//! A Butterworth lowpass filter has the form
//!
//! ```math
//!                     1
//! |H(s)|^2 = ------------------
//!               1+ (omega/omega_c)^(2n)
//! ```
//!
//!  where `n`` is the order of the filter.

use approx::abs_diff_eq;

use super::PoleOrZero;
use crate::config::*;

/// Create iterator that returns the poles of a butterworth lowpass filter.
///
/// # Args
///
/// - `fc` - Cutoff-frequency in \[Hz\]
/// - `n` - Filter order
pub fn butter_lowpass_roots(fc: Flt, n: u32) -> impl Iterator<Item = PoleOrZero> {
    let omgc = 2. * pi * fc;
    let nf = n as Flt;
    (1..=n).filter_map(move |k| {
        let kf = k as Flt;

        let angle = pi * (2. * kf + nf - 1.) / (2. * nf);
        let pole = omgc * Cflt::exp(I * angle);
        if abs_diff_eq!(pole.im(), 0., epsilon = 1e-5) {
            Some(PoleOrZero::Real1(pole.re()))
        } else if pole.im() > 0. {
            // We only pick the roots with positive imaginary part
            Some(PoleOrZero::Complex(pole))
        } else {
            // Negative imaginary part. Will be filtered out
            None
        }
    })
}
