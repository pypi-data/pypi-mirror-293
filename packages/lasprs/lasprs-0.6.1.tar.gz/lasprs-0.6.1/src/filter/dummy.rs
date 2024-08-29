use itertools::Itertools;

use super::*;

/// A Dummy fillter just does 'nothing', its input equals its output. It is
/// equal to [Biquad::unit], but then with the option to fully optimize it away.
#[derive(Clone, Copy, Debug)]
pub struct DummyFilter;

impl Filter for DummyFilter {
    #[inline]
    fn filter(&mut self, input: &[Flt]) -> Vec<Flt> {
        // Just returns an allocated copy
        input.to_vec()
    }
    fn reset(&mut self) {}
    fn clone_dyn(&self) -> Box<dyn Filter> {
        Box::new(*self)
    }
}
impl<'a, T: AsArray<'a, Flt>> TransferFunction<'a, T> for DummyFilter {
    fn tf(&self, _fs: Flt, freq: T) -> Ccol {
        let freq = freq.into();
        Ccol::ones(freq.len())
    }
}
