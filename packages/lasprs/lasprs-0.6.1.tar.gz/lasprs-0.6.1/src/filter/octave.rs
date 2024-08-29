use crate::{config::*, ZPKModel};
use anyhow::{anyhow, bail, Result};
use num::{traits::float, Float};
use rayon::iter::Filter;
use softfloat::F64;
use std::{borrow::Cow, cmp::Ordering};

/// Names of standard octave filters
const OCTAVE_NOMINAL_MIDBAND_NAMES: [&str; 12] = [
    "8", "16", "31.5", "63", "125", "250", "500", "1k", "2k", "4k", "8k", "16k",
];
const OCTAVE_NAMES_OFFSET: i32 = 7;

const MIN_MIDBAND_FREQ: Flt = 8.;
const MAX_MIDBAND_FREQ: Flt = 20e3;

const THIRDOCTAVE_NOMINAL_MIDBAND_NAMES: [&'static str; 33] = [
    "12.5", "16", "20", "25", "31.5", "40", "50", "63", "80", "100", "125", "160", "200", "250",
    "315", "400", "500", "630", "800", "1k", "1.25k", "1.6k", "2k", "2.5k", "3.15k", "4k", "5k",
    "6.3k", "8k", "10k", "12.5k", "16k", "20k",
];
const THIRDOCTAVE_NAMES_OFFSET: i32 = 19;

/// Return the num x-value for a certain 'name', like '16', or '1k'
fn nominal_octave_designator(name: &str) -> Result<i32> {
    debug_assert!(OCTAVE_NOMINAL_MIDBAND_NAMES[OCTAVE_NAMES_OFFSET as usize] == "1k");
    Ok(OCTAVE_NOMINAL_MIDBAND_NAMES
        .iter()
        .position(|i| *i == name)
        .ok_or(anyhow!(
            "Cannot find name in list of OCTAVE_NOMINAL_MIDBAND_NAMES"
        ))? as i32
        - OCTAVE_NAMES_OFFSET)
}

fn nominal_thirdoctave_designator(name: &str) -> Result<i32> {
    debug_assert!(THIRDOCTAVE_NOMINAL_MIDBAND_NAMES[THIRDOCTAVE_NAMES_OFFSET as usize] == "1k");
    Ok(THIRDOCTAVE_NOMINAL_MIDBAND_NAMES
        .iter()
        .position(|i| *i == name)
        .ok_or(anyhow!(
            "Cannot find name in list of THIRDOCTAVE_NOMINAL_MIDBAND_NAMES"
        ))? as i32
        - THIRDOCTAVE_NAMES_OFFSET)
}
// Raise a^b. In const-mode.
const fn powf(a: Flt, b: Flt) -> Flt {
    let a = a as f64;
    let b = b as f64;
    let a = softfloat::F64::from_native_f64(a);
    let b = softfloat::F64::from_native_f64(b);
    softfloat::F64::exp(b.mul(a.ln())).to_native_f64() as Flt
}

/// Octave ratio. We use G_10, which is 10^(3/10) ≅ 1.995
pub const G: Flt = powf(10., 0.3);
/// Reference freuqency, 1kHz
pub const FREQ_REF: Flt = 1000.;

