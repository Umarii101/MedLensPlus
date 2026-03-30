# Cloud Computing and Edge Intelligence — Course Project Assessment

---

## 1. Overview

This course adopts a semester-long comprehensive project as the primary assessment method. The project centers on **designing and implementing a cloud-edge-device collaborative intelligent application system**. It is divided into three progressive phases, each assessed independently by one of the three course instructors.

Students are free to choose their own technology stacks and implementation approaches. The use of open-source simulation tools is encouraged.

---

## 2. Schedule and Grading

| Phase | Duration | Instructor | Weight |
|-------|----------|------------|--------|
| Phase 1: System Design and Cloud Platform Development | Weeks 2–7 (submit in Week 7) | Instructor A | **30%** |
| Phase 2: Edge Intelligence Deployment and Optimization | Weeks 7–12 (submit in Week 12) | Instructor B | **35%** |
| Phase 3: Cloud-Edge Collaboration and System Integration | Weeks 13–17 (submit in Week 17) | Instructor C | **35%** |

**Final Score = Phase 1 × 0.3 + Phase 2 × 0.35 + Phase 3 × 0.35**

---

## 3. Project Topics

### Topic 1: Intelligent Video Surveillance System

Perform real-time object detection or behavior recognition on video streams at the edge. Upload alarm events and statistical data to the cloud for storage, querying, and visual analytics.

### Topic 2: Industrial IoT Anomaly Detection System

Simulate industrial sensors continuously generating equipment operation data. The edge performs real-time anomaly detection and early warning, while the cloud handles historical data analysis, model updates, and a management dashboard.

### Topic 3: Smart Traffic Flow Analysis System

Simulate traffic data collection from multiple intersections. The edge performs vehicle counting, license plate recognition, or congestion detection. The cloud aggregates multi-intersection data for global analysis and scheduling optimization.

### Topic 4: Edge-Assisted Intelligent Q&A / Text Processing System

Deploy a lightweight language model (e.g., a quantized small LLM) at the edge to handle simple queries. Complex requests are offloaded to a large cloud-based model. Design a reasonable task routing strategy.

### Topic 5: Intelligent Medical Data Processing System

Simulate wearable devices collecting physiological data. The edge performs preliminary analysis and anomaly alerts. The cloud handles data storage, in-depth analysis, and medical report generation. Data privacy protection should be considered.

### Topic 6: Multi-Node Collaborative Federated Learning System

Simulate multiple edge nodes training models on local data. The cloud is responsible for model aggregation and global coordination. Analyze the impact of different aggregation strategies and communication compression methods on model performance and communication overhead.

### Topic 7: Cloud-Edge Collaborative Recommendation System

The edge provides lightweight real-time recommendations based on recent user behavior. The cloud trains a global recommendation model using full-scale data and periodically pushes updates. Design model synchronization and personalization fusion strategies.

### Topic 8: Self-Proposed Topic

Students may propose their own topics, provided that:

- The system covers three layers: cloud, edge, and device.
- At least one AI/ML model is deployed at the edge.
- There is a clear need for cloud-edge collaboration.
- **The proposal must be submitted by Week 2 and approved by all three instructors.**

---

## 4. Phase Requirements

### Phase 1: System Design and Cloud Platform Development (Weeks 1–6, Instructor A)

**Requirements:**

1. **System Architecture Design**
   - Provide a complete system architecture diagram clearly indicating the responsibilities of the cloud, edge, and device layers.
   - Describe the data flow and interaction patterns between layers.
   - Justify technology choices with references to literature or established practices.

2. **Cloud-Side Implementation**
   - Set up a simulated cloud environment and implement core functionalities including data storage, API services, and business logic.
   - The cloud services should be operational and accessible via interfaces.

3. **Deliverables**
   - Architecture design report (5–8 pages)
   - A runnable cloud service demo (with deployment instructions)
   - 10-minute defense presentation

