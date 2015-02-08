# -*- encoding: utf-8 -*-

"""Use a JPL ephemeris to predict planet positions.

This package can load and use a Jet Propulsion Laboratory (JPL)
ephemeris for predicting the position and velocity of a planet or other
Solar System body.  Its only needs `NumPy <http://www.numpy.org/>`_,
which ``pip`` will automatically attempt to install alongside
``pyephem`` when you run::

    $ pip install jplephem

If you see NumPy compilation errors, then try downloading and installing
it directly from `its web site <http://www.numpy.org/>`_ or simply try
using a distribution of Python with science tools already installed,
like `Anaconda <http://continuum.io/downloads>_`.

Note that ``jplephem`` offers only the logic necessary to produce plain
three-dimensional vectors.  Most programmers interested in astronomy
will want to look at `Skyfield <http://rhodesmill.org/skyfield/>`_
instead, which uses ``jplephem`` but converts the numbers into more
traditional measurements like right ascension and declination.

Most users will use ``jplephem`` with the Satellite Planet Kernel (SPK)
files that the NAIF facility at NASA JPL offers for use with their own
SPICE toolkit.  They have collected their most useful kernels beneath
the directory:

http://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/

The recent DE430 ephemeris is a useful starting point.  It weighs in at
115 MB, but provides predictions across the generous range of years
1550–2650:

http://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de430.bsp

After the kernel has downloaded, you can use ``jplephem`` to load this
SPK file and learn about the segments it offers:

>>> from jplephem.spk import SPK
>>> k = SPK.open('de430.bsp')
>>> print(k)
File type DAF/SPK and format LTL-IEEE with 14 segments:
2287184.50..2688976.50  Solar System Barycenter (0) -> Mercury Barycenter (1)
2287184.50..2688976.50  Solar System Barycenter (0) -> Venus Barycenter (2)
2287184.50..2688976.50  Solar System Barycenter (0) -> Earth Barycenter (3)
2287184.50..2688976.50  Solar System Barycenter (0) -> Mars Barycenter (4)
2287184.50..2688976.50  Solar System Barycenter (0) -> Jupiter Barycenter (5)
2287184.50..2688976.50  Solar System Barycenter (0) -> Saturn Barycenter (6)
2287184.50..2688976.50  Solar System Barycenter (0) -> Uranus Barycenter (7)
2287184.50..2688976.50  Solar System Barycenter (0) -> Neptune Barycenter (8)
2287184.50..2688976.50  Solar System Barycenter (0) -> Pluto Barycenter (9)
2287184.50..2688976.50  Solar System Barycenter (0) -> Sun (10)
2287184.50..2688976.50  Earth Barycenter (3) -> Moon (301)
2287184.50..2688976.50  Earth Barycenter (3) -> Earth (399)
2287184.50..2688976.50  Mercury Barycenter (1) -> Mercury (199)
2287184.50..2688976.50  Venus Barycenter (2) -> Venus (299)

Each segment of the file lets you predict the position of an object with
respect to some other reference point.  If you want the coordinates of
Mars at 2457061.5 (2015 February 8) with respect to the center of the
solar system, this ephemeris only requires you to take a single step:

>>> mars = k[0,4]
>>> position = mars.compute(2457061.5)
>>> print(position)
[  2.05700211e+08   4.25141646e+07   1.39379183e+07]

But learning the position of Mars with respect to the Earth takes three
steps, from Mars to the Solar System barycenter to the Earth-Moon
barycenter and finally to Earth itself:

>>> earthmoon = k[0,3]
>>> earth = k[3,399]
>>> position = mars.compute(2457061.5)
>>> position -= earthmoon.compute(2457061.5) + earth.compute(2457061.5)
>>> print(position)
[  3.16065185e+08  -4.67929557e+07  -2.47554111e+07]

You can see that the output of this ephemeris is in kilometers.  If you
use another ephemeris, check its documentation to be sure of the units
that it employs.



Legacy Ephemeris Packages
-------------------------



    pip install de421

Loading DE421 and computing a position require one line of Python each,
given a barycentric dynamical time expressed as a Julian date::

    import de421
    from jplephem import Ephemeris

    eph = Ephemeris(de421)
    x, y, z = eph.position('mars', 2444391.5)  # 1980.06.01

The result of calling ``position()`` is a 3-element NumPy array giving
the planet's position in the solar system in kilometers along the three
axes of the ICRF (a more precise reference frame than J2000 but oriented
in the same direction).  If you also want to know the planet's velocity,
call ``position_and_velocity()`` instead::

    position, velocity = eph.position_and_velocity('mars', 2444391.5)
    x, y, z = position            # a NumPy array
    xdot, ydot, zdot = velocity   # another array

Velocities are returned as kilometers per day.

Both of these methods will also accept a NumPy array, which is the most
efficient way of computing a series of positions or velocities.  For
example, the position of Mars at each midnight over an entire year can
be computed with::

    import numpy as np
    t0 = 2444391.5
    t = np.arange(t0, t0 + 366.0, 1.0)
    x, y, z = eph.position('mars', 2444391.5)

You will find that ``x``, ``y``, and ``z`` in this case are each a NumPy
array of the same length as your input ``t``.

The string that you provide to ``e.compute()``, like ``'mars'`` in the
example above, actually names the data file that you want loaded from
the ephemeris package.  To see the list of data files that an ephemeris
provides, consult its ``names`` attribute.  Most of the JPL ephemerides
provide thirteen data sets::

    earthmoon   mercury    pluto   venus
    jupiter     moon       saturn
    librations  neptune    sun
    mars        nutations  uranus

Each ephemeris covers a specific range of dates, beyond which it cannot
provide reliable predictions of each planet's position.  These limits
are available as attributes of the ephemeris::

    t0, t1 = eph.jalpha, eph.jomega

The ephemerides currently available as Python packages (the following
links explain the differences between them) are:

* `DE405 <http://pypi.python.org/pypi/de405>`_ (May 1997)
  — 54 MB covering years 1600 through 2200
* `DE406 <http://pypi.python.org/pypi/de406>`_ (May 1997)
  — 190 MB covering years -3000 through 3000
* `DE421 <http://pypi.python.org/pypi/de421>`_ (February 2008)
  — 27 MB covering years 1900 through 2050
* `DE422 <http://pypi.python.org/pypi/de422>`_ (September 2009)
  — 531 MB covering years -3000 through 3000
* `DE423 <http://pypi.python.org/pypi/de423>`_ (February 2010)
  — 36 MB covering years 1800 through 2200

Earth and Moon
--------------

The raw ephemerides provide one position for the Earth-Moon barycenter,
and another for the position of the Moon relative to the geocenter.  The
JPL expects you to combine these values yourself if you want the Solar
System location of the Earth or Moon, which gives you the chance to be
more efficient by asking the ephemeris for each position only once::

    barycenter = eph.position('earthmoon', j)
    moonvector = eph.position('moon', j)

    earth = barycenter - moonvector * eph.earth_share
    moon = barycenter + moonvector * eph.moon_share

High-Precision Dates
--------------------

Since all modern Julian dates are numbers larger than 2.4 million, a
standard 64-bit Python or NumPy float necessarily leaves only a limited
number of bits available for the fractional part.  Technical Note
2011-02 from the United States Naval Observatory's Astronomical
Applications Department suggests that the `precision possible with a
64-bit floating point Julian date is around 20.1 µs
<http://jplephem.s3.amazonaws.com/JD_precision_test.pdf>`_.

If you need to supply times and receive back planetary positions with
greater precision than 20.1 µs, then you have two options.

First, you can supply times using the special ``float96`` NumPy type,
which is also aliased to the name ``longfloat``.  If you provide either
a ``float96`` scalar or a ``float96`` array as your ``tdb`` parameter to
any ``jplephem`` routine, you should get back a high-precision result.

Second, you can split your date or dates into two pieces, and supply
them as a pair of arguments two ``tdb`` and ``tdb2``; one popular
approach for how to split your date is to use the ``tdb`` float for the
integer Julian date, and ``tdb2`` for the fraction that specifies the
time of day.  Nearly all ``jplephem`` routines accept this optional
``tdb2`` argument if you wish to provide it, thanks to the work of
Marten van Kerkwijk!

Waiting To Compute Velocity
---------------------------

When a high-level astronomy library computes the distance between an
observer and a solar system body, it typically measures the light travel
delay between the observer and the body, and then uses a loop to take
the position several steps backwards in time until it has determined
where the planet *was* back when the light left its surface (or cloud
deck) that is reaching the eye or sensor of the observer right *now*.

To make such a loop less computationally expensive — a loop that only
needs to compute the planet position repeatedly, and can wait to compute
the velocity until the loop's conclusion — ``jplephem`` provides a way
to split the ``position_and_velocity()`` call into two pieces.  This
lets you examine the position *before* deciding whether to also proceed
with the expense of computing the velocity.

The key is the special ``compute_bundle()`` method, which returns a
tuple containing the coefficients and intermediate results that are
needed by *both* the position and the velocity computations.  There is
nothing wasted in calling ``compute_bundle()`` whether you are going to
ask for the position, the velocity, or both as your next computing step!

So your loop can look something like this::

    while True:
        bundle = eph.compute_bundle('mars', tdb)
        position = eph.position_from_bundle(bundle)

        # ...determine whether you are happy...

        if you_are_happy:
            break

        # ...otherwise, adjust `tdb` and then let
        # control return back to the top of the loop

    # Now we can re-use the values in `bundle`, for free!

    velocity = eph.velocity_from_bundle(bundle)

This is especially important when the number of dates in ``tdb`` is
large, since vector operations over thousands or millions of dates are
going to take a noticeable amount of time, and every mass operation that
can be avoided will help move your program toward completion.

Reporting issues
----------------

You can report any issues, bugs, or problems at the GitHub repository:

https://github.com/brandon-rhodes/python-jplephem/

Changelog
---------

**2015 February 8 — Version 2.0**

* Added support for SPICE SPK files downloaded directly from NASA.

**2013 November 26 — Version 1.2**

* Helge Eichhorn fixed the default for the ``position_and_velocity()``
  argument ``tdb2`` so it defaults to zero days instead of 2.0 days.
  Tests were added to prevent any future regression.

**2013 July 10 — Version 1.1**

* Deprecates the old ``compute()`` method in favor of separate
  ``position()`` and ``position_and_velocity()`` methods.

* Supports computing position and velocity in two separate phases by
  saving a “bundle” of coefficients returned by ``compute_bundle()``.

* From Marten van Kerkwijk: a second ``tdb2`` time argument, for users
  who want to build higher precision dates out of two 64-bit floats.

**2013 January 18 — Version 1.0**

* Initial release

References
----------

The Jet Propulsion Laboratory's “Solar System Dynamics” page introduces
the various options for doing solar system position computations:
http://ssd.jpl.nasa.gov/?ephemerides

The plain ASCII format element sets from which the ``jplephem`` Python
ephemeris packages are built, along with documentation, can be found at:
ftp://ssd.jpl.nasa.gov/pub/eph/planets/ascii/

Equivalent FORTRAN code for using the ephemerides be found at the same
FTP site: ftp://ssd.jpl.nasa.gov/pub/eph/planets/fortran/

"""
from .ephem import Ephemeris, DateError

__all__ = ['Ephemeris', 'DateError']