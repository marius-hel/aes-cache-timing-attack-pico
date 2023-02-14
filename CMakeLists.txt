cmake_minimum_required(VERSION 3.19)

include(pico_sdk_import.cmake)

project(rp2040_freertos_aes)

pico_sdk_init()

add_executable(rp2040_freertos_aes
        src/main.c
        src/rijndael-alg-fst.c
)

FILE(GLOB FreeRTOS_src FreeRTOS-Kernel/*.c)

add_library( FreeRTOS STATIC
        ${FreeRTOS_src}
        FreeRTOS-Kernel/portable/GCC/ARM_CM0/port.c
        FreeRTOS-Kernel/portable/MemMang/heap_4.c
)

target_include_directories( FreeRTOS PUBLIC
        FreeRTOS-Kernel/include
        include/
        FreeRTOS-Kernel/portable/GCC/ARM_CM0
)

# Pull in our pico_stdlib which aggregates commonly used features
target_link_libraries( rp2040_freertos_aes
        pico_stdlib
        pico_bootrom
        FreeRTOS
)

# enable usb output, disable uart output
pico_enable_stdio_usb(rp2040_freertos_aes 1)
pico_enable_stdio_uart(rp2040_freertos_aes 0)

# create map/bin/hex/uf2 file etc.
pico_add_extra_outputs(rp2040_freertos_aes)
