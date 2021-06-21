from unittest import mock
import pytest

from index import start

@mock.patch("index.create_table")
def test_is_coin_doesnt_exist(create_table):
  create_table.return_value = mock.Mock(True)
  with pytest.raises(KeyError, match="Uma das moedas passada é invalida ou inexistente"):
    start("USDT_BTC")

@mock.patch("index.start_monitoring")
@mock.patch("index.create_table")
def test_is_(create_table, start_monitoring):
  create_table.return_value = mock.Mock(True)
  start_monitoring.return_value = mock.Mock(True)
  assert start(["USDT_BTC"]) == "Programa finalizado"