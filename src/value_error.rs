use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use std::{error::Error, fmt};

/// Parameter error message
///
/// For invalid parameter values used in problem setup
#[derive(Debug, PartialEq)]
pub struct ValueError {
    pub message: String,
}

impl ValueError {
    pub fn new(message: String) -> Self {
        Self { message }
    }
}

impl Error for ValueError {}

impl fmt::Display for ValueError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "Parameter error: {}", &self.message)
    }
}

impl std::convert::From<ValueError> for PyErr {
    fn from(err: ValueError) -> PyErr {
        PyValueError::new_err(err.to_string())
    }
}
