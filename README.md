# CCTARGET

A cross-compilation target demonstration project that showcases how to configure C compiler (CC) and target architecture settings in a Makefile-based build system.

## Overview

CCTARGET is a simple C project that demonstrates:
- Cross-compilation target configuration
- Compiler detection and selection
- Platform and architecture detection at compile-time
- Makefile-based build system with flexible target options

## Building

### Prerequisites
- GCC or Clang compiler
- Make build tool
- (Optional) Cross-compilation toolchains for ARM targets

### Quick Start

Build with default settings (native target):
```bash
make
```

Run the program:
```bash
make run
```

### Building for Different Targets

Build for 64-bit x86:
```bash
make TARGET=x86_64
```

Build for 32-bit x86:
```bash
make TARGET=x86
```

Build for ARM (requires cross-compiler):
```bash
make TARGET=arm
```

Build for ARM64 (requires cross-compiler):
```bash
make TARGET=arm64
```

### Using Different Compilers

Use Clang instead of GCC:
```bash
make CC=clang
```

Combine compiler and target:
```bash
make CC=clang TARGET=x86_64
```

## Available Make Targets

- `make` or `make all` - Build the project
- `make clean` - Remove build artifacts
- `make run` - Build and run the program
- `make info` - Display build configuration
- `make help` - Show detailed help message

## Project Structure

```
.
├── Makefile           # Build configuration with CC/TARGET support
├── README.md          # This file
├── src/
│   ├── main.c         # Main program entry point
│   ├── cctarget.c     # Target information display
│   └── cctarget.h     # Header file
├── build/             # Compiled object files (generated)
└── bin/               # Binary output (generated)
```

## How It Works

The Makefile uses the `CC` (C Compiler) and `TARGET` variables to configure the build:

1. **CC Variable**: Specifies which compiler to use (gcc, clang, etc.)
2. **TARGET Variable**: Determines the target architecture and sets appropriate compiler flags

The C code uses preprocessor directives to detect:
- Operating system (Linux, Windows, macOS, Unix)
- CPU architecture (x86, x86_64, ARM, ARM64)
- Compiler version and type

## Example Output

```
CCTARGET - Cross-Compilation Target Demonstrator
=================================================

Compilation Target Information:
-------------------------------
Operating System: Linux
Architecture: x86_64 (64-bit)
Compiler: GCC 11.4.0
Pointer Size: 8 bytes
```

## License

This project is provided as-is for educational and demonstration purposes.
