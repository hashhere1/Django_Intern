### What is Django?

Django is a **high-level Python web framework** that allows developers to build secure, maintainable websites quickly. It follows the **"batteries-included" philosophy**, meaning it comes with a wide range of built-in features such as authentication, admin panel, ORM (Object-Relational Mapping), form handling, and more.

Django is built on the **MVC (Model-View-Controller)** pattern, although in Django it's referred to as **MTV (Model-Template-View)**:
- **Model** – Defines the data structure and interacts with the database.
- **Template** – Defines how data is presented to the user (HTML pages).
- **View** – Contains the logic to process requests and return responses.

#### Key Features of Django:
- **Rapid Development**: You can build web apps quickly with Django’s built-in tools.
- **Security**: Protects against common attacks like SQL injection, XSS, CSRF, etc.
- **Scalability**: Used by big platforms like Instagram and Pinterest.
- **Admin Interface**: Comes with a powerful, auto-generated admin panel for managing content.
- **ORM**: Lets you interact with the database using Python code instead of SQL.

---
# Daily Progress Report

## Date: August 4, 2025

### Topics Covered
- Introduction to Django
- Understanding Django apps and their role in project structure
- Basic Django commands and project navigation

###  Tasks Completed

- **Learned the basics of Django**  

- **Created three Django apps:**
  - `playground`
  - `store`
  - `tags`

  > *In Django, an app is a Python package that contains a specific functionality (e.g., a blog, a store). A project can contain multiple apps. e.g. a component in website is an app*

- **Installed and configured `django-debug-toolbar`**  
  This is a powerful tool for developers that shows detailed debug information right in your browser. It helps with analyzing SQL queries, cache usage, template rendering time, and more.

- **Updated project `settings.py`**
  - Added the new apps to `INSTALLED_APPS`
  - Configured settings required for `django-debug-toolbar` to work properly

- **Created models in the `store` app:**
  - `Product` – Represents an item available for sale, typically includes fields like name, price, and description.
  - `Customer` – Represents a user or buyer, with fields like name and contact details.
  - `Order` – Represents a purchase record, connecting customers and products with details like quantity and date.

  > *In Django, models are Python classes that define the structure of your database tables. Each model maps to a single table. e.g. a whole website is a project*

- **Learned and practiced basic Django commands:**
  - `django-admin startproject` – To create a new Django project
  - `python manage.py startapp` – To create a new app within a Django project
  - `python manage.py makemigrations` – To create new database migrations based on model changes
  - `python manage.py migrate` – To apply migrations and create/update database tables
  - `python manage.py runserver` – To start the development server
  - `python manage.py shell` – To open an interactive shell with project context

### Skills Learned
- How Django projects and apps are organized
- Writing Django models and understanding their relationship with databases
- Using `django-debug-toolbar` for better development insights
- Executing common Django commands to manage apps and data

### Tools Used
- Django (Python web framework)
- django-debug-toolbar (debugging utility)

---
## Date: August 5, 2025
# Task List with Explanations

- **Added one-to-one and one-to-many relationships between different models**  
  Defined how different models relate to each other using Django’s ORM relationships.  
  - *One-to-one*: Each instance of a model is linked to exactly one instance of another model.  
  - *One-to-many*: One model instance can be related to multiple instances of another model (e.g., one Customer has many Orders).

- **Created a new app named _likes_**  
  Used Django’s `startapp` command to create a separate app for managing likes functionality, keeping the project modular and organized.

- **Created a database in MySQL**  
  Set up a new MySQL database to store the project’s data.

- **Configured the MySQL database attributes in `settings.py`**  
  Added database connection settings (like database name, user, password, host, and port) in the Django `settings.py` file to enable communication with the MySQL database.

- **Checked the data using DataGrip**  
  Used DataGrip, a database management tool, to connect to MySQL and verify the data and schema.

- **Made migrations for the changes**  
  Ran Django management commands to generate and apply database migrations reflecting the updated models and relationships.

- **Added mock data**  
  Created sample data to populate the database for testing and development purposes.

  # Django Models Overview

- **Promotion**  
  Stores promotion details like description and discount.

- **Product**  
  Represents products with fields like title, price, inventory, linked to one collection and multiple promotions.

- **Customer**  
  Stores customer info including name, email, phone, birth date, and membership level.

- **Order**  
  Records customer orders with timestamp and payment status.

- **OrderItem**  
  Details products and quantities within an order.

- **Address**  
  Stores customer address; each customer has exactly one address.

- **Collection**  
  Groups products into categories with an optional featured product.

- **Cart**  
  Represents a shopping cart with creation time.

- **CartItem**  
  Items in a cart, linking products and quantities.

### Relationships:
- One-to-many: Collection → Product, Customer → Order, Order → OrderItem, Cart → CartItem  
- One-to-one: Customer → Address  
- Many-to-many: Product ↔ Promotion
---
## Date: August 7, 2025
# Task List with Explanations

