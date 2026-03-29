# MedLens Week 1-4 Visual Pack

Use these Mermaid diagrams directly in Markdown slides, GitHub, or Mermaid Live Editor.

## 1. Cloud-Edge-Device Architecture

```mermaid
flowchart LR
    U[User] --> D[Device Layer\nAndroid MedLens App UI]
    D --> E[Edge Layer\nBiomedCLIP INT8 + MedGemma Q4]
    E --> R[Routing Engine\nComplexity + Confidence + Latency]

    R -->|Simple Query| L[Local Response\nLow Latency, Private]
    R -->|Complex Query| C[Cloud API Gateway]

    C --> M[Large Medical Model API\nMedGemma 24B or Equivalent]
    C --> DB[(User + Session DB)]
    C --> LOG[(Audit + Telemetry Logs)]

    L --> D
    M --> C --> D
```

## 2. End-to-End Interaction Flow

```mermaid
sequenceDiagram
    autonumber
    participant User
    participant App as Android App
    participant Edge as Edge Models
    participant Router as Routing Logic
    participant Cloud as Cloud API
    participant LLM as Large Model

    User->>App: Upload image + ask question
    App->>Edge: Run BiomedCLIP + local MedGemma
    Edge-->>Router: Confidence + local draft + complexity features

    alt Simple and high confidence
        Router-->>App: Keep on edge
        App-->>User: Show edge response
    else Complex or low confidence
        Router->>Cloud: Send anonymized context
        Cloud->>LLM: Inference request
        LLM-->>Cloud: Enhanced response
        Cloud-->>App: Cloud response + source tag
        App-->>User: Show cloud-enhanced response
    end
```

## 3. Routing Decision Diagram

```mermaid
flowchart TD
    A[Start Request] --> B[Extract Features\nPrompt Length, Entity Count, Confidence]
    B --> C{Complexity >= 0.65?}
    C -- Yes --> G[Route to Cloud]
    C -- No --> D{Edge Confidence <= 0.55?}
    D -- Yes --> G
    D -- No --> E{User requests second opinion?}
    E -- Yes --> G
    E -- No --> F[Route to Edge]
    F --> H[Return Edge Response]
    G --> I[Return Cloud Response]
```

## 4. Week 1-4 Milestone Timeline

```mermaid
gantt
    title Week 1-4 Progress Timeline
    dateFormat  YYYY-MM-DD
    axisFormat  Week %W

    section Planning
    Topic selection and team formation     :done, w1, 2026-02-03, 7d

    section Analysis
    Requirements and literature survey     :done, w2, 2026-02-10, 7d

    section Design
    Architecture and data flow design      :done, w3, 2026-02-17, 7d

    section Week 4 Focus
    Cloud API contract and service design  :active, w4a, 2026-02-24, 4d
    Routing strategy definition            :active, w4b, 2026-02-24, 4d
    Week 4 presentation prep               :active, w4c, 2026-02-27, 3d
```

## 5. Week 4 Cloud Services Map

```mermaid
flowchart LR
    Client[Android MedLens App] --> API1[POST /v1/route-evaluate]
    Client --> API2[POST /v1/qa/cloud-infer]
    Client --> API3[POST /v1/sessions]
    Client --> API4[GET /v1/health]

    API1 --> SVC[Routing Service]
    API2 --> ORCH[LLM Orchestrator]
    API3 --> STORE[(PostgreSQL)]
    API4 --> MON[Health Monitor]

    ORCH --> LLM[Cloud Large Medical Model]
    SVC --> POL[Policy Rules]
    ORCH --> LOG[(Inference Logs)]
```

## 6. Suggested Slide Mapping

- Slide 1: Architecture diagram
- Slide 2: End-to-end interaction sequence
- Slide 3: Routing decision logic
- Slide 4: Week 1-4 timeline
- Slide 5: Cloud services map
