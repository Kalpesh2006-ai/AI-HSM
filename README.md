AI-HSM/
│
├── hardware/
│   ├── esp32/
│   │   ├── main.cpp
│   │   ├── microphone.cpp
│   │   ├── microphone.h
│   │   ├── speaker.cpp
│   │   ├── speaker.h
│   │   ├── display.cpp
│   │   ├── display.h
│   │   └── config.h
│   │
│   └── circuit/
│       ├── circuit_diagram.png
│       └── components.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── README.md
│
├── backend/
│   ├── server.js
│   ├── routes/
│   │   ├── voice.js
│   │   ├── query.js
│   │   └── health.js
│   ├── controllers/
│   ├── services/
│   │   ├── speechService.js
│   │   ├── aiService.js
│   │   └── ragService.js
│   ├── models/
│   ├── config/
│   │   └── database.js
│   └── package.json
│
├── rag/
│   │
│   ├── government_schemes/
│   │   │
│   │   ├── raw_data/
│   │   │   ├── pmegp/
│   │   │   ├── pm_vishwakarma/
│   │   │   ├── day_nrlm/
│   │   │   ├── pmfme/
│   │   │   ├── cgtmse/
│   │   │   └── maharashtra_schemes/
│   │   │
│   │   ├── processed_data/
│   │   │   └── government_schemes.json
│   │   │
│   │   ├── questions/
│   │   │   └── government_scheme_questions.json
│   │   │
│   │   ├── documents/
│   │   │   ├── pmegp/
│   │   │   ├── pm_vishwakarma/
│   │   │   └── ...
│   │   │
│   │   └── metadata/
│   │       └── sources.json
│   │
│   ├── embeddings/
│   │   └── government_schemes/
│   │
│   └── vector_db/
│       └── government_schemes/
│
├── ai/
│   ├── prompts/
│   │   ├── system_prompt.txt
│   │   └──government_scheme_prompt .txt
│   │
│   ├── rag/
│   │   ├── retriever.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   └── rag_pipeline.py
│   │
│   └── llm/
│       └── llm_service.py
│
├── database/
│   ├── schemas/
│   └── seed/
│
├── tests/
│   ├── rag/
│   ├── backend/
│   └── hardware/
│
├── .env
├── .gitignore
├── requirements.txt
├── package.json
└── README.md