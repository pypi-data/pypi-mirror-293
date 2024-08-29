use crate::config::*;
use strum_macros::{Display, EnumMessage};
/// Sound level frequency weighting type (A, C, Z)

// Do the following when Pyo3 0.22 can finally be used combined with rust-numpy:
// #[cfg_attr(feature = "python-bindings", pyclass(eq, eq_int))]
// For now:
#[cfg_attr(feature = "python-bindings", pyclass)]
#[derive(Display, Debug, EnumMessage, Default, Clone, PartialEq)]
pub enum FreqWeighting {
    /// A-weighting
    A,
    /// C-weighting
    C,
    /// Z-weighting, or no weighting
    #[default]
    Z,
}
#[cfg(test)]
mod test {
    use super::*;
    #[test]
    fn test() {
        let a = FreqWeighting::A;
        let c = FreqWeighting::C;
        let z = FreqWeighting::Z;
        println!("A-weighting: {a}");
        println!("C-weighting: {c}");
        println!("Z-weighting: {z}");
    }
}
