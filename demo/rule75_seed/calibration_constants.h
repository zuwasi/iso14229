/**
 * @file calibration_constants.h
 * SPDX-License-Identifier: MIT
 * @brief Seeded MISRA C:2025 Rule 7.5 violations for the Sourcegraph + Parasoft demo.
 *
 * Demo seed only: these constants are not part of the iso14229 library.
 * Rule 7.5: the argument of an integer constant macro shall have an appropriate form.
 */

#ifndef DEMO_CALIBRATION_CONSTANTS_H
#define DEMO_CALIBRATION_CONSTANTS_H

#include <stdint.h>

/* --- Mechanical class 1: unary minus inside the macro argument (auto-fixable) --- */
#define DEMO_TEMP_OFFSET   (-INT32_C(40))   /* cold plateau */
#define DEMO_MIN_PRESSURE  (-INT32_C(100))
#define DEMO_TRIM_LIMIT    (-INT64_C(500))
#define DEMO_HYST_LOW      (-INT32_C(5))    /* degrees C */

/* --- Mechanical class 2: suffix inside the macro argument (auto-fixable) --- */
#define DEMO_MASK          UINT32_C(0xFF)
#define DEMO_SAMPLE_RATE   UINT32_C(100)
#define DEMO_TIMEOUT_MS    UINT64_C(5000)

/* --- Excluded from automation, fixed by expert decision (compliant forms) --- */
#define DEMO_INT32_MIN_SENTINEL ((-INT32_C(2147483647))-1)

/* --- Manual-review class: non-literal argument, fixed by expert decision --- */
#define DEMO_DERIVED_GAIN  DEMO_TEMP_OFFSET

/* --- Compliant reference forms (the fix targets these shapes) --- */
#define DEMO_TEMP_OFFSET_OK   (-INT32_C(40))
#define DEMO_MASK_OK          UINT32_C(0xFF)

/* Declarations for the demo translation unit (Rule 8.4). */
void demo_seed_call_sites(void);
int32_t demo_get_trim(void);
uint32_t demo_get_mask(void);

#endif /* DEMO_CALIBRATION_CONSTANTS_H */
