#  Django Storefront API

A robust, scalable, and feature-rich RESTful API backend for an e-commerce platform, built with Django and Django REST Framework (DRF). This project demonstrates modern API design patterns, including a decoupled architecture, JWT authentication, and efficient data modeling.

##  Features

- **JWT Authentication & Authorization**: Secure user registration and login using Djoser. Role-based permissions for customers and administrators.
- **Complete E-commerce Logic**: Full implementation of products, collections, shopping carts, orders, and customers.
- **Flexible Product Catalog**: Support for products with images, categories (collections), promotions, and customer reviews.
- **Generic Likes System**: A reusable "like" functionality that can be attached to any model (e.g., products, reviews) using Django's Content Types framework.
- **Optimized Performance**: Utilizes `select_related`, `prefetch_related`, and annotations to minimize database queries.
- **Advanced Filtering & Search**: Integrated with `django-filter` for field-level filtering and DRF's built-in search and ordering.
- **Admin Dashboard**: Customized Django admin interface for managing the entire platform.
- **Debugging Ready**: Pre-configured with Django Debug Toolbar for performance analysis.
---
## System Architecture & Data Model

The application is built with a clean, modular structure:

### Apps Overview
*   `core`: Custom user model extending `AbstractUser`.
*   `store`: Core e-commerce functionality (Products, Orders, Carts, etc.).
*   `likes`: Generic liking system using Django's ContentTypes.
---
### High-Level Architecture

```mermaid
flowchart TD
    subgraph Frontend [Client Application]
        WebApp[Web/Mobile App]
    end

    subgraph Django [Django Project - Storefront]
        subgraph Apps [Apps & Models]
            direction TB
            Core[core: User]
            Store[store: Product, Order, Cart, etc.]
            Likes[likes: LikedItem]
        end

        API[DRF API Viewsets]
        Admin[Django Admin]
    end

    subgraph Services [External Services]
        Auth[JWT Authentication]
    end

    subgraph Data [Data Layer]
        DB[(Database)]
    end

    WebApp -->|API Requests| API
    WebApp -->|Login/Register| Auth
    API -->|Query| DB
    Admin -->|Manage Data| DB
    API -->|Uses| Apps
    Auth -->|Validates User| Core
```
---
##  API Endpoints

| Endpoint | Method | Description | Permission |
| :--- | :--- | :--- | :--- |
| `/auth/` | POST, etc | User registration & JWT token management | Public |
| `/store/products/` | GET | List all products (with filtering, search, ordering) | Public |
| `/store/products/` | POST | Create a new product | Admin Only |
| `/store/products/{id}/` | GET | Get product details | Public |
| `/store/carts/` | POST | Create a new cart | Public |
| `/store/carts/{uuid}/` | GET | Retrieve a cart with its items | Public |
| `/store/carts/{uuid}/items/` | POST | Add an item to the cart | Public |
| `/store/orders/` | POST | Create a new order from cart | Authenticated |
| `/store/orders/` | GET | List user's orders | Authenticated |
| `/store/products/{id}/reviews/` | POST | Create a review for a product | Authenticated |
| `/customers/me/` | GET, PUT | Retrieve or update customer profile | Authenticated |

*For a complete list of nested routes (e.g., `/store/products/{id}/reviews/`), check the `store/urls.py` file.*

---
## 🛠️ Installation & Setup

### Prerequisites
- Python 3.10+
- PostgreSQL
- pip

### Steps
1.  **Clone the repository**
    ```bash
    git clone https://github.com/your-username/django-storefront-api.git
    cd django-storefront-api
    ```

2.  **Create a virtual environment and activate it**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run migrations**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server**
    ```bash
    python manage.py runserver
    ```
    The API will be available at `http://localhost:8000/`. The Django admin site is at `http://localhost:8000/admin/`.
---
## 📁 Project Structure

```
django-storefront-api/
├── core/                         # Custom user model app
│   ├── models.py
│   ├── serializers.py
│   └── signals.py
├── likes/                        # Generic likes app
│   └── models.py
├── store/                        # Main e-commerce app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── permissions.py
│   └── signals.py
├── storefront/                   # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py
└── requirements.txt
```
---
## Key Workflows

### User Registration & Authentication Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant API as Django API
    participant DB as Database

    C->>API: POST /auth/users/ (username, email, password)
    API->>DB: Create new User
    DB-->>API: User created
    Note over API, DB: Signal: create_customer_for_new_user
    API->>DB: Create Customer profile
    API-->>C: 201 - User created

    C->>API: POST /auth/jwt/create/ (username, password)
    API->>DB: Validate credentials
    DB-->>API: Credentials valid
    API-->>C: 200 - Access & Refresh tokens
```
---
### Complete Purchase Sequence

```mermaid
sequenceDiagram
    participant C as Client (Auth User)
    participant V as View (OrderViewSet)
    participant S as Serializer (CreateOrderSerializer)
    participant M as Model (Order, OrderItem)
    participant Sig as Signals (order_created)
    participant CartM as Model (Cart, CartItem)

    Note over C, CartM: 1. Initiate Checkout
    C->>V: POST /store/orders/ { "cart_id": "uuid" }<br>(with JWT Header)

    Note over V, S: 2. Validation & Data Preparation
    V->>S: create(data, context={'user_id': request.user.id})
    S->>S: validate_cart_id(cart_id)
    S->>CartM: Check if cart exists & is not empty
    CartM-->>S: Validation Result
    S-->>V: is_valid()? → True

    Note over S, M: 3. Database Transaction
    S->>M: transaction.atomic()
    S->>M: Customer.objects.get(user_id=user_id)
    S->>M: Order.objects.create(customer=customer)
    S->>CartM: CartItem.objects.select_related('product').filter(cart_id=cart_id)
    S->>M: OrderItem.objects.bulk_create(order_items_list)
    S->>CartM: Cart.objects.filter(pk=cart_id).delete()

    Note over S, Sig: 4. Post-Creation Signal
    S->>Sig: order_created.send_robust(order=order)
    Sig-->>Sig: Execute any connected receivers<br>(e.g., send confirmation email task)

    Note over S, C: 5. Response
    S-->>V: Return Order instance
    V->>S: OrderSerializer(order)
    S-->>V: Serialized order data
    V-->>C: HTTP 201 Created<br>{ "id": 123, "customer": "...", "items": [...], ... }