## Expressions in Django ORM

Django provides several expression types to allow complex queries directly in the ORM.

### • Value
Used to represent a literal value in queries, often with annotations.

```python
from django.db.models import Value
from django.db.models.functions import Concat

# Example: Add static string in a query
qs = Author.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name'))
```

---

### • F
`F()` expressions are used to refer to model field values directly in queries, allowing operations without fetching them into Python.

```python
from django.db.models import F

# Example: Increase all product prices by 10
Product.objects.update(price=F('price') + 10)
```

---

### • Func
`Func` allows use of SQL functions within queries.

```python
from django.db.models import Func

# Example: UPPER SQL function
Author.objects.annotate(upper_name=Func(F('name'), function='UPPER'))
```

---

### • Aggregate (Count, Sum, etc.)
Used to perform calculations on a queryset.

```python
from django.db.models import Count, Sum

# Example: Total price of all products
total = Product.objects.aggregate(Sum('price'))

# Example: Number of orders per user
User.objects.annotate(order_count=Count('orders'))
```

---

### • ExpressionWrapper
Used when combining expressions where a specific output field type must be declared.

```python
from django.db.models import ExpressionWrapper, FloatField

qs = Product.objects.annotate(
    discounted_price=ExpressionWrapper(F('price') * 0.9, output_field=FloatField())
)
```

---

### • Content-type
Django provides `ContentType` framework for generic relationships across models.

```python
from django.contrib.contenttypes.models import ContentType

# Get content type of a model
content_type = ContentType.objects.get_for_model(MyModel)
```

---

## CRUD Operations

### Insert
Creating and saving new records:

```python
product = Product(title='Shirt', price=500)
product.save()
```

Or using `create()`:

```python
Product.objects.create(title='Pant', price=800)
```

---

### Update
Updating existing records:

```python
Product.objects.filter(id=1).update(price=600)
```

---

### Delete
Deleting records:

```python
Product.objects.get(id=1).delete()
```

---

## Transaction Logic

Transactions ensure a group of operations are atomic (all or nothing).

```python
from django.db import transaction

with transaction.atomic():
    order = Order.objects.create(customer=customer)
    Payment.objects.create(order=order, amount=500)
    # Any error here rolls back the whole block
```

Use `transaction.atomic()` to manage database consistency in critical operations.

---

## Date- 08 August,2025
# Django Admin Enhancements

## 1. Added Tag Inline to Product
- Created `TagInLine` using `GenericTabularInline` for managing tags linked to products.
- Enabled `autocomplete_fields` for faster tag selection.

## 2. Customized Product Admin
- **Actions**:
  - Added `clear_inventory` action to bulk set product inventory to `0`.
  - Display a success/error message after execution using `self.message_user()`.
- **Display Fields**:
  - `collection_title` → Shows related collection name.
  - `inventory_status` → Displays `"Low"` if inventory < 10, else `"OK"`.
- **Features**:
  - Autocomplete for `collection` field.
  - Search by `title`.
  - Prepopulate `slug` from `title`.
  - Inline tag management (`TagInLine`).
  - Inline editing of `unit_price`.
  - List filter by `collection` and `last_update`.

## 3. Customized Customer Admin
- Added `orders` column showing the number of orders placed by the customer.
- Made order count clickable, linking to filtered order list for that customer.
- Enabled search by first and last name (case-insensitive, startswith).
- Annotated queryset with `orders` count using `Count("order")`.

## 4. Customized Collection Admin
- Added `product_count` column showing the number of products in the collection.
- Made product count clickable, linking to filtered product list by collection.
- Enabled search by `title`.
- Annotated queryset with `product_count` using `Count("product")`.

## 5. Enhanced Order Admin
- Added `OrderItemInLine` for inline editing of order items within orders.
- Autocomplete for `product` in order items.
- Set constraints: `min_num=1`, `max_num=10`, `extra=0` (no empty extra rows).
- Enabled autocomplete for `customer` in orders.

## 6. Overall Improvements
- Used `@admin.display(ordering=...)` for sortable custom columns.
- Used `reverse()` + `urlencode()` + `format_html()` to create clickable links in list displays.
- Leveraged `list_select_related` to optimize queries for related objects.
---
## Date- 11th August, 2025
# Storefront Project Features

Implements a basic storefront API to manage products and collections with CRUD operations, validation, query optimizations, error handling, and clean serialization.

---

## Product Management

- **List Products:** Get all products with related collection.
- **Create Product:** Add a new product with validation.
- **Retrieve Product:** Get product details by ID.
- **Update Product:** Modify an existing product.
- **Delete Product:** Block deletion if linked to order items.

---

## Collection Management

- **List Collections:** Get all collections with `product_count`.
- **Create Collection:** Add a new collection.
- **Retrieve Collection:** Get collection details with `product_count`.
- **Update Collection:** Modify an existing collection.
- **Delete Collection:** Block deletion if it contains products.

