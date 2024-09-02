from business.controller.base import GlobalState
from ctools import string_tools


def get_tmp_token():
  tmp_token = string_tools.get_uuid()
  GlobalState.tmp_token.append(tmp_token)
  return tmp_token


def remove_tmp_token(token: str):
  if token in GlobalState.tmp_token:
    GlobalState.tmp_token.remove(token)
