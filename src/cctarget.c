#include <stdio.h>
#include "cctarget.h"

void display_target_info(void) {
    printf("Compilation Target Information:\n");
    printf("-------------------------------\n");
    
    #ifdef __linux__
        printf("Operating System: Linux\n");
    #elif defined(_WIN32) || defined(_WIN64)
        printf("Operating System: Windows\n");
    #elif defined(__APPLE__) && defined(__MACH__)
        printf("Operating System: macOS\n");
    #elif defined(__unix__)
        printf("Operating System: Unix\n");
    #else
        printf("Operating System: Unknown\n");
    #endif
    
    #ifdef __x86_64__
        printf("Architecture: x86_64 (64-bit)\n");
    #elif defined(__i386__)
        printf("Architecture: x86 (32-bit)\n");
    #elif defined(__aarch64__) || defined(__arm64__)
        printf("Architecture: ARM64\n");
    #elif defined(__arm__)
        printf("Architecture: ARM\n");
    #else
        printf("Architecture: Unknown\n");
    #endif
    
    #ifdef __GNUC__
        printf("Compiler: GCC %d.%d.%d\n", __GNUC__, __GNUC_MINOR__, __GNUC_PATCHLEVEL__);
    #elif defined(__clang__)
        printf("Compiler: Clang %d.%d.%d\n", __clang_major__, __clang_minor__, __clang_patchlevel__);
    #elif defined(_MSC_VER)
        printf("Compiler: MSVC %d\n", _MSC_VER);
    #else
        printf("Compiler: Unknown\n");
    #endif
    
    printf("Pointer Size: %zu bytes\n", sizeof(void*));
}