/// Standard filter descriptor. Used to generate bandpass filters that are
/// compliant with IEC 61260 (1995).
///
/// # Examples
///
/// ## Create a 16 Hz octave band digital filter running at 48kHz.
///
/// ```rust
/// use lasprs::filter::*;
/// # fn main() -> anyhow::Result<()> {
/// let desc = StandardFilterDescriptor::Octave("16")?;
/// let filter = desc.genFilter().bilinear(48e3);
/// #    Ok(())
/// # }
/// ```
///
/// ## Create a one-third octave band bandpass filter that has the frequency of 42 in its pass-band
///
/// ```rust
///
/// use lasprs::filter::*;
/// # fn main() -> anyhow::Result<()> {
/// let desc = StandardFilterDescriptor::filterForFreq(3, 42.)?;
/// let filter = desc.genFilter().bilinear(48e3);
/// # Ok(())
/// # }
/// ```
///
/// ## Create a set of octave band filters
///
/// ```rust
/// use lasprs::filter::*;
/// # fn main() -> anyhow::Result<()> {
/// // Generate custom set..
/// let desc = StandardFilterDescriptor::genOctaveFilterSet("16", "16k").unwrap();
/// // Or, when lazy: just generate the full set
/// let desc = StandardFilterDescriptor::fullOctaveFilterSet();
/// let filters: Vec<SeriesBiquad> = desc.iter()
///     .map(|desc| desc.genFilter().bilinear(48e3))
///     .collect();
/// # Ok(())
/// # }
/// ```
#[cfg_attr(feature = "python-bindings", pyclass)]
#[derive(PartialEq, Clone, Debug)]
pub struct StandardFilterDescriptor {
    /// b and x. Bandwidth and offset w.r.t. reference frequency.
    ///
    /// Band width fraction of an octave. 1 means full octave of bandwidth. 3
    /// means 1/3th octave, 6 means 1/6th, and so on.
    ///
    /// If bx is None, it means we do not filter at all (an overall channel)
    b: u32,
    x: i32,
}

impl StandardFilterDescriptor {
    /// Create analog filter specification from descriptor
    pub fn genFilter(&self) -> ZPKModel {
        let order = 5;
        if let Some((fl, fu)) = self.fl_fh() {
            ZPKModel::butter(crate::FilterSpec::Bandpass { fl, fu, order })
        } else {
            ZPKModel::default()
        }
    }
    // Check whether a certain midband frequency of created
    // StandardFilterDescriptor is in the allowed range. This is a helper
    // function that is used to check wheter created StandardFilterDescriptors
    // are valid.
    fn check_fmid_in_range(&self) -> Result<()> {
        if let Some(fm) = self.fm() {
            if fm < MIN_MIDBAND_FREQ / 2. {
                bail!(
                    "Invalid x. Computed filter center frequency is {} Hz, which is too low. Lowest allowed is {} Hz",
                    fm, MIN_MIDBAND_FREQ
                )
            } else if fm > 25e3 {
                bail!(
                    "Invalid x. Computed filter center frequency is {} Hz, which is too high. Highest allowed is {} Hz",
                    fm, MAX_MIDBAND_FREQ
                )
            }
        }

        Ok(())
    }
    /// Create new standard filter descriptor `b` from given relative bandwidth
    /// and band designator `x`. If not sure what `x` and `b` are, see
    /// documentation on [StandardFilterDescriptor::genFilterSetByDesignator].
    pub fn build(b: u32, x: i32) -> Result<StandardFilterDescriptor> {
        let desc = StandardFilterDescriptor { b, x };
        desc.check_fmid_in_range()?;
        match b {
            0 => Ok(desc),
            1 => Ok(desc),
            3 => Ok(desc),
            6 => Ok(desc),
            12 => Ok(desc),
            24 => Ok(desc),
            _ => bail!(
                "Bandwidth {} is invalid. Please choose a value from 0, 1, 3, 6, 12 or 24",
                b
            ),
        }
    }
    /// Generate filter descriptor. Practically applies no filtering at all.
    pub fn Overall() -> Result<StandardFilterDescriptor> {
        Ok(StandardFilterDescriptor { b: 0, x: 0 })
    }
    /// Generate filter descriptor for octave band.
    ///
    /// # Args
    ///
    /// - `band_descr` - band designator. Can be '1k', or 0.
    pub fn Octave<T>(band_descr: T) -> Result<StandardFilterDescriptor>
    where
        T: TryInto<OctaveBandDescriptor, Error = anyhow::Error>,
    {
        let x = band_descr.try_into()?.x;
        Ok(StandardFilterDescriptor { b: 1, x })
    }
    /// Generate filter descriptor for one-third octave band.
    ///
    /// # Args
    ///
    /// - `x` - band designator
    pub fn ThirdOctave<T>(band_descr: T) -> Result<StandardFilterDescriptor>
    where
        T: TryInto<ThirdOctaveBandDescriptor, Error = anyhow::Error>,
    {
        let x = band_descr.try_into()?.x;
        Ok(StandardFilterDescriptor { b: 3, x })
    }

