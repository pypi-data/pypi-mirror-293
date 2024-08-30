#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only
import os
import pathlib
from pylinuxauto.config import config
from pylinuxauto.remote.client import client
from pylinuxauto.remote.guard import guard_rpc
from pylinuxauto.remote.rpc_method import RpcMethods


@guard_rpc(os.path.splitext(pathlib.Path(__file__).name)[0])
def _rpc_gui_client(
        user=None,
        ip=None,
        password=None,
        auto_restart=False,
        project_abspath=None
):
    return client(ip=ip, port=config.RPC_PORT)


class RpcGui:

    def __init__(
            self,
            user,
            ip,
            password,
            project_abspath,
            auto_restart=False,
    ):
        self.user = user
        self.ip = ip
        self.password = password
        self.project_abspath = project_abspath
        self.auto_restart = auto_restart

    @property
    def rgui(self) -> RpcMethods:
        return _rpc_gui_client(
            user=self.user,
            ip=self.ip,
            password=self.password,
            auto_restart=self.auto_restart,
            project_abspath=self.project_abspath
        )


