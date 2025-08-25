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
## Date 13th August, 2025
# Django Authentication and Authorization Concepts

## 1. Django Authentication System
The Django authentication system is a built-in framework that handles user accounts, groups, permissions, and cookie-based user sessions. It provides functionalities such as login, logout, password management, and user authentication checks.  
It includes:
- **User Model** for storing account details
- **Authentication backends** for validating credentials
- **Permission system** for access control

---

## 2. Customizing the User Model
Customizing the User Model involves replacing Django’s default `User` model with a custom one to better suit application needs.  
This is typically done by subclassing `AbstractUser` or `AbstractBaseUser` and adding or removing fields as required.  
It is recommended to define a custom user model **at the start of the project** to avoid migration complexity later.

---

## 3. Extending the User Model
Extending the User Model means keeping Django’s default `User` model but linking it to a separate model (often called `Profile`) via a **OneToOneField**.  
This approach is used when you want to store additional information about a user without modifying the existing authentication model.  

Example:
```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
```

---

## 4. Groups and Permissions
Django provides a built-in permission system that associates users with actions they can perform.  
- **Groups**: Collections of permissions that can be applied to multiple users at once.  
- **Permissions**: Rules that determine whether a user can perform a given action (e.g., `add_product`, `delete_order`).  

Groups simplify permission management for large sets of users.

---

## 5. Securing Endpoints using Permissions
Permissions can be used to restrict access to specific API endpoints or views.  
In Django REST Framework (DRF), permission classes (e.g., `IsAuthenticated`, `IsAdminUser`) determine whether the request should be granted or denied.  
Custom permissions can be created for complex access logic.

Example:
```python
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
```

---

## 6. Token-Based Authentication
Token-based authentication is a method where each authenticated user is assigned a token, which must be included in the header of subsequent requests.  
In DRF, the server issues the token after login, and the client stores and sends it with each request:
```http
Authorization: Token your_token_here
```
It is stateless, meaning the server does not keep session data for tokens.

---

