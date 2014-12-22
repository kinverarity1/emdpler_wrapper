import logging
import os
import shutil
import subprocess
import tempfile
import textwrap

import fortranformat as ff
import numpy

logger = logging.getLogger(__name__)


INPUT_TEMPLATE = """
DIPOLE CHARACTERISTIC PARAMETERS:
IFACT(Without-1/With-2 Displacement Current Factor) Format(I5)
{calc_disp_currs} 
IDIPOL(VMD-1,HMD-2,HED-3)--ICOMP(Hr/Hx-1,Ephai/Hy-2,Hz-3,Ex-4,Ey-5) Format(2I5)
{IDIPOL}{ICOMP} 
R(S-R Offset)--HT(Source Height)--Z(Receiver Level)(Format(3F9.2)
{src_rec_offset}{src_height}{rec_level}
FREQ1(Highest Freq.)------FREQL(Lowest Freq) ---Format(2F12.2)
{freq_h}{freq_l}
RI(Current-Ampere)-Area(Dipole Area)-RM(Dipole Moment)-Format(3F9.2)
{rec_curr}{rec_area}{rec_dip_moment} 
X (X- HMD & HED)--Y (Y- HMD & HED)--(Receiver position w.r.t. Dipole)--Format(2F9.3)
{hx}{hy} 
MODEL PARAMETERS:
NLYR-------Resistivity--and---Thickness----Format(10F8.3)
{nlyr}
{res}{thk}    
"""[1:-1]


class results(dict):
    def __init__(self, *args, **kwargs):
        self.__dict__ = self


def vmd(src_rec_offset, src_height, rec_level,
        res, thk=None,
        nlayers=None, 
        freq_h=1e5, freq_l=10,
        rec_curr=1, rec_area=1, rec_dip_moment=1,
        hx=0, hy=0, 
        field_components=("Hz", ), calc_displ_currs=False,
        emdpler_exe=None, print_input_files=False, print_output=False):
    """Run forward model for vertical magnetic dipole configuration (VMD).

    Arguments:
        src_rec_offset (float):
        src_height (float):
        rec_level (float):
        res (array of floats): list of N resistivities for N model layers
        thk (array of floats): list of N-1 thicknesses for N-1 model layers
            (the last resistivity is for the underlying halfspace?)
        field_components (list of strings): field components to calculate,
            can be a list containing any number of the values
            "Hz" (more to follow in the future).
        calc_disp_currs (bool): include displacement currents
        emdpler_exe (string): path to emdpler executable

    """
    if emdpler_exe is None:
        suffix = ""
        if os.name == "nt":
            suffix = ".exe"
        emdpler_exe = os.path.join(os.path.dirname(__file__), "emdpler" + suffix)
        assert os.path.isfile(emdpler_exe)

    IFACT = {True: 2, False: 1}[calc_displ_currs]
    if nlayers is None:
        nlayers = len(res)
    if thk is None:
        thk = []
    # TODO: loop and allow multiple runs of Emdpler to calculate more field components.
    ICOMP = {"Hz": 3}[field_components[0]]

    temp_dir = tempfile.mkdtemp(prefix="tmp_emdpler")
    logger.info("Running modelling in %s" % temp_dir)
    logger.debug("Creating input file...")
    input_template = str(INPUT_TEMPLATE)
    res_sl = ["%f" % r for r in res]
    res_s = textwrap.wrap(" ".join(res_sl))

    input_template = input_template.format(
        calc_disp_currs = "%.0f" % IFACT,
        IDIPOL = "1", 
        ICOMP = ff.FortranRecordWriter('(2I5)').write([ICOMP]),
        src_rec_offset = ff.FortranRecordWriter('(3F9.2)').write([src_rec_offset]),
        src_height = ff.FortranRecordWriter('(3F9.2)').write([src_height]),
        rec_level = ff.FortranRecordWriter('(3F9.2)').write([rec_level]),
        freq_h = ff.FortranRecordWriter('(2F12.2)').write([freq_h]),
        freq_l = ff.FortranRecordWriter('(2F12.2)').write([freq_l]),
        rec_curr = ff.FortranRecordWriter('(3F9.2)').write([rec_curr]),
        rec_area = ff.FortranRecordWriter('(3F9.2)').write([rec_area]),
        rec_dip_moment = ff.FortranRecordWriter('(3F9.2)').write([rec_dip_moment]), 
        hx = ff.FortranRecordWriter('(2F9.3)').write([hx]),
        hy = ff.FortranRecordWriter('(2F9.3)').write([hy]),
        nlyr = ff.FortranRecordWriter('(2I5)').write([nlayers]),
        res = "\n".join(textwrap.wrap(" ".join([ff.FortranRecordWriter('(10F8.3)').write([r]) for r in res]))), 
        thk = "\n".join(textwrap.wrap(" ".join([ff.FortranRecordWriter('(10F8.3)').write([t]) for t in thk]))), 
        )
    input_fn = os.path.join(temp_dir, "Input.in")
    with open(input_fn, mode="w") as inf:
        inf.write(input_template)
        logger.debug("Wrote input file at " + input_fn)
        if print_input_files:
            print input_template
    try:
        pr_output = subprocess.check_output([emdpler_exe], cwd=temp_dir)
        if print_output:
            print pr_output
    except:
        raise
    finally:
        r1 = numpy.loadtxt(os.path.join(temp_dir, "RESULT1.DAT"))
        r2 = numpy.loadtxt(os.path.join(temp_dir, "RESULT2.DAT"))
        r3 = numpy.loadtxt(os.path.join(temp_dir, "RESULT3.DAT"))
        shutil.rmtree(temp_dir)
        logger.info("Finished modelling in %s" % temp_dir)
    rfreq = results()
    rindn = results()
    assert (r1[:,0] == r3[:, 0]).all()
    rfreq.freq = r1[:,0]
    rfreq.ampl = r1[:,1]
    rfreq.phase = fix_phases(r1[:,2])
    rfreq.norm_ampl = r3[:,1]
    rfreq.norm_phase = fix_phases(r3[:,2])
    rindn.ind_num = r2[:,0]
    rindn.ampl = r2[:,1]
    rindn.phase = fix_phases(r2[:,2])
    return rfreq, rindn


