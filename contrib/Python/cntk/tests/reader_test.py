# Copyright (c) Microsoft. All rights reserved.

# Licensed under the MIT license. See LICENSE.md file in the project root
# for full license information.
# ==============================================================================

import os
import pytest

from ..reader import *
from ..graph import *
from ..context import *
from ..ops.variables_and_parameters import *
from ..ops import cntk1 as cntk1_ops

from cntk.tests.test_utils import *

# Keeping things short
C = constant
I = input_reader


def test_two_inputs(device_id, precision):
    a = AA([[1, 2]])
    b = AA([[10, 20]])

    expected = a + b

    op_node = I([a], has_dynamic_axis=True) + \
        I([b], has_dynamic_axis=True)

    unittest_helper(op_node, None, [expected], device_id=device_id,
                    precision=precision, clean_up=True, backward_pass=False)


def test_serialize_unmapped_node(tmpdir):
    tmpfile = str(tmpdir / 'out.txt')
    from cntk.reader import LazyInputReader
    i1 = input_reader(
        # 2 samples with 2 sequences each
        [
            AA([[[1, 2]], [[3, 4]]]),
            AA([[[10, 20]]])
        ], alias='X', has_dynamic_axis=True)

    i2 = input_reader(
        # 2 samples with 1 sequence each
        [
            AA([[[44, 55]]]),
            AA([[[66, 77]]])
        ], has_dynamic_axis=True)

    expected = '''\
0	|X 1 2 |_I_0 44 55
0	|X 3 4
1	|X 10 20 |_I_0 66 77
'''

    im = InputMap()
    im._add_unmapped(i1)
    im._add_unmapped(i2)
    im._serialize_unmapped_nodes(tmpfile)

    with open(tmpfile, 'r') as f:
        assert f.read() == expected

