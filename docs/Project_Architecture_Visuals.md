# MedLens Cloud-Edge Hybrid Architecture 

This document contains the complete architectural visuals for the MedLens Cloud-Edge integration project. These Mermaid diagrams can be previewed directly in GitHub, Markdown editors, or the Mermaid Live Editor.

## 1. Cloud-Edge-Device Architecture Layout

```mermaid
flowchart LR
    %% Entities
    User((User / Doctor))
    
    subgraph Device Level ["📱 Android Client"]
        UI[Jetpack Compose UI]
        Engine[Inference Engine]
    end
    
    subgraph Edge Level ["⚡ On-Device Models"]
        EdgeModel1[BiomedCLIP INT8\nImage Context]
        EdgeModel2[MedGemma Q4\nLocal Reasoning]
    end
    
    subgraph Local Router ["🧠 Complexity Router"]
        RouterLogic{Decision Logic:\nComplexity >= Threshold?}
    end
    
    subgraph Cloud Level ["☁️ Cloud API Backend"]
        Gateway[Django REST API Gateway]
        LLMOrch[LLM Orchestrator]
        CloudDB[(Relational DB\ne.g., PostgreSQL)]
        MassiveLLM[Large Medical LLM\n24B+ Params]    
    end

    %% Flow
    User -->|Prompts + Scans| UI
    UI --> Engine
    Engine <--> EdgeModel1
    Engine --> RouterLogic
    
    %% Routing conditional
    RouterLogic -->|Simple / Low Complexity| EdgeModel2
    EdgeModel2 --> UI
    
    RouterLogic -->|Complex / Low Confidence| Gateway
    Gateway --> LLMOrch
    LLMOrch <--> MassiveLLM
    LLMOrch <--> CloudDB
    Gateway -->|Cloud Response| UI
```

## 2. End-to-End Fallback Interaction Flow

```mermaid
sequenceDiagram
    autonumber
    actor U as User
    participant App as Android Client
    participant Edge as Local Models (Edge)
    participant Cloud as Django Backend
    participant DB as Cloud Database
    participant LLM as Remote Large Model

    U->>App: Submits Medical Query + Image
    App->>Edge: Pre-process with BiomedCLIP
    Edge-->>App: Image Encodings / Feature Data
    App->>App: Evaluate query complexity

    alt Complexity < Threshold (Stay on Edge)
        App->>Edge: Run MedGemma Q4 (Local)
        Edge-->>App: Local Draft Response
        App-->>U: Deliver Edge Response (Fast)
    else Complexity >= Threshold (Offload to Cloud)
        App->>Cloud: POST /api/chat/ (Multipart Data)
        Cloud->>DB: Fetch/Create Chat Session
        DB-->>Cloud: Chat Context history
        Cloud->>LLM: Enhanced Prompt with Full Context
        LLM-->>Cloud: Advanced Answer
        Cloud->>DB: Save updated history logs
        Cloud-->>App: Return Comprehensive Response
        App-->>U: Deliver Cloud Response
    end
```

## 3. Detailed Cloud Backend Data Flow

```mermaid
flowchart TD
    Req[Incoming POST Request] --> Parse[Extract multipart/form-data]
    Parse --> CheckChat{Chat ID Valid?}
    
    CheckChat -- No --> CreateChat[Create New Chat Instance]
    CheckChat -- Yes --> FetchChat[(Fetch from DB)]
    
    CreateChat --> Combine
    FetchChat --> Combine
    
    Parse --> HandleFile{Contains File/Image?}
    HandleFile -- Yes --> SaveFile[(Save to File Storage)] --> Combine
    HandleFile -- No --> Combine[Build LLM Context History]
    
    Combine --> CallLLM[Execute Remote LLM Inference]
    CallLLM -- Success --> SaveDb[(Save Conversation Logs to DB)]
    SaveDb --> Res[Return 200 JSON Response]
    CallLLM -- Failure --> Err[Return 500 Error Response]
```

## 4. Cloud Services Resource Map

```mermaid
flowchart LR
    Mobile[MedLens Client] -->|HTTPS POST| REST[Django REST Framework]
    
    subgraph Backend Infrastructure
        REST --> API[Chat API View]
        API --> DB[(Database\nConversations)]
        API --> BLOB[(File Storage\nMedia/Uploads)]
        API --> UTIL[LLM Utils]
    end
    
    UTIL -->|API Call| ExLLM[External/Hosted Large LLM]
```
