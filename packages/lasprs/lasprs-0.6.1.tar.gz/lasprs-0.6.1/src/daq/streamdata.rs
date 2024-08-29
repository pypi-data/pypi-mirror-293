//! Provides stream messages that come from a running stream
use crate::config::*;
use crate::siggen::Siggen;
use anyhow::{bail, Result};
use cpal::{FromSample, Sample};
use itertools::Itertools;
use num::cast::AsPrimitive;
use num::{Bounded, FromPrimitive, Num};

use super::*;
use super::*;
use parking_lot::RwLock;
use reinterpret::{reinterpret_slice, reinterpret_vec};
use std::any::TypeId;
use std::sync::Arc;
use std::u128::MAX;
use strum_macros::Display;

/// Raw stream data coming from a stream or going to a stream.
#[derive(Clone, Debug)]
pub enum RawStreamData {
    /// 8-bits integers
    Datai8(Vec<i8>),
    /// 16-bits integers
    Datai16(Vec<i16>),
    /// 32-bits integers
    Datai32(Vec<i32>),
    /// 32-bits floats
    Dataf32(Vec<f32>),
    /// 64-bits floats
    Dataf64(Vec<f64>),
}

impl RawStreamData {
    /// Create raw stream data from slice of data, or vec of data. Copies over
    /// the data.
    fn new<T, U>(input: T) -> RawStreamData
    where
        T: Into<Vec<U>> + 'static,
        U: num::ToPrimitive + Clone + 'static,
    {
        let input = input.into();
        // Apparently, this code does not work with a match. I have searched
        // around and have not found the reason for this. So this is a bit of
        // stupid boilerplate.
        let i8type: TypeId = TypeId::of::<i8>();
        let i16type: TypeId = TypeId::of::<i16>();
        let i32type: TypeId = TypeId::of::<i32>();
        let f32type: TypeId = TypeId::of::<f32>();
        let f64type: TypeId = TypeId::of::<f64>();

        // The type to create for
        let thetype: TypeId = TypeId::of::<U>();

        if i8type == thetype {
            let v: Vec<i8> = unsafe { reinterpret_vec(input) };
            RawStreamData::Datai8(v)
        } else if i16type == thetype {
            let v: Vec<i16> = unsafe { reinterpret_vec(input) };
            RawStreamData::Datai16(v)
        } else if i32type == thetype {
            let v: Vec<i32> = unsafe { reinterpret_vec(input) };
            RawStreamData::Datai32(v)
        } else if f32type == thetype {
            let v: Vec<f32> = unsafe { reinterpret_vec(input) };
            RawStreamData::Dataf32(v)
        } else if f64type == thetype {
            let v: Vec<f64> = unsafe { reinterpret_vec(input) };
            RawStreamData::Dataf64(v)
        } else {
            panic!("Not implemented sample type! Type: {thetype:?}, i8 = {i8type:?}, i16 = {i16type:?}, i32 = {i32type:?}, f32 = {f32type:?}, f64 = {f64type:?}.")
        }
    }
    /// Return a reference to the slice of data.
    ///
    /// # Panics
    ///
    /// - If the tye requested does not match the type stored.
    pub fn getRef<T>(&self) -> &[T]
    where
        T: Sample + 'static,
    {
        let type_requested = TypeId::of::<T>();
        macro_rules! ret_ref {
            ($c:expr,$t:ty) => {{
                let type_this = TypeId::of::<$t>();
                assert_eq!(type_requested, type_this, "Wrong type requested");
                unsafe { reinterpret_slice::<$t, T>(&$c) }
            }};
        }
        use RawStreamData::*;
        match &self {
            Datai8(v) => {
                ret_ref!(v, i8)
            }
            Datai16(v) => {
                ret_ref!(v, i16)
            }
            Datai32(v) => {
                ret_ref!(v, i32)
            }
            Dataf32(v) => {
                ret_ref!(v, f32)
            }
            Dataf64(v) => {
                ret_ref!(v, f64)
            }
        }
    }
}
/// Stream data (audio / other) coming from a stream or to be send to a stream
#[derive(Debug)]
pub struct InStreamData {
    /// Package counter. Should always increase monotonically.
    pub ctr: usize,

    /// Stream metadata. All info required for properly interpreting the raw data.
    pub meta: Arc<StreamMetaData>,

    /// This is typically what is stored when recording
    raw: RawStreamData,

    // Converted to floating point format. Used for further real time
    // processing. Stored in an rw-lock. The first thread that acesses this data
    // will perform the conversion. All threads after that will get the data.
    converted: RwLock<Option<Arc<Dmat>>>,
}