---

## Serialization

-  **Definition:** Serializes product data, including a calculated `price_with_tax` field.  
  **Explanation:** Converts product objects into JSON-friendly format and adds extra computed fields.
- **CollectionSerializer:** Formats collection data with `product_count`.

---

## Query Optimization

- **select_related:** Fetch related collection with products in fewer queries.
- **annotate + Count:** Calculate product counts efficiently.

---

## Error Handling

- Returns proper HTTP codes and messages for invalid actions  
  (e.g., deleting a product with orders or a collection with products).
---
## Date 12th August, 2025
## Tasks Performed Today

### 1. Worked with **Generic Views** in Django REST Framework
- **`ListCreateAPIView`**  
  - Combined two operations into one view:
    - **List** (`GET`): Retrieve and return a list of all objects from the database.
    - **Create** (`POST`): Accept JSON input, validate it using a serializer, and store it as a new database entry.
  - Useful for resources where you often need both listing and creation from the same endpoint.
  
- **`RetrieveUpdateDestroyAPIView`**  
  - Handles single object operations:
    - **Retrieve** (`GET`): Return the details of one resource.
    - **Update** (`PUT` / `PATCH`): Modify existing data.
    - **Destroy** (`DELETE`): Remove a resource from the database.
  - Helps avoid repetitive boilerplate code by combining three actions in one class.

- **`ModelViewSet`**  
  - Provides **all CRUD operations** automatically when paired with DRF routers.
  - Eliminates the need to define individual views for listing, creating, retrieving, updating, and deleting objects.

---

### 2. Implemented **Routers**
- Used **SimpleRouter** and **Nested Routers** to auto-generate URL patterns for viewsets.
- Reduced the amount of manual URL configuration in `urls.py`.
- Nested routers allowed creation of endpoints such as:
  - `/products/{product_id}/reviews/` → reviews linked to a specific product.

---

### 3. Built **Serializers**
- Created serializers in `serializers.py` for multiple models:
  - **ProductSerializer** — converts `Product` model instances to JSON and validates product data when creating/updating.
  - **ReviewSerializer** — handles serialization for reviews, including mapping a product foreign key.
  - **CartSerializer** & **CartItemSerializer** — serialize cart data along with related cart items and their products.
- Used nested serializers to include related objects in responses (e.g., showing product details inside a cart item).
- Added `read_only` fields for IDs to ensure they are not editable by API users.

---

### 4. Created **View Functions / Viewsets**
- Implemented class-based viewsets (`ModelViewSet`, `GenericViewSet` with mixins) to handle API logic.
- Linked each viewset to its corresponding serializer and queryset.
- Configured `lookup_field` for UUID-based models like `Cart` to support URLs such as:
- Used `CreateModelMixin`, `RetrieveModelMixin`, and others as needed for different endpoints.

---

### 5. Built **Reviews API**
- Designed API endpoints to:
- List all reviews for a given product.
- Create a new review for a specific product.
- Used nested routing so reviews are tied directly to a product ID.
- Implemented serializer context to pass `product_id` into the `ReviewSerializer` during creation.

---

### 6. Applied **Data Filtering**
- Used `DjangoFilterBackend` to filter results based on query parameters.
- Example:  
- Filtering made the API more flexible and allowed users to retrieve targeted subsets of data.

---

### 7. Implemented **Sorting**
- Enabled ordering via query parameters using DRF’s `OrderingFilter`.
- Examples:
- Allowed multiple ordering criteria (e.g., `ordering=price,title`).

---

### 8. Learned about **GUID / UUID**
- **GUID**: Globally Unique Identifier — ensures each value is unique across time and space.
- Implemented using Django’s `UUIDField` for models like `Cart`.
- Benefits:
- Secure and harder to guess than integer IDs.
- Prevents collisions when merging data from multiple sources.
- Example:

---

### 9. Built **Cart API** with CRUD Operations
- Endpoints:
- **Create** (`POST /carts/`) — generates a new empty cart.
- **Retrieve** (`GET /carts/{uuid}/`) — returns cart details with all items.
- **Update** (`PATCH /carts/{uuid}/`) — modify cart items.
- **Delete** (`DELETE /carts/{uuid}/`) — remove the entire cart.
- Added related cart item management:
- Add new products to the cart.
- Update quantity of existing cart items.
- Remove items from the cart.

---

### 10. Calculated **Total Price** of Cart
- Added a calculated field in the serializer to sum the price of all cart items:
- Ensured this calculation is done dynamically so it always reflects the current cart contents.
- Returned the total price in the API response to improve user experience.

---

### 11. Debugging & Fixes
- Fixed `404` error for retrieving carts by adding `RetrieveModelMixin` to `CartViewSet`.
- Fixed `'Product' object is not iterable` error by removing `many=True` from `ProductSerializer` inside `CartItemSerializer` because each cart item references a **single** product.
---
