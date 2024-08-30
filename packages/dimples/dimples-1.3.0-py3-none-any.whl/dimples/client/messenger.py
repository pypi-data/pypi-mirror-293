# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2019 Albert Moky
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
    Messenger for client
    ~~~~~~~~~~~~~~~~~~~~

    Transform and send message
"""

from typing import Optional, List

from dimples import EntityType, ID, EVERYONE
from dimples import Document
from dimples import Station
from dimples import Envelope, InstantMessage, ReliableMessage
from dimples import ContentType, ReceiptCommand, DocumentCommand

from ..common import HandshakeCommand, ReportCommand, LoginCommand
from ..common import CommonMessenger

from .network import ClientSession
from .archivist import ClientArchivist


class ClientMessenger(CommonMessenger):

    @property
    def session(self) -> ClientSession:
        sess = super().session
        assert isinstance(sess, ClientSession), 'session error: %s' % sess
        return sess

    async def handshake(self, session_key: Optional[str]):
        """ send handshake command to current station """
        session = self.session
        station = session.station
        srv_id = station.identifier
        if session_key is None:
            # first handshake
            facebook = self.facebook
            user = facebook.current_user
            assert user is not None, 'current user not found'
            meta = await user.meta
            visa = await user.visa
            if visa is None:
                self.warning(msg='user visa not found: %s' % user)
            else:
                # clone visa to update
                doc = Document.parse(document=visa.copy_dictionary())
                pri_key = await facebook.private_key_for_visa_signature(identifier=user.identifier)
                if doc is None or pri_key is None:
                    self.error(msg='should not happen, visa: %s, private key: %s' % (doc, pri_key))
                else:
                    # update visa
                    doc.set_property(key='sys', value={
                        'os': 'Linux',
                    })
                    if doc.sign(private_key=pri_key) is None:
                        self.error(msg='failed to sign visa: %s, private key: %s' % (doc, pri_key))
                    elif await facebook.save_document(document=doc):
                        self.info(msg='visa updated: %s' % doc)
                        visa = doc
                    else:
                        self.error(msg='failed to save visa: %s' % doc)
            env = Envelope.create(sender=user.identifier, receiver=srv_id)
            cmd = HandshakeCommand.start()
            # send first handshake command as broadcast message
            cmd.group = Station.EVERY
            # create instant message with meta & visa
            i_msg = InstantMessage.create(head=env, body=cmd)
            i_msg.set_map(key='meta', value=meta)
            i_msg.set_map(key='visa', value=visa)
            await self.send_instant_message(msg=i_msg, priority=-1)
        else:
            # handshake again
            cmd = HandshakeCommand.restart(session=session_key)
            await self.send_content(sender=None, receiver=srv_id, content=cmd, priority=-1)

    # Override
    async def handshake_success(self):
        # broadcast current documents after handshake success
        await self.broadcast_document()

    async def broadcast_document(self, updated: bool = False):
        """ broadcast meta & visa document to all stations """
        facebook = self.facebook
        user = facebook.current_user
        assert user is not None, 'current user not found'
        me = user.identifier
        meta = await user.meta
        visa = await user.visa
        assert visa is not None, 'visa not found: %s' % user
        command = DocumentCommand.response(identifier=me, meta=meta, document=visa)
        archivist = facebook.archivist
        assert isinstance(archivist, ClientArchivist), 'client archivist error: %s' % archivist
        #
        #  send to all contacts
        #
        contacts = await facebook.get_contacts(identifier=me)
        for item in contacts:
            if archivist.is_documents_respond_expired(identifier=item, force=updated):
                self.info(msg='sending visa to: %s' % item)
                await self.send_content(sender=me, receiver=item, content=command, priority=1)
            else:
                # response not expired yet
                self.debug(msg='document response not expired yet: %s => %s' % (me, item))
        #
        #  broadcast to everyone@everywhere
        #
        if archivist.is_documents_respond_expired(identifier=EVERYONE, force=updated):
            self.info(msg='sending visa to: %s' % EVERYONE)
            await self.send_content(sender=me, receiver=EVERYONE, content=command, priority=1)
        else:
            # response not expired yet
            self.debug(msg='document response not expired yet: %s => %s' % (me, EVERYONE))

    async def broadcast_login(self, sender: ID, user_agent: str):
        """ send login command to keep roaming """
        # get current station
        station = self.session.station
        assert sender.type != EntityType.STATION, 'station (%s) cannot login: %s' % (sender, station)
        # create login command
        command = LoginCommand(identifier=sender)
        command.agent = user_agent
        command.station = station
        # broadcast to everyone@everywhere
        await self.send_content(sender=sender, receiver=EVERYONE, content=command, priority=1)

    async def report_online(self, sender: ID = None):
        """ send report command to keep user online """
        command = ReportCommand(title=ReportCommand.ONLINE)
        await self.send_content(sender=sender, receiver=Station.ANY, content=command, priority=1)

    async def report_offline(self, sender: ID = None):
        """ Send report command to let user offline """
        command = ReportCommand(title=ReportCommand.OFFLINE)
        await self.send_content(sender=sender, receiver=Station.ANY, content=command, priority=1)

    # Override
    async def process_reliable_message(self, msg: ReliableMessage) -> List[ReliableMessage]:
        # call super
        responses = await super().process_reliable_message(msg=msg)
        if len(responses) == 0 and self._needs_receipt(msg=msg):
            current_user = self.facebook.current_user
            text = 'Message received.'
            res = ReceiptCommand.create(text=text, envelope=msg.envelope)
            env = Envelope.create(sender=current_user.identifier, receiver=msg.sender)
            i_msg = InstantMessage.create(head=env, body=res)
            s_msg = await self.encrypt_message(msg=i_msg)
            assert s_msg is not None, 'failed to encrypt message: %s -> %s' % (current_user, msg.sender)
            r_msg = await self.sign_message(msg=s_msg)
            assert r_msg is not None, 'failed to sign message: %s -> %s' % (current_user, msg.sender)
            responses = [r_msg]
        return responses

    # noinspection PyMethodMayBeStatic
    def _needs_receipt(self, msg: ReliableMessage) -> bool:
        if msg.type == ContentType.COMMAND:
            # filter for looping message (receipt for receipt)
            return False
        sender = msg.sender
        # receiver = msg.receiver
        # if sender.type == EntityType.STATION or sender.type == EntityType.BOT:
        #     if receiver.type == EntityType.STATION or receiver.type == EntityType.BOT:
        #         # message between bots
        #         return False
        if sender.type != EntityType.USER:  # and receiver.type != EntityType.USER:
            # message between bots
            return False
        # current_user = self.facebook.current_user
        # if receiver != current_user.identifier:
        #     # forward message
        #     return True
        # TODO: other condition?
        return True
