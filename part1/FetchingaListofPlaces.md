```mermaid
sequenceDiagram
    participant Client as User
    participant API as API/Service
    participant BL as Business Logic
    participant DB as Persistence Layer (DB)

    Client->>API: GET /places?criteria=filters
    API->>BL: fetchPlaces(criteria)
    BL->>DB: SELECT places WHERE criteria match
    DB-->>BL: Return list of matching places
    BL-->>API: Return list of place objects
    API-->>Client: 200 OK, list of places
