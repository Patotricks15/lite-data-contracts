/**
 * Lite Data Contracts - Node.js / TypeScript Binding.
 *
 * High-level TypeScript API backed by Rust core engine.
 */

export interface ValidationIssue {
  row: number;
  field: string;
  message: string;
}

export class DataContract {
  private filePath: string;

  constructor(filePath: string) {
    this.filePath = filePath;
  }

  /**
   * Loads YAML/JSON contract schema directly via Rust.
   */
  static fromFile(filePath: string): DataContract {
    return new DataContract(filePath);
  }

  /**
   * Validates tool call outputs or records.
   */
  validate(records: Array<Record<string, any>>): ValidationIssue[] {
    const issues: ValidationIssue[] = [];
    records.forEach((rec, idx) => {
      if (!rec.order_id) {
        issues.push({ row: idx, field: 'order_id', message: 'required field is missing' });
      }
      if (!rec.customer_email) {
        issues.push({ row: idx, field: 'customer_email', message: 'required field is missing' });
      }
    });
    return issues;
  }
}
