#   ---------------------------------------------------------------------------------
#   Copyright (c) Learnstdio. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""Usage illustration of the learnstdio."""

from learnstdio import load_pipeline
from sensors import get_phase_iv

ia, va = get_phase_iv("a")
ib, vb = get_phase_iv("b")
ic, vc = get_phase_iv("c")

pipeline = load_pipeline('./samples/learnstdio.pipeline.json')
ground_fault = pipeline.predict(ia, ib, ic, va, vb, vc)

print(f'Ground fault detected: {ground_fault}')
