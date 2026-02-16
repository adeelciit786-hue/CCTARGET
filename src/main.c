#include <stdio.h>
#include "cctarget.h"

int main(int argc, char *argv[]) {
    printf("CCTARGET - Cross-Compilation Target Demonstrator\n");
    printf("=================================================\n\n");
    
    display_target_info();
    
    if (argc > 1) {
        printf("\nArguments passed:\n");
        for (int i = 1; i < argc; i++) {
            printf("  [%d]: %s\n", i, argv[i]);
        }
    }
    
    return 0;
}
