# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: game_state.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


# import player_dto_pb2 as player__dto__pb2
import src.common.proto_compiled.player_dto_pb2 as player__dto__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10game_state.proto\x12\ttron_game\x1a\x10player_dto.proto\"2\n\tGameState\x12%\n\x07players\x18\x01 \x03(\x0b\x32\x14.tron_game.PlayerDTOb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'game_state_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GAMESTATE._serialized_start=49
  _GAMESTATE._serialized_end=99
# @@protoc_insertion_point(module_scope)