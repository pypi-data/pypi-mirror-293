import os
import sys
import argparse
from pathlib import Path
from setuptools import setup, Extension
import pybind11
import time
from typing import Literal, Any, Optional

def generate_binding_file(module_name, header_file, binding_file):
    """Generates a binding file using pybind11 to wrap the provided header functions."""
    with open(binding_file, 'w') as f:
        f.write('#include <pybind11/pybind11.h>\n')
        f.write(f'#include "{header_file}"\n\n')  # Include the header correctly
        f.write('namespace py = pybind11;\n\n')
        f.write(f'PYBIND11_MODULE({module_name}, m) {{\n')

        current_namespace = ""  # To track the current namespace

        with open(header_file, 'r') as header:
            for line in header:
                line = line.strip()

                # Check for namespace declarations
                if line.startswith("namespace"):
                    current_namespace = line.split()[1].strip('{')
                    continue
                elif line == "}":  # Closing a namespace
                    current_namespace = ""
                    continue

                # Detect function declarations and bind them with correct namespaces
                if line.startswith("void") or line.startswith("int"):
                    func_name = line.split()[1].split('(')[0]
                    if current_namespace:
                        f.write(f'    m.def("{func_name}", &{current_namespace}::{func_name});\n')
                    else:
                        f.write(f'    m.def("{func_name}", &{func_name});\n')

        f.write('}\n')

def generate_stub_file(output_dir, module_name, header_file) -> str:
    #  raise NotImplementedError("Stub Files are currently not supported.")

    custom = """uint8_t = int
uint16_t = int
uint32_t = int
uint64_t = int
int8_t = int
int16_t = int
int32_t = int
int64_t = int
double = float\n"""

    """Generates a .pyi stub file for the generated module based on the header file."""
    stub_file = Path(output_dir) / f"{module_name}.pyi"
    print(f"Creating stubs at {stub_file}")
    with open(stub_file, 'w') as f:
        f.write(f"# Stubs for {module_name}\n")
        f.write("from typing import Any\n\n")
        f.write(custom)

        current_namespace = ""
        namespace_stack = []

        with open(header_file, 'r') as header:
            for line in header:
                line = line.strip()

                # Detect function declarations and generate corresponding stubs
                if line.startswith("void"):
                    func_name = line.split()[1].split('(')[0]
                    f.write(f"def {current_namespace}.{func_name}() -> None: ...\n")
                elif line.startswith("int"):
                    func_name = line.split()[1].split('(')[0]
                    f.write(f"def {func_name}(a: int) -> int: ...\n")
    return str(stub_file)

def build_extension(source_file, binding_file, output_dir, module_name):
    """Builds the extension using setuptools."""
    header_dir = Path(source_file).parent  # Get the directory of the source file

    ext_modules = [
        Extension(
            module_name,
            [source_file, binding_file],
            include_dirs=[pybind11.get_include(), str(header_dir)],  # Add the header file's directory
            language='c++'
        ),
    ]

    setup(
        name=module_name,
        version='0.1',
        ext_modules=ext_modules,
        script_args=['build_ext', '--inplace', '--build-temp', output_dir],
    )

def compile_file(source_file: str, header_file: str, output_package: str, language: Literal["c++"] = "c++", auto_stubs: bool = True) -> dict[str, Any]:

    start = time.perf_counter()

    if language not in {'c++'}:
        raise NotImplementedError(f"Language '{language}' was not implemented yet!")

    # Create a temporary build directory
    build_dir = Path("build")
    build_dir.mkdir(exist_ok=True)

    # Generate the binding file
    binding_file = build_dir / "bindings.cpp"
    generate_binding_file(output_package, header_file, binding_file)

    # Generate bindings and compile
    build_extension(source_file, str(binding_file), build_dir, output_package)
    stub_location: Optional[str] = None
    if auto_stubs:
        stub_location = generate_stub_file(build_dir, output_package, header_file)

    end = time.perf_counter()

    return {
        'time': end - start,
        'stubs?': auto_stubs,
        'stub_location': stub_location
    }
