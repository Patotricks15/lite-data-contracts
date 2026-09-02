/**
 * Lite Data Contracts - High-Level TypeScript Pipeline Example.
 *
 * Loads contract schemas directly via the Rust core engine and validates LLM tool outputs.
 */

import { DataContract } from '../bindings/node/index';

async function main() {
  console.log('=== Lite Data Contracts - High-Level TypeScript Example ===');

  // 1. Rust carrega e valida o arquivo de contrato YAML
  const contractPath = 'examples/orders-v1.yaml';
  console.log(`\n[1] Carregando contrato '${contractPath}' diretamente no Rust Core...`);
  const contract = DataContract.fromFile(contractPath);

  // 2. Validando saída estruturada de Tool Call
  console.log('\n[2] Validando resposta de Tool Call gerada por LLM...');
  const toolOutputs = [
    { order_id: 'ORD-9901', customer_email: 'support@store.com', legacy_code: 12 },
  ];

  const issues = contract.validate(toolOutputs);
  if (issues.length === 0) {
    console.log(' -> Validação: APROVADO (Zero violações detectadas)');
  } else {
    console.log(` -> Violações: ${JSON.stringify(issues)}`);
  }
}

main().catch(console.error);
  try {
    await handleLlmToolCall(JSON.stringify({ recipient: "dev@example.com", body: "Missing subject" }));
  } catch (err: any) {
    console.log(" -> Handled expected contract failure.");
  }
}

main().catch(console.error);
