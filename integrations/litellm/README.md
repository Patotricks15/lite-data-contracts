# Framework Integration

Use Lite Data Contracts before an LLM call to validate structured tool arguments, retrieval payloads, or application metadata. Include contract version and issue count in the observability metadata provided by your framework.

LiteLLM can receive this through request `metadata`; LangChain and LangGraph can carry it in runnable or graph state. This library is framework-agnostic and is not a model provider.