    /// Searches for a filter with `1/b` relative bandwidth w.r.t one octave
    /// that has frequency `f` in its pass-band.
    ///
    pub fn filterForFreq(b: u32, f: Flt) -> Result<StandardFilterDescriptor> {
        if f < MIN_MIDBAND_FREQ || f > MAX_MIDBAND_FREQ {
            bail!("Invalid frequency. Please use search frequency between 8 Hz and 20 kHz")
        }
        match b {
            0 => Self::Overall(),
            1 | 3 | 6 | 12 | 24 => {
                let mut desc = StandardFilterDescriptor { b, x: 0 };

                let f_in_range = |desc: &StandardFilterDescriptor| {
                    let (fl, fh) = desc.fl_fh().unwrap();
                    // println!("fl: {fl}, fh: {fh}");
                    if f < fl {
                        Ordering::Less
                    } else if f > fh {
                        Ordering::Greater
                    } else {
                        Ordering::Equal
                    }
                };

                loop {
                    // Get midband. Assuming we are not overall if we arrive
                    // here in the loop
                    let fm = desc.fm().unwrap();
                    let ord = f_in_range(&desc);
                    // Bands for midband frequencies are a bit wider here
                    if fm < MIN_MIDBAND_FREQ - 3. || fm > MAX_MIDBAND_FREQ * 1.1 {
                        bail!("Frequency not in range");
                    }
                    match ord {
                        Ordering::Equal => break,
                        Ordering::Less => desc = StandardFilterDescriptor { b, x: desc.x - 1 },
                        Ordering::Greater => desc = StandardFilterDescriptor { b, x: desc.x + 1 },
                    }
                }
                Ok(desc)
            }
            _ => Self::build(b, 0),
        }
    }

    /// Creates a set of octave filters.
    pub fn genOctaveFilterSet<T>(low_f: T, high_f: T) -> Result<Vec<Self>>
    where
        T: TryInto<OctaveBandDescriptor, Error = anyhow::Error>,
    {
        let xmin = low_f.try_into()?.x;
        let xmax = high_f.try_into()?.x;
        Ok((xmin..=xmax).map(|x| Self::Octave(x).unwrap()).collect())
    }

    /// Generate a full third octave bandpass filter set
    pub fn fullThirdOctaveFilterSet() -> Vec<Self> {
        Self::genThirdOctaveFilterSet(
            THIRDOCTAVE_NOMINAL_MIDBAND_NAMES[0],
            *(THIRDOCTAVE_NOMINAL_MIDBAND_NAMES.last().unwrap()),
        )
        .unwrap()
    }

    /// Generate a full octave bandpass filter set
    pub fn fullOctaveFilterSet() -> Vec<Self> {
        Self::genOctaveFilterSet(
            OCTAVE_NOMINAL_MIDBAND_NAMES[0],
            *(OCTAVE_NOMINAL_MIDBAND_NAMES.last().unwrap()),
        )
        .unwrap()
    }

    /// Creates a set of one-third octave bandpass filters.
    pub fn genThirdOctaveFilterSet<T>(low_f: T, high_f: T) -> Result<Vec<Self>>
    where
        T: TryInto<ThirdOctaveBandDescriptor, Error = anyhow::Error>,
    {
        let xmin = low_f.try_into()?.x;
        let xmax = high_f.try_into()?.x;
        Ok((xmin..=xmax)
            .map(|x| Self::ThirdOctave(x).unwrap())
            .collect())
    }

