.. py:currentmodule:: lsst.ts.guitool

.. _lsst.ts.guitool-version_history:

##################
Version History
##################

.. towncrier release notes start

v0.3.1 (2025-10-07)
===================

New Features
------------

- Use the ts-conda-build 0.5 in conda recipe. (`OSW-1202 <https://rubinobs.atlassian.net//browse/OSW-1202>`_)


0.3.0 (2025-08-06)
===================

New Features
------------

- Support the towncrier. (`OSW-274 <https://rubinobs.atlassian.net//browse/OSW-274>`_)
- Improve the run_command() to use the repr() for the error message. (`OSW-806 <https://rubinobs.atlassian.net//browse/OSW-806>`_)


0.2.7
=====

* Add the **QT_QPA_PLATFORM** to ``meta.yaml`` to fix the test section of conda recipe.


0.2.6
=====

* Improve the ``setup.py`` to support the version of Python 3.11 and 3.12.


0.2.5
=====

* Improve the ``figure_constant.py`` for the adjustment of y-axis automatically.


0.2.4
=====

* Remove the **ts_idl**.


0.2.3
=====

* Fix the **Jenkinsfile.conda**.


0.2.2
=====

* Add the ``read_yaml_file()``, ``get_config_dir()``, and ``update_boolean_indicator_status()``.


0.2.1
=====

* Add the ``create_radio_indicators()``, ``update_button_color()``, and ``create_double_spin_box()``.


0.2.0
=====

* Migrate the ``ControlTabs`` and ``TabDefault`` classes from **ts_m2gui**.


0.1.0
=====

* Migrate the reusable functions from **ts_m2gui**.
