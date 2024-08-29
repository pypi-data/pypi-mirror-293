//! A time buffer is used as intermediate storage for samples, to spare up
//! enough values to do 'something' with. Typical application: getting enough
//! samples to perform an FFT. The use case is computing average power spectra.
use super::*;
use crate::config::*;
use std::collections::VecDeque;

/// TimeBuffer, storage to add blocks of data in a ring buffer, that can be
/// extracted by blocks of other size. Also, we can keep samples in a buffer to
/// create, for example, overlapping windows of time data.
#[derive(Default)]
pub struct TimeBuffer {
    data: Vec<VecDeque<Flt>>,
}
impl TimeBuffer {
    /// Allocate new empty TimeBuffer.
    pub fn new() -> TimeBuffer {
        TimeBuffer { data: Vec::new() }
    }
    /// Reset the buffer. Clears all data in it.
    pub fn reset(&mut self) {
        *self = Self::new();
    }
    /// Push new data to the buffer. Keep
    ///
    /// # Panics
    ///
    /// When the number of columns does not match with the first time this
    /// method is called.
    pub fn push<'a, T>(&mut self, new_data: T)
    where
        T: AsArray<'a, Flt, Ix2>,
    {
        let new_data = new_data.into();
        let nch = new_data.shape()[1];
        if self.data.is_empty() {
            self.data = vec![VecDeque::new(); nch];
        }
        if self.data.len() != nch {
            panic!("BUG: Number of channels does not match with time buffer");
        }
        for (new_dat, buf) in new_data.columns().into_iter().zip(self.data.iter_mut()) {
            let slice = new_dat.as_slice().unwrap();
            buf.extend(slice);
        }
    }
    /// Return the number of samples that is currently stored
    pub fn nsamples(&self) -> usize {
        if let Some(q) = self.data.first() {
            return q.len();
        };
        0
    }
    /// Pop samples from the queue, only returns Some(Dmat) when there are
    /// enough samples to return. Never returns less samples than
    /// `nsamples_requested`.
    pub fn pop(&mut self, nsamples_requested: usize, nsamples_keep: usize) -> Option<Dmat> {
        if self.data.is_empty() {
            return None;
        }
        if nsamples_keep > nsamples_requested {
            panic!("BUG: Cannot keep more samples than requested to return");
        }

        debug_assert!(!self.data.is_empty());
        let c1 = unsafe { self.data.get_unchecked(0) };

        let nsamples_available = c1.len();
        debug_assert!(nsamples_available == self.nsamples());
        if nsamples_available < nsamples_requested {
            // println!("Less available than requested");
            return None;
        }
        // Number of channels
        let nchannels = self.data.len();

        // Create output array, .f() means fortran contiguous array
        let mut res = Dmat::zeros((nsamples_requested, nchannels).f());
        {
            for (mut col, dat) in res.columns_mut().into_iter().zip(&mut self.data) {
                // This expect should never happen, as above it is called with .f().
                let col_slice = col
                    .as_slice_mut()
                    .expect("Data is not contiguous on the sample axis!");

                // Split data of current channel in two slices of the underlying data
                let (dat_slice1, dat_slice2) = dat.as_slices();

                if dat_slice1.len() >= nsamples_requested {
                    // Only copy from the first slice
                    col_slice.copy_from_slice(&dat_slice1[..nsamples_requested]);
                } else {
                    let slice1len = dat_slice1.len();
                    // Copy from first slice
                    col_slice[..slice1len].copy_from_slice(dat_slice1);
                    // Copy rest from second slice
                    col_slice[slice1len..nsamples_requested]
                        .copy_from_slice(&dat_slice2[..nsamples_requested - slice1len]);
                }

                // From documentation:
                // Removes the specified range from the deque in bulk, returning all removed
                // elements as an iterator. If the iterator is dropped before being fully
                // consumed, it drops the remaining removed elements.
                dat.drain(0..nsamples_requested - nsamples_keep);
            }
        }
        let c1 = unsafe { self.data.get_unchecked(0) };
        let nsamples_available = c1.len();
        debug_assert!(self
            .data
            .iter()
            .map(|ch| ch.len()) // Iterator over all channels, transform to the amount of samples in each channel.
            .all(|v| v == nsamples_available));

        Some(res)
    }
}

#[cfg(test)]
mod test {
    use crate::{Dcol, Dmat};
    use ndarray::s;

    use super::TimeBuffer;

    #[test]
    fn test_timebuffer1() {
        let mut t1 = Dmat::zeros((10, 1));
        t1[[9, 0]] = 1.0;
        let mut tb = TimeBuffer::new();

        tb.push(&t1);
        let out = tb.pop(10, 2).unwrap();
        assert_eq!(out.len(), 10);
        let out = tb.pop(3, 0);
        assert!(out.is_none());
        let out = tb.pop(2, 0).unwrap();
        // println!("{:?}", out);
        assert_eq!(out.len(), 2);
        assert_eq!(tb.nsamples(), 0);
        assert_eq!(out[[1, 0]], 1.0);

        tb.reset();
        assert_eq!(tb.nsamples(), 0);
    }

    #[test]
    fn test_timebuffer2() {
        let mut tb = TimeBuffer::new();
        let tlin = Dcol::linspace(0., 100., 101);
        // println!("{:?}", tlin);
        let mut t2 = Dmat::zeros((101, 0));
        t2.push_column(tlin.view()).unwrap();
        t2.push_column(tlin.view()).unwrap();
        tb.push(&t2);
        assert_eq!(tb.nsamples(), 101);

        let tres = tb.pop(50, 49).unwrap();
        assert_eq!(tres.shape(), [50, 2]);
        assert_eq!(t2.slice(s![..50, ..2]), tres);
    }
    #[test]
    fn test_timebuffer3() {
        let mut tb = TimeBuffer::new();
        let t1 = Dmat::zeros((10,1));
        tb.push(&t1);
        tb.push(&t1);
        assert_eq!(tb.nsamples(), 20);

        let tres = tb.pop(10, 5).unwrap();
        assert_eq!(tres.shape(), [10, 1]);
        assert_eq!(tb.nsamples(), 15);
        let _ = tb.pop(10, 0).unwrap();
        assert_eq!(tb.nsamples(), 5);
        let tres = tb.pop(5, 5).unwrap();
        assert_eq!(tres.shape(), [5, 1]);
        assert_eq!(tb.nsamples(), 5);
        // assert_eq!(t2.slice(s![..50, ..2]), tres);
    }
}
