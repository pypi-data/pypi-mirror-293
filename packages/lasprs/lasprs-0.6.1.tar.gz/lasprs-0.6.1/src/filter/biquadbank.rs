use super::*;
use super::seriesbiquad::*;
use rayon::prelude::*;
#[cfg_attr(feature = "python-bindings", pyclass)]
#[derive(Clone)]
/// Multiple biquad filter that operate in parallel on a signal, and can apply a gain value to each
/// of the returned values. The BiquadBank can be used to decompose a signal by running it through
/// parallel filters, or it can directly be used to eq a signal. For the latter process, also a
/// gain can be applied when the output is made as the sum of the filtered inputs for each biquad.
///
/// # Detailed description
///
/// Below is an example of the signal flow is for the case of three SeriesBiquad filters, `h1`,
/// `h2` and `h3`:
///
/// ```markdown
///
///            analysis()       gain application             sum()              
///                                                               
///                  +------+   +-----+                    +------------+
///            +-----+ h1   |---+ g1  +-------------+      |            |
///            |     +------+   +-----+             ++     |   +------  |
///            |                                     +-----|   ++       |
///  Input     |     +------+   +-----+                    |    ++      |   Output of filter()
///--------|>--+-----+ h2   |---+ g2  |--------------------|     +-+    +----------------|>
///            |     ---+---+   +-----+                    |     +-+    |
///            |                                     +-----|    ++      |
///            |     +------+   +-----+             ++     |   ++       |
///            +-----+ h3   |---+ g3  |-------------+      |   +------  |
///                  +------+   +-----+                    |            |
///                           |                            +------------+
///                           |                  
///                           | Output of analysis() method (optional)
///                           +-------------|>
/// ```
pub struct BiquadBank {
    biqs: Vec<Box<dyn Filter>>,
    gains: Vec<Flt>,
}

#[cfg(feature = "python-bindings")]
#[cfg_attr(feature = "python-bindings", pymethods)]
/// Methods to wrap it in Python
impl BiquadBank {
    #[new]
    /// Create new biquadbank filter set. See [BiquadBank::new()]
    ///
    pub fn new_py<'py>(coefs: PyReadonlyArrayDyn<Flt>) -> PyResult<Self> {
        let mut filts = vec![];
        for col in coefs.as_array().columns() {
            match col.as_slice() {
                Some(colslice) => {
                    let new_ser = SeriesBiquad::new(colslice)?;
                    filts.push(new_ser.clone_dyn());
                }
                None => {
                    return Err(PyValueError::new_err("Error generating column"));
                }
            }
        }
        Ok(BiquadBank::new(filts))
    }
    #[pyo3(name = "filter")]
    /// See: [BiquadBank::filter()]
    pub fn filter_py<'py>(
        &mut self,
        py: Python<'py>,
        input: PyArrayLike1<Flt>,
    ) -> PyResult<PyArr1Flt<'py>> {
        Ok(self.filter(input.as_slice()?).into_pyarray_bound(py))
    }
    #[pyo3(name = "reset")]
    /// See: [BiquadBank::reset()]
    pub fn reset_py(&mut self) {
        self.reset();
    }

    #[pyo3(name = "set_gains")]
    /// See: [BiquadBank::set_gains()]
    pub fn set_gains_py<'py>(&mut self, gains: PyArrayLike1<Flt>) -> PyResult<()> {
        if gains.len()? != self.len() {
            return Err(PyValueError::new_err("Invalid number of provided gains"));
        }
        self.set_gains(gains.as_slice()?);
        Ok(())
    }
    #[pyo3(name = "set_gains_dB")]
    /// See: [BiquadBank::set_gains_dB()]
    pub fn set_gains_dB_py<'py>(&mut self, gains_dB: PyArrayLike1<Flt>) -> PyResult<()> {
        if gains_dB.len()? != self.len() {
            return Err(PyValueError::new_err("Invalid number of provided gains"));
        }
        self.set_gains_dB(gains_dB.as_slice()?);
        Ok(())
    }
    #[pyo3(name = "len")]
    /// See: [BiquadBank::len()]
    pub fn len_py(&self) -> usize {
        self.len()
    }
}

impl BiquadBank {
    /// Create new biquad bank. Initialized from given vector of series biquads.
    pub fn new(biqs: Vec<Box<dyn Filter>>) -> BiquadBank {
        let gains = vec![1.0; biqs.len()];
        BiquadBank { biqs, gains }
    }
    /// Return the number of parallel filters installed.
    pub fn len(&self) -> usize {
        self.biqs.len()
    }

    /// Set the gains for each of the biquad. The gains are not used in the analyisis phase, but in
    /// the reconstruction phase, so when BiquadBank::filter() is run on an input signal.
    ///
    /// # Panics
    ///
    /// When gains_dB.len() != to the number of filters.
    pub fn set_gains_dB(&mut self, gains_dB: &[Flt]) {
        if gains_dB.len() != self.gains.len() {
            panic!("Invalid gains size!");
        }
        self.gains
            .iter_mut()
            .zip(gains_dB)
            .for_each(|(g, gdB)| *g = Flt::powf(10., gdB / 20.));
    }
    /// Set linear gain values for each biquad. Same comments hold as for
    /// [BiquadBank::set_gains_dB()].
    pub fn set_gains(&mut self, gains: &[Flt]) {
        if gains.len() != self.gains.len() {
            panic!("Invalid gains size!");
        }
        // This could be done more efficient, but it does not matter. How often would you change
        // the gain values?
        self.gains.clone_from(&gains.to_vec());
    }
    /// Analysis step. Runs input signal through all filters. Outputs a vector of output results,
    /// one for each filter in the bank.

    pub fn analysis(&mut self, input: &[Flt]) -> Vec<Vd> {
        // Filtered output for each filter in biquad bank
        let filtered_out: Vec<Vd> = self
            .biqs
            .par_iter_mut()
            // .iter_mut()
            .map(|biq| biq.filter(input))
            .collect();
        filtered_out
    }
}

impl Filter for BiquadBank {
    fn filter(&mut self, input: &[Flt]) -> Vd {
        // Sum of filter output times gains
        let filtered_out = self.analysis(input);

        let mut out: Vd = vec![0.; input.len()];

        for (f, g) in filtered_out.iter().zip(&self.gains) {
            for (outi, fi) in out.iter_mut().zip(f) {
                // Sum and multiply by gain value
                *outi += g * fi;
            }
        }
        out
    }
    fn reset(&mut self) {
        self.biqs.iter_mut().for_each(|b| b.reset());
    }
    fn clone_dyn(&self) -> Box<dyn Filter> {
        Box::new(self.clone())
    }
}