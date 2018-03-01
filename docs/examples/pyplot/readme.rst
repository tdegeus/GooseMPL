
.. _examples-pyplot:

********
Examples
********

Plot
====

[:download:`source: plot.py <plot.py>`]

.. literalinclude:: plot.py
   :language: python

.. image:: plot.svg
  :width: 600px
  :align: center

Subplot
=======

[:download:`source: subplot.py <subplot.py>`]

.. literalinclude:: subplot.py
   :language: python

.. image:: subplot.svg
  :width: 1000px
  :align: center

Plot: use colormap
==================

[:download:`source: plot-cmap.py <plot-cmap.py>`]

.. note:: References

  `StackOverflow - "Matplotlib: Add colorbar to non-mappable object" <http://stackoverflow.com/questions/43805821/matplotlib-add-colorbar-to-non-mappable-object/43807666#43807666>`_

.. note::

  This example features a colorbar where the 'ticks' are placed in the middle of the color blocks. Should you be interested in something simpler, you could also use:

  .. code-block:: python

    sm   = plt.cm.ScalarMappable(cmap=cmap, norm=mpl.colors.Normalize(vmin=0,vmax=2))
    sm.set_array([])

    cbar = fig.colorbar(sm)
    cbar.set_ticks(...)
    cbar.set_ticklabels(...)

.. literalinclude:: plot-cmap.py
   :language: python

.. image:: plot-cmap.svg
  :width: 600px
  :align: center

Image
=====

[:download:`source: image.py <image.py>`]

.. literalinclude:: image.py
   :language: python

.. image:: image.svg
  :width: 600px
  :align: center

Colorbar
========

[:download:`source: image_subplots.py <image_subplots.py>`]

.. literalinclude:: image_subplots.py
   :language: python

.. image:: image_subplots.svg
  :width: 1000px
  :align: center

.. note:: References

  * `StackOverflow - "positioning the colorbar" <https://stackoverflow.com/a/43425119/2646505>`_

Colorbar positioning
====================

[:download:`source: image_subplots_bottom.py <image_subplots_bottom.py>`]

.. literalinclude:: image_subplots_bottom.py
   :language: python

.. image:: image_subplots_bottom.svg
  :width: 1000px
  :align: center

Stand-alone colorbar
====================

[:download:`source: colorbar.py <colorbar.py>`]

.. note:: References

  * `matplotlib documentation - "colorbar_only" <http://matplotlib.org/examples/api/colorbar_only.html>`_

.. literalinclude:: colorbar.py
   :language: python

.. image:: colorbar.svg
  :width: 600px
  :align: center
