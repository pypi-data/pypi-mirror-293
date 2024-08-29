use super::RpcAddress;
use super::RpcTransaction;
use borsh::{BorshDeserialize, BorshSerialize};
use serde::{Deserialize, Serialize};

#[cfg(not(target_family = "wasm"))]
use pyo3::pyclass;

#[derive(Clone, Debug, Serialize, Deserialize, BorshSerialize, BorshDeserialize)]
#[cfg(not(target_family = "wasm"))]
#[pyclass]
pub struct RpcMempoolEntry {
    #[pyo3(get)]
    pub fee: u64,
    #[pyo3(get)]
    pub transaction: RpcTransaction,
    #[pyo3(get)]
    pub is_orphan: bool,
}

#[derive(Clone, Debug, Serialize, Deserialize, BorshSerialize, BorshDeserialize)]
#[cfg(target_family = "wasm")]
pub struct RpcMempoolEntry {
    pub fee: u64,
    pub transaction: RpcTransaction,
    pub is_orphan: bool,
}

impl RpcMempoolEntry {
    pub fn new(fee: u64, transaction: RpcTransaction, is_orphan: bool) -> Self {
        Self { fee, transaction, is_orphan }
    }
}

#[derive(Clone, Debug, Serialize, Deserialize, BorshSerialize, BorshDeserialize)]
#[cfg(not(target_family = "wasm"))]
#[pyclass]
pub struct RpcMempoolEntryByAddress {
    #[pyo3(get)]
    pub address: RpcAddress,
    #[pyo3(get)]
    pub sending: Vec<RpcMempoolEntry>,
    #[pyo3(get)]
    pub receiving: Vec<RpcMempoolEntry>,
}

#[derive(Clone, Debug, Serialize, Deserialize, BorshSerialize, BorshDeserialize)]
#[cfg(target_family = "wasm")]
pub struct RpcMempoolEntryByAddress {
    pub address: RpcAddress,
    pub sending: Vec<RpcMempoolEntry>,
    pub receiving: Vec<RpcMempoolEntry>,
}

impl RpcMempoolEntryByAddress {
    pub fn new(address: RpcAddress, sending: Vec<RpcMempoolEntry>, receiving: Vec<RpcMempoolEntry>) -> Self {
        Self { address, sending, receiving }
    }
}

cfg_if::cfg_if! {
    if #[cfg(feature = "wasm32-sdk")] {
        use wasm_bindgen::prelude::*;

        #[wasm_bindgen(typescript_custom_section)]
        const TS_MEMPOOL_ENTRY: &'static str = r#"
            /**
             * Mempool entry.
             * 
             * @category Node RPC
             */
            export interface IMempoolEntry {
                fee : bigint;
                transaction : ITransaction;
                isOrphan : boolean;
            }
        "#;
    }
}