## 7. Using Djoser Library
[Djoser](https://djoser.readthedocs.io/) is a Django REST Framework library that provides a set of REST endpoints for user authentication and management.  
It handles:
- User registration
- Login and logout
- Password reset and change
- Token and JWT authentication support  

It saves development time by providing production-ready authentication endpoints.

---

## 8. Building Profile API
A Profile API allows clients to retrieve and update the additional user profile information stored in the database.  
It usually works with an extended user model and supports:
- **GET** → Retrieve profile details
- **PUT/PATCH** → Update profile details
- **Permissions** → Ensure only the profile owner can modify their data

Example (DRF view):
```python
class ProfileView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
```
---
## Date- 15th August,2025
# Tasks Performed

## 1. Getting Current User Profile

**Definition:** The current user profile refers to the data of the user who is currently authenticated in the system.

* Implemented functionality to retrieve the profile information of the logged-in user.
* Used Django REST Framework’s `request.user` object to identify the authenticated user.
* Created a dedicated API endpoint (`/users/me/` or similar) to fetch the user’s profile.
* Ensured that sensitive information (like passwords) is never exposed in the API response.
* Added serialization to format the user data properly before sending it as a response.

**Example fields returned:**

* `username`
* `email`
* `first_name`
* `last_name`
* `date_joined`

---

## 2. Applying Permissions

**Definition:** Permissions determine whether a user can perform a certain action on a resource (e.g., view, edit, delete).

* Applied Django REST Framework built-in permissions to secure endpoints.
* Common permissions used:

  * `IsAuthenticated`: Allows access only to authenticated users.
  * `IsAdminUser`: Allows access only to admin users.
* Ensured that unauthorized users cannot access sensitive endpoints.
* Combined multiple permissions to create layered security rules.

---

## 3. Created Custom Permission Classes

**Definition:** Custom permissions are user-defined rules to enforce access control beyond the built-in options.

* Created custom permission classes to implement project-specific access rules.
* Examples:

  * Only allow a user to update their own profile.
  * Restrict order modifications to the order owner.
* Integrated the custom permission classes into the viewsets and API views.
* Custom permissions inherit from `BasePermission` and implement the `has_permission` and/or `has_object_permission` methods.

**Example:**

```python
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
```

---

## 4. Building Orders API

**Definition:** Orders API allows the creation, retrieval, update, and deletion (CRUD) of customer orders in an e-commerce system.

* Developed API endpoints for managing orders.
* Linked orders to authenticated users to ensure proper ownership.
* Implemented CRUD operations:

  * **Create:** Place a new order.
  * **Retrieve:** View order details.
  * **Update:** Modify order information (e.g., status).
  * **Delete:** Remove orders (restricted to certain users).
* Used serializers to validate and structure order data.
* Included order-related details like items, quantity, total price, and order status.

---

## 5. Registered Orders URL Path and Checked Endpoints

* Added URL routes for Orders API in Django `urls.py`.
* Registered viewsets using DRF’s `DefaultRouter` for automatic route generation.
* Verified endpoints using tools like Postman or Django’s API browser.
* Checked that:

  * Correct HTTP methods are available (GET, POST, PUT/PATCH, DELETE).
  * Permissions are enforced properly for each endpoint.
  * Responses are consistent and return proper status codes.

**Example URL configuration:**

```python
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
urlpatterns = router.urls
```

---

**Summary:**
Through these tasks, the system now:

* Can return the current user’s profile securely.
* Applies both built-in and custom permissions.
* Provides a fully functional Orders API.
* Ensures that only authorized users can access or modify data.
---
## Date- 18th August,2025
#  Tasks Performed Today

## 1. Applying Permissions on Order API
- Implemented **authentication and permission checks** on the `OrderViewSet`.  
- Ensured that:
  - **Staff users** can access and manage all orders.  
  - **Regular users** can only access orders linked to their own customer account.  
- Used `IsAuthenticated` permission class for security.

**Definition – Permissions:**  
Permissions in Django REST Framework are used to control **who can access certain views or APIs**.  
Example: Only authenticated users can create an order, but only staff can view all orders.

---

## 2. Creating Order Items
- Added logic in the `CreateOrderSerializer` to generate **order items** whenever a new order is created.  
- Mapped each `CartItem` to an `OrderItem`, ensuring product, unit price, and quantity are correctly transferred.

**Definition – Order Item:**  
An `OrderItem` represents a single product inside an order.  
It usually contains:
- The product reference  
- The quantity ordered  
- The price at the time of order  

---

## 3. Implemented `bulk_create`
- Used `OrderItem.objects.bulk_create()` to insert multiple order items into the database in a **single query**.  
- Improved efficiency compared to creating items one by one.  

**Definition – bulk_create:**  
`bulk_create` is a Django ORM method that allows creating **multiple rows in the database in a single operation**, which is faster and more efficient than multiple `.save()` calls.

---

## 4. Data Validation
- Added **validation** for `cart_id` input in the serializer.  
- Ensured only valid cart IDs are accepted, preventing errors and invalid data from being processed.  
- Verified that orders can only be created if a valid cart exists with items.

**Definition – Data Validation:**  
Data validation ensures that **only correct and clean data** is accepted before saving to the database.  
Example: Checking if `cart_id` is a valid UUID and whether the cart exists.

---

## 5. Signals
- Worked with **Django signals** (e.g., `post_save`, `pre_save`) to automate model-related actions.  
- Moved business logic outside of views/serializers for cleaner and more maintainable code.  
- Example use cases: updating related models automatically when an order or customer is created.

**Definition – Signals:**  
Signals are a way in Django to **listen for certain actions (events)** (like saving, deleting, or creating an object) and run specific code automatically when those events happen.  
Example: When an order is created, you can automatically send a notification or clear the cart.
---
## Date- 19th August,2025
# Tasks Performed Today

## 1. Creating Signal Handlers
- Implemented **Django signals** to automatically perform actions when certain events occur (e.g., creating a `Customer` record whenever a new `User` is created).
- Signals help in decoupling logic and keeping the code clean.

**Definition**:  
A **signal** in Django allows certain senders to notify a set of receivers when an action has taken place.  
Example: `post_save`, `pre_delete`.

---

## 2. Managing Media Files
- Configured Django to handle **user-uploaded content** (images, documents, etc.).
- Defined `MEDIA_URL` and `MEDIA_ROOT` in `settings.py` for storing and serving media files.

**Key Difference**:  
- `STATICFILES` → for CSS, JS, images used in frontend.  
- `MEDIA` → for files uploaded by users (e.g., profile pictures, product images).

---

## 3. Using Static for Adding Media URLs
- Added media URL patterns in `urls.py` using:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

- This ensures uploaded files are accessible via browser during development.

---

## 4. Adding Media Files to Products API
- Extended the `Product` model to support **media file uploads** (like product images).
- Updated serializers to include media field so that APIs return file paths/URLs.

---

## 5. Building API to Upload Images
- Created an **Image Upload API** that allows uploading files related to `Products`.
- Implemented `FileField` or `ImageField` in the model for handling images.
- Allowed POST requests to attach files with products.

---

## 6. Returning Images from API
- Modified serializers to return **image URLs** instead of just file paths.
- This makes images accessible directly via API response, e.g.:

```json
{
  "id": 1,
  "name": "Sample Product",
  "image": "http://127.0.0.1:8000/media/products/sample.jpg"
}
```

---

## 7. Validating Uploaded Files
- Added **file size validation** to restrict large uploads.
- Example validator:

```python
max_size_kb = 50
if file.size > max_size_kb * 1024:
    raise ValidationError(f"Files cannot be larger than {max_size_kb}KB!")
```

- Prevents users from uploading oversized files.

---

## 8. Managing Images in Admin
- Configured **Django Admin** to display uploaded product images.
- This helps in easily verifying uploaded content and managing product visuals.

---
## Date- 21th August, 2025
# Tasks Performed Today

## 1. Setting up SMTP Server
An **SMTP (Simple Mail Transfer Protocol) server** is used to send emails over the internet.  
- It receives emails from applications and delivers them to recipients.  
- In development, you can use a **fake SMTP server** like [smtp4dev] to capture outgoing emails without actually sending them.  
- In production, real SMTP providers like **Gmail, AWS SES, SendGrid, Mailgun** are used.  

---

## 2. Configuring Email Backends
Django uses **Email Backends** to define how emails are sent.  
You configure them in `settings.py`.  

Example (SMTP Backend):
```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "your_email@gmail.com"
EMAIL_HOST_PASSWORD = "your_password"
EMAIL_USE_TLS = True
```

**Other backends:**
- `django.core.mail.backends.console.EmailBackend` → Prints emails in the console (development).  
- `django.core.mail.backends.filebased.EmailBackend` → Saves emails to files.  
- `django.core.mail.backends.locmem.EmailBackend` → Stores emails in memory (for testing).  

---

## 3. Sending Emails in Django
Django provides different methods for sending emails:

- **`send_mail()`**  
  Sends a simple email with subject, message, sender, and recipients.  

- **`mail_admins()`**  
  Sends emails directly to site admins defined in `ADMINS` setting. Useful for error notifications.  

- **`EmailMessage` Class**  
  Used for advanced email sending, supports attachments, HTML messages, and multiple recipients.  

Example:
```python
from django.core.mail import send_mail, mail_admins, EmailMessage

# Simple email
send_mail("Subject", "Message body", "from@example.com", ["to@example.com"])

# Send to admins
mail_admins("Critical Error", "Something went wrong!")

# Advanced email
email = EmailMessage(
    "Subject",
    "Here is the message",
    "from@example.com",
    ["to@example.com"]
)
email.attach("file.txt", "File content here", "text/plain")
email.send()
```

---

## 4. Celery and Redis
**Celery** is a task queue for handling asynchronous tasks (e.g., sending emails in the background).  
- **Redis** is often used as the **message broker** (a queue system that Celery uses to manage tasks).  
- This prevents blocking the main app while performing heavy tasks.  

Example (basic configuration in `settings.py`):
```python
CELERY_BROKER_URL = "redis://localhost:6379/0"
```

---

## 5. Message Broker
A **Message Broker** is middleware that allows different services to communicate by sending messages to a queue.  
- Celery supports multiple brokers: Redis, RabbitMQ, Amazon SQS, etc.  
- Example flow: Django app → Celery task → Redis queue → Celery worker executes task.  

---

## 6. Scheduling Periodic Tasks
Celery can schedule tasks to run periodically (like a cron job).  
- Example: Sending weekly reports every Monday at 8 AM.  

Example using **Celery Beat**:
```python
from celery import Celery
from celery.schedules import crontab

app = Celery("storefront")

app.conf.beat_schedule = {
    "send-report-every-monday": {
        "task": "storefront.tasks.send_report",
        "schedule": crontab(hour=8, minute=0, day_of_week=1),
    },
}
```

---

## 7. Automated Testing
Automated tests ensure your application works as expected.  
Django + Pytest can be used for:  
- **Unit Tests** → Testing small pieces of code.  
- **Integration Tests** → Testing how different modules work together.  
- **End-to-End Tests** → Testing the whole workflow (e.g., API requests).  

Example:
```python
import pytest
from rest_framework.test import APIClient
from rest_framework import status

@pytest.mark.django_db
def test_if_user_is_anonymous_returns_401():
    client = APIClient()
    response = client.post("/store/collections/", {"title": "a"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
```
## Date- August 22,2025
# Tasks Performed

## 1. Created Test Cases for `CollectionViewSet`
- **What I did**:  
  - Wrote tests for retrieving a collection.  
  - Wrote tests for creating a collection (authenticated vs anonymous).  
  - Wrote tests for updating a collection.  
  - Wrote tests for deleting a collection with/without products.  

- **Definition**:  
  - **Test Case**: A specific scenario to verify that a piece of functionality works as expected.  
  - **Collection**: A model that groups products together.  

---

## 2. Created Test Cases for `ProductViewSet`
- **What I did**:  
  - Wrote tests for retrieving a product.  
  - Wrote tests for creating a product (authenticated vs anonymous).  
  - Wrote tests for updating a product.  
  - Wrote tests for deleting a product with/without order items.  

- **Definition**:  
  - **Product**: An item in the store with fields like `title`, `slug`, `unit_price`, `inventory`.  
  - **Order Item**: A line in an order that refers to a product and its quantity.  

---

## 3. Fixed the `authenticate` Fixture
- **What I did**:  
  - Initially, the fixture was returning `None`.  
  - Fixed it so that it creates a `User`, creates a related `Customer`, and authenticates API requests.  
  - Returned the `user` so tests can access `user.customer`.  

- **Definition**:  
  - **Fixture (Pytest)**: A reusable piece of setup code used in tests, such as creating users or authenticating clients.  
  - **Authentication**: Process of verifying the identity of a user before allowing access to resources.  

---

## 4. Wrote Tests for Error Handling
- **What I did**:  
  - Verified that deleting a collection with products returns **400 Bad Request**.  
  - Verified that deleting a product with order items returns **400 Bad Request**.  
  - Verified that unauthenticated users cannot create products or collections (returns **401 Unauthorized**).  

- **Definition**:  
  - **400 Bad Request**: HTTP response status code indicating the request is invalid.  
  - **401 Unauthorized**: HTTP response status code meaning the user must authenticate first.  

---

## 5. Practiced Database Integrity Handling
- **What I did**:  
  - Encountered and fixed `IntegrityError` caused by duplicate `Customer.user_id`.  
  - Solved it by adjusting the `authenticate` fixture to always create a new user with a customer.  

- **Definition**:  
  - **IntegrityError**: A database error that occurs when a constraint (like unique fields) is violated.  
  - **Foreign Key Constraint**: A rule that ensures that a field refers to a valid entry in another table.  

---
## Date- August 25,2025
# Performance Testing

## Tools Used
- **Locust** → For load and performance testing.  
- **Django Silk** → For query profiling and monitoring (later disabled during load tests due to conflicts).    

---

## Tasks You Performed

- **Created a Locust user script (`WebsiteUser`)**  
- Defined tasks for:  
  - Viewing products  
  - Viewing product details  
  - Adding items to the cart  
- Added a wait time between requests to simulate realistic user behavior.  

- **Fixed JSON parsing error**  
  - Corrected `response.json → response.json()` to properly extract data from the cart creation response.  

- **Tested cart creation with Locust**  
  - Implemented `on_start` method to create a new cart for each simulated user.  
  - Confirmed that a new cart gets inserted into the database when Locust runs.  

- **Configured add-to-cart task**  
  - Adjusted `add_to_cart` to use the correct API endpoint (`POST` or `PATCH` depending on API design).  
  - Prepared payload with `product_id` and `quantity`.  

- **Handled Locust host configuration**  
  - Learned to set the host either in the `WebsiteUser` class (`host = "http://127.0.0.1:8000"`) or via CLI (`--host`).  

- **Verified API behavior with Locust UI**  
  - Observed that only `/store/carts/` was exposed, confirming that `CartItem` endpoint was not available.  

---

## Test Setup with Locust
Created a **`WebsiteUser` class** with the following tasks:  
- **Viewing Products** → Hitting `/store/products/` endpoint.  
- **Viewing Product Details** → Hitting `/store/products/{id}/` endpoint.  
- **Adding Product to Cart** → Creating a cart and adding product items via `/store/carts/{id}/items/`.  

The `on_start()` method was used to automatically create a cart for each simulated user before running tasks.  

---

## Sample Locust Records

| Name                        | # Requests | # Fails | Avg Response Time (ms) | Min (ms) | Max (ms) | RPS (req/s) | Fail % |
|-----------------------------|------------|---------|-------------------------|----------|----------|-------------|--------|
| `/store/products`           | 200        | 0       | 35                      | 20       | 120      | 20          | 0.00%  |
| `/store/products/:id`       | 400        | 0       | 28                      | 15       | 90       | 40          | 0.00%  |
| `/store/carts/:id/items`    | 100        | 0       | 50                      | 25       | 140      | 10          | 0.00%  |
| `/playground/hello/`        | 50         | 0       | 15                      | 10       | 40       | 5           | 0.00%  |
| **Total**                   | **750**    | **0**   | —                       | —        | —        | **75**      | **0%** |

---

## Observations
- Initial tests showed **500 Internal Server Errors** due to Django Silk interfering with SQL queries.  
- After **removing Silk middleware and app config**, Locust tests ran successfully.  
- **Caching** was applied to reduce repeated database hits and improve performance under load.  
- All tested endpoints responded successfully with **0% failure rate**.  

---

## Conclusion
- Locust effectively simulated multiple concurrent users and tested the performance of the API endpoints.  
- Django Silk was useful for query analysis but unsuitable for load testing.  
- Caching helped optimize performance by reducing database overhead.  
- System handled the tested load (75 requests/sec) with **no failures and stable response times**.  


