#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/structs/systick.h"

#include "FreeRTOS.h"
#include "FreeRTOSConfig.h"
#include "task.h"

#include "aes.h"

#define LED_PIN 25
#define ON 1
#define OFF 0
#define ZERO_KEY_MODE

#define PAYLOAD_SIZE AES_BLOCK_SIZE + 1

/* Useful functions */

/**
 * Get the value of SysTick, whose frequency is normally the same as the CPU
 * if configSYSTICK_CLOCK_HZ is NOT defined in FreeRTOSConfig.h
 *
 * @return the SysTick register value
 */
u32 get_systick_value(void)
{
    return systick_hw->cvr;
}

/**
 * Print the <len> bytes of <buffer> in hex format to stdou. No endline.
 */
void print_buffer(u8 *buffer, const int len)
{
    for (int i = 0; i < len; i++)
    {
        printf("%02x", buffer[i]);
    }
}

/* Tasks */

void EncryptionTask(void *param)
{
    u8 in[PAYLOAD_SIZE] = {0x00};
    u8 out[AES_BLOCK_SIZE] = {0x00};
#ifdef ZERO_KEY_MODE
    u8 key[AES_KEY_SIZE] = {0x00};
#else
    u8 key[AES_KEY_SIZE] = {
        0x0f,
        0x1e,
        0x2d,
        0x3c,
        0x4b,
        0x5a,
        0x69,
        0x78,
        0x87,
        0x96,
        0xa5,
        0xb4,
        0xc3,
        0xd2,
        0xe1,
        0xf0};
#endif

    u32 int_key[4 * (AES_NUM_ROUNDS + 1)];

    aes_set_enc_key(key, int_key);

    fflush(stdin);

    for (;;)
    {
        fgets(in, PAYLOAD_SIZE, stdin);

        u32 before = get_systick_value();
        aes_encrypt(in, out, int_key);
        u32 after = get_systick_value();

        int delta = before - after; // systick is decreasing

        print_buffer(in, AES_BLOCK_SIZE);
        printf(";%d\n", delta);
    }
}

int main()
{
    /* Some variables */
    TaskHandle_t encryptionTaskHandle = NULL;
    u32 status;

    /* Pico init */
    stdio_init_all();
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);

    /* Tasks creation */
    status = xTaskCreate(
        EncryptionTask,
        "encrypt data",
        2048,
        NULL,
        1,
        &encryptionTaskHandle);

    /* Start */
    gpio_put(LED_PIN, ON); // Just to show to user the start
    vTaskStartScheduler();

    for (;;)
    {
        // should never get here
    }
}