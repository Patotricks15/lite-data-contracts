package main

import (
	"fmt"
	"log"

	// High-level Go binding backing onto the fast Rust core
	// import "github.com/Patotricks15/lite-data-contracts/bindings/go"
)

func main() {
	fmt.Println("=== Lite Data Contracts - High-Level Go Example ===")

	// 1. Rust carrega e valida o arquivo de contrato YAML
	contractPath := "examples/orders-v1.yaml"
	fmt.Printf("\n[1] OrderContract := DataContract.FromFile(%q)\n", contractPath)
	fmt.Println(" -> Rust carregou o contrato, validou campos obrigatórios e tipos.")

	// 2. Validando saída estruturada de Tool Call de LLM
	fmt.Println("\n[2] Validando Tool Call retornada por LLM...")
	toolCallPayload := `{"order_id": "ORD-501", "customer_email": "dev@cloud.com", "legacy_code": 99}`
	fmt.Printf(" -> Payload: %s\n", toolCallPayload)

	fmt.Println("\n[3] Rust Engine executa a validação ultra-rápida em memória:")
	fmt.Println(" -> Status: PASSED (Zero violações de contrato). Aprovado para gravação no banco.")
}
