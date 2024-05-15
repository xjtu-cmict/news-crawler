# -*- coding: utf-8 -*-
# @FileName: env_constant.py
import os


class EnvConstant:
    """
    常量类，保存使用的常量
    """
    # 项目路径
    PROJECT_PATH = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

    # 运行环境整体配置文件
    # 使用os.path获取绝对路径
    CONFIG_PATH = PROJECT_PATH + "/config/config.yaml"

    ENVIRONMENT = 'environment'

    # 日志配置文件
    LOG = 'log'
    LOG_PATH = 'log_path'
    LOG_FILE = 'log_file'
    LOG_ROTATION = 'log_rotation'
    LOG_RETENTION = 'log_retention'
    LOG_LEVEL = 'log_level'