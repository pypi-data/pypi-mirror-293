//! Configuration of module. Here, we can choose to compile for 32-bits or
//! 64-bit floating point values as basic data storage and computation size.
//! Default is f64.
//!

cfg_if::cfg_if! {
    if #[cfg(feature="f64")] {
        /// Floating-point value, compile time option to make it either f32, or
        /// f64.
        pub type Flt = f64;
        /// Ratio between circumference and diameter of a circle
        pub const pi: Flt = std::f64::consts::PI;

        
    }
    else if #[cfg(feature="f32")] {
        /// Floating-point value, compile time option to make it either f32, or f64
        pub type Flt = f32;
        /// Ratio between circumference and diameter of a circle
        pub const pi: Flt = std::f32::consts::PI;
    }
    else {
        std::compile_error!("feature should be f32 or f64");
    }
}

cfg_if::cfg_if! {
if #[cfg(feature = "python-bindings")] {
    pub use numpy::{IntoPyArray,PyArray, PyArray1, PyArrayDyn, PyArrayLike1, PyReadonlyArrayDyn};
    pub use pyo3::prelude::*;
    pub use pyo3::exceptions::PyValueError;
    pub use pyo3::{pymodule, types::PyModule, PyResult};
    pub use pyo3::anyhow::*;
    pub use pyo3;

}
}
pub use ndarray::prelude::*;
pub use ndarray::{Array1, Array2, ArrayView1, ArrayViewMut1};

pub use ndarray::Zip;
use num::complex::Complex;
pub use num::complex::ComplexFloat;

/// View into 1D array of floats
#[allow(dead_code)]
pub type VdView<'a> = ArrayView1<'a, Flt>;

/// View into 1D array of complex floats
#[allow(dead_code)]
pub type VcView<'a> = ArrayView1<'a, Cflt>;

/// Complex number floating point
pub type Cflt = Complex<Flt>;

/// Complex unit sqrt(-1)
pub const I: Cflt = Cflt::new(0., 1.);

/// (Owning) Vector of floating point values
pub type Vd = Vec<Flt>;

/// (Owning) Vector of complex floating point values
pub type Vc = Vec<Cflt>;

/// 1D array of floats
pub type Dcol = Array1<Flt>;

/// 1D array of complex floats
pub type Ccol = Array1<Cflt>;

/// 2D array of floats
pub type Dmat = Array2<Flt>;

/// 2D array of complex floats
pub type Cmat = Array2<Cflt>;

cfg_if::cfg_if! {
if #[cfg(feature = "python-bindings")] {

    /// 1D array of T as returned from Rust to Numpy
    pub type PyArr1<'py, T> = Bound<'py, PyArray<T, ndarray::Dim<[usize; 1]>>>;

    /// 1D array Floats returned from Rust to Numpy
    pub type PyArr1Flt<'py> = PyArr1<'py, Flt>;

    /// 1D array of Complex returned from Rust to Numpy
    pub type PyArr1Cflt<'py> = PyArr1<'py, Cflt>;

}}
