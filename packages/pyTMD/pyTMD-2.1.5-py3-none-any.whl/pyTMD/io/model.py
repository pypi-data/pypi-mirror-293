#!/usr/bin/env python
u"""
model.py
Written by Tyler Sutterley (08/2024)
Retrieves tide model parameters for named tide models and
    from model definition files

UPDATE HISTORY:
    Updated 08/2024: added attribute for minor constituents to infer
        allow searching over iterable glob strings in definition files
        added option to try automatic detection of definition file format
    Updated 07/2024: added new FES2022 and FES2022_load to list of models
        added JSON format for model definition files
        use parse function from constituents class to extract names
        renamed format for ATLAS to ATLAS-compact
        renamed format for netcdf to ATLAS-netcdf
        renamed format for FES to FES-netcdf and added FES-ascii
        renamed format for GOT to GOT-ascii and added GOT-netcdf
    Updated 05/2024: make subscriptable and allow item assignment
    Updated 04/2024: append v-components of velocity only to netcdf format
    Updated 11/2023: revert TPXO9-atlas currents changes to separate dicts
    Updated 09/2023: fix scale values for TPXO9-atlas currents
    Updated 08/2023: changed ESR netCDF4 format to TMD3 format
        updated filenames for CATS2008-v2023 to final version
    Updated 06/2023: remap FES2012 e2 constituent to eps2
    Updated 04/2023: added global HAMTIDE11 model
        made ICESat, ICESat-2 and output file attributes properties
        updated model definition read function for currents
        using pathlib to define and expand tide model paths
        add basic file searching with glob strings in definition files
        add long_name and description attributes for current variables
        added exceptions for files missing when using glob patterns
        simplify TPXO9-atlas currents dictionaries to single list
    Updated 03/2023: add basic variable typing to function inputs
    Updated 12/2022: moved to io and added deprecation warning to old
    Updated 11/2022: use f-strings for formatting verbose or ascii output
    Updated 06/2022: added Greenland 1km model (Gr1kmTM) to list of models
        updated citation url for Global Ocean Tide (GOT) models
    Updated 05/2022: added ESR CATS2022 to list of models
        added attribute for flexure fields being available for model
    Updated 04/2022: updated docstrings to numpy documentation format
        include utf-8 encoding in reads to be windows compliant
        set default directory to None for documentation
    Updated 03/2022: added static decorators to define model lists
    Updated 02/2022: added Arctic 2km model (Arc2kmTM) to list of models
    Updated 01/2022: added global Empirical Ocean Tide model (EOT20)
    Updated 12/2021: added TPXO9-atlas-v5 to list of available tide models
        added atl10 attributes for tidal elevation files
    Written 09/2021
"""
from __future__ import annotations

import re
import io
import copy
import json
import pathlib
import pyTMD.io.constituents
from collections.abc import Iterable

