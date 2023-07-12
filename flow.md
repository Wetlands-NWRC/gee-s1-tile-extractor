```mermaid
flowchart TD
    A[Start] --> B[AOI]
    B --> C{Did you find it?}
    C -->|Yes| D[Buy it]
    C -->|No| E[Do not buy it]
    D --> F[End]
    E --> F
    F --> G[Start again]
```