**Grading Rubric (100 points):**

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Architecture design quality | 35% | Clear layering, well-justified choices, reasonable data flow |
| Cloud implementation completeness | 35% | Functional completeness, operational service |
| Documentation quality | 15% | Clear writing, proper diagrams, appropriate references |
| Defense performance | 15% | Logical presentation, ability to answer technical questions |

---

### Phase 2: Edge Intelligence Deployment and Optimization (Weeks 7–12, Instructor B)

**Requirements:**

1. **Model Selection and Training**
   - Select or train an AI model suitable for the chosen scenario.
   - Justify the model choice in terms of accuracy, complexity, and applicability.

2. **Edge Optimization**
   - Apply at least one model optimization technique (quantization, pruning, knowledge distillation, lightweight architecture design, etc.).
   - Deploy and run inference in a simulated resource-constrained environment.

3. **Comparative Experiments**
   - Design proper comparative experiments covering at least: model accuracy, inference latency, and resource consumption (memory / model size).
   - Analyze the effectiveness and applicable conditions of the optimization methods.

4. **Deliverables**
   - Technical report (5–8 pages)
   - A runnable edge inference demo (with resource constraint specifications)
   - 10-minute defense presentation

**Grading Rubric (100 points):**

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Model optimization methods | 35% | Reasonable approach, rigorous description, theoretical basis |
| Experiment design and analysis | 30% | Sufficient experiments, insightful analysis, supported conclusions |
| Edge deployment | 20% | Successful deployment, functional in constrained environment |
| Defense performance | 15% | Logical presentation, ability to answer technical questions |

---

### Phase 3: Cloud-Edge Collaboration and System Integration (Weeks 13–17, Instructor C)

**Requirements:**

1. **System Integration**
   - Connect Phase 1 (cloud) and Phase 2 (edge) into a complete end-to-end data pipeline.
   - The system should be fully operational and demonstrable.

2. **Cloud-Edge Collaboration Strategy**
   - Design and implement at least one collaboration strategy, such as:
     - Task offloading decisions (based on latency, workload, or task complexity)
     - Data synchronization mechanisms (incremental sync, priority scheduling)
     - Model update workflows (pushing updated models from cloud to edge)
     - Privacy-preserving mechanisms (differential privacy, federated aggregation, etc.)
   - Justify the strategy design with theoretical support.

3. **System Evaluation**
   - Evaluate system performance under varying conditions (network latency, bandwidth, workload levels).
   - Evaluation metrics should include at least: end-to-end latency, throughput, and resource utilization.
   - Discuss scalability, limitations, and potential improvements.

4. **Deliverables**
   - Final project report (8–12 pages) integrating all three phases
   - System demonstration (live demo or recorded video)
   - 15-minute final defense presentation

**Grading Rubric (100 points):**

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Collaboration strategy design | 30% | Reasonable strategy with theoretical support |
| System integration completeness | 25% | End-to-end operational, functionally complete |
| Experimental evaluation | 25% | Comprehensive metrics, diverse conditions, in-depth analysis |
| Final report and defense | 20% | Complete and well-structured report, strong defense |

---

## 5. Weekly Discussion Sessions (45 minutes each)

Each week includes a 45-minute in-class discussion session for progress reports, peer feedback, and Q&A with instructors. The discussion content is designed to align with the project phases and guide students through key milestones.

---

### Phase 1: System Design and Cloud Platform Development (Weeks 1–6)

#### Week 1 — Topic Selection and Team Formation

- **Progress report**: Each team briefly introduces their selected topic and team members (3 min per team).
- **Discussion focus**:
  - What are the core requirements of your chosen scenario?
  - What cloud-edge-device responsibilities can you identify at this stage?
- **Instructor guidance**: Provide feedback on topic feasibility and scope. Help teams with self-proposed topics refine their ideas.
- **Milestone**: Teams finalized; preliminary topic selected.

#### Week 2 — Requirements Analysis and Literature Survey

- **Progress report**: Each team presents their requirements analysis and relevant literature findings (5 min per team).
- **Discussion focus**:
  - What existing systems or papers are relevant to your project?
  - What are the key technical challenges you foresee?
  - How do similar systems partition responsibilities between cloud and edge?
