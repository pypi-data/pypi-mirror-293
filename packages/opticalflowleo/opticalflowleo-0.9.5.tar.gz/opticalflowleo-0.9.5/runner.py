from opticalflowleo.polar_RAFT_runner import run_multi, run_single
from opticalflowleo.polar_RAFT_runner import cris_product_str, atms_mirs_product_str, metop_avhrr_product_str

# mode can be 'multi' or 'single'
# for 'multi', supply a directory path
# for 'single', supply a file path
mode = 'single'

# path_to_first = '/Users/tomrink/data/cris/twin_hurricanes/nh_descnd/N20*/'
# path_to_second = '/Users/tomrink/data/cris/twin_hurricanes/nh_descnd/N21*/'

path_to_first = './data/CrIS_j01_d20230913_t0239439_dr_atm_prof_rtv.h5'
path_to_second = './data/CrIS_j02_d20230913_t0303449_dr_atm_prof_rtv.h5'

# product can be: cris_product_str, atms_mirs_product_str, metop_avhrr_product_str
product_str = cris_product_str


if mode == 'multi':

    """
    Computes winds from a set of overlapping pairs of granules through multiple pressure levels.
    (See global parameters at top of this module)
    :param path_to_first: directory containing files of first orbit platform to cross equator.
    :param path_to_second: directory containing files for the second platform
    :param product_str: name of product to work on.
    :param do_plots: output to animated gif.
    :param do_write: output to CF-compliant NetCDF4 file.
    :param press_low: low pressure (hPa), default = 100mb
    :param press_high: high pressure (hPa), default = 800mb
    :param press_skip: number of pressure levels to skip, default = 4
     Note: the vertical coordinate is ignored if product is type imager, or field data is 2D. In the case of field data
     varying with pressure or radiometric channel, the backing data array must be 3D only.
    :param wind_plot_skip: skip factor for wind vectors in plot. Default value is 6
    """

    run_multi(path_to_first,
              path_to_second,
              product_str)

elif mode == 'single':

    """
    Computes winds for a single overlapping pair of granules through multiple pressure levels.
    (See global parameters at top of this module).
    :param filepath_t0: path for the first granule
    :param filepath_t1: path for the second (later in time) granule
    :param product_str: product identifier
    :param do_plots: output to animated gif.
    :param do_write: output to CF-compliant NetCDF4.
    :param press_low: low pressure (hPa). Default value is 100mb
    :param press_high: high pressure (hPa). Default value is 800mb
    :param press_skip: number of pressure levels to skip. Default value is 4
    :param wind_plot_skip: skip factor for wind vector plots. Default value is 6
    """

    run_single(path_to_first,
               path_to_second,
               product_str,
               do_plots=True,
               do_write=True,
               press_low=300.0,
               press_high=300.0,
               press_skip=1)