    /// Generate a filter set using designators
    ///
    /// # Args
    ///
    /// - `b` - Inverse of the relative bandwidth w.r.t. one octave. `b=0` means
    ///   overall, `b=1` is one octave, `b=3`` is one-third, etc.
    /// - `xmin` - Band designator of lowest band. Midband frequency can be computed as [FREQ_REF]*[G]^(`xmin/b`)
    /// - `xmax` - Band designator of lowest band. Midband frequency can be computed as [FREQ_REF]*[G]^(`xmax/b`)
    /// - `append_overall` - If `true`, adds an overall filter (a no-op) as the last designator in the list
    pub fn genFilterSetByDesignator(
        b: u32,
        xmin: i32,
        xmax: i32,
        append_overall: bool,
    ) -> Result<Vec<Self>> {
        if xmin > xmax {
            bail!("xmin should be <= xmax");
        }
        let cap = (xmax - xmin) as usize + if append_overall { 1 } else { 0 };
        let mut res = Vec::with_capacity(cap);

        for x in xmin..=xmax {
            res.push(StandardFilterDescriptor::build(b, x)?);
        }

        if append_overall {
            res.push(StandardFilterDescriptor::Overall()?)
        }

        Ok(res)
    }

    /// Convenience function for creating a filter bank. Creates a set of
    /// standard filters with relative bandwidth `b`, that has `fl` in the
    /// lowest bandpass filter and `fu` in the highest.
    ///
    /// # Other args
    ///
    /// - `append_overall` - If `true`, adds an overall filter (a no-op) as the
    ///   last filter in the list.
    pub fn genFilterSetForRange(
        b: u32,
        fl: Flt,
        fu: Flt,
        append_overall: bool,
    ) -> Result<Vec<Self>> {
        let xmin = StandardFilterDescriptor::filterForFreq(b, fl)?.x;
        let xmax = StandardFilterDescriptor::filterForFreq(b, fu)?.x;
        StandardFilterDescriptor::genFilterSetByDesignator(b, xmin, xmax, append_overall)
    }

    /// Returns the midband frequency in \[Hz\]
    pub fn fm(&self) -> Option<Flt> {
        if self.b == 0 {
            None
        } else {
            let b = self.b as Flt;
            let x = self.x as Flt;
            Some(FREQ_REF * G.powf(x / b))
        }
    }

    /// Cuton frequency and cut-off frequency, in \[Hz\].
    /// Returns none if it does not apply, for [StandardFilterDescriptor::Overall].
    pub fn fl_fh(&self) -> Option<(Flt, Flt)> {
        match self.b {
            0 => None,
            b => {
                let fm = self.fm().unwrap();
                let b = b as Flt;
                let fl = fm * G.powf(-1. / (2. * b));
                let fu = fm * G.powf(1. / (2. * b));
                Some((fl, fu))
            }
        }
    }
    /// Give a common name to filter, specifically the filters are named after
    /// the midband frequency.
    pub fn name(&self) -> Cow<'static, str> {
        let x = self.x;
        match self.b {
            0 => Cow::Borrowed("Overall"),
            1 => OctaveBandDescriptor { x }.name(),
            3 => ThirdOctaveBandDescriptor { x }.name(),
            6 => {
                if x % 2 == 0 {
                    ThirdOctaveBandDescriptor { x: x / 2 }.name()
                } else {
                    Default::default()
                }
            }
            12 => {
                if x % 2 == 0 {
                    StandardFilterDescriptor {
                        b: self.b / 2,
                        x: self.x / 2,
                    }
                    .name()
                } else {
                    Default::default()
                }
            }
            _ => unreachable!(),
        }
    }
}

/// A valid descriptor for a standard one-third octave band
pub struct ThirdOctaveBandDescriptor {
    x: i32,
}
/// A valid descriptor for a standard octave band
pub struct OctaveBandDescriptor {
    x: i32,
}

