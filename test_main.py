import subprocess
import sys
import unittest
from pathlib import Path


ARQUIVO_PRINCIPAL = Path(__file__).with_name("main.py")


def executar_programa(*entradas):
    dados = "\n".join(str(entrada) for entrada in entradas) + "\n"
    resultado = subprocess.run(
        [sys.executable, str(ARQUIVO_PRINCIPAL)],
        input=dados,
        text=True,
        capture_output=True,
        timeout=5,
    )
    if resultado.returncode != 0:
        raise AssertionError(resultado.stderr)
    return resultado.stdout


def verificar_saldos(teste, saida, conta1, conta2):
    teste.assertIn(f"Conta 1: R${conta1:.2f}", saida)
    teste.assertIn(f"Conta 2: R${conta2:.2f}", saida)


class TestSistemaBancario(unittest.TestCase):
    def test_ct01_saldos_iniciais_positivos(self):
        saida = executar_programa(1000, 500, 4)
        verificar_saldos(self, saida, 1000, 500)

    def test_ct02_saldos_iniciais_iguais_a_zero(self):
        saida = executar_programa(0, 0, 4)
        verificar_saldos(self, saida, 0, 0)

    def test_ct03_saldo_inicial_negativo(self):
        saida = executar_programa(-100, 100, 50, 4)
        self.assertIn("O saldo inicial não pode ser negativo.", saida)
        verificar_saldos(self, saida, 100, 50)

    def test_ct04_saldo_inicial_nao_numerico(self):
        saida = executar_programa("abc", 100, 50, 4)
        self.assertIn("Digite apenas números.", saida)
        verificar_saldos(self, saida, 100, 50)

    def test_ct05_saldos_iniciais_decimais(self):
        saida = executar_programa(100.50, 50.25, 4)
        verificar_saldos(self, saida, 100.50, 50.25)

    def test_ct06_deposito_na_conta_1(self):
        saida = executar_programa(100, 50, 1, 1, 30, 4)
        self.assertIn("Depósito de R$30.00 realizado.", saida)
        verificar_saldos(self, saida, 130, 50)

    def test_ct07_deposito_na_conta_2(self):
        saida = executar_programa(100, 50, 1, 2, 25, 4)
        verificar_saldos(self, saida, 100, 75)

    def test_ct08_deposito_decimal(self):
        saida = executar_programa(100, 50, 1, 1, 25.50, 4)
        verificar_saldos(self, saida, 125.50, 50)

    def test_ct09_deposito_igual_a_zero(self):
        saida = executar_programa(100, 50, 1, 1, 0, 4)
        self.assertIn("O valor do depósito deve ser maior que zero.", saida)
        verificar_saldos(self, saida, 100, 50)

    def test_ct10_deposito_negativo(self):
        saida = executar_programa(100, 50, 1, 1, -20, 4)
        self.assertIn("O valor do depósito deve ser maior que zero.", saida)
        verificar_saldos(self, saida, 100, 50)

    def test_ct11_deposito_nao_numerico(self):
        saida = executar_programa(100, 50, 1, 1, "vinte", 20, 4)
        self.assertIn("Digite apenas números.", saida)
        verificar_saldos(self, saida, 120, 50)

    def test_ct12_conta_inexistente_no_deposito(self):
        saida = executar_programa(100, 50, 1, 3, 20, 4)
        self.assertIn("Conta inválida.", saida)
        verificar_saldos(self, saida, 100, 50)

    def test_ct13_saque_valido_da_conta_1(self):
        saida = executar_programa(100, 50, 2, 1, 30, 4)
        self.assertIn("Saque de R$30.00 realizado.", saida)
        verificar_saldos(self, saida, 70, 50)

    def test_ct14_saque_valido_da_conta_2(self):
        saida = executar_programa(100, 100, 2, 2, 40, 4)
        verificar_saldos(self, saida, 100, 60)

    def test_ct15_saque_de_todo_o_saldo(self):
        saida = executar_programa(100, 50, 2, 1, 100, 4)
        verificar_saldos(self, saida, 0, 50)

    def test_ct16_saque_maior_que_o_saldo(self):
        saida = executar_programa(100, 50, 2, 1, 100.01, 4)
        self.assertIn("Saldo insuficiente.", saida)
        verificar_saldos(self, saida, 100, 50)

    def test_ct17_saque_em_conta_zerada(self):
        saida = executar_programa(0, 50, 2, 1, 10, 4)
        self.assertIn("Saldo insuficiente.", saida)
        verificar_saldos(self, saida, 0, 50)

    def test_ct18_saque_com_valores_invalidos(self):
        for valor in (0, -10):
            with self.subTest(valor=valor):
                saida = executar_programa(100, 50, 2, 1, valor, 4)
                self.assertIn("O valor do saque deve ser maior que zero.", saida)
                verificar_saldos(self, saida, 100, 50)

        saida = executar_programa(100, 50, 2, 1, "abc", 10, 4)
        self.assertIn("Digite apenas números.", saida)
        verificar_saldos(self, saida, 90, 50)

    def test_ct19_conta_inexistente_no_saque(self):
        saida = executar_programa(100, 50, 2, 5, 20, 4)
        self.assertIn("Conta inválida.", saida)
        verificar_saldos(self, saida, 100, 50)

    def test_ct20_transferencia_da_conta_1_para_a_2(self):
        saida = executar_programa(100, 50, 3, 1, 30, 4)
        self.assertIn("Transferência de R$30.00 realizada.", saida)
        verificar_saldos(self, saida, 70, 80)

    def test_ct21_transferencia_da_conta_2_para_a_1(self):
        saida = executar_programa(100, 50, 3, 2, 20, 4)
        verificar_saldos(self, saida, 120, 30)

    def test_ct22_transferencia_de_todo_o_saldo(self):
        saida = executar_programa(100, 50, 3, 1, 100, 4)
        verificar_saldos(self, saida, 0, 150)

    def test_ct23_transferencia_acima_do_saldo(self):
        saida = executar_programa(100, 50, 3, 1, 100.01, 4)
        self.assertIn(
            "Saldo insuficiente para realizar a transferência.", saida
        )
        verificar_saldos(self, saida, 100, 50)

    def test_ct24_transferencia_partindo_de_conta_zerada(self):
        saida = executar_programa(0, 50, 3, 1, 10, 4)
        self.assertIn(
            "Saldo insuficiente para realizar a transferência.", saida
        )
        verificar_saldos(self, saida, 0, 50)

    def test_ct25_transferencia_com_valores_invalidos(self):
        for valor in (0, -20):
            with self.subTest(valor=valor):
                saida = executar_programa(100, 50, 3, 1, valor, 4)
                self.assertIn(
                    "O valor da transferência deve ser maior que zero.", saida
                )
                verificar_saldos(self, saida, 100, 50)

        saida = executar_programa(100, 50, 3, 1, "abc", 10, 4)
        self.assertIn("Digite apenas números.", saida)
        verificar_saldos(self, saida, 90, 60)

    def test_ct26_conta_de_origem_inexistente(self):
        saida = executar_programa(100, 50, 3, 3, 20, 4)
        self.assertIn("Conta inválida.", saida)
        verificar_saldos(self, saida, 100, 50)

    def test_ct27_transferencia_conserva_o_total(self):
        saida = executar_programa(100, 50, 3, 1, 30, 4)
        verificar_saldos(self, saida, 70, 80)
        self.assertEqual(70 + 80, 100 + 50)

    def test_ct28_opcoes_invalidas_do_menu(self):
        saida = executar_programa(100, 50, 0, 5, "A", "abc", 4)
        self.assertEqual(saida.count("Opção inválida."), 4)
        verificar_saldos(self, saida, 100, 50)

    def test_ct29_saida_imediata(self):
        saida = executar_programa(100, 50, 4)
        self.assertIn("Saldos finais:", saida)
        verificar_saldos(self, saida, 100, 50)

    def test_ct30_varias_operacoes_consecutivas(self):
        saida = executar_programa(
            1000,
            500,
            1, 1, 200,
            2, 2, 50,
            3, 1, 300,
            1, 2, 25,
            2, 1, 100,
            4,
        )
        verificar_saldos(self, saida, 800, 775)


if __name__ == "__main__":
    unittest.main(verbosity=2)
