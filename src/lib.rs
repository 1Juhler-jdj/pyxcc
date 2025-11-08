mod value_error;

use ::algoxcc as xcc;
use pyo3::prelude::*;
use value_error::ValueError;

#[derive(FromPyObject)]
#[pyclass(module = "algoxcc")]
pub struct Option {
    pub label: String,
    pub primary_items: Vec<String>,
    pub secondary_items: Vec<(String, String)>,
}
#[pymethods]
impl Option {
    #[new]
    pub fn new(
        label: String,
        primary_items: Vec<String>,
        secondary_items: Vec<(String, String)>,
    ) -> Result<Self, ValueError> {
        let result = xcc::option_validate(
            &primary_items.iter().map(|s| s.as_str()).collect(),
            &secondary_items
                .iter()
                .map(|s| (s.0.as_str(), s.1.as_str()))
                .collect(),
        );
        match result {
            Ok(()) => Ok(Option {
                label,
                primary_items,
                secondary_items,
            }),
            Err(e) => Err(ValueError::new(e.message)),
        }
    }
    pub fn add_primary_item(&mut self, item: String) -> Result<(), ValueError> {
        let result = xcc::new_primary_validate(
            &self.primary_items.iter().map(|s| s.as_str()).collect(),
            &item.as_str(),
        );
        match result {
            Ok(()) => {
                self.primary_items.push(item);
                Ok(())
            }
            Err(e) => Err(ValueError::new(e.message)),
        }
    }
    pub fn add_secondary_item(&mut self, item: (String, String)) -> Result<(), ValueError> {
        let result = xcc::new_secondary_validate(
            &self
                .secondary_items
                .iter()
                .map(|s| (s.0.as_str(), s.1.as_str()))
                .collect(),
            &(item.0.as_str(), item.1.as_str()),
        );
        match result {
            Ok(()) => {
                self.secondary_items.push(item);
                Ok(())
            }
            Err(e) => Err(ValueError::new(e.message)),
        }
    }
    #[getter]
    pub fn get_label(&self) -> &str {
        &self.label
    }
    #[setter]
    pub fn set_label(&mut self, label: String) {
        self.label = label;
    }
    #[getter]
    pub fn primary_items(&self) -> Vec<String> {
        self.primary_items.iter().map(|i| i.clone()).collect()
    }
    #[getter]
    pub fn secondary_items(&self) -> Vec<(String, String)> {
        self.secondary_items.iter().map(|i| i.clone()).collect()
    }
}

#[derive(FromPyObject)]
#[pyclass(module = "algoxcc")]
pub struct Problem {
    pub primary_items: Vec<String>,
    pub secondary_items: Vec<String>,
    pub options: Vec<Option>,
}
#[pymethods]
impl Problem {
    #[new]
    pub fn new(
        primary_items: Vec<String>,
        secondary_items: Vec<String>,
        options: Vec<Option>,
    ) -> Result<Self, ValueError> {
        let result = xcc::problem_validate(
            &primary_items.iter().map(|s| s.as_str()).collect(),
            &secondary_items.iter().map(|s| s.as_str()).collect(),
            &options
                .iter()
                .map(|o| {
                    xcc::Option::new_validated(
                        o.label.as_str(),
                        &o.primary_items.iter().map(|s| s.as_str()).collect(),
                        &o.secondary_items
                            .iter()
                            .map(|s| (s.0.as_str(), s.1.as_str()))
                            .collect(),
                    )
                })
                .collect(),
        );
        match result {
            Ok(_) => Ok(Problem {
                primary_items,
                secondary_items,
                options,
            }),
            Err(e) => Err(ValueError::new(e.message)),
        }
    }
    pub fn add_primary_item(&mut self, item: String) -> Result<(), ValueError> {
        let result = xcc::new_item_validate(
            &self.primary_items.iter().map(|s| s.as_str()).collect(),
            &item,
        );
        match result {
            Ok(()) => {
                self.primary_items.push(item);
                Ok(())
            }
            Err(e) => Err(ValueError::new(e.message)),
        }
    }
    pub fn add_secondary_item(&mut self, item: String) -> Result<(), ValueError> {
        let result = xcc::new_item_validate(
            &self.secondary_items.iter().map(|s| s.as_str()).collect(),
            &item,
        );
        match result {
            Ok(()) => {
                self.secondary_items.push(item);
                Ok(())
            }
            Err(e) => Err(ValueError::new(e.message)),
        }
    }
    pub fn add_option(&mut self, option: Option) -> Result<(), ValueError> {
        let rust_option = xcc::Option::new_validated(
            option.label.as_str(),
            &option.primary_items.iter().map(|s| s.as_str()).collect(),
            &option
                .secondary_items
                .iter()
                .map(|s| (s.0.as_str(), s.1.as_str()))
                .collect(),
        );
        let result = xcc::new_option_validate(
            &self
                .options
                .iter()
                .map(|o| {
                    xcc::Option::new_validated(
                        o.label.as_str(),
                        &o.primary_items.iter().map(|s| s.as_str()).collect(),
                        &o.secondary_items
                            .iter()
                            .map(|s| (s.0.as_str(), s.1.as_str()))
                            .collect(),
                    )
                })
                .collect(),
            &rust_option,
        );
        match result {
            Ok(()) => {
                self.options.push(option);
                Ok(())
            }
            Err(e) => Err(ValueError::new(e.message)),
        }
    }
}

#[pyfunction]
pub fn solve(problem: &Problem, get_all: bool) -> Result<Vec<Vec<String>>, ValueError> {
    let rust_problem = xcc::Problem::new_validated(
        &problem.primary_items.iter().map(|s| s.as_str()).collect(),
        &problem.secondary_items.iter().map(|s| s.as_str()).collect(),
        &problem
            .options
            .iter()
            .map(|o| {
                xcc::Option::new_validated(
                    o.label.as_str(),
                    &o.primary_items.iter().map(|s| s.as_str()).collect(),
                    &o.secondary_items
                        .iter()
                        .map(|s| (s.0.as_str(), s.1.as_str()))
                        .collect(),
                )
            })
            .collect(),
    );
    let result = xcc::DancingCells::new(&rust_problem);
    if result.is_err() {
        return Err(ValueError {
            message: result.err().unwrap().message,
        });
    }
    let mut dc = result.unwrap();
    if get_all {
        return Ok(dc.solve_all());
    }
    Ok(dc.solve_first())
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn algoxcc(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Option>()?;
    m.add_class::<Problem>()?;
    m.add_function(wrap_pyfunction!(solve, m)?)?;
    Ok(())
}
