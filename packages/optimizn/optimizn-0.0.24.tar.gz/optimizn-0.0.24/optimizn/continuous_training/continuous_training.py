# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
import pickle
from datetime import datetime
import logging
from optimizn.utils import get_logger


class ContinuousTraining:
    def __init__(self, logger=None):
        self.init_time = datetime.now()
        self.init_secs = int(self.init_time.timestamp())
        if logger is None:
            self.logger = get_logger(f'{self.name}_logger')
        else:
            self.logger = logger

    def persist(self):
        # set name attribute, check for params attribute 
        self.name = self.__class__.__name__
        if not hasattr(self, 'params'):
            raise Exception(
                'All problem class instances must have a "params" attribute, '
                + 'which is an object that contains the input parameters '
                + 'to the problem class')

        create_folders(self.name)
        existing_obj = load_latest_pckl(
            "Data//" + self.name + "//DailyObj", self.logger)
        self.obj_changed = (existing_obj != self.params)
        if self.obj_changed or existing_obj is None:
            # Write the latest input object that has changed.
            f_name = "Data//" + self.name + "//DailyObj//" +\
                        str(self.init_secs) + ".obj"
            file1 = open(f_name, 'wb')
            pickle.dump(self.params, file1)
            self.logger.info("Wrote to DailyObj")
        # Write the optimization object.
        f_name = "Data//" + self.name + "//DailyOpt//" + str(self.init_secs)\
            + ".obj"
        file1 = open(f_name, 'wb')
        pickle.dump(self, file1)
        self.logger.info("Wrote to DailyOpt")

        # Now check if the current best is better than the global best
        existing_best = load_latest_pckl(
            "Data//" + self.name + "//GlobalOpt", self.logger)
        if existing_best is None or self.best_cost < existing_best.best_cost\
                or self.obj_changed:
            f_name = "Data//" + self.name + "//GlobalOpt//" +\
                        str(self.init_secs) + ".obj"
            file1 = open(f_name, 'wb')
            pickle.dump(self, file1)
            self.logger.info("Wrote to GlobalOpt")


def create_folders(name):
    if not os.path.exists("Data//"):
        os.mkdir("Data//")
    if not os.path.exists("Data//" + name + "//"):
        os.mkdir("Data//" + name + "//")
    if not os.path.exists("Data//" + name + "//DailyObj//"):
        os.mkdir("Data//" + name + "//DailyObj//")
    if not os.path.exists("Data//" + name + "//DailyOpt//"):
        os.mkdir("Data//" + name + "//DailyOpt//")
    if not os.path.exists("Data//" + name + "//GlobalOpt//"):
        os.mkdir("Data//" + name + "//GlobalOpt//")


def load_latest_pckl(path1="Data/DailyObj", logger=None):
    if not os.path.exists(path1):
        return None
    msh_files = os.listdir(path1)
    msh_files = [i for i in msh_files if not i.startswith('.')]
    msh_files = sorted(msh_files)
    if len(msh_files) > 0:
        latest_file = msh_files[len(msh_files)-1]
        filepath = path1 + "//" + latest_file
        if os.path.getsize(filepath) == 0:
            if logger is None:
                logger = logging.getLogger('optimizn_logger')
                logger.setLevel(logging.INFO)
            logger.info('File located at', filepath, 'is empty')
        else:
            filehandler = open(filepath, 'rb')
            existing_obj = pickle.load(filehandler)
            return existing_obj
    return None