- **Instructor guidance**: Suggest key references; help teams identify gaps in their understanding.
- **Milestone**: Self-proposed topics submitted for approval; literature survey completed.

#### Week 3 — System Architecture Design Review

- **Progress report**: Each team presents their draft system architecture diagram and technology choices (5–8 min per team).
- **Discussion focus**:
  - Is the layering (cloud/edge/device) clear and reasonable?
  - Are the data flows and interfaces well-defined?
  - Peer critique: other teams provide feedback and suggestions.
- **Instructor guidance**: Identify potential architectural issues early; suggest improvements.
- **Milestone**: Architecture diagram and technology stack determined.

#### Week 4 — Cloud Platform Development Progress

- **Progress report**: Each team reports on cloud-side implementation progress (5 min per team).
- **Discussion focus**:
  - What services have been implemented (storage, APIs, business logic)?
  - What technical difficulties have you encountered?
  - Open Q&A: teams can raise specific technical problems for group discussion.
- **Instructor guidance**: Help resolve technical blockers; share best practices.
- **Milestone**: Core cloud services under active development.

#### Week 5 — Cloud Platform Testing and Refinement

- **Progress report**: Each team demonstrates their current cloud service prototype (5–8 min per team).
- **Discussion focus**:
  - Live demo or walkthrough of cloud-side functionality.
  - Peer feedback on completeness and usability.
  - Are the interfaces designed to support future edge integration?
- **Instructor guidance**: Assess readiness for Phase 1 submission; suggest refinements.
- **Milestone**: Cloud services functional; preparing for submission.

#### Week 6 — Phase 1 Defense Presentations

- **Format**: Each team delivers a 10-minute formal defense presentation followed by Q&A.
- **Content**: Architecture design report, cloud service demo, technology justification.
- **Peer participation**: Other teams ask questions and provide written feedback.
- **Milestone**: Phase 1 deliverables submitted; graded by Instructor A.

---

### Phase 2: Edge Intelligence Deployment and Optimization (Weeks 7–12)

#### Week 7 — Phase 2 Kick-off: Model Selection and Planning

- **Progress report**: Each team presents their chosen AI model and edge deployment plan (5 min per team).
- **Discussion focus**:
  - Why did you choose this model? What are the alternatives?
  - What optimization techniques are you planning to apply?
  - What are the expected resource constraints at the edge?
- **Instructor guidance**: Advise on model selection and optimization strategy feasibility.
- **Milestone**: Model and optimization plan determined.

#### Week 8 — Model Training and Baseline Results

- **Progress report**: Each team reports on model training progress and baseline performance (5 min per team).
- **Discussion focus**:
  - What dataset are you using? How was it prepared?
  - What is the baseline accuracy/performance before optimization?
  - Any training issues (convergence, data quality, compute limitations)?
- **Instructor guidance**: Help troubleshoot training issues; discuss evaluation methodology.
- **Milestone**: Baseline model trained with benchmark results.

#### Week 9 — Edge Optimization Techniques: Implementation Progress

- **Progress report**: Each team presents their optimization implementation progress (5–8 min per team).
- **Discussion focus**:
  - Which optimization technique(s) have you applied so far?
  - What are the initial results (accuracy vs. efficiency trade-offs)?
  - Cross-team knowledge sharing: teams using different techniques share insights.
- **Instructor guidance**: Provide theoretical context for optimization methods; suggest improvements.
- **Milestone**: At least one optimization technique applied.

#### Week 10 — Edge Deployment and Comparative Experiments

- **Progress report**: Each team demonstrates edge-side inference and presents experimental results (5–8 min per team).
- **Discussion focus**:
  - How did you set up the resource-constrained environment?
  - Comparison: original model vs. optimized model (accuracy, latency, memory).
  - Are the experimental conditions fair and reproducible?
- **Instructor guidance**: Review experimental design rigor; suggest additional experiments.
- **Milestone**: Comparative experiments largely completed.

#### Week 11 — Results Analysis and Report Preparation

