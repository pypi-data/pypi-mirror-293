#!/usr/bin/env python3

import os

from siliconcompiler import Chip
from siliconcompiler.targets import asap7_demo
from siliconcompiler.tools._common.asic import get_mainlib
from scgallery import Gallery


def setup(target=asap7_demo):
    chip = Chip('swerv')

    if __name__ == '__main__':
        Gallery.design_commandline(chip)
    else:
        chip.use(target)

    sdc_root = os.path.join('swerv', 'constraints')
    lint_root = os.path.join('swerv', 'lint')

    chip.register_source('swerv-eh1',
                         path='git+https://github.com/chipsalliance/Cores-VeeR-EH1.git',
                         ref='695883a674c4a59cf96fae874ff4bfac5fecf4e8')

    chip.input('swerv/config/common_defines.vh',
               fileset='rtl',
               filetype='systemverilog', package='scgallery-designs')

    for src in ('design/include/swerv_types.sv',
                'design/lib/beh_lib.sv',
                'design/mem.sv',
                'design/pic_ctrl.sv',
                'design/dma_ctrl.sv',
                'design/ifu/ifu_aln_ctl.sv',
                'design/ifu/ifu_compress_ctl.sv',
                'design/ifu/ifu_ifc_ctl.sv',
                'design/ifu/ifu_bp_ctl.sv',
                'design/ifu/ifu_ic_mem.sv',
                'design/ifu/ifu_mem_ctl.sv',
                'design/ifu/ifu_iccm_mem.sv',
                'design/ifu/ifu.sv',
                'design/dec/dec_decode_ctl.sv',
                'design/dec/dec_gpr_ctl.sv',
                'design/dec/dec_ib_ctl.sv',
                'design/dec/dec_tlu_ctl.sv',
                'design/dec/dec_trigger.sv',
                'design/dec/dec.sv',
                'design/exu/exu_alu_ctl.sv',
                'design/exu/exu_mul_ctl.sv',
                'design/exu/exu_div_ctl.sv',
                'design/exu/exu.sv',
                'design/lsu/lsu.sv',
                'design/lsu/lsu_bus_buffer.sv',
                'design/lsu/lsu_clkdomain.sv',
                'design/lsu/lsu_addrcheck.sv',
                'design/lsu/lsu_lsc_ctl.sv',
                'design/lsu/lsu_stbuf.sv',
                'design/lsu/lsu_bus_intf.sv',
                'design/lsu/lsu_ecc.sv',
                'design/lsu/lsu_dccm_mem.sv',
                'design/lsu/lsu_dccm_ctl.sv',
                'design/lsu/lsu_trigger.sv',
                'design/dbg/dbg.sv',
                'design/dmi/dmi_wrapper.v',
                'design/dmi/dmi_jtag_to_core_sync.v',
                'design/dmi/rvjtag_tap.sv',
                'design/lib/mem_lib.sv',
                'design/lib/ahb_to_axi4.sv',
                'design/lib/axi4_to_ahb.sv',
                'design/swerv.sv',
                'design/swerv_wrapper.sv'):
        chip.input(src, package='swerv-eh1')

    chip.add('option', 'idir', 'swerv/config', package='scgallery-designs')
    chip.add('option', 'idir', 'design', package='swerv-eh1')
    chip.add('option', 'idir', 'design/include', package='swerv-eh1')

    chip.add('option', 'define', 'PHYSICAL')

    mainlib = get_mainlib(chip)
    chip.input(os.path.join(sdc_root, f'{mainlib}.sdc'), package='scgallery-designs')

    # Lint setup
    chip.set('tool', 'verilator', 'task', 'lint', 'file', 'config',
             os.path.join(lint_root, 'verilator'), package='scgallery-designs')

    return chip


if __name__ == '__main__':
    chip = setup()

    chip.run()
    chip.summary()
