use borsh::{BorshDeserialize, BorshSerialize};
use serde::{Deserialize, Serialize};

#[cfg(not(target_family = "wasm"))]
use pyo3::{pyclass};

#[derive(Clone, Debug, Serialize, Deserialize, BorshSerialize, BorshDeserialize, Default)]
#[serde(rename_all = "camelCase")]
#[cfg(not(target_family = "wasm"))]
#[pyclass]
pub struct BlockCount {
    #[pyo3(get)]
    pub header_count: u64,
    #[pyo3(get)]
    pub block_count: u64,
}

#[derive(Clone, Debug, Serialize, Deserialize, BorshSerialize, BorshDeserialize, Default)]
#[serde(rename_all = "camelCase")]
#[cfg(target_family = "wasm")]
pub struct BlockCount {
    pub header_count: u64,
    pub block_count: u64,
}

impl BlockCount {
    pub fn new(block_count: u64, header_count: u64) -> Self {
        Self { block_count, header_count }
    }
}

#[derive(Clone, Default)]
pub struct VirtualStateStats {
    /// Number of direct parents of virtual
    pub num_parents: u32,
    pub daa_score: u64,
    pub bits: u32,
    pub past_median_time: u64,
}

pub struct ConsensusStats {
    /// Block and header counts
    pub block_counts: BlockCount,

    /// Overall number of current DAG tips
    pub num_tips: u64,

    /// Virtual-related stats
    pub virtual_stats: VirtualStateStats,
}
