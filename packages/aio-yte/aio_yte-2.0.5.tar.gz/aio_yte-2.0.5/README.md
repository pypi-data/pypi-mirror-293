# AIO-YTE - An Asynchronous YAML Template Engine with Python Expressions

[![Docs](https://img.shields.io/badge/user-documentation-green)](https://yte-template-engine.github.io)
[![test coverage: 100%](https://img.shields.io/badge/test%20coverage-100%25-green)](https://github.com/yte-template-engine/yte/blob/main/pyproject.toml#L30)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/yte-template-engine/yte/testing.yml?branch=main)
![PyPI](https://img.shields.io/pypi/v/yte)
[![Conda Recipe](https://img.shields.io/badge/recipe-yte-green.svg)](https://anaconda.org/conda-forge/yte)
[![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/yte.svg)](https://anaconda.org/conda-forge/yte)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/yte.svg)](https://github.com/conda-forge/yte-feedstock)

AIO-YTE is an asynchronous template engine for YAML format that extends the YAML structure with Python expressions, enabling dynamic YAML document generation. The key feature of AIO-YTE is its ability to process Python expressions asynchronously, making it ideal for use in environments that require asynchronous operations, such as web servers or other I/O-bound applications.

## Key Features

- **Asynchronous Evaluation:** AIO-YTE allows you to use `await` within your YAML templates, enabling asynchronous processing of expressions. This is particularly useful in modern Python applications where asynchronous code is prevalent.
  
- **YAML-First Approach:** Like its predecessor YTE, AIO-YTE leverages YAML's structure to simplify2the syntax for template expressions, making it more intuitive and human-readable while maintaining YAML's native semantics.

- **Python Expression Integration:** AIO-YTE integrates Python syntax directly into YAML, allowing you to use conditionals, loops, and other Python expressions seamlessly within your templates.

## Documentation

Comprehensive documentation for YTE can be found at [yte-template-engine.github.io](https://yte-template-engine.github.io).

## Comparison with Other Engines

Many template engines are available, such as the popular [jinja2](https://jinja.palletsprojects.com). AIO-YTE is specifically designed for YAML, offering several advantages:

1. **YAML-Specific Syntax:** By utilizing YAML's syntax, AIO-YTE reduces the need for additional control flow symbols, making the templates more readable and less foreign to those familiar with YAML.
2. **Improved Whitespace Handling:** YAML's semantics require careful handling of whitespace, which AIO-YTE manages seamlessly without the need for complex configurations, as might be necessary with engines like jinja2.

Other YAML-specific template engines include:

- **[Yglu](https://yglu.io)**
- **[Yte](https://github.com/yte-template-engine/yte)**
- **[Emrichen](https://github.com/con2/emrichen)**

The main distinction of AIO-YTE is its extension of YAML with native Python syntax and its support for asynchronous operations. This allows for more natural and powerful template processing, particularly in applications that require asynchronous execution.

## Differences Between AIO-YTE and YTE

While AIO-YTE retains the core functionality of YTE, it introduces several key enhancements:

- **Asynchronous Processing:** The primary difference is the ability to handle asynchronous expressions, enabling the use of `await` directly within YAML templates.
- **Enhanced Error Handling:** AIO-YTE improves error handling, particularly in the context of asynchronous operations, ensuring more robust and predictable template evaluation.
- **Backwards Compatibility:** AIO-YTE remains compatible with existing YTE templates but extends their capabilities to handle async code, making it a drop-in replacement for applications that require async processing.

By incorporating these features, AIO-YTE is designed to meet the needs of modern Python applications, offering a powerful and flexible template engine for YAML.
