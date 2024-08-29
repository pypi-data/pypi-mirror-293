use crate::config::*;
/// Time weighting to use in level detection of Sound Level Meter.
/// 
// Do the following when Pyo3 0.22 can finally be used combined with rust-numpy:
// #[cfg_attr(feature = "python-bindings", pyclass(eq))]
// For now:
#[cfg_attr(feature = "python-bindings", pyclass)]
#[derive(Clone, Copy, PartialEq)]
pub enum TimeWeighting {
    // I know that the curly braces here are not required and add some
    // boilerplate, but this is the only way Pyo3 swallows complex enums at the
    // moment.
    /// Slow time weighting ~ 1 s
    Slow {},
    /// Fast time weighting ~ 1/8 s
    Fast {},
    /// Impulse time weighting ~ 30 ms
    Impulse {},
    /// A custom symmetric time weighting
    CustomSymmetric {
        /// Custom time constant [s]
        t: Flt,
    },
    
    /// A custom symmetric time weighting
    CustomAsymmetric {
        /// Time weighting when level is increasing
        tup: Flt,
        /// Time weighting when level is decreasing
        tdown: Flt,
    },
}
impl Default for TimeWeighting {
    fn default() -> Self {
        TimeWeighting::Fast {}
    }
}
impl TimeWeighting {
    /// get the analog poles of the single pole lowpass filter required for
    /// getting the 'rectified' level (detection phase of SLM).
    pub fn getLowpassPoles(&self) -> (Flt, Option<Flt>) {
        use TimeWeighting::*;
        match self {
            Slow {} => (-1.0, None),
            Fast {} =>
            // Time constant is 1/8 s, pole is at -8 rad/s
            {
                (-8., None)
            }
            Impulse {} => {
                // For the impulse time weighting, some source says ~ 2.9 dB/s
                // drop for the decay
                // [https://www.nti-audio.com/en/support/know-how/fast-slow-impulse-time-weighting-what-do-they-mean].
                //
                // Other source
                // [https://support.dewesoft.com/en/support/solutions/articles/14000139949-exponential-averaging-fast-f-slow-s-impulse-i-]
                // say a time constant of 1.5 s. Are they compatible?

                // Compute decay rate in dB/s from the filter time constant. An
                // initial value drops as exp(-t/tau). So in 1 s the level drops
                // with 10*log10(exp(-1.0/tau)) = -10/ln(10)/tau ≅ -4.34/tau
                // dB/s where ln denotes the natural logarithm. So suppose we
                // have 1.5 s, we indeed get a decay rate of 2.9 dB/s
                (-1. / 35e-3, Some(-1. / 1.5))
            }
            CustomSymmetric { t } => {
                assert!(*t > 0.);
                (-*t, None)
            }
            CustomAsymmetric { tup, tdown } => {
                assert!(*tup > 0.);
                assert!(*tdown > 0.);
                (-*tup, Some(-*tdown))
            }
        }
    }
}
