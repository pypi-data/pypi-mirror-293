# -*- coding: utf-8 -*-
#
#   Ming-Ke-Ming : Decentralized User Identity Authentication
#
#                                Written in 2023 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2023 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

from dimsdk import ID, Meta, MetaType

from .network import NetworkType, network_to_type
from .entity import EntityID, EntityIDFactory

from .btc import CompatibleBTCAddress

from .meta import CompatibleDefaultMeta, CompatibleBTCMeta, CompatibleMetaFactory

from .compatible import patch
# from .compatible import patch_meta, patch_cmd
from .compatible import fix_meta_attachment, fix_meta_version
from .compatible import fix_cmd, fix_command
from .compatible import fix_receipt_command, fix_document_command, fix_report_command


patch()


def register_compatible_factories():
    # ID
    ID.register(factory=EntityIDFactory())
    # meta
    Meta.register(version=MetaType.MKM, factory=CompatibleMetaFactory(version=MetaType.MKM))
    Meta.register(version=MetaType.BTC, factory=CompatibleMetaFactory(version=MetaType.BTC))
    Meta.register(version=MetaType.ExBTC, factory=CompatibleMetaFactory(version=MetaType.ExBTC))


__all__ = [

    'NetworkType', 'network_to_type',
    'EntityID', 'EntityIDFactory',

    'CompatibleBTCAddress',

    'CompatibleDefaultMeta', 'CompatibleBTCMeta', 'CompatibleMetaFactory',

    'register_compatible_factories',

    'fix_meta_version', 'fix_meta_attachment',
    'fix_cmd', 'fix_command',
    'fix_receipt_command', 'fix_document_command', 'fix_report_command',

]
