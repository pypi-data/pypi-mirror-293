//! Compute forward single sided amplitude spectra
use crate::config::*;
use realfft::{RealFftPlanner, RealToComplex};
use std::sync::Arc;

#[derive(Clone)]
pub struct FFT {
    // The fft engine
    fft: Arc<dyn RealToComplex<Flt>>,
    // Copy over time data, as it is used as scratch data in the fft engine
    timescratch: Vec<Flt>,
    // rounded down nfft/2
    half_nfft_rounded: usize,
    // nfft stored as float, this is how it is required most often
    nfftF: Flt,
}

impl FFT {
    /// Create new FFT from given nfft
    #[allow(dead_code)]
    pub fn newFromNFFT(nfft: usize) -> FFT {
        let mut planner = RealFftPlanner::<Flt>::new();
        let fft = planner.plan_fft_forward(nfft);
        Self::new(fft)
    }
    /// Create new fft engine from given fft engine
    pub fn new(fft: Arc<dyn RealToComplex<Flt>>) -> FFT {
        let nfft = fft.len();
        let timescratch = vec![0.; nfft];
        FFT {
            fft,
            timescratch,
            half_nfft_rounded: nfft / 2,
            nfftF: nfft as Flt,
        }
    }
    pub fn process<'a, T, U>(&mut self, time: T, freq: U)
    where
        T: Into<ArrayView<'a, Flt, Ix1>>,
        U: Into<ArrayViewMut<'a, Cflt, Ix1>>,
    {
        let mut freq = freq.into();
        let time = time.into();
        self.timescratch.copy_from_slice(time.as_slice().unwrap());
        let _ = self
            .fft
            .process(&mut self.timescratch, freq.as_slice_mut().unwrap());

        freq[0] /= self.nfftF;
        freq[self.half_nfft_rounded] /= self.nfftF;
        freq.slice_mut(s![1..self.half_nfft_rounded])
            .par_mapv_inplace(|x| 2. * x / self.nfftF);
    }
}
