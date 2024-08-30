# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2021 Albert Moky
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
    Server extensions for MessageProcessor
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from typing import Optional, Union, List, Dict

from dimsdk import EntityType, ID, ANYONE, EVERYONE
from dimsdk import Station
from dimsdk import InstantMessage, ReliableMessage
from dimsdk import Envelope
from dimsdk import Content, ContentType, Command
from dimsdk import TextContent, ReceiptCommand
from dimsdk import ContentProcessor, ContentProcessorCreator

from dimsdk.cpu import BaseContentProcessor, BaseContentProcessorCreator

from ..common import HandshakeCommand, LoginCommand
from ..common import ReportCommand, AnsCommand
from ..common import CommonFacebook, CommonMessenger
from ..common import CommonMessagePacker
from ..common import CommonMessageProcessor

from .cpu import HandshakeCommandProcessor
from .cpu import LoginCommandProcessor
from .cpu import ReportCommandProcessor
from .cpu import AnsCommandProcessor

from .cpu import DocumentCommandProcessor

from .packer import FilterManager
from .dispatcher import Dispatcher


class ServerMessageProcessor(CommonMessageProcessor):

    @property
    def messenger(self) -> CommonMessenger:
        transceiver = super().messenger
        assert isinstance(transceiver, CommonMessenger), 'messenger error: %s' % transceiver
        return transceiver

    @property
    def facebook(self) -> CommonFacebook:
        barrack = super().facebook
        assert isinstance(barrack, CommonFacebook), 'facebook error: %s' % barrack
        return barrack

    # protected
    # noinspection PyMethodMayBeStatic
    async def is_blocked(self, msg: ReliableMessage) -> bool:
        block_filter = FilterManager().block_filter
        return await block_filter.is_blocked(msg=msg)

    def _suspend_reliable_message(self, msg: ReliableMessage, error: Dict):
        packer = self.messenger.packer
        assert isinstance(packer, CommonMessagePacker), 'message packer error: %s' % packer
        packer.suspend_reliable_message(msg=msg, error=error)

    # Override
    async def process_reliable_message(self, msg: ReliableMessage) -> List[ReliableMessage]:
        # check block list
        if await self.is_blocked(msg=msg):
            self.warning(msg='user is blocked: %s -> %s (group: %s)' % (msg.sender, msg.receiver, msg.group))
            return []
        messenger = self.messenger
        session = messenger.session
        current = self.facebook.current_user
        station = current.identifier
        receiver = msg.receiver
        # 0. verify message
        s_msg = await messenger.verify_message(msg=msg)
        if s_msg is None:
            # TODO: suspend and waiting for sender's meta if not exists
            return []
        # 1. check receiver
        if receiver == station:
            # message to this station
            # maybe a meta command, document command, etc ...
            pass
        elif receiver == Station.ANY or receiver == ANYONE:
            # if receiver == 'station@anywhere':
            #     it must be the first handshake without station ID;
            # if receiver == 'anyone@anywhere':
            #     it should be other plain message without encryption.
            pass
        else:
            # message not for this station, check session for delivering
            if session.identifier is None or not session.active:
                # not login?
                # 1.1. suspend this message for waiting handshake
                error = {
                    'message': 'user not login',
                }
                self._suspend_reliable_message(msg=msg, error=error)
                # 1.2. ask client to handshake again (with session key)
                # this message won't be delivered before handshake accepted
                return await self._force_handshake(msg=msg)
            # session is active and user login success
            # if sender == session.ID,
            #   we can trust this message an no need to verify it;
            # else if sender is a neighbor station,
            #   we can trust it too;
            if receiver == Station.EVERY or receiver == EVERYONE:
                # broadcast message (to neighbor stations)
                # e.g.: 'stations@everywhere', 'everyone@everywhere'
                await self._broadcast_message(msg=msg, station=station)
                # if receiver == 'everyone@everywhere':
                #     broadcast message to all destinations,
                #     current station is it's receiver too.
            elif receiver.is_broadcast:
                # broadcast message (to station bots)
                # e.g.: 'archivist@anywhere', 'announcer@anywhere', 'monitor@anywhere', ...
                await self._broadcast_message(msg=msg, station=station)
                return []
            elif receiver.is_group:
                # encrypted group messages should be sent to the group assistant,
                # the station will never process these messages.
                await self._split_group_message(msg=msg, station=station)
                return []
            else:
                # this message is not for current station,
                # deliver to the real receiver and respond to sender
                return await self._deliver_message(msg=msg)
        # 2. process message
        responses = await messenger.process_secure_message(msg=s_msg, r_msg=msg)
        if len(responses) == 0:
            # nothing to respond
            return []
        # 3. sign message
        messages = []
        for res in responses:
            signed = await messenger.sign_message(msg=res)
            if signed is not None:
                messages.append(signed)
        return messages
        # TODO: override to deliver to the receiver when catch exception "receiver error ..."

    async def _force_handshake(self, msg: ReliableMessage) -> List[ReliableMessage]:
        session = self.messenger.session
        sess_id = session.identifier
        current = self.facebook.current_user
        sid = current.identifier
        sender = msg.sender
        if sess_id is not None:
            assert sess_id == sender, 'sender error: %s, %s' % (sender, sess_id)
        # build 'handshake' command message
        command = HandshakeCommand.ask(session=session.key)
        command['force'] = True
        r_msg = await pack_message(content=command, sender=sid, receiver=sender, messenger=self.messenger)
        if r_msg is None:
            assert False, 'failed to send "handshake" command to: %s' % sender
        else:
            return [r_msg]

    async def _broadcast_message(self, msg: ReliableMessage, station: ID):
        """ broadcast message to actual recipients """
        sender = msg.sender
        receiver = msg.receiver
        assert receiver.is_broadcast, 'broadcast message error: %s -> %s' % (sender, receiver)
        self.info(msg='broadcast message %s -> %s (%s)' % (sender, receiver, msg.group))
        if receiver.is_user:
            # broadcast message to station bots
            # e.g.: 'archivist@anywhere', 'announcer@anywhere', 'monitor@anywhere', ...
            name = receiver.name
            assert name is not None and name != 'station' and name != 'anyone', 'receiver error: %s' % receiver
            bot = AnsCommandProcessor.ans_id(name=name)
            if bot is None:
                self.warning(msg='failed to get receiver: %s' % receiver)
                return False
            elif bot == sender:
                self.warning(msg='skip cycled message: %s -> %s' % (sender, receiver))
                return False
            elif bot == station:
                self.warning(msg='skip current station: %s -> %s' % (sender, receiver))
                return False
            else:
                self.info(msg='forward to bot: %s -> %s' % (name, bot))
                receiver = bot
        # deliver by dispatcher
        dispatcher = Dispatcher()
        await dispatcher.deliver_message(msg=msg, receiver=receiver)

    async def _split_group_message(self, msg: ReliableMessage, station: ID):
        """ redirect group message to assistant """
        sender = msg.sender
        receiver = msg.receiver
        self.error(msg='group message should not send to station: %s, %s -> %s' % (station, sender, receiver))

    async def _deliver_message(self, msg: ReliableMessage) -> List[ReliableMessage]:
        messenger = self.messenger
        current = self.facebook.current_user
        sid = current.identifier
        sender = msg.sender
        receiver = msg.receiver
        # deliver
        dispatcher = Dispatcher()
        responses = await dispatcher.deliver_message(msg=msg, receiver=receiver)
        assert len(responses) > 0, 'should not happen'
        messages = []
        for res in responses:
            r_msg = await pack_message(content=res, sender=sid, receiver=sender, messenger=messenger)
            if r_msg is None:
                assert False, 'failed to send respond to: %s' % sender
            else:
                messages.append(r_msg)
        return messages

    # Override
    async def process_content(self, content: Content, r_msg: ReliableMessage) -> List[Content]:
        # 0. process first
        responses = await super().process_content(content=content, r_msg=r_msg)
        messenger = self.messenger
        sender = r_msg.sender
        # 1. check login
        session = messenger.session
        if session.identifier is None:  # or not session.active:
            # not login yet, force to handshake again
            if not isinstance(content, HandshakeCommand):
                handshake = HandshakeCommand.ask(session=session.key)
                responses.insert(0, handshake)
        # 2. check response
        contents = []
        for res in responses:
            if res is None:
                # should not happen
                continue
            elif isinstance(res, ReceiptCommand):
                if sender.type == EntityType.STATION:
                    # no need to respond receipt to station
                    self.info(msg='drop receipt to %s, origin msg time=[%s]' % (sender, r_msg.time))
                    continue
            elif isinstance(res, TextContent):
                if sender.type == EntityType.STATION:
                    # no need to respond text message to station
                    self.info(msg='drop text to %s, origin time=[%s], text=%s' % (sender, r_msg.time, res.text))
                    continue
            contents.append(res)
        # OK
        return contents

    # Override
    def _create_creator(self) -> ContentProcessorCreator:
        return ServerContentProcessorCreator(facebook=self.facebook, messenger=self.messenger)