def plot_results(rfreq, rindn, fig=None, fign=None, figsize=(15, 6), 
                 amplim=(None, None), phaselim=(None, None), gskws={}, pltkws={}):
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec

    if fig is None:
        fig = plt.figure(fign, figsize=figsize)

    pltkws["color"] = pltkws.get("color", "k")
    gskws["wspace"] = gskws.get("wspace", 0.3)
    gskws["hspace"] = gskws.get("hspace", 0.3)
    gs = gridspec.GridSpec(2, 3, **gskws)

    ax = fig.add_subplot(gs[0])
    ax.plot(rfreq.freq, rfreq.ampl, **pltkws)
    ax.set_xscale("log")
    ax.set_xlim(*ax.get_xlim()[::-1])
    ax.set_ylim(*amplim)
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("Amplitude")
    ax.yaxis.get_major_formatter().set_powerlimits((-2, 3))

    ax = fig.add_subplot(gs[3])
    ax.plot(rfreq.freq, rfreq.phase, **pltkws)
    ax.set_xscale("log")
    ax.set_xlim(*ax.get_xlim()[::-1])
    ax.set_ylim(*phaselim)
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("Phase")
    ax.yaxis.get_major_formatter().set_powerlimits((-2, 3))

    ax = fig.add_subplot(gs[1])
    ax.plot(rfreq.freq, rfreq.norm_ampl, **pltkws)
    ax.set_xscale("log")
    ax.set_xlim(*ax.get_xlim()[::-1])
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("Normalized amplitude")
    ax.yaxis.get_major_formatter().set_powerlimits((-2, 3))

    ax = fig.add_subplot(gs[4])
    ax.plot(rfreq.freq, rfreq.norm_phase, **pltkws)
    ax.set_xscale("log")
    ax.set_xlim(*ax.get_xlim()[::-1])
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("Normalized phase [deg]")
    ax.yaxis.get_major_formatter().set_powerlimits((-2, 3))

    ax = fig.add_subplot(gs[2])
    ax.plot(rindn.ind_num, rindn.ampl, **pltkws)
    ax.set_xscale("log")
    ax.set_xlim(*ax.get_xlim()[::-1])
    ax.set_ylim(*amplim)
    ax.set_xlabel("Induction number")
    ax.set_ylabel("Amplitude")
    ax.yaxis.get_major_formatter().set_powerlimits((-2, 3))

    ax = fig.add_subplot(gs[5])
    ax.plot(rindn.ind_num, rindn.phase, **pltkws)
    ax.set_xscale("log")
    ax.set_xlim(*ax.get_xlim()[::-1])
    ax.set_ylim(*phaselim)
    ax.set_xlabel("Induction number")
    ax.set_ylabel("Phase [deg]")
    ax.yaxis.get_major_formatter().set_powerlimits((-2, 3))


def fix_phases(arr):
    for i in range(len(arr)):
        while arr[i] > 180:
            arr[i] = arr[i] - 180
        while arr[i] < -180:
            arr[i] = arr[i] + 180
    return arr