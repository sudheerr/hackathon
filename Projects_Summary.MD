# Project: Enterprise Underwriting AI Assistant POC

## Objective

Build an enterprise-grade AI-assisted underwriting review system.

The system performs a first-pass review of insurance policy submissions against internal underwriting guideline documents.

The goal is NOT autonomous underwriting decisions.

The goal IS:

* guideline retrieval
* rule detection
* checklist generation
* underwriting note drafting
* agent email drafting
* concern flagging
* source citation generation
* auditability
* human-in-the-loop review

The system should be designed as a scalable enterprise architecture suitable for future production hardening.

---

# High-Level Architecture

Frontend:

* Existing Java/Angular UI (not part of this project)
* This project exposes APIs consumed by the UI

Backend:

* FastAPI
* Python 3.12+

LLM:

* Claude API (Anthropic)

Embeddings:

* Voyage AI embeddings

Vector Store:

* CosmosDB with vector indexing
* Abstract retrieval layer so future migration is possible

Document Sources:

* PDF
* DOCX

---

# Core Workflow

1. Policy payload received from PRS system
2. Normalize payload into internal policy domain model
3. Deterministic trigger detection engine identifies applicable underwriting rules
4. Retrieval engine fetches relevant guideline chunks
5. Claude generates:

    * compliance checklist
    * underwriting concern list
    * agent email draft
    * underwriting note template
    * citations
6. Validation layer verifies:

    * schema validity
    * citation presence
    * no unsupported claims
7. Full audit trail stored
8. Structured response returned to UI

---

# Critical Design Principles

The system MUST:

* prioritize deterministic logic over AI when possible
* use AI only for reasoning/summarization/generation
* be explainable
* be auditable
* support human review
* support future governance/compliance requirements
* avoid hallucinated underwriting rules
* use structured JSON outputs everywhere possible

---

# Required Project Structure

Create a clean enterprise structure like:

app/
api/
core/
domain/
services/
retrieval/
ingestion/
llm/
prompts/
validators/
audit/
models/
workflows/
tests/

Include:

* dependency injection
* configuration management
* environment variables
* logging
* tracing hooks
* extensibility points

---

# Domain Modeling Requirements

Create Pydantic models for:

## Policy Models

* HomePolicy
* Applicant
* Coverage
* Property
* ClaimsHistory

## Trigger Models

* RuleTrigger
* TriggerResult

## Retrieval Models

* GuidelineChunk
* RetrievalResult

## LLM Output Models

* ChecklistItem
* ConcernItem
* AgentEmail
* UnderwriterNote
* CitationReference

## Audit Models

* ReviewAuditRecord

---

# Deterministic Trigger Engine

Implement a rule engine.

Initial trigger examples:

* rented_to_others
* entity ownership
* dwelling limit threshold
* high value home
* coastal exposure
* prior claims count

The trigger engine MUST:

* be deterministic
* configurable
* extensible
* support metadata-driven rules
* support future YAML/JSON rule configuration

Example:

IF:
rented_to_others = true

THEN:
trigger:
RENTAL_EXPOSURE

severity:
HIGH

---

# Retrieval Layer

Implement hybrid retrieval architecture.

Required capabilities:

* vector similarity search
* metadata filtering
* keyword search hooks
* reranking hooks
* retrieval scoring

Chunk metadata MUST include:

* document name
* version
* section heading
* page number
* state applicability
* line of business
* effective date
* expiration date
* rule category

Create interfaces/abstractions for:

* EmbeddingProvider
* VectorStore
* Retriever

---

# Document Ingestion Pipeline

Offline/manual ingestion process.

Capabilities:

* PDF extraction
* DOCX extraction
* structure-aware chunking
* metadata extraction
* embedding generation
* CosmosDB indexing

Chunking requirements:

* preserve section hierarchy
* preserve tables
* overlap chunks
* maintain citation traceability

Include sample ingestion CLI.

---

# LLM Orchestration

Implement Claude orchestration service.

Requirements:

* structured JSON outputs only
* retry handling
* timeout handling
* prompt versioning
* prompt templates
* citation enforcement
* deterministic temperature settings

Prompt must instruct Claude:

* never invent rules
* only use retrieved guideline sections
* include citations for every concern
* state uncertainty explicitly

---

# Validation Layer

Implement post-LLM validation.

Checks:

* JSON schema validation
* citation existence
* required fields
* confidence thresholds
* unsupported claim detection
* empty retrieval detection

If retrieval confidence is low:

* system must return:
  "Manual review required"

---

# Audit & Observability

Implement:

* structured logging
* request correlation IDs
* audit records
* workflow tracing hooks

Audit record should include:

* policy ID
* retrieved chunks
* triggers fired
* prompt version
* model version
* timestamps
* output JSON
* reviewer actions

---

# APIs

Create FastAPI endpoints:

POST /review-policy
POST /ingest-guidelines
GET /health
GET /audit/{policy_id}

Use async APIs where appropriate.

---

# Testing Requirements

Create:

* unit tests
* retrieval tests
* trigger engine tests
* validation tests
* mock Claude integration tests

Add sample test policies.

---

# Non-Functional Requirements

The system should:

* be modular
* support future scaling
* support future multi-agent orchestration
* support future Azure deployment
* support future event-driven architecture
* support future LangGraph integration

---

# Security Considerations

Design placeholders for:

* RBAC
* PII masking
* encryption hooks
* API authentication
* secure secret handling

Do not fully implement auth, but structure for future integration.

---

# Deliverables

Generate:

1. Full project structure
2. Initial implementation
3. Sample configuration
4. Example prompts
5. Sample policy payloads
6. Mock guideline documents
7. Retrieval abstraction layer
8. README with setup instructions
9. Architecture diagram in markdown
10. Example end-to-end workflow

---

# Coding Standards

Requirements:

* clean architecture principles
* SOLID principles
* type hints everywhere
* Pydantic validation
* docstrings
* modular services
* avoid monolithic files
* enterprise readability

---

# Important Constraints

DO NOT:

* build a chatbot UI
* build autonomous underwriting
* make underwriting decisions
* hardcode business logic into prompts
* tightly couple retrieval to CosmosDB
* rely solely on vector search

DO:

* separate deterministic logic from AI reasoning
* prioritize explainability
* prioritize auditability
* keep architecture extensible

---

# First Task

Generate:

1. Complete project folder structure
2. Core domain models
3. FastAPI app bootstrap
4. Trigger engine skeleton
5. Retrieval abstraction interfaces
6. Claude orchestration service skeleton
7. Example review-policy endpoint
8. README with local setup instructions

Then stop and wait for the next implementation phase.