```
---
## Data Model (ERD)

This diagram illustrates the core relationships between the main models in the application:

```mermaid
erDiagram
    USER ||--o{ CUSTOMER : extends
    USER {
        int id PK
        string username
        string email UK
        string password
    }
    CUSTOMER {
        int user_id PK,FK
        string phone
        date birth_date
        string membership
    }
    CUSTOMER ||--o{ ORDER : places
    ORDER {
        int id PK
        datetime placed_at
        char payment_status
        int customer_id FK
    }
    ORDER ||--o{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : referenced_in
    PRODUCT {
        int id PK
        string title
        string slug
        decimal unit_price
    }
    ORDER_ITEM {
        int id PK
        int order_id FK
        int product_id FK
        int quantity
        decimal unit_price
    }
    PRODUCT ||--o{ PRODUCT_IMAGE : has
    PRODUCT_IMAGE {
        int id PK
        int product_id FK
        image image
    }
    PRODUCT ||--o{ REVIEW : has
    REVIEW {
        int id PK
        int product_id FK
        string name
        text description
        date date
    }
    COLLECTION {
        int id PK
        string title
        int featured_product_id FK
    }
    COLLECTION ||--o{ PRODUCT : contains
    PRODUCT }o--o{ PROMOTION : has
    CART {
        uuid id PK
        datetime created_at
    }
    CART ||--o{ CART_ITEM : contains
    CART_ITEM {
        int id PK
        uuid cart_id FK
        int product_id FK
        int quantity
    }
    USER ||--o{ LIKED_ITEM : creates
    LIKED_ITEM {
        int id PK
        int user_id FK
        int content_type_id FK
        int object_id
    }

```
---
### Models Flowchart

```mermaid
flowchart TD
    subgraph A[Authentication & Core]
        direction TB
        User[core.User<br>extends AbstractUser<br>+ email: EmailField unique]
    end

    subgraph S[Store Models]
        direction TB
        Product[Product<br>+ title, slug, unit_price, etc.<br>+ collection: ForeignKey]
        Collection[Collection<br>+ title<br>+ featured_product: ForeignKey]
        Promotion[Promotion<br>+ description, discount]
        ProductImage[ProductImage<br>+ image: ImageField<br>+ product: ForeignKey]
        Review[Review<br>+ name, description, date<br>+ product: ForeignKey]
        
        Customer[Customer<br>+ phone, birth_date, membership<br>+ user: OneToOneField]
        Address[Address<br>+ street, city<br>+ customer: OneToOneField primary_key]
        
        Cart[Cart<br>+ id: UUIDField primary_key<br>+ created_at]
        CartItem[CartItem<br>+ quantity<br>+ cart: ForeignKey<br>+ product: ForeignKey]
        
        Order[Order<br>+ placed_at, payment_status<br>+ customer: ForeignKey]
        OrderItem[OrderItem<br>+ quantity, unit_price<br>+ order: ForeignKey<br>+ product: ForeignKey]
    end

    subgraph L[Likes Model]
        direction TB
        LikedItem[LikedItem<br>Generic Foreign Key<br>+ user: ForeignKey<br>+ content_type: ForeignKey<br>+ object_id: PositiveInteger<br>+ content_object: GenericForeignKey]
    end

    %% Define relationships
    User -->|OneToOne| Customer
    Customer -->|OneToOne| Address
    
    Customer -->|OneToMany| Order
    Order -->|OneToMany| OrderItem
    OrderItem -->|ManyToOne| Product
    
    Collection -->|OneToMany| Product
    Product -->|ManyToMany| Promotion
    Product -->|OneToMany| ProductImage
    Product -->|OneToMany| Review
    
    Cart -->|OneToMany| CartItem
    CartItem -->|ManyToOne| Product
    
    User -->|OneToMany| LikedItem
    LikedItem -->|Points to any model| Product
    LikedItem -->|Points to any model| Review
```
---
## Testing the API

Use a tool like **Postman** or **Thunder Client (VSCode)** to test the endpoints.

1.  **Register a User:**
    `POST /auth/users/`
    ```json
    {
      "username": "johndoe",
      "password": "securepassword123",
      "email": "john@example.com"
    }
    ```

2.  **Get JWT Tokens:**
    `POST /auth/jwt/create/`
    ```json
    {
      "username": "johndoe",
      "password": "securepassword123"
    }
    ```
    Use the returned `access` token in the `Authorization: Bearer <token>` header for subsequent requests.

3.  **Create an Order:**
    `POST /store/orders/`
    ```json
    {
      "cart_id": "a1b2c3d4-1234-5678-9abc-abcdef123456"
    }
    ```
---
## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the project.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

---

## Acknowledgments

- Built with [Django](https://www.djangoproject.com/) and [Django REST Framework](https://www.django-rest-framework.org/).
- Authentication powered by [Djoser](https://djoser.readthedocs.io/).
- Nested routing simplified with [DRF Nested Routers](https://github.com/alanjds/drf-nested-routers).