impl InStreamData {
    #[inline]
    /// Return reference to underlying raw data storage
    pub fn getRaw(&self) -> &RawStreamData {
        &self.raw
    }
    #[inline]
    /// Convenience function to return the number of channels in this instreamdata.
    pub fn nchannels(&self) -> usize {
        self.meta.nchannels()
    }
    /// Iterate over raw data of a certain channel. Tye should be specificied
    /// and if not set correctly, this results in undefined behavior
    pub fn iter_channel_raw<'a, T>(&'a self, ch: usize) -> impl Iterator<Item = &'a T> + 'a
    where
        T: Sample + Copy + 'static,
    {
        let type_requested: TypeId = TypeId::of::<T>();
        macro_rules! create_iter {
            ($c:expr,$t:ty) => {{
                // Check that the type matches the type stored
                let cur_type: TypeId = TypeId::of::<$t>();
                assert!(
                    type_requested == cur_type,
                    "BUG: Type mismatch on channel data iterator"
                );
                let v: &'a [T] = unsafe { reinterpret_slice($c) };
                v.iter().skip(ch).step_by(self.meta.nchannels())
            }};
        }

        match &self.raw {
            RawStreamData::Datai8(c) => {
                create_iter!(c, i8)
            }
            RawStreamData::Datai16(c) => {
                create_iter!(c, i16)
            }
            RawStreamData::Datai32(c) => {
                create_iter!(c, i32)
            }
            RawStreamData::Dataf32(c) => {
                create_iter!(c, f32)
            }
            RawStreamData::Dataf64(c) => {
                create_iter!(c, f64)
            }
        }
    }
    /// Iterate over all channels, deinterleaved. So first all samples from the
    /// first channel, etc...
    pub fn iter_deinterleaved_raw_allchannels<'a, T>(
        &'a self,
    ) -> Box<dyn Iterator<Item = &'a T> + 'a>
    where
        T: Sample + Copy + 'static,
    {
        Box::new(
            (0..self.meta.nchannels())
                .flat_map(|chi| self.iter_channel_raw(chi)),
        )
    }
    fn iter_channel_converted<T>(&self, ch: usize) -> impl Iterator<Item = Flt> + '_
    where
        T: Sample + Copy + 'static,
        Flt: FromSample<T>,
    {
        self.iter_channel_raw(ch)
            .copied()
            .map(move |v: T| Flt::from_sample(v) / self.meta.channelInfo[ch].sensitivity)
    }

    /// Iterate over data. where data is converted to floating point, and
    /// corrected for sensivity values. Returns all data, in order of channel.
    pub fn iter_deinterleaved_converted<'a, T>(&'a self) -> Box<dyn Iterator<Item = Flt> + 'a>
    where
        T: Sample + Copy + 'static,
        Flt: FromSample<T>,
    {
        Box::new(
            (0..self.meta.nchannels())
                .flat_map(move |chi| self.iter_channel_converted(chi)),
        )
    }

    /// Create new stream data object.
    pub fn new<T, U>(ctr: usize, meta: Arc<StreamMetaData>, raw: T) -> InStreamData
    where
        T: Into<Vec<U>> + 'static,
        U: Sample + num::ToPrimitive + Clone + 'static,
    {
        InStreamData {
            ctr,
            meta,
            raw: RawStreamData::new(raw),
            converted: RwLock::new(None),
        }
    }

    /// Returns the number of frames in this InstreamData
    pub fn nframes(&self) -> usize {
        let nch = self.meta.nchannels();
        match &self.raw {
            RawStreamData::Datai8(c) => {
                c.len() / nch
            }
            RawStreamData::Datai16(c) => {
                c.len() / nch
            }
            RawStreamData::Datai32(c) => {
                c.len() / nch
            }
            RawStreamData::Dataf32(c) => {
                c.len() / nch
            }
            RawStreamData::Dataf64(c) => {
                c.len() / nch
            }
        }
    }
    /// Get the data in floating point format. If already converted, uses the
    /// cached float data.
    pub fn getFloatData(&self) -> Arc<Dmat> {
        if let Some(dat) = self.converted.read().as_ref() {
            return dat.clone();
        }

        // In case we reach here, the data has not yet be converted to floating
        // point, so we do this.
        let mut write_lock = self.converted.write();

        // It might be that another thread was 'first', and already performed
        // the conversion. In that case, we still do an early return, and we
        // just openend the lock twice for writing. Not a problem.
        if let Some(dat) = write_lock.as_ref() {
            return dat.clone();
        }

        let errmsg = "Data cannot be converted to floating point";

        macro_rules! convert_data {
            ($t:ty) => {
                Dmat::from_shape_vec(
                    (self.nframes(), self.nchannels()).f(),
                    self.iter_deinterleaved_converted::<$t>().collect(),
                )
                .expect(errmsg)
            };
        }

        // Perform the actual conversion
        let converted_data = match &self.raw {
            RawStreamData::Datai8(_) => convert_data!(i8),
            RawStreamData::Datai16(_) => convert_data!(i16),
            RawStreamData::Datai32(_) => convert_data!(i32),
            RawStreamData::Dataf32(_) => convert_data!(f32),
            RawStreamData::Dataf64(_) => convert_data!(f64),
        };
        let converted_data = Arc::new(converted_data);
        // Replace the option with the Some
        write_lock.replace(converted_data.clone());

        converted_data
    }
}

#[cfg(test)]
mod test {
    use cpal::Sample;
    use num::traits::sign;

    use super::*;
    use crate::siggen::Siggen;

    #[test]
    fn test() {
        const fs: Flt = 20.;
        // Number of samples per channel
        const Nframes: usize = 20;
        const Nch: usize = 2;
        let mut signal = [0.; Nch * Nframes];
        let mut siggen = Siggen::newSine(Nch, 1.);

        siggen.reset(fs);
        siggen.setMute(&[false, true]);
        siggen.genSignal(&mut signal);

        let raw: Vec<i16> = Vec::from_iter(signal.iter().map(|o| o.to_sample::<i16>()));

        let ms1 = raw
            .iter()
            .step_by(2)
            .map(|s1| *s1 as f64 * *s1 as f64)
            .sum::<f64>()
            / Nframes as f64;

        let i16maxsq = (i16::MAX as f64).powf(2.);
        // println!("ms1: {} {}", ms1, i16maxsq/2.);
        // println!("{:?}", raw.iter().cloned().step_by(2).collect::<Vec<i16>>());
        // println!("{:?}", i16::EQUILIBRIUM);
        assert!(f64::abs(ms1 - i16maxsq / 2.) / i16maxsq < 1e-3);
    }
}
