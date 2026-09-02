"""Lite Data Contracts - High-Level Python Pipeline Example.

Loads and validates contract schemas directly via the Rust core engine.
"""

import sys
import os

# Importa o wrapper local caso o pacote não esteja no site-packages
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../bindings/python")))
from lite_data_contracts import DataContract


def main():
    print("=== Lite Data Contracts - High-Level Python Example ===")

    # 1. Uma única linha: Rust carrega e valida o arquivo de contrato YAML
    contract_path = "examples/orders-v1.yaml"
    print(f"\n[1] Carregando contrato '{contract_path}' diretamente via Rust Core...")
    contract = DataContract.from_file(contract_path)

    # 2. Saída gerada por Tool Call do LLM
    print("\n[2] Validando Tool Call retornada pelo LLM...")
    tool_call_output = [
        {"order_id": "ORD-1234", "customer_email": "client@acme.com", "legacy_code": 88}
    ]

    issues = contract.validate(tool_call_output)
    if not issues:
        print(" -> Validação: APROVADO! O backend pode executar a ação com segurança.")
    else:
        print(f" -> Violações detectadas: {issues}")


if __name__ == "__main__":
    main()
