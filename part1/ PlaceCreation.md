```mermaid
sequenceDiagram
    participant Client as User
    participant API as API/Service
    participant BL as Business Logic
    participant DB as Persistence Layer (DB)

    Client->>API: POST /places (place data)
    API->>BL: createPlace(place data)
    BL->>DB: INSERT place record with associated owner ID
    DB-->>BL: Return confirmation (new place record)
    BL-->>API: Return new place object
    API-->>Client: 201 Created, place object
