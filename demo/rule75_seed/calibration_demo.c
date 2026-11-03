/**
 * @file calibration_demo.c
 * SPDX-License-Identifier: MIT
 * @brief Call sites exercising the seeded Rule 7.5 violations.
 *
 * Demo seed only. Rule 7.5 applies at call sites too, not only at #define.
 */

#include "calibration_constants.h"

static int32_t demo_trim;
static uint32_t demo_mask_applied;

void demo_seed_call_sites(void)
{
    /* Call sites match the same violation classes as the #defines. */
    demo_trim = INT32_C(-25);
    demo_mask_applied = (uint32_t)UINT32_C(0xFFUL);
}

int32_t demo_get_trim(void)
{
    return demo_trim;
}

uint32_t demo_get_mask(void)
{
    return demo_mask_applied;
}
