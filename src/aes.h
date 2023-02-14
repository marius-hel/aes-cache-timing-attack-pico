#ifndef _AES_ATTACK_H
#define _AES_ATTACK_H

#include "rijndael-alg-fst.h"

/* AES-128-bit constants */
#define AES_KEY_SIZE 16
#define AES_NUM_ROUNDS ((AES_KEY_SIZE / 4) + 6)
#define AES_BLOCK_SIZE 16

/**
 * Encrypt <in> block with <int_key> and stores result in <out>.
 */
#define aes_encrypt(in, out, int_key) \
    rijndaelEncrypt((u32 *)(int_key), AES_NUM_ROUNDS, (u8 *)(in), (u8 *)(out))

/**
 * Set encryption <key> and stores it into <key_int>.
 */
#define aes_set_enc_key(key, int_key) \
    rijndaelKeySetupEnc((u32 *)(int_key), (const u8 *)(key), AES_KEY_SIZE * 8)

#endif