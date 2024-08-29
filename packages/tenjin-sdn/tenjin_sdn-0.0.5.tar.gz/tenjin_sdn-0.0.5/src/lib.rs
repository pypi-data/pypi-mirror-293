pub mod cli;
use pyo3::prelude::*;
use tenjin::{
    example::{Controller10, Controller13},
    openflow::{ofp10::ControllerFrame10, ofp13::ControllerFrame13},
};

#[pyfunction]
fn cli_default() {
    cli::system();
}

#[pyfunction]
fn say_hello() -> String {
    "Hello".to_string()
}

#[pyfunction]
fn controller13(address: String) {
    Controller13::new().listener(&address);
}

#[pyfunction]
fn controller10(address: String) {
    Controller10::new().listener(&address);
}

#[pymodule]
fn tenjin_sdn(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(say_hello, m)?)?;
    m.add_function(wrap_pyfunction!(cli_default, m)?)?;
    m.add_function(wrap_pyfunction!(controller13, m)?)?;
    m.add_function(wrap_pyfunction!(controller10, m)?)?;
    Ok(())
}
