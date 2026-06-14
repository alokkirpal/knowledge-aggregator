# Knowledge Store Architecture

## Pipeline

Seed URLs  
↓  
Crawler  
↓  
Link Classifier  
↓  
Text Extraction  
↓  
Cleaning  
↓  
Chunking  
↓  
Source Registry + Knowledge Chunks  
↓  
Syllabus Refinement  
↓  
LLM Topic Hierarchy Generation  
↓  
Knowledge Store  

## Link Classification

| Link Type | Action |
|---|---|
| HTML page | Process |
| PDF | Process later/current if supported |
| YouTube/video | Defer |
| Social media | Ignore |
| Store/login/unrelated | Ignore |

## Current Outputs

1. sources.json
2. chunks.json
3. refined_syllabus_draft.json
4. topic_hierarchy_draft.json