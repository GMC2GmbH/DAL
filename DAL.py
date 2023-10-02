from ast import Try
from typing_extensions import Self
import yaml
import json
from TM1py.Services import TM1Service
from TM1py.Utils import Utils
from collections import namedtuple
from typing import overload
import os
import logging


""" Class DataAccessLayer manages all relevant pull and push requests """


class DataAccessLayer:

    __version__ = 'V0.13'
    __author__ = 'Alexander Gusser'

    def __init__(self, path):
        with open(os.path.join(os.path.dirname(__file__), path)) as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)
            self.tm1 = _PlanningAnalytics(config=self.config)

    def show_config(self):
        print(self.config)

    def load_data_by_mdx(self, mdx, raw=False):
        """load cube data by mdx statement

        Args:
            mdx (string): the mdx statement should contain all the needed parts -> SELECT [...] on ROWS, [...] on COLUMNS, FROM [...] WHERE([..]).
            raw (bool, optional): Determine return value neither as raw cellset data or as pandas.DataFrame.

        Returns:
            pandas.DataFrame: Two-dimensional, size-mutable, potentially heterogeneous tabular data.
        """

        return self.tm1.data_by_mdx(mdx, raw)

    def load_data_by_view(self, cube, view, raw=False):
        """load cube data by view

        Args:
            cube (string): name of the corresponding cube
            view (string): name of the cube view

        Returns:
            pandas.DataFrame: Two-dimensional, size-mutable, potentially heterogeneous tabular data.
        """

        return self.tm1.data_by_view(cube, view, raw)

    def write_cellset(self, cube, cellset):
        self.tm1.write_cellset(cube, cellset)
        
    def write_dataframe(self, cube, dataframe):
        self.tm1.write_dataframe(cube, dataframe)
        
    def run_ti(self, name, parameters=None):
        self.tm1.run_ti(name,parameters)


""" _PlanningAnalytics is an internal class with the purpose of establishing communication between Python and Planning Analytics """

class _PlanningAnalytics:

    __version__ = 'V0.1'
    __author__ = 'Alexander Gusser, Johannes Droste, Stefan Breuer'

    def __init__(self, config):
        # get and set config!
        self.config = namedtuple("Config", config["planning_analytics"].keys())(
            *config["planning_analytics"].values())

        # Check the connection!
        self.check_connection()

    def _get_service(self):
        """returns the TM1Service

        Returns:
            TM1py.Services: to establish the connection!
        """
        return TM1Service(**dict(self.config._asdict()))

    def check_connection(self):
        try:
            with self._get_service() as tm1:
                server = tm1.server.get_configuration()
                # log
                logging.info(f'connection {server["ServerName"]} [V{server["ProductVersion"]}] is established!')
        except Exception as e:
            logging.error(f'error: {str(e)}')

    def data_by_mdx(self, mdx, raw=False):
        """load planning analytics cube cells by mdx statement

        Args:
            mdx (String): mdx statement with all necessary information
        """
        with self._get_service() as tm1:
            # Get data from cube through MDX
            data = tm1.cubes.cells.execute_mdx(mdx)

            if(raw):
                # return raw cellset data
                return data
            else:
                # Build pandas DataFrame from raw cellset data
                return Utils.build_pandas_dataframe_from_cellset(data)

    def data_by_view(self, cube, view, raw=False):
        with self._get_service() as tm1:
            # Get data from cube through View
            data = tm1.cubes.cells.execute_view(cube, view, private=False)

            if(raw):
                # return raw cellset data
                return data
            else:
                # Build pandas DataFrame from raw cellset data
                return Utils.build_pandas_dataframe_from_cellset(data)

    def write_dataframe(self, cube, dataframe):
        try:
            with self._get_service() as tm1: 
                # write new values
                tm1.cubes.cells.write_dataframe(cube_name=cube, data=dataframe, use_ti=True)
                # log
                logging.info(f'dataframe in {cube} are stored!')
        except Exception as e:
            logging.error(f'error: {str(e)}')
            
    def write_cellset(self, cube, cellset):
        try:
            with self._get_service() as tm1:
                # write new values
                tm1.cubes.cells.write_values(cube_name=cube, cellset_as_dict=cellset)
                # log
                logging.info(f'cellset in {cube} are stored!')
        except Exception as e:
            logging.error(f'error: {str(e)}')
    
    def run_ti(self, name,parameters=None):
        try:
            with self._get_service() as tm1:
                #get process
                process =  tm1.processes.get(name_process=name)
                # write new values
                sucess, status, error_log_file = tm1.processes.execute_process_with_return(process,**parameters)
                # log
                logging.info(f'process {name} executed! {sucess} | {status}')
        except Exception as e:
            logging.error(f'error: {str(e)}')
