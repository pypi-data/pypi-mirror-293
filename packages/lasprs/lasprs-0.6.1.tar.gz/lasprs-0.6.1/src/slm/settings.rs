use super::{TimeWeighting, SLM, SLM_MAX_CHANNELS};
use crate::{config::*, filter::StandardFilterDescriptor, Flt, FreqWeighting};
use anyhow::Result;
use clap::builder;
use derive_builder::Builder;
use smallvec::{smallvec, SmallVec};

const Lref_default: Flt = 20e-6;

/// Settings used to create a Sound Level Meter.
#[derive(Builder, Clone)]
#[builder(setter(into))]
#[cfg_attr(feature = "python-bindings", pyclass)]
pub struct SLMSettings {
    /// Sampling frequency in \[Hz\]
    pub fs: Flt,
    /// Reference level, in units of measured quantity. For sound pressure in
    /// air, this is typically 20 μPa. This is also the default value.
    #[builder(default = "Lref_default")]
    pub Lref: Flt,
    /// Frequency weightin A/C/Z applied to data. Defaults to [FreqWeighting::default()].
    #[builder(default)]
    pub freqWeighting: FreqWeighting,
    /// For time-dependent output, the time weighthing applied (Fast / Slow)
    pub timeWeighting: TimeWeighting,
    /// Descriptors for the filters, maximum of 64, which is a reasonable amount
    /// and - if all used - might already choke a computer.
    pub filterDescriptors: Vec<StandardFilterDescriptor>,
}

#[cfg(feature="python-bindings")]
#[cfg_attr(feature = "python-bindings", pymethods)]
impl SLMSettings {
    #[new]
    #[pyo3(signature=
        (fs, freqWeighting, 
         timeWeighting,
         filterDescriptors, 
         Lref=(Lref_default)))]
    fn new_py(
        fs: Flt,
        freqWeighting: FreqWeighting,
        timeWeighting: TimeWeighting,
        filterDescriptors: Vec<StandardFilterDescriptor>,
        Lref: Flt,
    ) -> SLMSettings {
        SLMSettings {
            fs,
            Lref,
            freqWeighting,
            timeWeighting,
            filterDescriptors,
        }
    }
}

#[cfg(test)]
mod test {
    use super::*;
    use anyhow::Result;

    #[test]
    fn test_slmsettings1() -> Result<()> {
        let desc = StandardFilterDescriptor::genFilterSetForRange(1, 100., 5e3, true).unwrap();

        let _ = SLMSettingsBuilder::default()
            .fs(1e3)
            .freqWeighting(FreqWeighting::A)
            .timeWeighting(TimeWeighting::Slow {})
            .filterDescriptors(desc)
            .build()
            .unwrap();

        Ok(())
    }
}