async def pack_message(content: Content, sender: ID, receiver: ID,
                       messenger: CommonMessenger) -> Optional[ReliableMessage]:
    envelope = Envelope.create(sender=sender, receiver=receiver)
    i_msg = InstantMessage.create(head=envelope, body=content)
    s_msg = await messenger.encrypt_message(msg=i_msg)
    if s_msg is not None:
        return await messenger.sign_message(msg=s_msg)


class ServerContentProcessorCreator(BaseContentProcessorCreator):

    # Override
    def create_content_processor(self, msg_type: Union[int, ContentType]) -> Optional[ContentProcessor]:
        # default
        if msg_type == 0:
            return BaseContentProcessor(facebook=self.facebook, messenger=self.messenger)
        # others
        return super().create_content_processor(msg_type=msg_type)

    # Override
    def create_command_processor(self, msg_type: Union[int, ContentType], cmd: str) -> Optional[ContentProcessor]:
        # document
        if cmd == Command.DOCUMENT:
            return DocumentCommandProcessor(facebook=self.facebook, messenger=self.messenger)
        # handshake
        if cmd == HandshakeCommand.HANDSHAKE:
            return HandshakeCommandProcessor(facebook=self.facebook, messenger=self.messenger)
        # login
        if cmd == LoginCommand.LOGIN:
            return LoginCommandProcessor(facebook=self.facebook, messenger=self.messenger)
        # report
        if cmd == ReportCommand.REPORT:
            return ReportCommandProcessor(facebook=self.facebook, messenger=self.messenger)
        # ans
        if cmd == AnsCommand.ANS:
            return AnsCommandProcessor(facebook=self.facebook, messenger=self.messenger)
        # others
        return super().create_command_processor(msg_type=msg_type, cmd=cmd)
