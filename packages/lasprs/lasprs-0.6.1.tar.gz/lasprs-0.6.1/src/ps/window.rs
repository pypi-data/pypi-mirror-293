#![allow(non_snake_case)]
use crate::config::*;

use strum_macros::Display;

/// Von Hann window, often misnamed as the 'Hanning' window.
fn hann(nfft: usize) -> Dcol {
    let nfftF = nfft as Flt;
    Dcol::from_iter((0..nfft).map(|i| {
        // 0.5*(1-cos(2*pi*i/(n-1)))
        0.5 * (1. - Flt::cos(2. * pi * i as Flt / (nfftF - 1.))) 
    }))
}
/// Rectangular window
fn rect(nfft: usize) -> Dcol {
    Dcol::ones(nfft)
}
// Blackman window
fn blackman(N: usize) -> Dcol {
    // Exact a0 coefficient, approximate value is 0.42
    const a0: Flt = 7938. / 18608.;
    // Exact a1 coefficient, approximate value is 0.50
    const a1: Flt = 9240. / 18608.;
    // Exact a2 coefficient, approximate value is 0.08
    const a2: Flt = 1430. / 18608.;

    let Nf = N as Flt;

    Dcol::from_iter((0..N).map(|i| {
        let iF = i as Flt;
        a0 - a1 * Flt::cos(2. * pi * iF / (Nf - 1.)) + a2 * Flt::cos(4. * pi * iF / (Nf - 1.))
    }))
}
fn bartlett(N: usize) -> Dcol {
    let Nf = N as Flt;
    Dcol::from_iter((0..N).map(|i| {
        let iF = i as Flt;
        if i <= (N - 1) / 2 {
            2. * iF / (Nf - 1.)
        } else {
            2. - 2. * iF / (Nf - 1.)
        }
    }))
}
fn hamming(N: usize) -> Dcol {
    let Nf = N as Flt;
    // Approx 0.54
    const a0: Flt = 25.0 / 46.0;
    // Approx 0.46
    const a1: Flt = 1. - a0;

    Dcol::from_iter((0..N).map(|i| 
        // Alessio et al.
        a0 - a1 * Flt::cos(2. * pi * i as Flt / (Nf - 1.))
    
    // end of map
    ) 
    // end from iter
    )
}

/// Window type descriptors. Used for computing the actual window with private
/// functions. See [Window], for the actual window (taper).
/// 
/// Window functions designed for Welch' method. Implementations are given for
/// the 5 classical window functions:
/// 
/// * Hann - Von Hann window (sometimes wrongly called "Hanning")
/// * Rect - rectangular
/// * Bartlett
/// * Hamming
/// * Blackman
/// 
/// The [WindowType::default] is [WindowType::Hann].
#[derive(Display,Default, Copy, Clone, Debug)]
pub enum WindowType {
    /// Von Hann window
    #[default]
    Hann = 0,
    /// Hamming window
    Hamming = 1,
    /// Boxcar / rectangular window
    Rect = 2,
    /// Bartlett window
    Bartlett = 3,
    /// Blackman window
    Blackman = 4,
}

/// Window (taper) computed from specified window type.
#[derive(Clone)]
pub struct Window {
    /// The enum from which it is generated
    pub w: WindowType,
    /// The actual window computed from specified nfft
    pub win: Dcol,
    /// The 'optimal' number of samples of shift per window average (hop size).
    pub R: usize,
}
impl Window {
    /// Create new window based on type and fft length. FFT length should be even. The (Window)
    /// struct contains type and generated window in the `win` member.
    ///
    /// # Panics
    ///
    /// If nfft %2 != 0
    pub fn new(w: WindowType, nfft: usize) -> Window {
        if nfft % 2 != 0 {
            panic!("Requires even nfft");
        }
        let win  = match w {
            WindowType::Hann => hann(nfft),
            WindowType::Hamming => hamming(nfft),
            WindowType::Rect => rect(nfft),
            WindowType::Bartlett => bartlett(nfft),
            WindowType::Blackman => blackman(nfft),
        };
        let R = nfft/2;
        Window { w, win, R }
    }
    /// Convenience function that returns the length of the window.
    pub fn len(&self) -> usize {
        self.win.len()
    }
}



#[cfg(test)]
mod test {
    use approx::assert_abs_diff_eq;

    use super::*;

    #[test]
    fn test_windows(){
        let Hann = hann(11);
        let Hamming = hamming(11);
        let Bartlett = bartlett(11);
        let Blackmann = bartlett(11);
        // let h = hann(11);
        assert_eq!(Hann[5] , 1.);
        assert_eq!(Hamming[5] , 1.);
        assert_eq!(Bartlett[5] , 1.);
        assert_eq!(Blackmann[5] , 1.);
    }
}
