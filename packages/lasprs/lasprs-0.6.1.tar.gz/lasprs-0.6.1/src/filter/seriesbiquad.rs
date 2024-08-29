use super::*;

use super::biquad::Biquad;
use anyhow::{bail, Result};

#[derive(Clone, Debug)]
#[cfg_attr(feature = "python-bindings", pyclass)]

/// Series of biquads that filter sequentially on an input signal
///
/// # Examples
///
/// See (tests)
///
pub struct SeriesBiquad {
    biqs: Vec<Biquad>,
}

#[cfg(feature = "python-bindings")]
#[cfg_attr(feature = "python-bindings", pymethods)]
impl SeriesBiquad {
    // Print biquad in Python
    fn __repr__(&self) -> String {
        format!("{self:?}")
    }
    
    /// Create new series filter set. See [SeriesBiquad::new()]
    ///
    #[new]
    pub fn new_py<'py>(coefs: PyReadonlyArrayDyn<Flt>) -> PyResult<Self> {
        Ok(SeriesBiquad::new(coefs.as_slice()?)?)
    }
    #[pyo3(name = "unit")]
    #[staticmethod]
    /// See: [Biquad::unit]
    pub fn unit_py() -> SeriesBiquad {
        SeriesBiquad::unit()
    }
    
    /// See: [SeriesBiquad::filter]
    #[pyo3(name = "filter")]
    pub fn filter_py<'py>(
        &mut self,
        py: Python<'py>,
        input: PyArrayLike1<Flt>,
    ) -> Result<PyArr1Flt<'py>> {
        let res = self.filter(input.as_slice()?);
        Ok(PyArray1::from_vec_bound(py, res))
    }
    #[pyo3(name = "reset")]
    /// See: [SeriesBiquad::reset()]
    pub fn reset_py(&mut self) {
        self.reset();
    }
}
impl SeriesBiquad {
    /// Create new series biquad from vector of biquads. No checks on the
    /// validity or the stability of the biquads are performed.
    ///
    pub fn newFromBiqs(biqs: Vec<Biquad>) -> SeriesBiquad {
        assert!(biqs.len() > 0);
        SeriesBiquad { biqs }
    }

    /// Return reference to internally stored biquads
    pub fn getBiquads(&self) -> &Vec<Biquad> {
        &self.biqs
    }

    /// Create a new series biquad, having an arbitrary number of biquads.
    ///
    /// # Arguments
    ///
    /// * `filter_coefs` - Vector of biquad coefficients, stored in a single array. The first six
    /// for the first biquad, and so on.
    ///
    ///
    pub fn new(filter_coefs: &[Flt]) -> Result<SeriesBiquad> {
        if filter_coefs.len() % 6 != 0 {
            bail!(
                "filter_coefs should be multiple of 6, given: {}.",
                filter_coefs.len()
            );
        }
        let nfilters = filter_coefs.len() / 6;

        let mut biqs: Vec<Biquad> = Vec::with_capacity(nfilters);
        for coefs in filter_coefs.chunks(6) {
            let biq = Biquad::new(coefs)?;
            biqs.push(biq);
        }

        if biqs.is_empty() {
            bail!("No filter coefficients given!");
        }

        Ok(SeriesBiquad { biqs })
    }

    /// Unit impulse response series biquad. Input = output
    pub fn unit() -> SeriesBiquad {
        let filter_coefs = &[1., 0., 0., 1., 0., 0.];
        SeriesBiquad::new(filter_coefs).unwrap()
    }

    #[allow(dead_code)]
    fn clone_dyn(&self) -> Box<dyn Filter> {
        Box::new(self.clone())
    }
}

impl Filter for SeriesBiquad {
    //! Filter input by applying all biquad filters in series on each input sample, to obtain the
    //! output samples.
    //!
    fn filter(&mut self, input: &[Flt]) -> Vd {
        let mut inout = input.to_vec();
        for biq in self.biqs.iter_mut() {
            biq.filter_inout(&mut inout);
        }
        inout
    }
    fn reset(&mut self) {
        self.biqs.iter_mut().for_each(|f| f.reset());
    }
    fn clone_dyn(&self) -> Box<dyn Filter> {
        Box::new(self.clone())
    }
}
impl<'a, T: AsArray<'a, Flt>> TransferFunction<'a, T> for SeriesBiquad {
    fn tf(&self, fs: Flt, freq: T) -> Ccol {
        let freq = freq.into();
        let mut res = self.biqs.first().unwrap().tf(fs, freq);
        for biq in self.biqs.iter().skip(1) {
            res = &res * biq.tf(fs, freq);
        }
        res
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    #[should_panic]
    fn test_biquad2() {
        // A a0 coefficient not in the right place, meaning we panic on unwrap
        let filter_coefs = vec![1., 0., 0., 0., 0., 0.];
        let mut ser = SeriesBiquad::new(&filter_coefs).unwrap();
        let inp = vec![1., 0., 0., 0., 0., 0.];
        let filtered = ser.filter(&inp);
        assert_eq!(&filtered, &inp);
    }
    #[test]
    fn test_biquad3() {
        let filter_coefs = vec![0.5, 0.5, 0., 1., 0., 0.];
        let mut ser = SeriesBiquad::new(&filter_coefs).unwrap();

        let mut inp = vec![1., 0., 0., 0., 0., 0.];
        let filtered = ser.filter(&inp);

        // Change input to see match what should come out of output
        inp[0] = 0.5;
        inp[1] = 0.5;
        assert_eq!(&inp, &filtered);
    }
    #[test]
    fn test_seriesbiquad_tf1() {
        let filter_coefs = vec![1., 0., 0., 1., 0., 0.];
        let ser = SeriesBiquad::new(&filter_coefs).unwrap();
        let tf = ser.tf(1., &[0., 1.]);
        assert_eq!(tf[0].re, 1.0);
        assert_eq!(tf[1].im, 0.0);
    }
    #[test]
    fn test_seriesbiquad_tf2() {
        let filter_coefs = &[0.5, 0., 0., 1., 0., 0., 0.5, 0., 0., 1., 0., 0.];
        let ser = SeriesBiquad::new(filter_coefs).unwrap();
        let tf = ser.tf(1., &[0., 1.]);
        assert_eq!(tf[0].re, 0.25);
        assert_eq!(tf[1].im, 0.0);
    }
}