- **Progress report**: Each team presents their analysis of experimental results (5 min per team).
- **Discussion focus**:
  - What conclusions can you draw from the experiments?
  - Under what conditions does the optimization work best/worst?
  - Peer review: exchange draft reports for feedback.
- **Instructor guidance**: Guide report writing; ensure analysis depth meets expectations.
- **Milestone**: Draft technical report ready for review.

#### Week 12 — Phase 2 Defense Presentations

- **Format**: Each team delivers a 10-minute formal defense presentation followed by Q&A.
- **Content**: Technical report, edge inference demo, experimental analysis.
- **Peer participation**: Other teams ask questions and provide written feedback.
- **Milestone**: Phase 2 deliverables submitted; graded by Instructor B.

---

### Phase 3: Cloud-Edge Collaboration and System Integration (Weeks 13–17)

#### Week 13 — Phase 3 Kick-off: Integration Planning and Collaboration Strategy Design

- **Progress report**: Each team presents their integration plan and proposed collaboration strategy (5–8 min per team).
- **Discussion focus**:
  - How will you connect the cloud and edge components?
  - What collaboration strategy (offloading, synchronization, model update, etc.) will you implement?
  - What are the expected challenges in system integration?
- **Instructor guidance**: Evaluate strategy feasibility; suggest theoretical frameworks.
- **Milestone**: Integration plan and collaboration strategy defined.

#### Week 14 — System Integration Progress

- **Progress report**: Each team reports on integration progress and demonstrates the current state of the end-to-end pipeline (5–8 min per team).
- **Discussion focus**:
  - Is the data flowing correctly from device to edge to cloud?
  - What integration issues have arisen (interface mismatch, data format, timing)?
  - Open troubleshooting: teams raise specific issues for collective problem-solving.
- **Instructor guidance**: Help resolve integration blockers; share debugging strategies.
- **Milestone**: End-to-end pipeline partially or fully operational.

#### Week 15 — System Evaluation and Performance Testing

- **Progress report**: Each team presents their evaluation setup and preliminary results (5–8 min per team).
- **Discussion focus**:
  - What conditions are you testing under (latency, bandwidth, workload variations)?
  - What metrics are you measuring (end-to-end latency, throughput, resource utilization)?
  - Are the results consistent with expectations? Any surprises?
- **Instructor guidance**: Review evaluation methodology; suggest additional test scenarios.
- **Milestone**: System evaluation largely completed.

#### Week 16 — Final Report Review and Rehearsal

- **Progress report**: Each team presents a summary of their complete project and shares the draft final report (5 min per team).
- **Discussion focus**:
  - Peer review of draft final reports: structure, completeness, writing quality.
  - Rehearsal feedback for the final defense presentation.
  - Discussion of limitations and future work directions.
- **Instructor guidance**: Final feedback on reports; presentation coaching.
- **Milestone**: Final report and presentation ready for submission.

#### Week 17 — Final Defense Presentations

- **Format**: Each team delivers a 15-minute final defense presentation followed by Q&A.
- **Content**: Complete project report integrating all three phases, system demonstration, evaluation results, and discussion.
- **Peer participation**: All teams participate in Q&A and provide written feedback.
- **Milestone**: Phase 3 deliverables submitted; graded by Instructor C. Course project completed.

---

## 6. General Requirements

1. **Team Size**: 2–3 students per team; cross-disciplinary collaboration is encouraged.
2. **Tools and Platforms**: No restrictions on technology stacks. Students choose freely based on their capabilities and preferences. The use of open-source simulation tools is encouraged.
3. **Report Format**: Use the university's postgraduate thesis template or IEEE/ACM conference format. References must be included.
4. **Code Submission**: Submit source code and deployment documentation for each phase to ensure reproducibility.
5. **Academic Integrity**: Referencing open-source projects is permitted but must be properly cited. Core design and experiments must be completed independently.
6. **Phase Continuity**: Each phase builds upon the previous one. The architecture designed in Phase 1 should anticipate interfaces for edge deployment and cloud-edge collaboration in subsequent phases.
