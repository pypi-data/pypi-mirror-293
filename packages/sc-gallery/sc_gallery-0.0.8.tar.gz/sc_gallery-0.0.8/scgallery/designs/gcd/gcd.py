#!/usr/bin/env python3

import os

from siliconcompiler import Chip
from siliconcompiler.targets import asap7_demo
from siliconcompiler.tools._common.asic import get_mainlib
from scgallery import Gallery


def setup(target=asap7_demo):
    chip = Chip('gcd')

    if __name__ == '__main__':
        Gallery.design_commandline(chip)
    else:
        chip.use(target)

    src_root = os.path.join('gcd', 'src')
    sdc_root = os.path.join('gcd', 'constraints')

    for src in ('gcd.v',):
        chip.input(os.path.join(src_root, src), package='scgallery-designs')

    mainlib = get_mainlib(chip)
    chip.input(os.path.join(sdc_root, f'{mainlib}.sdc'), package='scgallery-designs')

    chip.set('tool', 'yosys', 'task', 'syn_asic', 'var', 'strategy', 'AREA3')
    chip.set('tool', 'yosys', 'task', 'syn_asic', 'var', 'map_adders', 'false')

    return chip


if __name__ == '__main__':
    chip = setup()

    chip.run()
    chip.summary()
