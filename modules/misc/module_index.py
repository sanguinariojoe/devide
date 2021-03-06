# $Id$

class advectionProperties:
    kits = ['vtk_kit']
    cats = ['Sources']
    help = """Given a series of prepared advection volumes (each input is a
    timestep), calculate a number of metrics.

    The first input HAS to have a VolumeIndex PointData attribute/array.  For
    example, the output of the pointsToSpheres that you used BEFORE having
    passed through the first probeFilters.  This first input will NOT be used
    for the actual calculations, but only for point -> volume lookups.
    Calculations will be performed for the second input and onwards.

    This module writes a CSV file with the volume centroids over time, and
    secretly writes a python file with all data as a python nested list.
    This can easily be loaded in a Python script for further analysis.
    """
    
class cptDistanceField:
    kits = ['vtk_kit']
    cats = ['Sources']
    help = """Driver module for Mauch's CPT code.

    This takes an image data and a mesh input.  The imagedata is only used
    to determine the bounds of the output distance field.  The mesh
    is converted to the CPT brep format using the DeVIDE cptBrepWRT module.
    A geom file is created.  The CPT driver is executed with the geom and
    brep files.  The output distance field is read, y-axis is flipped, and
    the whole shebang is made available at the output.

    Contributions to module code by Stef Busking.

    Suggestion: On Windows, your driver.bat could make use of plink /
    pscp to copy data to a linux server and run Mauch's code there,
    and then copy everything back.  On Linux you can run Mauch's code
    directly.
    """

    
class implicitToVolume:
    kits = ['vtk_kit']
    cats = ['Sources']
    help = """Given an implicit function, this module will evaluate it over
    a volume and yield that volume as output.
    """

class manualTransform:
    kits = ['vtk_kit']
    cats = ['Sources']
    help = """Manually create linear transform by entering scale factors,
    rotation angles and translations.

    Scaling is performed, then rotation, then translation.  It is often easier
    to chain manualTransform modules than performing all transformations at
    once.

    """

class MarschnerLobb:
    kits = ['vtk_kit']
    cats = ['Sources']
    help = """Pure Python filter to generate Marschner-Lobb test
    volume.

    When resolution is left at the default value of 40, the generated
    volume should be at the Nyquist frequency of the signal (analytic
    function) that it has sampled.

    Pure Python implementation: for the default resolution, takes a
    second or two, 200 cubed takes about 20 seconds on Core2 hardware.
    """

class PassThrough:
    kits = []
    cats = ['Filters', 'System']
    help = """Simple pass-through filter.

    This is quite useful if you have a source that connects to a
    number of consumers, and you want to be able to change sources
    easily.  Connect the source to the PassThrough, and the
    PassThrough output to all the consumers.  Now when you replace the
    source, you only have to reconnect one module.
    """

class pointsToSpheres:
    kits = ['vtk_kit']
    cats = ['Sources']
    help = """Given a set of selected points (for instance from a slice3dVWR),
    generate polydata spheres centred at these points with user-specified
    radius.  The spheres' interiors are filled with smaller spheres.  This is
    useful when using selected points to generate points for seeding
    streamlines or calculating advection by a vector field.

    Each point's sphere has an array associated to its pointdata called
    'VolumeIndex'.  All values in this array are equal to the corresponding
    point's index in the input points list.
    """


class superQuadric:
    kits = ['vtk_kit']
    cats = ['Sources']
    help = """Generates a SuperQuadric implicit function and polydata as
    outputs.
    """


