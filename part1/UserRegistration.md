```mermaid
sequenceDiagram
    participant Client
    participant API
    participant UserModel
    participant DB

    Client->>API: POST / api / v1 / users
    API->>UserModel: validate_user_data(data)
    UserModel->>DB: INSERT INTO users
    DB-->>UserModel: user_id
    UserModel-->>API: return created user
    API-->>Client: 201 Created + user data