impl TryFrom<i32> for OctaveBandDescriptor {
    type Error = anyhow::Error;
    fn try_from(x: i32) -> Result<Self, Self::Error> {
        if x + OCTAVE_NAMES_OFFSET < 0
            || x + OCTAVE_NAMES_OFFSET >= OCTAVE_NOMINAL_MIDBAND_NAMES.len() as i32
        {
            bail!(
                "Invalid filter designator x. Should be >= -{OCTAVE_NAMES_OFFSET} and < {}",
                OCTAVE_NOMINAL_MIDBAND_NAMES.len() as i32 - OCTAVE_NAMES_OFFSET
            );
        }
        Ok(Self { x })
    }
}
impl TryFrom<&str> for OctaveBandDescriptor {
    type Error = anyhow::Error;
    fn try_from(name: &str) -> Result<Self, Self::Error> {
        Ok(Self {
            x: nominal_octave_designator(name)?,
        })
    }
}
impl TryFrom<i32> for ThirdOctaveBandDescriptor {
    type Error = anyhow::Error;
    fn try_from(x: i32) -> Result<Self, Self::Error> {
        if x + THIRDOCTAVE_NAMES_OFFSET < 0
            || x + THIRDOCTAVE_NAMES_OFFSET >= THIRDOCTAVE_NOMINAL_MIDBAND_NAMES.len() as i32
        {
            bail!(
                "Invalid filter designator x. Should be >= -{THIRDOCTAVE_NAMES_OFFSET} and < {}",
                THIRDOCTAVE_NOMINAL_MIDBAND_NAMES.len() as i32 - THIRDOCTAVE_NAMES_OFFSET
            );
        }
        Ok(Self { x })
    }
}
impl TryFrom<&str> for ThirdOctaveBandDescriptor {
    type Error = anyhow::Error;
    fn try_from(name: &str) -> Result<Self, Self::Error> {
        Ok(Self {
            x: nominal_thirdoctave_designator(name)?,
        })
    }
}
impl TryFrom<Flt> for ThirdOctaveBandDescriptor {
    type Error = anyhow::Error;
    fn try_from(value: Flt) -> Result<Self, Self::Error> {
        Ok(ThirdOctaveBandDescriptor {
            x: StandardFilterDescriptor::filterForFreq(3, value)?.x,
        })
    }
}
impl TryFrom<Flt> for OctaveBandDescriptor {
    type Error = anyhow::Error;
    fn try_from(value: Flt) -> Result<Self, Self::Error> {
        Ok(OctaveBandDescriptor {
            x: StandardFilterDescriptor::filterForFreq(1, value)?.x,
        })
    }
}

trait BandDescriptor {
    fn name(&self) -> Cow<'static, str>;
}
impl BandDescriptor for OctaveBandDescriptor {
    fn name(&self) -> Cow<'static, str> {
        Cow::Borrowed(
            OCTAVE_NOMINAL_MIDBAND_NAMES
                .get((self.x + OCTAVE_NAMES_OFFSET) as usize)
                .map(|s| *s)
                .unwrap_or_default(),
        )
    }
}
impl BandDescriptor for ThirdOctaveBandDescriptor {
    fn name(&self) -> Cow<'static, str> {
        Cow::Borrowed(
            THIRDOCTAVE_NOMINAL_MIDBAND_NAMES
                .get((self.x + THIRDOCTAVE_NAMES_OFFSET) as usize)
                .map(|s| *s)
                .unwrap_or_default(),
        )
    }
}

#[cfg(feature = "python-bindings")]
#[cfg_attr(feature = "python-bindings", pymethods)]
impl StandardFilterDescriptor {
    #[pyo3(name = "genFilter")]
    fn genFilter_py(&self) -> ZPKModel {
        self.genFilter()
    }
    #[staticmethod]
    #[pyo3(name = "Overall")]
    fn Overall_py() -> StandardFilterDescriptor {
        StandardFilterDescriptor::Overall().unwrap()
    }

    #[staticmethod]
    #[pyo3(name = "genThirdOctaveFilterSet")]
    fn genThirdOctaveFilterSet_py(fmin: Flt, fmax: Flt) -> PyResult<Vec<StandardFilterDescriptor>> {
        Ok(Self::genThirdOctaveFilterSet(fmin, fmax)?)
    }

    #[staticmethod]
    #[pyo3(name = "genOctaveFilterSet")]
    fn genOctaveFilterSetFromFreq(fmin: Flt, fmax: Flt) -> PyResult<Vec<StandardFilterDescriptor>> {
        Ok(Self::genOctaveFilterSet(fmin, fmax)?)
    }

    #[staticmethod]
    fn genThirdOctaveFilterSetFromFreq(
        fmin: Flt,
        fmax: Flt,
    ) -> PyResult<Vec<StandardFilterDescriptor>> {
        Ok(Self::genThirdOctaveFilterSet(fmin, fmax)?)
    }

