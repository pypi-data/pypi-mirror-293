#!/usr/bin/env python3

'''
Advanced Encryption Standard

Source: http://www.opencores.org/cores/aes_core/
'''

import os

from siliconcompiler import Chip
from siliconcompiler.targets import asap7_demo
from siliconcompiler.tools._common.asic import get_mainlib
from scgallery import Gallery


def setup(target=asap7_demo):
    chip = Chip('aes')
    chip.set('option', 'entrypoint', 'aes_cipher_top')

    if __name__ == '__main__':
        Gallery.design_commandline(chip)
    else:
        chip.use(target)

    src_root = os.path.join('aes', 'src')
    sdc_root = os.path.join('aes', 'constraints')

    for src in ('aes_cipher_top.v',
                'aes_inv_cipher_top.v',
                'aes_inv_sbox.v',
                'aes_key_expand_128.v',
                'aes_rcon.v',
                'aes_sbox.v'):
        chip.input(os.path.join(src_root, src), package='scgallery-designs')

    chip.add('option', 'idir', src_root, package='scgallery-designs')

    mainlib = get_mainlib(chip)
    chip.input(os.path.join(sdc_root, f'{mainlib}.sdc'), package='scgallery-designs')

    if mainlib.startswith('sky130'):
        # Decrease density due to high routing runtime
        chip.set('constraint', 'density', 30)
        chip.set('tool', 'openroad', 'task', 'place', 'var', 'place_density', '0.50')
    else:
        chip.set('tool', 'openroad', 'task', 'place', 'var', 'place_density', '0.65')

    return chip


if __name__ == '__main__':
    chip = setup()

    chip.run()
    chip.summary()
