# CCTARGET Makefile
# Demonstrates cross-compilation target configuration

# Compiler configuration
CC ?= gcc
TARGET ?= native

# Directories
SRC_DIR := src
BUILD_DIR := build
BIN_DIR := bin

# Source files
SRCS := $(wildcard $(SRC_DIR)/*.c)
OBJS := $(SRCS:$(SRC_DIR)/%.c=$(BUILD_DIR)/%.o)

# Output binary
BINARY := $(BIN_DIR)/cctarget

# Compiler flags
CFLAGS := -Wall -Wextra -std=c99
LDFLAGS :=

# Target-specific configurations
ifeq ($(TARGET),arm)
    CC := arm-linux-gnueabi-gcc
    CFLAGS += -march=armv7-a
else ifeq ($(TARGET),arm64)
    CC := aarch64-linux-gnu-gcc
    CFLAGS += -march=armv8-a
else ifeq ($(TARGET),x86)
    CFLAGS += -m32
else ifeq ($(TARGET),x86_64)
    CFLAGS += -m64
else ifeq ($(TARGET),native)
    # Use default compiler and flags
else
    $(warning Unknown target: $(TARGET), using native)
endif

# Phony targets
.PHONY: all clean run help info

# Default target
all: $(BINARY)

# Create directories
$(BUILD_DIR) $(BIN_DIR):
	mkdir -p $@

# Compile source files
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

# Link binary
$(BINARY): $(OBJS) | $(BIN_DIR)
	$(CC) $(LDFLAGS) $^ -o $@
	@echo "Built $(BINARY) for target: $(TARGET)"

# Run the program
run: $(BINARY)
	./$(BINARY)

# Display compiler and target info
info:
	@echo "Compiler: $(CC)"
	@echo "Target: $(TARGET)"
	@echo "CFLAGS: $(CFLAGS)"
	@echo "LDFLAGS: $(LDFLAGS)"
	@echo "Source files: $(SRCS)"
	@echo "Object files: $(OBJS)"
	@echo "Binary: $(BINARY)"

# Clean build artifacts
clean:
	rm -rf $(BUILD_DIR) $(BIN_DIR)

# Help message
help:
	@echo "CCTARGET Build System"
	@echo "===================="
	@echo ""
	@echo "Available targets:"
	@echo "  all (default) - Build the project"
	@echo "  clean         - Remove build artifacts"
	@echo "  run           - Build and run the program"
	@echo "  info          - Display build configuration"
	@echo "  help          - Show this help message"
	@echo ""
	@echo "Build variables:"
	@echo "  CC            - C compiler (default: gcc)"
	@echo "  TARGET        - Target architecture (default: native)"
	@echo ""
	@echo "Supported TARGET values:"
	@echo "  native        - Native compilation (default)"
	@echo "  x86           - 32-bit x86"
	@echo "  x86_64        - 64-bit x86"
	@echo "  arm           - ARM 32-bit"
	@echo "  arm64         - ARM 64-bit"
	@echo ""
	@echo "Examples:"
	@echo "  make                    # Build with default settings"
	@echo "  make TARGET=x86_64      # Build for 64-bit x86"
	@echo "  make CC=clang           # Use Clang compiler"
	@echo "  make TARGET=arm CC=gcc  # Cross-compile for ARM"
