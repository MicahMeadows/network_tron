# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: message.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto


@dataclass
class Message(betterproto.Message):
    label: str = betterproto.string_field(1)
    body: str = betterproto.string_field(2)
