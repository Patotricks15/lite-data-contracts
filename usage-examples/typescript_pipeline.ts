/**
 * Lite Data Contracts - TypeScript LLM Tool Validation Example.
 *
 * Validates tool calls / structured outputs from LLM flows.
 */

interface Contract {
  required_fields: string[];
}

interface ValidationIssue {
  row: number;
  field: string;
  message: string;
}

function validateToolArguments(contract: Contract, args: Record<string, any>): ValidationIssue[] {
  const issues: ValidationIssue[] = [];
  for (const field of contract.required_fields) {
    if (args[field] === undefined || args[field] === null) {
      issues.push({ row: 0, field, message: `Missing required field: ${field}` });
    }
  }
  return issues;
}

async function handleLlmToolCall(rawToolOutput: string) {
  console.log(`\nEvaluating LLM tool output: ${rawToolOutput}`);
  const contract: Contract = {
    required_fields: ["recipient", "subject", "body"],
  };

  const parsedArgs = JSON.parse(rawToolOutput);
  const issues = validateToolArguments(contract, parsedArgs);

  if (issues.length > 0) {
    console.error(" -> [CONTRACT VIOLATION]:", issues);
    throw new Error(`LLM output violates contract: ${issues.map((i) => i.message).join(", ")}`);
  }

  console.log(" -> [VALID] Tool arguments adhere to contract. Running tool execution...");
  return { delivered: true };
}

async function main() {
  console.log("=== Lite Data Contracts - TypeScript Example ===");
  // Valid output
  await handleLlmToolCall(JSON.stringify({ recipient: "dev@example.com", subject: "Deployment", body: "Release v1 ready" }));

  // Invalid output
  try {
    await handleLlmToolCall(JSON.stringify({ recipient: "dev@example.com", body: "Missing subject" }));
  } catch (err: any) {
    console.log(" -> Handled expected contract failure.");
  }
}

main().catch(console.error);
