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

/* --- Excluded: signed minimum must never be auto-fixed (expert case) --- */
#define DEMO_INT32_MIN_SENTINEL INT32_C(-2147483648)

/* --- Manual-review class: non-literal argument (never auto-fixed) --- */
#define DEMO_DERIVED_GAIN  INT32_C(DEMO_TEMP_OFFSET)

/* --- Compliant reference forms (the fix targets these shapes) --- */
#define DEMO_TEMP_OFFSET_OK   (-INT32_C(40))
#define DEMO_MASK_OK          UINT32_C(0xFF)

#endif /* DEMO_CALIBRATION_CONSTANTS_H */
