# MedLens Cloud-Edge Intelligence Intergration

This repository contains the ongoing Cloud Computing course project aimed at transforming the **MedLens** edge AI application into a **Cloud-Edge Hybrid** architecture. 

The goal is to implement an intelligent routing engine that evaluates user queries. Simple and high-confidence queries remain on the device (Edge) for speed and privacy, while complex or low-confidence queries are offloaded to a powerful remote Large Model (Cloud/Backend).

## Repository Structure

```
📁 docs/                     # Project documentation, designs, and architectural diagrams
   📄 Project_Architecture_Visuals.md
   📄 Cloud_Edge_Intelligence_Course_Project.md
   📄 Week4_MedLense_Design_Report.md
   ...

📁 Test_App/                 # Standalone Android Test Client
   # Built purely to validate the network connection strategy and multipart requests 
   # before integrating into the main MedLens Android repository. 
```

## Quick Start (Test App Local Diagnostics)

We are testing connectivity against a Django backend hosted on a secondary machine. 

To launch the Test Android App locally:
1. Open the `Test_App` directory in **Android Studio**. Compile and install it on your device.
2. Open the **Config** panel in the app.
3. Enter the network IP address of the target server host (e.g. `http://192.168...:8000`).
4. Test sending a chat message and an image.

## Architecture

The system utilizes an offloading threshold constraint:
* **Edge Models:** BiomedCLIP INT8, MedGemma Q4.
* **Server Infrastructure:** Django REST Framework API, Relational Database, Massive LLMs integration.

For a full view of the architecture and mermaid diagrams, please check [docs/Project_Architecture_Visuals.md](docs/Project_Architecture_Visuals.md).