class model:
    """Retrieves tide model parameters for named models or
    from a model definition file for use in the pyTMD tide
    prediction programs

    Attributes
    ----------
    atl03: str
        HDF5 dataset string for output ATL03 tide heights
    atl06: str
        HDF5 dataset string for output ATL06 tide heights
    atl07: str
        HDF5 dataset string for output ATL07 tide heights
    atl10: str
        HDF5 dataset string for output ATL10 tide heights
    atl11: str
        HDF5 dataset string for output ATL11 tide heights
    atl12: str
        HDF5 dataset string for output ATL12 tide heights
    compressed: bool
        Model files are gzip compressed
    constituents: list or None
        Model constituents for ``FES`` models
    minor: list or None
        Minor constituents for inference
    description: str
        HDF5 ``description`` attribute string for output tide heights
    directory: str, pathlib.Path or None, default None
        Working data directory for tide models
    flexure: bool
        Flexure adjustment field for tide heights is available
    format: str
        Model format

            - ``OTIS``
            - ``ATLAS-compact``
            - ``TMD3``
            - ``ATLAS-netcdf``
            - ``GOT-ascii``
            - ``GOT-netcdf``
            - ``FES-ascii``
            - ``FES-netcdf``
    gla12: str
        HDF5 dataset string for output GLA12 tide heights
    grid_file: pathlib.Path
        Model grid file for ``OTIS``, ``ATLAS-compact``, ``ATLAS-netcdf``, and ``TMD3`` models
    gzip: bool
        Suffix if model is compressed
    long_name: str
        HDF5 ``long_name`` attribute string for output tide heights
    model_directory: pathlib.Path
        Full path to model directory
    model_file: pathlib.Path or list
        Model constituent file or list of files
    name: str
        Model name
    projection: str
        Model projection for ``OTIS``, ``ATLAS-compact`` and ``TMD3`` models
    scale: float
        Model scaling factor for converting to output units
    suffix: str
        Suffix if model is ``'ATLAS-netcdf'``, ``GOT-ascii``, or ``'GOT-netcdf'`` formats
    type: str
        Model type

            - ``z``
            - ``u``
            - ``v``
    verify: bool
        Verify that all model files exist
    version: str
        Tide model version
    """
    def __init__(self, directory: str | pathlib.Path | None = None, **kwargs):
        # set default keyword arguments
        kwargs.setdefault('compressed', False)
        kwargs.setdefault('format', 'ATLAS-netcdf')
        kwargs.setdefault('verify', True)
        # set initial attributes
        self.compressed = copy.copy(kwargs['compressed'])
        self.constituents = None
        self.minor = None
        # set working data directory
        self.directory = None
        if directory is not None:
            self.directory = pathlib.Path(directory).expanduser()
        self.flexure = False
        # set tide model format
        self.format = copy.copy(kwargs['format'])
        self.grid_file = None
        self.model_file = None
        self.name = None
        self.projection = None
        self.reference = None
        self.scale = None
        self.type = None
        self.variable = None
        self.verify = copy.copy(kwargs['verify'])
        self.version = None

    def grid(self, m: str):
        """
        Create a model object from known tide grid files

        Parameters
        ----------
        m: str
            model name
        """
        # set working data directory if unset
        if self.directory is None:
            self.directory = pathlib.Path().absolute()
        # model name
        self.name = m
        # select between known tide models
        if (m == 'CATS0201'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('cats0201_tmd')
            self.grid_file = self.pathfinder('grid_CATS')
        elif (m == 'CATS2008'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('CATS2008')
            self.grid_file = self.pathfinder('grid_CATS2008')
        elif (m == 'CATS2008_load'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath(
                'CATS2008a_SPOTL_Load')
            self.grid_file = self.pathfinder('grid_CATS2008a_opt')
        elif (m == 'CATS2008-v2023'):
            self.format = 'TMD3'
            self.model_directory = self.directory.joinpath('CATS2008_v2023')
            self.grid_file = self.pathfinder('CATS2008_v2023.nc')
        elif (m == 'TPXO9-atlas'):
            self.model_directory = self.directory.joinpath('TPXO9_atlas')
            self.grid_file = self.pathfinder('grid_tpxo9_atlas')
            self.version = 'v1'
        elif (m == 'TPXO9-atlas-v2'):
            self.model_directory = self.directory.joinpath('TPXO9_atlas_v2')
            self.grid_file = self.pathfinder('grid_tpxo9_atlas_30_v2')
            self.version = 'v2'
        elif (m == 'TPXO9-atlas-v3'):
            self.model_directory = self.directory.joinpath('TPXO9_atlas_v3')
            self.grid_file = self.pathfinder('grid_tpxo9_atlas_30_v3')
            self.version = 'v3'
        elif (m == 'TPXO9-atlas-v4'):
            self.model_directory = self.directory.joinpath('TPXO9_atlas_v4')
            self.grid_file = self.pathfinder('grid_tpxo9_atlas_30_v4')
            self.version = 'v4'
        elif (m == 'TPXO9-atlas-v5'):
            self.model_directory = self.directory.joinpath('TPXO9_atlas_v5')
            self.grid_file = self.pathfinder('grid_tpxo9_atlas_30_v5')
            self.version = 'v5'
        elif (m == 'TPXO9.1'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('TPXO9.1','DATA')
            self.grid_file = self.pathfinder('grid_tpxo9')
            self.version = '9.1'
        elif (m == 'TPXO8-atlas'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('tpxo8_atlas')
            self.grid_file = self.pathfinder('grid_tpxo8atlas_30_v1')
            self.version = '8'
        elif (m == 'TPXO7.2'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('TPXO7.2_tmd')
            self.grid_file = self.pathfinder('grid_tpxo7.2')
            self.version = '7.2'
        elif (m == 'TPXO7.2_load'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('TPXO7.2_load')
            self.grid_file = self.pathfinder('grid_tpxo6.2')
            self.version = '7.2'
        elif (m == 'AODTM-5'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('aodtm5_tmd')
            self.grid_file = self.pathfinder('grid_Arc5km')
        elif (m == 'AOTIM-5'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('aotim5_tmd')
            self.grid_file = self.pathfinder('grid_Arc5km')
        elif (m == 'AOTIM-5-2018'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('Arc5km2018')
            self.grid_file = self.pathfinder('grid_Arc5km2018')
            self.version = '2018'
        elif (m == 'Arc2kmTM'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('Arc2kmTM')
            self.grid_file = self.pathfinder('grid_Arc2kmTM_v1')
        elif (m == 'Gr1kmTM'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('Gr1kmTM')
            self.grid_file = self.pathfinder('grid_Gr1kmTM_v1')
        elif (m == 'Gr1km-v2'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('greenlandTMD_v2')
            self.grid_file = self.pathfinder('grid_Greenland8.v2')
            self.version = 'v2'
        else:
            raise ValueError(f"Unlisted tide model {m}")
        # return the model parameters
        self.validate_format()
        return self

    def elevation(self, m: str):
        """
        Create a model object from known tidal elevation models

        Parameters
        ----------
        m: str
            model name
        """
        # set working data directory if unset
        if self.directory is None:
            self.directory = pathlib.Path().absolute()
        # model name
        self.name = m
        # model type
        self.type = 'z'
        # select between known tide models
        if (m == 'CATS0201'):
            self.model_directory = self.directory.joinpath('cats0201_tmd')
            self.grid_file = self.pathfinder('grid_CATS')
            self.model_file = self.pathfinder('h0_CATS02_01')
            self.format = 'OTIS'
            self.projection = '4326'
            # model description and references
            self.reference = ('https://mail.esr.org/polar_tide_models/'
                'Model_CATS0201.html')
            self.variable = 'tide_ocean'
        elif (m == 'CATS2008'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('CATS2008')
            self.grid_file = self.pathfinder('grid_CATS2008')
            self.model_file = self.pathfinder('hf.CATS2008.out')
            self.projection = 'CATS2008'
            # model description and references
            self.reference = 'https://doi.org/10.15784/601235'
            self.variable = 'tide_ocean'
        elif (m == 'CATS2008_load'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath(
                'CATS2008a_SPOTL_Load')
            self.grid_file = self.pathfinder('grid_CATS2008a_opt')
            self.model_file = self.pathfinder('h_CATS2008a_SPOTL_load')
            self.projection = 'CATS2008'
            # model description and references
            self.reference = 'https://doi.org/10.15784/601235'
            self.variable = 'tide_load'
        elif (m == 'CATS2008-v2023'):
            self.format = 'TMD3'
            self.model_directory = self.directory.joinpath('CATS2008_v2023')
            self.grid_file = self.pathfinder('CATS2008_v2023.nc')
            self.model_file = self.pathfinder('CATS2008_v2023.nc')
            self.projection = 'CATS2008'
            # internal flexure field is available
            self.flexure = True
            # model description and references
            self.reference = ('https://www.esr.org/research/'
                'polar-tide-models/list-of-polar-tide-models/cats2008/')
            self.variable = 'tide_ocean'
        elif (m == 'TPXO9-atlas'):
            self.model_directory = self.directory.joinpath('TPXO9_atlas')
            self.grid_file = self.pathfinder('grid_tpxo9_atlas')
            model_files = ['h_q1_tpxo9_atlas_30','h_o1_tpxo9_atlas_30',
                'h_p1_tpxo9_atlas_30','h_k1_tpxo9_atlas_30',
                'h_n2_tpxo9_atlas_30','h_m2_tpxo9_atlas_30',
                'h_s2_tpxo9_atlas_30','h_k2_tpxo9_atlas_30',
                'h_m4_tpxo9_atlas_30','h_ms4_tpxo9_atlas_30',
                'h_mn4_tpxo9_atlas_30','h_2n2_tpxo9_atlas_30']
            self.model_file = self.pathfinder(model_files)
            self.projection = '4326'
            self.scale = 1.0/1000.0
            self.version = 'v1'
            # model description and references
            self.reference = ('http://volkov.oce.orst.edu/tides/'
                'tpxo9_atlas.html')
            self.variable = 'tide_ocean'
        elif (m == 'TPXO9-atlas-v2'):
            self.model_directory = self.directory.joinpath('TPXO9_atlas_v2')
            self.grid_file = self.pathfinder('grid_tpxo9_atlas_30_v2')
            model_files = ['h_q1_tpxo9_atlas_30_v2','h_o1_tpxo9_atlas_30_v2',
                'h_p1_tpxo9_atlas_30_v2','h_k1_tpxo9_atlas_30_v2',
                'h_n2_tpxo9_atlas_30_v2','h_m2_tpxo9_atlas_30_v2',
                'h_s2_tpxo9_atlas_30_v2','h_k2_tpxo9_atlas_30_v2',
                'h_m4_tpxo9_atlas_30_v2','h_ms4_tpxo9_atlas_30_v2',
                'h_mn4_tpxo9_atlas_30_v2','h_2n2_tpxo9_atlas_30_v2']
            self.model_file = self.pathfinder(model_files)
            self.projection = '4326'
            self.scale = 1.0/1000.0
            self.version = 'v2'
            # model description and references
            self.reference = 'https://www.tpxo.net/global/tpxo9-atlas'
            self.variable = 'tide_ocean'
        elif (m == 'TPXO9-atlas-v3'):
            self.model_directory = self.directory.joinpath('TPXO9_atlas_v3')
            self.grid_file = self.pathfinder('grid_tpxo9_atlas_30_v3')
            model_files = ['h_q1_tpxo9_atlas_30_v3','h_o1_tpxo9_atlas_30_v3',
                'h_p1_tpxo9_atlas_30_v3','h_k1_tpxo9_atlas_30_v3',
                'h_n2_tpxo9_atlas_30_v3','h_m2_tpxo9_atlas_30_v3',
                'h_s2_tpxo9_atlas_30_v3','h_k2_tpxo9_atlas_30_v3',
                'h_m4_tpxo9_atlas_30_v3','h_ms4_tpxo9_atlas_30_v3',
                'h_mn4_tpxo9_atlas_30_v3','h_2n2_tpxo9_atlas_30_v3',
                'h_mf_tpxo9_atlas_30_v3','h_mm_tpxo9_atlas_30_v3']
            self.model_file = self.pathfinder(model_files)
            self.projection = '4326'
            self.scale = 1.0/1000.0
            self.version = 'v3'
            # model description and references
            self.reference = 'https://www.tpxo.net/global/tpxo9-atlas'
            self.variable = 'tide_ocean'
        elif (m == 'TPXO9-atlas-v4'):
            self.model_directory = self.directory.joinpath('TPXO9_atlas_v4')
            self.grid_file = self.pathfinder('grid_tpxo9_atlas_30_v4')
            model_files = ['h_q1_tpxo9_atlas_30_v4','h_o1_tpxo9_atlas_30_v4',
                'h_p1_tpxo9_atlas_30_v4','h_k1_tpxo9_atlas_30_v4',
                'h_n2_tpxo9_atlas_30_v4','h_m2_tpxo9_atlas_30_v4',
                'h_s2_tpxo9_atlas_30_v4','h_k2_tpxo9_atlas_30_v4',
                'h_m4_tpxo9_atlas_30_v4','h_ms4_tpxo9_atlas_30_v4',
                'h_mn4_tpxo9_atlas_30_v4','h_2n2_tpxo9_atlas_30_v4',
                'h_mf_tpxo9_atlas_30_v4','h_mm_tpxo9_atlas_30_v4']
            self.model_file = self.pathfinder(model_files)
            self.projection = '4326'
            self.scale = 1.0/1000.0
            self.version = 'v4'
            # model description and references
            self.reference = 'https://www.tpxo.net/global/tpxo9-atlas'
            self.variable = 'tide_ocean'
        elif (m == 'TPXO9-atlas-v5'):
            self.model_directory = self.directory.joinpath('TPXO9_atlas_v5')
            self.grid_file = self.pathfinder('grid_tpxo9_atlas_30_v5')
            model_files = ['h_q1_tpxo9_atlas_30_v5','h_o1_tpxo9_atlas_30_v5',
                'h_p1_tpxo9_atlas_30_v5','h_k1_tpxo9_atlas_30_v5',
                'h_n2_tpxo9_atlas_30_v5','h_m2_tpxo9_atlas_30_v5',
                'h_s1_tpxo9_atlas_30_v5','h_s2_tpxo9_atlas_30_v5',
                'h_k2_tpxo9_atlas_30_v5','h_m4_tpxo9_atlas_30_v5',
                'h_ms4_tpxo9_atlas_30_v5','h_mn4_tpxo9_atlas_30_v5',
                'h_2n2_tpxo9_atlas_30_v5','h_mf_tpxo9_atlas_30_v5',
                'h_mm_tpxo9_atlas_30_v5']
            self.model_file = self.pathfinder(model_files)
            self.projection = '4326'
            self.scale = 1.0/1000.0
            self.version = 'v5'
            # model description and references
            self.reference = 'https://www.tpxo.net/global/tpxo9-atlas'
            self.variable = 'tide_ocean'
        elif (m == 'TPXO9.1'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('TPXO9.1','DATA')
            self.grid_file = self.pathfinder('grid_tpxo9')
            self.model_file = self.pathfinder('h_tpxo9.v1')
            self.projection = '4326'
            self.version = '9.1'
            # model description and references
            self.reference = ('http://volkov.oce.orst.edu/'
                'tides/global.html')
            self.variable = 'tide_ocean'
        elif (m == 'TPXO8-atlas'):
            self.format = 'ATLAS-compact'
            self.model_directory = self.directory.joinpath('tpxo8_atlas')
            self.grid_file = self.pathfinder('grid_tpxo8atlas_30_v1')
            self.model_file = self.pathfinder('hf.tpxo8_atlas_30_v1')
            self.projection = '4326'
            self.version = '8'
            # model description and references
            self.reference = ('http://volkov.oce.orst.edu/'
                'tides/tpxo8_atlas.html')
            self.variable = 'tide_ocean'
        elif (m == 'TPXO7.2'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('TPXO7.2_tmd')
            self.grid_file = self.pathfinder('grid_tpxo7.2')
            self.model_file = self.pathfinder('h_tpxo7.2')
            self.projection = '4326'
            self.version = '7.2'
            # model description and references
            self.reference = ('http://volkov.oce.orst.edu/'
                'tides/global.html')
            self.variable = 'tide_ocean'
        elif (m == 'TPXO7.2_load'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('TPXO7.2_load')
            self.grid_file = self.pathfinder('grid_tpxo6.2')
            self.model_file = self.pathfinder('h_tpxo7.2_load')
            self.projection = '4326'
            self.version = '7.2'
            # model description and references
            self.reference = ('http://volkov.oce.orst.edu/'
                'tides/global.html')
            self.variable = 'tide_load'
        elif (m == 'AODTM-5'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('aodtm5_tmd')
            self.grid_file = self.pathfinder('grid_Arc5km')
            self.model_file = self.pathfinder('h0_Arc5km.oce')
            self.projection = 'PSNorth'
            # model description and references
            self.reference = ('https://www.esr.org/research/'
                'polar-tide-models/list-of-polar-tide-models/'
                'aodtm-5/')
            self.variable = 'tide_ocean'
        elif (m == 'AOTIM-5'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('aotim5_tmd')
            self.grid_file = self.pathfinder('grid_Arc5km')
            self.model_file = self.pathfinder('h_Arc5km.oce')
            self.projection = 'PSNorth'
            # model description and references
            self.reference = ('https://www.esr.org/research/'
                'polar-tide-models/list-of-polar-tide-models/'
                'aotim-5/')
            self.variable = 'tide_ocean'
        elif (m == 'AOTIM-5-2018'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('Arc5km2018')
            self.grid_file = self.pathfinder('grid_Arc5km2018')
            self.model_file = self.pathfinder('h_Arc5km2018')
            self.projection = 'PSNorth'
            self.version = '2018'
            # model description and references
            self.reference = ('https://www.esr.org/research/'
                'polar-tide-models/list-of-polar-tide-models/'
                'aotim-5/')
            self.variable = 'tide_ocean'
        elif (m == 'Arc2kmTM'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('Arc2kmTM')
            self.grid_file = self.pathfinder('grid_Arc2kmTM_v1')
            self.model_file = self.pathfinder('h_Arc2kmTM_v1')
            self.projection = '3413'
            self.version = 'v1'
            # model description and references
            self.reference = 'https://doi.org/10.18739/A2D21RK6K'
            self.variable = 'tide_ocean'
        elif (m == 'Gr1kmTM'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('Gr1kmTM')
            self.grid_file = self.pathfinder('grid_Gr1kmTM_v1')
            self.model_file = self.pathfinder('h_Gr1kmTM_v1')
            self.projection = '3413'
            self.version = 'v1'
            # model description and references
            self.reference = 'https://doi.org/10.18739/A2B853K18'
            self.variable = 'tide_ocean'
        elif (m == 'Gr1km-v2'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('greenlandTMD_v2')
            self.grid_file = self.pathfinder('grid_Greenland8.v2')
            self.model_file = self.pathfinder('h_Greenland8.v2')
            self.projection = '3413'
            self.version = 'v2'
            # model description and references
            self.reference = 'https://doi.org/10.1002/2016RG000546'
            self.variable = 'tide_ocean'
        elif (m == 'GOT4.7'):
            self.format = 'GOT-ascii'
            self.model_directory = self.directory.joinpath(
                'GOT4.7','grids_oceantide')
            model_files = ['q1','o1','p1','k1','n2','m2','s2','k2','s1','m4']
            self.model_file = self.pathfinder(model_files)
            self.scale = 1.0/100.0
            self.version = '4.7'
            # list of minor constituents for inference
            self.minor = ['2q1', 'sigma1', 'rho1', 'm1b', 'm1', 'chi1', 'pi1',
                'phi1', 'theta1', 'j1', 'oo1', '2n2', 'mu2', 'nu2', 'lambda2',
                'l2', 'l2b', 't2']
            # model description and references
            self.reference = 'https://ntrs.nasa.gov/citations/19990089548'
            self.variable = 'tide_ocean'
        elif (m == 'GOT4.7_load'):
            self.format = 'GOT-ascii'
            self.model_directory = self.directory.joinpath(
                'GOT4.7','grids_loadtide')
            model_files = ['q1load','o1load','p1load','k1load','n2load',
                'm2load','s2load','k2load','s1load','m4load']
            self.model_file = self.pathfinder(model_files)
            self.scale = 1.0/1000.0
            self.version = '4.7'
            # list of minor constituents for inference
            self.minor = ['2q1', 'sigma1', 'rho1', 'm1b', 'm1', 'chi1', 'pi1',
                'phi1', 'theta1', 'j1', 'oo1', '2n2', 'mu2', 'nu2', 'lambda2',
                'l2', 'l2b', 't2']
            # model description and references
            self.reference = 'https://ntrs.nasa.gov/citations/19990089548'
            self.variable = 'tide_load'
        elif (m == 'GOT4.8'):
            self.format = 'GOT-ascii'
            self.model_directory = self.directory.joinpath(
                'got4.8','grids_oceantide')
            model_files = ['q1','o1','p1','k1','n2','m2','s2','k2','s1','m4']
            self.model_file = self.pathfinder(model_files)
            self.scale = 1.0/100.0
            self.version = '4.8'
            # list of minor constituents for inference
            self.minor = ['2q1', 'sigma1', 'rho1', 'm1b', 'm1', 'chi1', 'pi1',
                'phi1', 'theta1', 'j1', 'oo1', '2n2', 'mu2', 'nu2', 'lambda2',
                'l2', 'l2b', 't2']
            # model description and references
            self.reference = 'https://ntrs.nasa.gov/citations/19990089548'
            self.variable = 'tide_ocean'
        elif (m == 'GOT4.8_load'):
            self.format = 'GOT-ascii'
            self.model_directory = self.directory.joinpath(
                'got4.8','grids_loadtide')
            model_files = ['q1load','o1load','p1load','k1load','n2load',
                'm2load','s2load','k2load','s1load','m4load']
            self.model_file = self.pathfinder(model_files)
            self.scale = 1.0/1000.0
            self.version = '4.8'
            # list of minor constituents for inference
            self.minor = ['2q1', 'sigma1', 'rho1', 'm1b', 'm1', 'chi1', 'pi1',
                'phi1', 'theta1', 'j1', 'oo1', '2n2', 'mu2', 'nu2', 'lambda2',
                'l2', 'l2b', 't2']
            # model description and references
            self.reference = 'https://ntrs.nasa.gov/citations/19990089548'
            self.variable = 'tide_load'
        elif (m == 'GOT4.10'):
            self.format = 'GOT-ascii'
            self.model_directory = self.directory.joinpath(
                'GOT4.10c','grids_oceantide')
            model_files = ['q1','o1','p1','k1','n2','m2','s2','k2','s1','m4']
            self.model_file = self.pathfinder(model_files)
            self.scale = 1.0/100.0
            self.version = '4.10'
            # list of minor constituents for inference
            self.minor = ['2q1', 'sigma1', 'rho1', 'm1b', 'm1', 'chi1', 'pi1',
                'phi1', 'theta1', 'j1', 'oo1', '2n2', 'mu2', 'nu2', 'lambda2',
                'l2', 'l2b', 't2']
            # model description and references
            self.reference = 'https://ntrs.nasa.gov/citations/19990089548'
            self.variable = 'tide_ocean'
        elif (m == 'GOT4.10_load'):
            self.format = 'GOT-ascii'
            self.model_directory = self.directory.joinpath(
                'GOT4.10c','grids_loadtide')
            model_files = ['q1load','o1load','p1load','k1load','n2load',
                'm2load','s2load','k2load','s1load','m4load']
            self.model_file = self.pathfinder(model_files)
            self.scale = 1.0/1000.0
            self.version = '4.10'
            # list of minor constituents for inference
            self.minor = ['2q1', 'sigma1', 'rho1', 'm1b', 'm1', 'chi1', 'pi1',
                'phi1', 'theta1', 'j1', 'oo1', '2n2', 'mu2', 'nu2', 'lambda2',
                'l2', 'l2b', 't2']
            # model description and references
            self.reference = 'https://ntrs.nasa.gov/citations/19990089548'
            self.variable = 'tide_load'
        elif (m == 'GOT5.5'):
            self.format = 'GOT-netcdf'
            self.model_directory = self.directory.joinpath(
                'GOT5.5','ocean_tides')
            model_files = ['2n2','j1','k1','k2','m2','m4','ms4','mu2','n2',
                'o1','oo1','p1','q1','s1','s2','sig1']
            self.model_file = self.pathfinder(model_files)
            self.scale = 1.0/100.0
            self.version = '5.5'
            # model description and references
            self.reference = 'https://ntrs.nasa.gov/citations/19990089548'
            self.variable = 'tide_ocean'
        elif (m == 'GOT5.5_load'):
            self.format = 'GOT-netcdf'
            self.model_directory = self.directory.joinpath(
                'GOT5.5','load_tides')
            model_files = ['2n2load','k1load','m2load','ms4load','n2load',
                'oo1load','q1load','s2load','j1load','k2load','m4load',
                'mu2load','o1load','p1load','s1load','sig1load']
            self.model_file = self.pathfinder(model_files)
            self.scale = 1.0/1000.0
            self.version = '5.5'
            # model description and references
            self.reference = 'https://ntrs.nasa.gov/citations/19990089548'
            self.variable = 'tide_load'
        elif (m == 'FES2014'):
            self.format = 'FES-netcdf'
            self.model_directory = self.directory.joinpath(
                'fes2014','ocean_tide')
            model_files = ['2n2.nc','eps2.nc','j1.nc','k1.nc',
                'k2.nc','l2.nc','la2.nc','m2.nc','m3.nc','m4.nc',
                'm6.nc','m8.nc','mf.nc','mks2.nc','mm.nc',
                'mn4.nc','ms4.nc','msf.nc','msqm.nc','mtm.nc',
                'mu2.nc','n2.nc','n4.nc','nu2.nc','o1.nc','p1.nc',
                'q1.nc','r2.nc','s1.nc','s2.nc','s4.nc','sa.nc',
                'ssa.nc','t2.nc']
            self.model_file = self.pathfinder(model_files)
            self.constituents = [self.parse_file(f) for f in model_files]
            self.scale = 1.0/100.0
            self.version = 'FES2014'
            # model description and references
            self.reference = ('https://www.aviso.altimetry.fr/'
                'en/data/products/auxiliary-products/'
                'global-tide-fes.html')
            self.variable = 'tide_ocean'
        elif (m == 'FES2014_load'):
            self.format = 'FES-netcdf'
            self.model_directory = self.directory.joinpath(
                'fes2014','load_tide')
            model_files = ['2n2.nc','eps2.nc','j1.nc','k1.nc',
                'k2.nc','l2.nc','la2.nc','m2.nc','m3.nc','m4.nc',
                'm6.nc','m8.nc','mf.nc','mks2.nc','mm.nc',
                'mn4.nc','ms4.nc','msf.nc','msqm.nc','mtm.nc',
                'mu2.nc','n2.nc','n4.nc','nu2.nc','o1.nc','p1.nc',
                'q1.nc','r2.nc','s1.nc','s2.nc','s4.nc','sa.nc',
                'ssa.nc','t2.nc']
            self.model_file = self.pathfinder(model_files)
            self.constituents = [self.parse_file(f) for f in model_files]
            self.scale = 1.0/100.0
            self.version = 'FES2014'
            # model description and references
            self.reference = ('https://www.aviso.altimetry.fr/'
                'en/data/products/auxiliary-products/'
                'global-tide-fes.html')
            self.variable = 'tide_load'
        elif (m == 'FES2022'):
            self.format = 'FES-netcdf'
            self.model_directory = self.directory.joinpath(
                'fes2022b','ocean_tide')
            model_files = ['2n2_fes2022.nc','eps2_fes2022.nc',
                'j1_fes2022.nc','k1_fes2022.nc','k2_fes2022.nc',
                'l2_fes2022.nc','lambda2_fes2022.nc','m2_fes2022.nc',
                'm3_fes2022.nc','m4_fes2022.nc','m6_fes2022.nc',
                'm8_fes2022.nc','mf_fes2022.nc','mks2_fes2022.nc',
                'mm_fes2022.nc','mn4_fes2022.nc','ms4_fes2022.nc',
                'msf_fes2022.nc','msqm_fes2022.nc','mtm_fes2022.nc',
                'mu2_fes2022.nc','n2_fes2022.nc','n4_fes2022.nc',
                'nu2_fes2022.nc','o1_fes2022.nc','p1_fes2022.nc',
                'q1_fes2022.nc','r2_fes2022.nc','s1_fes2022.nc',
                's2_fes2022.nc','s4_fes2022.nc','sa_fes2022.nc',
                'ssa_fes2022.nc','t2_fes2022.nc']
            self.model_file = self.pathfinder(model_files)
            self.constituents = [self.parse_file(f) for f in model_files]
            self.scale = 1.0/100.0
            self.version = 'FES2022'
            # model description and references
            self.reference = 'https://doi.org/10.24400/527896/A01-2024.004'
            self.variable = 'tide_ocean'
        elif (m == 'FES2022_load'):
            self.format = 'FES-netcdf'
            self.model_directory = self.directory.joinpath(
                'fes2022b','load_tide')
            model_files = ['2n2_fes2022.nc','eps2_fes2022.nc',
                'j1_fes2022.nc','k1_fes2022.nc','k2_fes2022.nc',
                'l2_fes2022.nc','lambda2_fes2022.nc','m2_fes2022.nc',
                'm3_fes2022.nc','m4_fes2022.nc','m6_fes2022.nc',
                'm8_fes2022.nc','mf_fes2022.nc','mks2_fes2022.nc',
                'mm_fes2022.nc','mn4_fes2022.nc','ms4_fes2022.nc',
                'msf_fes2022.nc','msqm_fes2022.nc','mtm_fes2022.nc',
                'mu2_fes2022.nc','n2_fes2022.nc','n4_fes2022.nc',
                'nu2_fes2022.nc','o1_fes2022.nc','p1_fes2022.nc',
                'q1_fes2022.nc','r2_fes2022.nc','s1_fes2022.nc',
                's2_fes2022.nc','s4_fes2022.nc','sa_fes2022.nc',
                'ssa_fes2022.nc','t2_fes2022.nc']
            self.model_file = self.pathfinder(model_files)
            self.constituents = [self.parse_file(f) for f in model_files]
            self.scale = 1.0/100.0
            self.version = 'FES2022'
            # model description and references
            self.reference = 'https://doi.org/10.24400/527896/A01-2024.004'
            self.variable = 'tide_load'
        elif (m == 'EOT20'):
            self.format = 'FES-netcdf'
            self.model_directory = self.directory.joinpath(
                'EOT20','ocean_tides')
            model_files = ['2N2_ocean_eot20.nc','J1_ocean_eot20.nc',
                'K1_ocean_eot20.nc','K2_ocean_eot20.nc',
                'M2_ocean_eot20.nc','M4_ocean_eot20.nc',
                'MF_ocean_eot20.nc','MM_ocean_eot20.nc',
                'N2_ocean_eot20.nc','O1_ocean_eot20.nc',
                'P1_ocean_eot20.nc','Q1_ocean_eot20.nc',
                'S1_ocean_eot20.nc','S2_ocean_eot20.nc',
                'SA_ocean_eot20.nc','SSA_ocean_eot20.nc',
                'T2_ocean_eot20.nc']
            self.model_file = self.pathfinder(model_files)
            self.constituents = [self.parse_file(f) for f in model_files]
            self.scale = 1.0/100.0
            self.version = 'EOT20'
            # model description and references
            self.reference = 'https://doi.org/10.17882/79489'
            self.variable = 'tide_ocean'
        elif (m == 'EOT20_load'):
            self.format = 'FES-netcdf'
            self.model_directory = self.directory.joinpath(
                'EOT20','load_tides')
            model_files = ['2N2_load_eot20.nc','J1_load_eot20.nc',
                'K1_load_eot20.nc','K2_load_eot20.nc',
                'M2_load_eot20.nc','M4_load_eot20.nc',
                'MF_load_eot20.nc','MM_load_eot20.nc',
                'N2_load_eot20.nc','O1_load_eot20.nc',
                'P1_load_eot20.nc','Q1_load_eot20.nc',
                'S1_load_eot20.nc','S2_load_eot20.nc',
                'SA_load_eot20.nc','SSA_load_eot20.nc',
                'T2_load_eot20.nc']
            self.model_file = self.pathfinder(model_files)
            self.constituents = [self.parse_file(f) for f in model_files]
            self.scale = 1.0/100.0
            self.version = 'EOT20'
            # model description and references
            self.reference = 'https://doi.org/10.17882/79489'
            self.variable = 'tide_load'
        elif (m == 'HAMTIDE11'):
            self.format = 'FES-netcdf'
            self.model_directory = self.directory.joinpath('hamtide')
            model_files = ['2n.hamtide11a.nc','k1.hamtide11a.nc','k2.hamtide11a.nc',
                'm2.hamtide11a.nc','n2.hamtide11a.nc','o1.hamtide11a.nc',
                'p1.hamtide11a.nc','q1.hamtide11a.nc','s2.hamtide11a.nc']
            self.model_file = self.pathfinder(model_files)
            self.constituents = [self.parse_file(f) for f in model_files]
            self.scale = 1.0/100.0
            self.version = 'HAMTIDE11'
            # model description and references
            self.reference = 'https://doi.org/10.1002/2013JC009766'
            self.variable = 'tide_ocean'
        else:
            raise ValueError(f"Unlisted tide model {m}")
        # return the model parameters
        self.validate_format()
        return self

    def current(self, m: str):
        """
        Create a model object from known tidal current models

        Parameters
        ----------
        m: str
            model name
        """
        # set working data directory if unset
        if self.directory is None:
            self.directory = pathlib.Path().absolute()
        # model name
        self.name = m
        # model type
        self.type = ['u','v']
        # select between tide models
        if (m == 'CATS0201'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('cats0201_tmd')
            self.grid_file = self.pathfinder('grid_CATS')
            self.model_file = dict(u=self.pathfinder('UV0_CATS02_01'))
            self.projection = '4326'
            # model description and references
            self.reference = ('https://mail.esr.org/polar_tide_models/'
                'Model_CATS0201.html')
        elif (m == 'CATS2008'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('CATS2008')
            self.grid_file = self.pathfinder('grid_CATS2008')
            self.model_file = dict(u=self.pathfinder('uv.CATS2008.out'))
            self.projection = 'CATS2008'
        elif (m == 'CATS2008-v2023'):
            self.format = 'TMD3'
            self.model_directory = self.directory.joinpath('CATS2008_v2023')
            self.grid_file = self.pathfinder('CATS2008_v2023.nc')
            self.model_file = dict(u=self.pathfinder('CATS2008_v2023.nc'))
            self.projection = 'CATS2008'
        elif (m == 'TPXO9-atlas'):
            self.model_directory = self.directory.joinpath('TPXO9_atlas')
            self.grid_file = self.pathfinder('grid_tpxo9_atlas')
            model_files = {}
            model_files['u'] = ['u_q1_tpxo9_atlas_30','u_o1_tpxo9_atlas_30',
                'u_p1_tpxo9_atlas_30','u_k1_tpxo9_atlas_30',
                'u_n2_tpxo9_atlas_30','u_m2_tpxo9_atlas_30',
                'u_s2_tpxo9_atlas_30','u_k2_tpxo9_atlas_30',
                'u_m4_tpxo9_atlas_30','u_ms4_tpxo9_atlas_30',
                'u_mn4_tpxo9_atlas_30','u_2n2_tpxo9_atlas_30']
            # add v-component if format is netcdf
            if (self.format == 'ATLAS-netcdf'):
                model_files['v'] = ['v_q1_tpxo9_atlas_30',
                    'v_o1_tpxo9_atlas_30','v_p1_tpxo9_atlas_30',
                    'v_k1_tpxo9_atlas_30','v_n2_tpxo9_atlas_30',
                    'v_m2_tpxo9_atlas_30','v_s2_tpxo9_atlas_30',
                    'v_k2_tpxo9_atlas_30','v_m4_tpxo9_atlas_30',
                    'v_ms4_tpxo9_atlas_30','v_mn4_tpxo9_atlas_30',
                    'v_2n2_tpxo9_atlas_30']
            # build model file dictionary
            self.model_file = {}
            for key,val in model_files.items():
                self.model_file[key] = self.pathfinder(val)
            self.projection = '4326'
            self.scale = 1e-4
            self.version = 'v1'
            # model description and references
            self.reference = ('http://volkov.oce.orst.edu/tides/'
                'tpxo9_atlas.html')
        elif (m == 'TPXO9-atlas-v2'):
            self.model_directory = self.directory.joinpath('TPXO9_atlas_v2')
            self.grid_file = self.pathfinder('grid_tpxo9_atlas_30_v2')
            model_files = {}
            model_files['u'] = ['u_q1_tpxo9_atlas_30_v2','u_o1_tpxo9_atlas_30_v2',
                'u_p1_tpxo9_atlas_30_v2','u_k1_tpxo9_atlas_30_v2',
                'u_n2_tpxo9_atlas_30_v2','u_m2_tpxo9_atlas_30_v2',
                'u_s2_tpxo9_atlas_30_v2','u_k2_tpxo9_atlas_30_v2',
                'u_m4_tpxo9_atlas_30_v2','u_ms4_tpxo9_atlas_30_v2',
                'u_mn4_tpxo9_atlas_30_v2','u_2n2_tpxo9_atlas_30_v2']
            # add v-component if format is netcdf
            if (self.format == 'ATLAS-netcdf'):
                model_files['v'] = ['v_q1_tpxo9_atlas_30_v2',
                    'v_o1_tpxo9_atlas_30_v2','v_p1_tpxo9_atlas_30_v2',
                    'v_k1_tpxo9_atlas_30_v2','v_n2_tpxo9_atlas_30_v2',
                    'v_m2_tpxo9_atlas_30_v2','v_s2_tpxo9_atlas_30_v2',
                    'v_k2_tpxo9_atlas_30_v2','v_m4_tpxo9_atlas_30_v2',
                    'v_ms4_tpxo9_atlas_30_v2','v_mn4_tpxo9_atlas_30_v2',
                    'v_2n2_tpxo9_atlas_30_v2']
            # build model file dictionary
            self.model_file = {}
            for key,val in model_files.items():
                self.model_file[key] = self.pathfinder(val)
            self.projection = '4326'
            self.scale = 1e-4
            self.version = 'v2'
            # model description and references
            self.reference = 'https://www.tpxo.net/global/tpxo9-atlas'
        elif (m == 'TPXO9-atlas-v3'):
            self.model_directory = self.directory.joinpath('TPXO9_atlas_v3')
            self.grid_file = self.pathfinder('grid_tpxo9_atlas_30_v3')
            model_files = {}
            model_files['u'] = ['u_q1_tpxo9_atlas_30_v3','u_o1_tpxo9_atlas_30_v3',
                'u_p1_tpxo9_atlas_30_v3','u_k1_tpxo9_atlas_30_v3',
                'u_n2_tpxo9_atlas_30_v3','u_m2_tpxo9_atlas_30_v3',
                'u_s2_tpxo9_atlas_30_v3','u_k2_tpxo9_atlas_30_v3',
                'u_m4_tpxo9_atlas_30_v3','u_ms4_tpxo9_atlas_30_v3',
                'u_mn4_tpxo9_atlas_30_v3','u_2n2_tpxo9_atlas_30_v3',
                'u_mf_tpxo9_atlas_30_v3','u_mm_tpxo9_atlas_30_v3']
            # add v-component if format is netcdf
            if (self.format == 'ATLAS-netcdf'):
                model_files['v'] = ['v_q1_tpxo9_atlas_30_v3',
                    'v_o1_tpxo9_atlas_30_v3','v_p1_tpxo9_atlas_30_v3',
                    'v_k1_tpxo9_atlas_30_v3','v_n2_tpxo9_atlas_30_v3',
                    'v_m2_tpxo9_atlas_30_v3','v_s2_tpxo9_atlas_30_v3',
                    'v_k2_tpxo9_atlas_30_v3','v_m4_tpxo9_atlas_30_v3',
                    'v_ms4_tpxo9_atlas_30_v3','v_mn4_tpxo9_atlas_30_v3',
                    'v_2n2_tpxo9_atlas_30_v3','v_mf_tpxo9_atlas_30_v3',
                    'v_mm_tpxo9_atlas_30_v3']
            # build model file dictionary
            self.model_file = {}
            for key,val in model_files.items():
                self.model_file[key] = self.pathfinder(val)
            self.projection = '4326'
            self.scale = 1e-4
            self.version = 'v3'
            # model description and references
            self.reference = 'https://www.tpxo.net/global/tpxo9-atlas'
        elif (m == 'TPXO9-atlas-v4'):
            self.model_directory = self.directory.joinpath('TPXO9_atlas_v4')
            self.grid_file = self.pathfinder('grid_tpxo9_atlas_30_v4')
            model_files = {}
            model_files['u'] = ['u_q1_tpxo9_atlas_30_v4','u_o1_tpxo9_atlas_30_v4',
                'u_p1_tpxo9_atlas_30_v4','u_k1_tpxo9_atlas_30_v4',
                'u_n2_tpxo9_atlas_30_v4','u_m2_tpxo9_atlas_30_v4',
                'u_s2_tpxo9_atlas_30_v4','u_k2_tpxo9_atlas_30_v4',
                'u_m4_tpxo9_atlas_30_v4','u_ms4_tpxo9_atlas_30_v4',
                'u_mn4_tpxo9_atlas_30_v4','u_2n2_tpxo9_atlas_30_v4',
                'u_mf_tpxo9_atlas_30_v4','u_mm_tpxo9_atlas_30_v4']
            # add v-component if format is netcdf
            if (self.format == 'ATLAS-netcdf'):
                model_files['v'] = ['v_q1_tpxo9_atlas_30_v4',
                    'v_o1_tpxo9_atlas_30_v4','v_p1_tpxo9_atlas_30_v4',
                    'v_k1_tpxo9_atlas_30_v4','v_n2_tpxo9_atlas_30_v4',
                    'v_m2_tpxo9_atlas_30_v4','v_s2_tpxo9_atlas_30_v4',
                    'v_k2_tpxo9_atlas_30_v4','v_m4_tpxo9_atlas_30_v4',
                    'v_ms4_tpxo9_atlas_30_v4','v_mn4_tpxo9_atlas_30_v4',
                    'v_2n2_tpxo9_atlas_30_v4','v_mf_tpxo9_atlas_30_v4',
                    'v_mm_tpxo9_atlas_30_v4']
            # build model file dictionary
            self.model_file = {}
            for key,val in model_files.items():
                self.model_file[key] = self.pathfinder(val)
            self.projection = '4326'
            self.scale = 1e-4
            self.version = 'v4'
            # model description and references
            self.reference = 'https://www.tpxo.net/global/tpxo9-atlas'
        elif (m == 'TPXO9-atlas-v5'):
            self.model_directory = self.directory.joinpath('TPXO9_atlas_v5')
            self.grid_file = self.pathfinder('grid_tpxo9_atlas_30_v5')
            model_files = {}
            model_files['u'] = ['u_q1_tpxo9_atlas_30_v5','u_o1_tpxo9_atlas_30_v5',
                'u_p1_tpxo9_atlas_30_v5','u_k1_tpxo9_atlas_30_v5',
                'u_n2_tpxo9_atlas_30_v5','u_m2_tpxo9_atlas_30_v5',
                'u_s1_tpxo9_atlas_30_v5','u_s2_tpxo9_atlas_30_v5',
                'u_k2_tpxo9_atlas_30_v5','u_m4_tpxo9_atlas_30_v5',
                'u_ms4_tpxo9_atlas_30_v5','u_mn4_tpxo9_atlas_30_v5',
                'u_2n2_tpxo9_atlas_30_v5','u_mf_tpxo9_atlas_30_v5',
                'u_mm_tpxo9_atlas_30_v5']
            # add v-component if format is netcdf
            if (self.format == 'ATLAS-netcdf'):
                model_files['v'] = ['u_q1_tpxo9_atlas_30_v5',
                    'u_o1_tpxo9_atlas_30_v5','u_p1_tpxo9_atlas_30_v5',
                    'u_k1_tpxo9_atlas_30_v5','u_n2_tpxo9_atlas_30_v5',
                    'u_m2_tpxo9_atlas_30_v5','u_s1_tpxo9_atlas_30_v5',
                    'u_s2_tpxo9_atlas_30_v5','u_k2_tpxo9_atlas_30_v5',
                    'u_m4_tpxo9_atlas_30_v5','u_ms4_tpxo9_atlas_30_v5',
                    'u_mn4_tpxo9_atlas_30_v5','u_2n2_tpxo9_atlas_30_v5',
                    'u_mf_tpxo9_atlas_30_v5','u_mm_tpxo9_atlas_30_v5']
            # build model file dictionary
            self.model_file = {}
            for key,val in model_files.items():
                self.model_file[key] = self.pathfinder(val)
            self.projection = '4326'
            self.scale = 1e-4
            self.version = 'v5'
            # model description and references
            self.reference = 'https://www.tpxo.net/global/tpxo9-atlas'
        elif (m == 'TPXO9.1'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('TPXO9.1')
            self.grid_file = self.pathfinder('grid_tpxo9')
            self.model_file = dict(u=self.pathfinder('u_tpxo9.v1'))
            self.projection = '4326'
            self.version = '9.1'
            # model description and references
            self.reference = ('http://volkov.oce.orst.edu/tides/'
                'global.html')
        elif (m == 'TPXO8-atlas'):
            self.format = 'ATLAS-compact'
            self.model_directory = self.directory.joinpath('tpxo8_atlas')
            self.grid_file = self.pathfinder('grid_tpxo8atlas_30_v1')
            self.model_file = dict(u=self.pathfinder('uv.tpxo8_atlas_30_v1'))
            self.projection = '4326'
            self.version = '8'
            # model description and references
            self.reference = ('http://volkov.oce.orst.edu/tides/'
                'tpxo8_atlas.html')
        elif (m == 'TPXO7.2'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('TPXO7.2_tmd')
            self.grid_file = self.pathfinder('grid_tpxo7.2')
            self.model_file = dict(u=self.pathfinder('u_tpxo7.2'))
            self.projection = '4326'
            self.version = '7.2'
            # model description and references
            self.reference = ('http://volkov.oce.orst.edu/tides/'
                'global.html')
        elif (m == 'AODTM-5'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('aodtm5_tmd')
            self.grid_file = self.pathfinder('grid_Arc5km')
            self.model_file = dict(u=self.pathfinder('UV0_Arc5km'))
            self.projection = 'PSNorth'
            # model description and references
            self.reference = ('https://www.esr.org/research/'
                'polar-tide-models/list-of-polar-tide-models/'
                'aodtm-5/')
        elif (m == 'AOTIM-5'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('aotim5_tmd')
            self.grid_file = self.pathfinder('grid_Arc5km')
            self.model_file = dict(u=self.pathfinder('UV_Arc5km'))
            self.projection = 'PSNorth'
            # model description and references
            self.reference = ('https://www.esr.org/research/'
                'polar-tide-models/list-of-polar-tide-models/'
                'aotim-5/')
        elif (m == 'AOTIM-5-2018'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('Arc5km2018')
            self.grid_file = self.pathfinder('grid_Arc5km2018')
            self.model_file = dict(u=self.pathfinder('UV_Arc5km2018'))
            self.projection = 'PSNorth'
            self.version = '2018'
            # model description and references
            self.reference = ('https://www.esr.org/research/'
                'polar-tide-models/list-of-polar-tide-models/'
                'aotim-5/')
        elif (m == 'Arc2kmTM'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('Arc2kmTM')
            self.grid_file = self.pathfinder('grid_Arc2kmTM_v1')
            self.model_file = dict(u=self.pathfinder('UV_Arc2kmTM_v1'))
            self.projection = '3413'
            self.version = 'v1'
            # model description and references
            self.reference = 'https://doi.org/10.18739/A2D21RK6K'
        elif (m == 'Gr1kmTM'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('Gr1kmTM')
            self.grid_file = self.pathfinder('grid_Gr1kmTM_v1')
            self.model_file = dict(u=self.pathfinder('UV_Gr1kmTM_v1'))
            self.projection = '3413'
            self.version = 'v1'
            # model description and references
            self.reference = 'https://doi.org/10.18739/A2B853K18'
        elif (m == 'Gr1km-v2'):
            self.format = 'OTIS'
            self.model_directory = self.directory.joinpath('greenlandTMD_v2')
            self.grid_file = self.pathfinder('grid_Greenland8.v2')
            self.model_file = dict(u=self.pathfinder('u_Greenland8_rot.v2'))
            self.projection = '3413'
            self.version = 'v2'
            # model description and references
            self.reference = 'https://doi.org/10.1002/2016RG000546'
        elif (m == 'FES2014'):
            self.format = 'FES-netcdf'
            model_directory = {}
            model_directory['u'] = self.directory.joinpath(
                'fes2014','eastward_velocity')
            model_directory['v'] = self.directory.joinpath(
                'fes2014','northward_velocity')
            model_files = ['2n2.nc','eps2.nc','j1.nc','k1.nc',
                'k2.nc','l2.nc','la2.nc','m2.nc','m3.nc','m4.nc',
                'm6.nc','m8.nc','mf.nc','mks2.nc','mm.nc',
                'mn4.nc','ms4.nc','msf.nc','msqm.nc','mtm.nc',
                'mu2.nc','n2.nc','n4.nc','nu2.nc','o1.nc','p1.nc',
                'q1.nc','r2.nc','s1.nc','s2.nc','s4.nc','sa.nc',
                'ssa.nc','t2.nc']
            self.model_file = {}
            for key, val in model_directory.items():
                self.model_directory = copy.copy(val)
                self.model_file[key] = self.pathfinder(model_files)
            self.constituents = [self.parse_file(f) for f in model_files]
            self.scale = 1.0
            self.version = 'FES2014'
            # model description and references
            self.reference = ('https://www.aviso.altimetry.fr/en/data/products'
                'auxiliary-products/global-tide-fes.html')
        elif (m == 'HAMTIDE11'):
            self.format = 'FES-netcdf'
            model_directory = {}
            model_directory['u'] = self.directory.joinpath('hamtide')
            model_directory['v'] = self.directory.joinpath('hamtide')
            model_files = ['HAMcurrent11a_2n.nc','HAMcurrent11a_k1.nc',
                'HAMcurrent11a_k2.nc','HAMcurrent11a_m2.nc',
                'HAMcurrent11a_n2.nc','HAMcurrent11a_o1.nc',
                'HAMcurrent11a_p1.nc','HAMcurrent11a_q1.nc',
                'HAMcurrent11a_s2.nc']
            self.model_file = {}
            for key, val in model_directory.items():
                self.model_directory = copy.copy(val)
                self.model_file[key] = self.pathfinder(model_files)
            self.constituents = [self.parse_file(f) for f in model_files]
            self.scale = 1.0
            self.version = 'HAMTIDE11'
            # model description and references
            self.reference = 'https://doi.org/10.1002/2013JC009766'
        else:
            raise ValueError(f"Unlisted tide model {m}")
        # return the model parameters
        self.validate_format()
        return self

    @property
    def gzip(self) -> str:
        """Returns suffix for gzip compression
        """
        return '.gz' if self.compressed else ''

    @property
    def suffix(self) -> str:
        """Returns format suffix for netCDF4 ATLAS files
        """
        if self.format in ('ATLAS-netcdf','GOT-netcdf'):
            return '.nc'
        elif self.format in ('GOT-ascii',):
            return '.d'
        else:
            return ''

    @property
    def atl03(self) -> str:
        """Returns ICESat-2 ATL03 attribute string for a given variable
        """
        if (self.type == 'z') and (self.variable == 'tide_ocean'):
            return 'tide_ocean'
        elif (self.type == 'z') and (self.variable == 'tide_load'):
            return 'tide_load'
        else:
            return None

    @property
    def atl06(self) -> str:
        """Returns ICESat-2 ATL06 attribute string for a given variable
        """
        if (self.type == 'z') and (self.variable == 'tide_ocean'):
            return 'tide_ocean'
        elif (self.type == 'z') and (self.variable == 'tide_load'):
            return 'tide_load'
        else:
            return None

    @property
    def atl07(self) -> str:
        """Returns ICESat-2 ATL07 attribute string for a given variable
        """
        if (self.type == 'z') and (self.variable == 'tide_ocean'):
            return 'height_segment_ocean'
        elif (self.type == 'z') and (self.variable == 'tide_load'):
            return 'height_segment_load'
        else:
            return None

    @property
    def atl10(self) -> str:
        """Returns ICESat-2 ATL07 attribute string for a given variable
        """
        if (self.type == 'z') and (self.variable == 'tide_ocean'):
            return 'height_segment_ocean'
        elif (self.type == 'z') and (self.variable == 'tide_load'):
            return 'height_segment_load'
        else:
            return None

    @property
    def atl11(self) -> str:
        """Returns ICESat-2 ATL11 attribute string for a given variable
        """
        if (self.type == 'z') and (self.variable == 'tide_ocean'):
            return 'tide_ocean'
        elif (self.type == 'z') and (self.variable == 'tide_load'):
            return 'tide_load'
        else:
            return None

    @property
    def atl12(self) -> str:
        """Returns ICESat-2 ATL12 attribute string for a given variable
        """
        if (self.type == 'z') and (self.variable == 'tide_ocean'):
            return 'tide_ocean_seg'
        elif (self.type == 'z') and (self.variable == 'tide_load'):
            return 'tide_load_seg'
        else:
            return None

    @property
    def gla12(self) -> str:
        """Returns ICESat GLA12 attribute string for a given variable
        """
        if (self.type == 'z') and (self.variable == 'tide_ocean'):
            return 'd_ocElv'
        elif (self.type == 'z') and (self.variable == 'tide_load'):
            return 'd_ldElv'
        else:
            return None

    @property
    def long_name(self) -> str:
        """Returns ``long_name`` attribute string for a given variable
        """
        if (self.type == 'z') and (self.variable == 'tide_ocean'):
            return 'ocean_tide_elevation'
        elif (self.type == 'z') and (self.variable == 'tide_load'):
            return 'load_tide_elevation'
        elif (self.type == ['u','v']):
            return dict(u='zonal_tidal_current', v='meridional_tidal_current')
        else:
            return None

    @property
    def description(self) -> str:
        """Returns ``description`` attribute string for a given variable
        """
        if (self.type == 'z') and (self.variable == 'tide_ocean'):
            return "Ocean tidal elevations derived from harmonic constants"
        elif (self.type == 'z') and (self.variable == 'tide_load'):
            return ("Local displacement due to ocean tidal loading "
                "derived from harmonic constants")
        elif (self.type == ['u','v']):
            attr = {}
            attr['u'] = ('Depth-averaged tidal zonal current '
                'derived from harmonic constants')
            attr['v'] = ('Depth-averaged tidal meridional current '
                'derived from harmonic constants')
            return attr
        else:
            return None

    @staticmethod
    def formats() -> list:
        """
        Returns list of known model formats
        """
        return ['OTIS','ATLAS-compact','TMD3','ATLAS-netcdf',
            'GOT-ascii','GOT-netcdf','FES-ascii','FES-netcdf']

    @staticmethod
    def global_ocean() -> list:
        """
        Returns list of global ocean tide elevation models
        """
        return ['TPXO9-atlas','TPXO9-atlas-v2','TPXO9-atlas-v3',
            'TPXO9-atlas-v4','TPXO9-atlas-v5','TPXO9.1','TPXO8-atlas',
            'TPXO7.2','GOT4.7','GOT4.8','GOT4.10','GOT5.5',
            'FES2014','FES2022','EOT20','HAMTIDE11']

    @staticmethod
    def global_load() -> list:
        """
        Returns list of global load tide elevation models
        """
        return ['TPXO7.2_load','GOT4.7_load','GOT4.8_load','GOT5.5_load',
            'GOT4.10_load','FES2014_load','FES2022_load','EOT20_load']

    @staticmethod
    def global_current() -> list:
        """
        Returns list of global tidal current models
        """
        return ['TPXO9-atlas','TPXO9-atlas-v2',
            'TPXO9-atlas-v3','TPXO9-atlas-v4','TPXO9-atlas-v5',
            'TPXO9.1','TPXO8-atlas','TPXO7.2','FES2014','HAMTIDE11']

    @staticmethod
    def antarctic_ocean() -> list:
        """
        Returns list of Antarctic ocean tide elevation models
        """
        return ['CATS0201','CATS2008','CATS2008-v2023']

    @staticmethod
    def antarctic_load() -> list:
        """
        Returns list of Antarctic load tide elevation models
        """
        return ['CATS2008_load']

    @staticmethod
    def antarctic_current() -> list:
        """
        Returns list of Antarctic tidal current models
        """
        return ['CATS0201','CATS2008','CATS2008-v2023']

    @staticmethod
    def arctic_ocean() -> list:
        """
        Returns list of Arctic ocean tide elevation models
        """
        return ['AODTM-5','AOTIM-5','AOTIM-5-2018','Arc2kmTM',
            'Gr1kmTM','Gr1km-v2']

    @staticmethod
    def arctic_load() -> list:
        """
        Returns list of Arctic load tide elevation models
        """
        return []

    @staticmethod
    def arctic_current() -> list:
        """
        Returns list of Arctic tidal current models
        """
        return ['AODTM-5','AOTIM-5','AOTIM-5-2018','Arc2kmTM',
            'Gr1kmTM','Gr1km-v2']

    @staticmethod
    def ocean_elevation() -> list:
        """
        Returns list of ocean tide elevation models
        """
        return ['CATS0201','CATS2008','CATS2008-v2023','TPXO9-atlas',
            'TPXO9-atlas-v2','TPXO9-atlas-v3','TPXO9-atlas-v4',
            'TPXO9-atlas-v5','TPXO9.1','TPXO8-atlas','TPXO7.2',
            'AODTM-5','AOTIM-5','AOTIM-5-2018','Arc2kmTM','Gr1kmTM',
            'Gr1km-v2','GOT4.7','GOT4.8','GOT4.10','GOT5.5',
            'FES2014','FES2022','EOT20','HAMTIDE11']

    @staticmethod
    def load_elevation() -> list:
        """
        Returns list of load tide elevation models
        """
        return ['CATS2008_load','TPXO7.2_load','GOT4.7_load',
            'GOT4.8_load','GOT4.10_load','GOT5.5_load',
            'FES2014_load','FES2022_load','EOT20_load']

    @staticmethod
    def ocean_current() -> list:
        """
        Returns list of tidal current models
        """
        return ['CATS0201','CATS2008','CATS2008-v2023','TPXO9-atlas',
            'TPXO9-atlas-v2','TPXO9-atlas-v3','TPXO9-atlas-v4',
            'TPXO9-atlas-v5','TPXO9.1','TPXO8-atlas','TPXO7.2',
            'AODTM-5','AOTIM-5','AOTIM-5-2018',
            'Arc2kmTM','Gr1kmTM','Gr1km-v2','FES2014','HAMTIDE11']

    @staticmethod
    def OTIS() -> list:
        """
        Returns list of OTIS format models
        """
        return ['CATS0201','CATS2008','CATS2008_load','TPXO9.1',
            'TPXO7.2','TPXO7.2_load','AODTM-5','AOTIM-5',
            'AOTIM-5-2018','Arc2kmTM','Gr1kmTM','Gr1km-v2']

    @staticmethod
    def ATLAS_compact() -> list:
        """
        Returns list of ATLAS compact format models
        """
        return ['TPXO8-atlas']

    @staticmethod
    def TMD3() -> list:
        """
        Returns list of TMD3 format models
        """
        return ['CATS2008-v2023']

    @staticmethod
    def ATLAS() -> list:
        """
        Returns list of ATLAS format models
        """
        return ['TPXO9-atlas','TPXO9-atlas-v2','TPXO9-atlas-v3',
            'TPXO9-atlas-v4','TPXO9-atlas-v5']

    @staticmethod
    def GOT() -> list:
        """
        Returns list of GOT format models
        """
        return ['GOT4.7','GOT4.7_load','GOT4.8','GOT4.8_load',
            'GOT4.10','GOT4.10_load','GOT5.5','GOT5.5_load']

    @staticmethod
    def FES() -> list:
        """
        Returns list of FES format models
        """
        return ['FES2014','FES2014_load','FES2022','FES2022_load',
            'EOT20','EOT20_load','HAMTIDE11']

    def pathfinder(self, model_file: str | pathlib.Path | list):
        """
        Completes file paths and appends file and gzip suffixes

        Parameters
        ----------
        model_file: str, pathlib.Path or list
            model file(s) to complete
        """
        # set working data directory if unset
        if self.directory is None:
            self.directory = pathlib.Path().absolute()
        # complete model file paths
        if isinstance(model_file, list):
            output_file = [self.pathfinder(f) for f in model_file]
            valid = all([f.exists() for f in output_file])
        elif isinstance(model_file, str):
            output_file = self.model_directory.joinpath(
                ''.join([model_file, self.suffix, self.gzip]))
            valid = output_file.exists()
        # check that (all) output files exist
        if self.verify and not valid:
            raise FileNotFoundError(output_file)
        # return the complete output path
        return output_file

    def from_file(self,
            definition_file: str | pathlib.Path | io.IOBase,
            format: str = 'auto'
        ):
        """
        Create a model object from an input definition file

        Parameters
        ----------
        definition_file: str, pathlib.Path or io.IOBase
            model definition file for creating model object
        format: str, default 'json'
            format of the input definition file

                - ``'ascii'``: tab-delimited definition file
                - ``'json'``: JSON formatted definition file
                - ``'auto'``: attempt to auto-detect format
        """
        # Opening definition file and assigning file ID number
        if isinstance(definition_file, io.IOBase):
            fid = copy.copy(definition_file)
        else:
            definition_file = pathlib.Path(definition_file).expanduser()
            fid = definition_file.open(mode="r", encoding='utf8')
        # load and parse definition file type
        if (format.lower() == 'ascii'):
            self._parse_file(fid)
        elif (format.lower() == 'json'):
            self._parse_json(fid)
        elif (format.lower() == 'auto'):
            self._parse_file(fid)
        # close the definition file
        fid.close()
        # return the model object
        return self

    def _parse_file(self, fid: io.IOBase):
        """
        Load and parse a model definition file

        Parameters
        ----------
        fid: io.IOBase
            open definition file object
        """
        # attempt to read and parse a JSON file
        try:
            self._parse_json(fid)
        except json.decoder.JSONDecodeError as exc:
            pass
        else:
            return self
        # rewind the definition file
        fid.seek(0)
        # attempt to read and parse an ascii file
        try:
            self._parse_ascii(fid)
        except Exception as exc:
            pass
        else:
            return self
        # raise an exception
        raise IOError('Cannot load model definition file')

    def _parse_ascii(self, fid: io.IOBase):
        """
        Load and parse tab-delimited definition file

        Parameters
        ----------
        fid: io.IOBase
            open definition file object
        """
        # variable with parameter definitions
        parameters = {}
        # for each line in the file will extract the parameter (name and value)
        for fileline in fid:
            # Splitting the input line between parameter name and value
            part = fileline.rstrip().split(maxsplit=1)
            # filling the parameter definition variable
            parameters[part[0]] = part[1]
        # convert from dictionary to model variable
        temp = self.from_dict(parameters)
        # verify model name, format and type
        assert temp.name
        temp.validate_format()
        assert temp.type
        assert temp.model_file
        # split type into list if currents (u,v)
        if re.search(r'[\s\,]+', temp.type):
            temp.type = re.split(r'[\s\,]+', temp.type)
        # split constituents into list if delimited-string
        if isinstance(temp.constituents, str) and \
            re.search(r'[\s\,]+', temp.constituents):
            temp.constituents = re.split(r'[\s\,]+', temp.constituents)
        # split model file into list if an ATLAS, GOT or FES file
        # model files can be comma, tab or space delimited
        # extract full path to tide model files
        # extract full path to tide grid file
        if temp.format in ('OTIS','ATLAS-compact','TMD3'):
            assert temp.grid_file
            # check if grid file is relative
            if (temp.directory is not None):
                temp.grid_file = temp.directory.joinpath(temp.grid_file).resolve()
            else:
                temp.grid_file = pathlib.Path(temp.grid_file).expanduser()
            # check if model files are as a delimited string
            multi_file = re.search(r'[\s\,]+', temp.model_file)
            # extract model files
            if (temp.type == ['u','v']) and multi_file:
                model_file = [pathlib.Path(f).expanduser() for f in
                    re.split(r'[\s\,]+', temp.model_file)]
                # copy to model file and directory dictionaries
                temp.model_file = dict(u=model_file, v=model_file)
                temp.model_directory = temp.model_file['u'][0].parent
            elif (temp.type == 'z') and multi_file:
                temp.model_file = [pathlib.Path(f).expanduser() for f in
                    re.split(r'[\s\,]+', temp.model_file)]
                temp.model_directory = temp.model_file[0].parent
            elif (temp.type == ['u','v']) and (temp.directory is not None):
                # use glob strings to find files in directory
                glob_string = copy.copy(temp.model_file)
                model_file = []
                # search singular glob string or iterable glob strings
                for p in re.split(r'[\s\,]+', temp.model_file):
                    model_file.extend(temp.directory.glob(p))
                # update model file
                temp.model_file = dict(u=model_file, v=model_file)
                # attempt to extract model directory
                try:
                    temp.model_directory = temp.model_file['u'][0].parent
                except (IndexError, AttributeError) as exc:
                    message = f'No model files found with {glob_string}'
                    raise FileNotFoundError(message) from exc
            elif (temp.type == 'z') and (temp.directory is not None):
                # use glob strings to find files in directory
                glob_string = copy.copy(temp.model_file)
                temp.model_file = []
                # search singular glob string or iterable glob strings
                for p in re.split(r'[\s\,]+', glob_string):
                    temp.model_file.extend(temp.directory.glob(p))
                # attempt to extract model directory
                try:
                    temp.model_directory = temp.model_file[0].parent
                except (IndexError, AttributeError) as exc:
                    message = f'No model files found with {glob_string}'
                    raise FileNotFoundError(message) from exc
            else:
                # fully defined single file case
                temp.model_file = pathlib.Path(temp.model_file).expanduser()
                temp.model_directory = temp.model_file.parent
        elif temp.format in ('ATLAS-netcdf',):
            assert temp.grid_file
            # check if grid file is relative
            if (temp.directory is not None):
                temp.grid_file = temp.directory.joinpath(temp.grid_file).resolve()
            else:
                temp.grid_file = pathlib.Path(temp.grid_file).expanduser()
            # extract model files
            if (temp.type == ['u','v']) and (temp.directory is not None):
                # split model file string at semicolon
                glob_string = temp.model_file.split(';')
                # use glob strings to find files in directory
                temp.model_file = {}
                temp.model_file['u'] = []
                temp.model_file['v'] = []
                # search singular glob string or iterable glob strings
                for p in re.split(r'[\s\,]+', glob_string[0]):
                    temp.model_file['u'].extend(temp.directory.glob(p))
                for p in re.split(r'[\s\,]+', glob_string[1]):
                    temp.model_file['v'].extend(temp.directory.glob(p))
                # attempt to extract model directory
                try:
                    temp.model_directory = temp.model_file['u'][0].parent
                except (IndexError, AttributeError) as exc:
                    message = f'No model files found with {glob_string}'
                    raise FileNotFoundError(message) from exc
            elif (temp.type == 'z') and (temp.directory is not None):
                # use glob strings to find files in directory
                glob_string = copy.copy(temp.model_file)
                temp.model_file = []
                # search singular glob string or iterable glob strings
                for p in re.split(r'[\s\,]+', glob_string):
                    temp.model_file.extend(temp.directory.glob(p))
                # attempt to extract model directory
                try:
                    temp.model_directory = temp.model_file[0].parent
                except (IndexError, AttributeError) as exc:
                    message = f'No model files found with {glob_string}'
                    raise FileNotFoundError(message) from exc
            elif (temp.type == ['u','v']):
                # split model file string at semicolon
                model_file = temp.model_file.split(';')
                # split model into list of files for each direction
                temp.model_file = {}
                temp.model_file['u'] = [pathlib.Path(f).expanduser() for f in
                    re.split(r'[\s\,]+', model_file[0])]
                temp.model_file['v'] = [pathlib.Path(f).expanduser() for f in
                    re.split(r'[\s\,]+', model_file[1])]
                # copy to directory dictionaries
                temp.model_directory = temp.model_file['u'][0].parent
            elif (temp.type == 'z'):
                temp.model_file = [pathlib.Path(f).expanduser() for f in
                    re.split(r'[\s\,]+', temp.model_file)]
                temp.model_directory = temp.model_file[0].parent
        elif temp.format in ('FES-ascii','FES-netcdf','GOT-ascii','GOT-netcdf'):
            # extract model files
            if (temp.type == ['u','v']) and (temp.directory is not None):
                # split model file string at semicolon
                glob_string = temp.model_file.split(';')
                # use glob strings to find files in directory
                temp.model_file = {}
                temp.model_file['u'] = []
                temp.model_file['v'] = []
                # search singular glob string or iterable glob strings
                for p in re.split(r'[\s\,]+', glob_string[0]):
                    temp.model_file['u'].extend(temp.directory.glob(p))
                for p in re.split(r'[\s\,]+', glob_string[1]):
                    temp.model_file['v'].extend(temp.directory.glob(p))
                # build model directory dictionaries
                temp.model_directory = {}
                for key, val in temp.model_file.items():
                    # attempt to extract model directory
                    try:
                        temp.model_directory[key] = val[0].parent
                    except (IndexError, AttributeError) as exc:
                        message = f'No model files found with {glob_string[key]}'
                        raise FileNotFoundError(message) from exc
            elif (temp.type == 'z') and (temp.directory is not None):
                # use glob strings to find files in directory
                glob_string = copy.copy(temp.model_file)
                temp.model_file = []
                # search singular glob string or iterable glob strings
                for p in re.split(r'[\s\,]+', glob_string):
                    temp.model_file.extend(temp.directory.glob(p))
                # build model directory
                temp.model_directory = temp.model_file[0].parent
                # attempt to extract model directory
                try:
                    temp.model_directory = temp.model_file[0].parent
                except (IndexError, AttributeError) as exc:
                    message = f'No model files found with {glob_string}'
                    raise FileNotFoundError(message) from exc
            elif (temp.type == ['u','v']):
                # split model file string at semicolon
                model_file = temp.model_file.split(';')
                # split model into list of files for each direction
                temp.model_file = {}
                temp.model_file['u'] = [pathlib.Path(f).expanduser() for f in
                    re.split(r'[\s\,]+', model_file[0])]
                temp.model_file['v'] = [pathlib.Path(f).expanduser() for f in
                    re.split(r'[\s\,]+', model_file[1])]
                # build model directory dictionaries
                temp.model_directory = {}
                for key, val in temp.model_file.items():
                    temp.model_directory[key] = val[0].parent
            elif (temp.type == 'z'):
                temp.model_file = [pathlib.Path(f).expanduser() for f in
                    re.split(r'[\s\,]+', temp.model_file)]
                temp.model_directory = temp.model_file[0].parent
        # verify that projection attribute exists for projected models
        if temp.format in ('OTIS','ATLAS-compact','TMD3'):
            assert temp.projection
        # convert scale from string to float
        if temp.format in ('ATLAS-netcdf','GOT-ascii','GOT-netcdf','FES-ascii','FES-netcdf'):
            assert temp.scale
            temp.scale = float(temp.scale)
        # assert that FES model has a version
        # get model constituents from constituent files
        if temp.format in ('FES-ascii','FES-netcdf',):
            assert temp.version
            if (temp.constituents is None):
                temp.parse_constituents()
        # convert boolean strings
        if isinstance(temp.compressed, str):
            temp.compressed = self.to_bool(temp.compressed)
        # return the model parameters
        return temp

    def _parse_json(self, fid: io.IOBase):
        """
        Load and parse JSON definition file

        Parameters
        ----------
        fid: io.IOBase
            open definition file object
        """
        # load JSON file
        parameters = json.load(fid)
        # convert from dictionary to model variable
        temp = self.from_dict(parameters)
        # verify model name, format and type
        assert temp.name
        temp.validate_format()
        assert temp.type
        assert temp.model_file
        # split model file into list if an ATLAS, GOT or FES file
        # model files can be comma, tab or space delimited
        # extract full path to tide model files
        # extract full path to tide grid file
        if temp.format in ('OTIS','ATLAS-compact','TMD3'):
            assert temp.grid_file
            # check if grid file is relative
            if (temp.directory is not None):
                temp.grid_file = temp.directory.joinpath(temp.grid_file).resolve()
            else:
                temp.grid_file = pathlib.Path(temp.grid_file).expanduser()
            # extract model files
            if (temp.type == ['u','v']) and (temp.directory is not None):
                # use glob strings to find files in directory
                for key, glob_string in temp.model_file.items():
                    # search singular glob string or iterable glob strings
                    if isinstance(glob_string, str):
                        # singular glob string
                        temp.model_file[key] = list(temp.directory.glob(glob_string))
                    elif isinstance(glob_string, Iterable):
                        # iterable glob strings
                        temp.model_file[key] = []
                        for p in glob_string:
                            temp.model_file[key].extend(temp.directory.glob(p))
                # attempt to extract model directory
                try:
                    temp.model_directory = temp.model_file['u'][0].parent
                except (IndexError, AttributeError) as exc:
                    message = f'No model files found with {glob_string}'
                    raise FileNotFoundError(message) from exc
            elif (temp.type == 'z') and (temp.directory is not None):
                # use glob strings to find files in directory
                glob_string = copy.copy(temp.model_file)
                # search singular glob string or iterable glob strings
                if isinstance(glob_string, str):
                    # singular glob string
                    temp.model_file = list(temp.directory.glob(glob_string))
                elif isinstance(glob_string, Iterable):
                    # iterable glob strings
                    temp.model_file = []
                    for p in glob_string:
                        temp.model_file.extend(temp.directory.glob(p))
                # attempt to extract model directory
                try:
                    temp.model_directory = temp.model_file[0].parent
                except (IndexError, AttributeError) as exc:
                    message = f'No model files found with {glob_string}'
                    raise FileNotFoundError(message) from exc
            elif (temp.type == ['u','v']) and isinstance(temp.model_file, dict):
                # resolve paths to model files for each direction
                for key, model_file in temp.model_file.items():
                    temp.model_file[key] = [pathlib.Path(f).expanduser() for f in
                        model_file]
                # copy directory dictionaries
                temp.model_directory = temp.model_file['u'][0].parent
            elif (temp.type == 'z') and isinstance(temp.model_file, list):
                # resolve paths to model files
                temp.model_file = [pathlib.Path(f).expanduser() for f in
                    temp.model_file]
                temp.model_directory = temp.model_file[0].parent
            else:
                # fully defined single file case
                temp.model_file = pathlib.Path(temp.model_file).expanduser()
                temp.model_directory = temp.model_file.parent
        elif temp.format in ('ATLAS-netcdf',):
            assert temp.grid_file
            # check if grid file is relative
            if (temp.directory is not None):
                temp.grid_file = temp.directory.joinpath(temp.grid_file).resolve()
            else:
                temp.grid_file = pathlib.Path(temp.grid_file).expanduser()
            # extract model files
            if (temp.type == ['u','v']) and (temp.directory is not None):
                # use glob strings to find files in directory
                for key, glob_string in temp.model_file.items():
                    # search singular glob string or iterable glob strings
                    if isinstance(glob_string, str):
                        # singular glob string
                        temp.model_file[key] = list(temp.directory.glob(glob_string))
                    elif isinstance(glob_string, Iterable):
                        # iterable glob strings
                        temp.model_file[key] = []
                        for p in glob_string:
                            temp.model_file[key].extend(temp.directory.glob(p))
                # attempt to extract model directory
                try:
                    temp.model_directory = temp.model_file['u'][0].parent
                except (IndexError, AttributeError) as exc:
                    message = f'No model files found with {glob_string}'
                    raise FileNotFoundError(message) from exc
            elif (temp.type == 'z') and (temp.directory is not None):
                # use glob strings to find files in directory
                glob_string = copy.copy(temp.model_file)
                # search singular glob string or iterable glob strings
                if isinstance(glob_string, str):
                    # singular glob string
                    temp.model_file = list(temp.directory.glob(glob_string))
                elif isinstance(glob_string, Iterable):
                    # iterable glob strings
                    temp.model_file = []
                    for p in glob_string:
                        temp.model_file.extend(temp.directory.glob(p))
                # attempt to extract model directory
                try:
                    temp.model_directory = temp.model_file[0].parent
                except (IndexError, AttributeError) as exc:
                    message = f'No model files found with {glob_string}'
                    raise FileNotFoundError(message) from exc
            elif (temp.type == ['u','v']):
                # resolve paths to model files for each direction
                for key, model_file in temp.model_file.items():
                    temp.model_file[key] = [pathlib.Path(f).expanduser() for f in
                        model_file]
                # copy to directory dictionaries
                temp.model_directory = temp.model_file['u'][0].parent
            elif (temp.type == 'z'):
                # resolve paths to model files
                temp.model_file = [pathlib.Path(f).expanduser() for f in
                    temp.model_file]
                temp.model_directory = temp.model_file[0].parent
        elif temp.format in ('FES-ascii','FES-netcdf','GOT-ascii','GOT-netcdf'):
            # extract model files
            if (temp.type == ['u','v']) and (temp.directory is not None):
                # use glob strings to find files in directory
                for key, glob_string in temp.model_file.items():
                    # search singular glob string or iterable glob strings
                    if isinstance(glob_string, str):
                        # singular glob string
                        temp.model_file[key] = list(temp.directory.glob(glob_string))
                    elif isinstance(glob_string, Iterable):
                        # iterable glob strings
                        temp.model_file[key] = []
                        for p in glob_string:
                            temp.model_file[key].extend(temp.directory.glob(p))
                # build model directory dictionaries
                temp.model_directory = {}
                for key, val in temp.model_file.items():
                    # attempt to extract model directory
                    try:
                        temp.model_directory[key] = val[0].parent
                    except (IndexError, AttributeError) as exc:
                        message = f'No model files found with {glob_string[key]}'
                        raise FileNotFoundError(message) from exc
            elif (temp.type == 'z') and (temp.directory is not None):
                # use glob strings to find files in directory
                glob_string = copy.copy(temp.model_file)
                # search singular glob string or iterable glob strings
                if isinstance(glob_string, str):
                    # singular glob string
                    temp.model_file = list(temp.directory.glob(glob_string))
                elif isinstance(glob_string, Iterable):
                    # iterable glob strings
                    temp.model_file = []
                    for p in glob_string:
                        temp.model_file.extend(temp.directory.glob(p))
                # attempt to extract model directory
                try:
                    temp.model_directory = temp.model_file[0].parent
                except (IndexError, AttributeError) as exc:
                    message = f'No model files found with {glob_string}'
            elif (temp.type == ['u','v']):
                # resolve paths to model files for each direction
                for key, model_file in temp.model_file.items():
                    temp.model_file[key] = [pathlib.Path(f).expanduser() for f in
                        model_file]
                # build model directory dictionaries
                temp.model_directory = {}
                for key, val in temp.model_file.items():
                    temp.model_directory[key] = val[0].parent
            elif (temp.type == 'z'):
                # resolve paths to model files
                temp.model_file = [pathlib.Path(f).expanduser() for f in
                    temp.model_file]
                temp.model_directory = temp.model_file[0].parent
        # verify that projection attribute exists for projected models
        if temp.format in ('OTIS','ATLAS-compact','TMD3'):
            assert temp.projection
        # convert scale from string to float
        if temp.format in ('ATLAS-netcdf','GOT-ascii','GOT-netcdf','FES-ascii','FES-netcdf'):
            assert temp.scale
        # assert that FES model has a version
        # get model constituents from constituent files
        if temp.format in ('FES-ascii','FES-netcdf',):
            assert temp.version
            if (temp.constituents is None):
                temp.parse_constituents()
        # return the model parameters
        return temp

    def validate_format(self):
        """Asserts that the model format is a known type"""
        # known remapped cases
        mapping = [('ATLAS','ATLAS-compact'), ('netcdf','ATLAS-netcdf'),
            ('FES','FES-netcdf'), ('GOT','GOT-ascii')]
        # iterate over known remapped cases
        for m in mapping:
            # check if tide model is a remapped case
            if (self.format == m[0]):
                self.format = m[1]
        # assert that tide model is a known format
        assert self.format in self.formats()

    def from_dict(self, d: dict):
        """
        Create a model object from a python dictionary

        Parameters
        ----------
        d: dict
            Python dictionary for creating model object
        """
        for key, val in d.items():
            setattr(self, key, copy.copy(val))
        # return the model parameters
        return self

    def parse_constituents(self) -> list:
        """
        Parses tide model files for a list of model constituents
        """
        if isinstance(self.model_file, (str, pathlib.Path)):
            # single file elevation case
            self.constituents = [self.parse_file(self.model_file)]
        elif isinstance(self.model_file, list):
            # multiple file elevation case
            self.constituents = [self.parse_file(f) for f in self.model_file]
        elif isinstance(self.model_file, dict) and \
            isinstance(self.model_file['u'], (str, pathlib.Path)):
            # single file currents case
            self.constituents = [self.parse_file(self.model_file['u'])]
        elif isinstance(self.model_file, dict) and \
            isinstance(self.model_file['u'], list):
            # multiple file currents case
            self.constituents = [self.parse_file(f) for f in self.model_file['u']]
        # return the model parameters
        return self

    @staticmethod
    def parse_file(
            model_file: str | pathlib.Path,
            raise_error: bool = False
        ):
        """
        Parses a model file for a tidal constituent name

        Parameters
        ----------
        model_file: str or pathlib.Path
            Tide model file to parse
        raise_error: bool, default False
            Raise exception if constituent is not found in file name

        Returns
        -------
        constituent: str or list
            constituent name
        """
        # convert to pathlib.Path
        model_file = pathlib.Path(model_file)
        # try to parse the constituent name from the file name
        try:
            return pyTMD.io.constituents.parse(model_file.name)
        except ValueError:
            pass
        # if no constituent name is found
        if raise_error:
            raise ValueError(f'Constituent not found in file {model_file}')
        else:
            return None

    @staticmethod
    def to_bool(val: str) -> bool:
        """
        Converts strings of True/False to a boolean values

        Parameters
        ----------
        val: str
            string for converting to True/False
        """
        if val.lower() in ('y', 'yes', 't', 'true', '1'):
            return True
        elif val.lower() in ('n', 'no', 'f', 'false', '0'):
            return False
        else:
            raise ValueError(f'Invalid boolean string {val}')

    def __str__(self):
        """String representation of the ``io.model`` object
        """
        properties = ['pyTMD.io.model']
        properties.append(f"    name: {self.name}")
        return '\n'.join(properties)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)
