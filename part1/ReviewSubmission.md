```mermaid
sequenceDiagram
    participant Client as User
    participant API as API/Service
    participant BL as Business Logic
    participant DB as Persistence Layer (DB)

    Client->>API: POST /places/{placeId}/reviews (review data)
    API->>BL: submitReview(review data, user ID, placeId)
    BL->>DB: INSERT review record linked to user and place
    DB-->>BL: Return confirmation (review record with timestamps)
    BL-->>API: Return review object
    API-->>Client: 201 Created, review object