    fn __repr__(&self) -> String {
        format! {"{:#?}", self}
    }

    fn __str__(&self) -> String {
        self.name().into()
    }

    #[staticmethod]
    #[pyo3(name = "genFilterSetInRange")]
    fn genFilterSetInRange_py(
        b: u32,
        fmin: Flt,
        fmax: Flt,
        append_overall: bool,
    ) -> PyResult<Vec<StandardFilterDescriptor>> {
        Ok(Self::genFilterSetForRange(b, fmin, fmax, append_overall)?)
    }
}

#[cfg(test)]
mod test {
    use super::*;
    use approx::assert_abs_diff_eq;

    #[test]
    fn test_finder() {
        // assert_eq!(
        //     StandardFilterDescriptor::filterForFreq(0, 1000.).unwrap(),
        //     StandardFilterDescriptor::Overall().unwrap()
        // );
        // assert_eq!(
        //     StandardFilterDescriptor::filterForFreq(1, 1e3).unwrap(),
        //     StandardFilterDescriptor::Octave(0).unwrap()
        // );
        assert_eq!(
            StandardFilterDescriptor::filterForFreq(1, 8.).unwrap(),
            StandardFilterDescriptor::Octave(-OCTAVE_NAMES_OFFSET).unwrap()
        );
        // assert_eq!(
        //     StandardFilterDescriptor::filterForFreq(3, 1000.).unwrap(),
        //     StandardFilterDescriptor::ThirdOctave(0).unwrap()
        // );
        // assert_eq!(
        //     StandardFilterDescriptor::filterForFreq(3, 12.).unwrap(),
        //     StandardFilterDescriptor::ThirdOctave(-THIRDOCTAVE_NAMES_OFFSET).unwrap()
        // );
    }

    #[test]
    fn test_builders() {
        assert_eq!(
            StandardFilterDescriptor::Octave("8").unwrap(),
            StandardFilterDescriptor::Octave(-OCTAVE_NAMES_OFFSET).unwrap()
        );
        assert_eq!(
            StandardFilterDescriptor::Octave("2k").unwrap(),
            StandardFilterDescriptor::Octave(1).unwrap()
        );
        assert_eq!(
            StandardFilterDescriptor::ThirdOctave("12.5").unwrap(),
            StandardFilterDescriptor::ThirdOctave(-THIRDOCTAVE_NAMES_OFFSET).unwrap()
        );
        assert_eq!(
            StandardFilterDescriptor::ThirdOctave("2k").unwrap(),
            StandardFilterDescriptor::ThirdOctave(3).unwrap()
        );
    }
    #[test]
    #[should_panic]
    fn out_range_octave1() {
        StandardFilterDescriptor::Octave("4").unwrap();
    }
    #[test]
    #[should_panic]
    fn out_range_octave2() {
        StandardFilterDescriptor::Octave("7").unwrap();
    }

    #[test]
    fn test_name_and_approx() {
        assert_eq!(
            StandardFilterDescriptor::filterForFreq(1, 16e3).unwrap(),
            StandardFilterDescriptor::Octave("16k").unwrap(),
        );
    }

    #[test]
    fn test_names() {
        assert_eq!(StandardFilterDescriptor::Octave(1).unwrap().name(), "2k");
        assert_eq!(
            StandardFilterDescriptor::ThirdOctave(1).unwrap().name(),
            "1.25k"
        );
    }

    #[test]
    fn test_octave() {
        assert_eq!(nominal_octave_designator("1k").unwrap(), 0);
        assert_eq!(nominal_octave_designator("2k").unwrap(), 1);
    }
    #[test]
    fn test_thirdoctave() {
        assert_eq!(nominal_thirdoctave_designator("1k").unwrap(), 0);
        assert_eq!(nominal_thirdoctave_designator("2k").unwrap(), 3);
    }

    #[test]
    fn test_G() {
        assert_abs_diff_eq!(G, (10 as Flt).powf(3. / 10.));
    }
}
