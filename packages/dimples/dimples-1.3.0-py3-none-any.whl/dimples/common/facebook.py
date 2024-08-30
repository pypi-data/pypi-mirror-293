# -*- coding: utf-8 -*-
#
#   DIM-SDK : Decentralized Instant Messaging Software Development Kit
#
#                                Written in 2022 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2022 Albert Moky
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

"""
    Common extensions for Facebook
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Barrack for cache entities
"""

from typing import Optional, List

from dimsdk import SignKey, DecryptKey
from dimsdk import ID, User
from dimsdk import Document, DocumentHelper
from dimsdk import Facebook

from ..utils import Logging

from .archivist import CommonArchivist
from .anonymous import Anonymous


class CommonFacebook(Facebook, Logging):

    def __init__(self):
        super().__init__()
        self.__current: Optional[User] = None
        self.__archivist = None

    @property
    def archivist(self) -> CommonArchivist:
        return self.__archivist

    @archivist.setter
    def archivist(self, db: CommonArchivist):
        self.__archivist = db

    #
    #   Super
    #

    @property  # Override
    async def local_users(self) -> List[User]:
        current = self.__current
        return [] if current is None else [current]

    @property
    def current_user(self) -> Optional[User]:
        """ Get current user (for signing and sending message) """
        return self.__current

    @current_user.setter
    def current_user(self, user: User):
        if user.data_source is None:
            user.data_source = self
        self.__current = user

    async def get_document(self, identifier: ID, doc_type: str = '*') -> Optional[Document]:
        all_documents = await self.get_documents(identifier=identifier)
        doc = DocumentHelper.last_document(all_documents, doc_type)
        # compatible for document type
        if doc is None and doc_type == Document.VISA:
            doc = DocumentHelper.last_document(all_documents, 'profile')
        return doc

    async def get_name(self, identifier: ID) -> str:
        if identifier.is_user:
            doc_type = Document.VISA
        elif identifier.is_group:
            doc_type = Document.BULLETIN
        else:
            doc_type = '*'
        # get name from document
        doc = await self.get_document(identifier=identifier, doc_type=doc_type)
        if doc is not None:
            name = doc.name
            if name is not None and len(name) > 0:
                return name
        # get name from ID
        return Anonymous.get_name(identifier=identifier)

    # # Override
    # async def save_meta(self, meta: Meta, identifier: ID) -> bool:
    #     # check valid
    #     if meta.valid and meta.match_identifier(identifier=identifier):
    #         pass
    #     else:
    #         # assert False, 'meta not valid: %s' % identifier
    #         return False
    #     # check old meta
    #     old = await self.get_meta(identifier=identifier)
    #     if old is not None:
    #         # assert meta == old, 'meta should not changed'
    #         return True
    #     # meta not exists yet, save it
    #     db = self.database
    #     return await db.save_meta(meta=meta, identifier=identifier)
    #
    # # Override
    # async def save_document(self, document: Document) -> bool:
    #     identifier = document.identifier
    #     if not document.valid:
    #         # try to verify
    #         meta = await self.get_meta(identifier=identifier)
    #         if meta is None:
    #             self.error(msg='meta not found: %s' % identifier)
    #             return False
    #         elif document.verify(public_key=meta.public_key):
    #             self.debug(msg='document verified: %s' % identifier)
    #         else:
    #             self.error(msg='failed to verify document: %s' % identifier)
    #             # assert False, 'document not valid: %s' % identifier
    #             return False
    #     doc_type = document.type
    #     if doc_type is None:
    #         doc_type = '*'
    #     # check old documents with type
    #     documents = await self.get_documents(identifier=identifier)
    #     old = DocumentHelper.last_document(documents, doc_type)
    #     if old is not None and DocumentHelper.is_expired(document, old):
    #         self.warning(msg='drop expired document: %s' % identifier)
    #         return False
    #     db = self.database
    #     return await db.save_document(document=document)
    #
    # #
    # #   EntityDataSource
    # #
    #
    # # Override
    # async def get_meta(self, identifier: ID) -> Optional[Meta]:
    #     # if identifier.is_broadcast:
    #     #     # broadcast ID has no meta
    #     #     return None
    #     db = self.database
    #     return await db.get_meta(identifier=identifier)
    #
    # # Override
    # async def get_documents(self, identifier: ID) -> List[Document]:
    #     # if identifier.is_broadcast:
    #     #     # broadcast ID has no documents
    #     #     return None
    #     db = self.database
    #     return await db.get_documents(identifier=identifier)

    #
    #   UserDataSource
    #

    # Override
    async def get_contacts(self, identifier: ID) -> List[ID]:
        db = self.archivist
        return await db.get_contacts(identifier)

    # Override
    async def private_keys_for_decryption(self, identifier: ID) -> List[DecryptKey]:
        db = self.archivist
        return await db.private_keys_for_decryption(identifier)

    # Override
    async def private_key_for_signature(self, identifier: ID) -> Optional[SignKey]:
        db = self.archivist
        return await db.private_key_for_signature(identifier)

    # Override
    async def private_key_for_visa_signature(self, identifier: ID) -> Optional[SignKey]:
        db = self.archivist
        return await db.private_key_for_visa_signature(identifier)

    # #
    # #    GroupDataSource
    # #
    #
    # # Override
    # async def get_founder(self, identifier: ID) -> Optional[ID]:
    #     db = self.database
    #     user = db.get_founder(group=identifier)
    #     if user is None:
    #         user = await super().get_founder(identifier=identifier)
    #     return user
    #
    # # Override
    # async def get_owner(self, identifier: ID) -> Optional[ID]:
    #     db = self.database
    #     user = db.get_owner(group=identifier)
    #     if user is None:
    #         user = await super().get_owner(identifier=identifier)
    #     return user
    #
    # # Override
    # async def get_members(self, identifier: ID) -> List[ID]:
    #     owner = await self.get_owner(identifier=identifier)
    #     if owner is None:
    #         # assert False, 'group owner not found: %s' % identifier
    #         return []
    #     db = self.database
    #     users = db.get_members(group=identifier)
    #     if len(users) == 0:
    #         users = await super().get_members(identifier=identifier)
    #         if len(users) == 0:
    #             users = [owner]
    #     assert owner == users[0], 'group owner must be the first member: %s, group: %s' % (owner, identifier)
    #     return users
    #
    # # Override
    # async def get_assistants(self, identifier: ID) -> List[ID]:
    #     db = self.database
    #     bots = db.get_assistants(group=identifier)
    #     if len(bots) == 0:
    #         bots = await super().assistants(identifier=identifier)
    #     return bots
