import pytest
from rest_framework import status
from model_bakery import baker

from core.models import User
from store.models import Customer, Order, OrderItem, Product

@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        return api_client.post("/store/products/", product)
    return do_create_product


@pytest.mark.django_db
class TestCreateProduct:
    def test_if_user_is_anonymous_returns_401(self, create_product):
        response = create_product({'title': 'a', 'slug': 'a', 'description': 'a', 'unit_price': 22, 'inventory': 2, 'collection': 1})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, create_product, authenticate):
        authenticate()

        response = create_product({'title': 'a', 'slug': 'a', 'description': 'a', 'unit_price': 22, 'inventory': 2, 'collection': 1})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, authenticate, create_product):
        authenticate(is_staff=True)

        response = create_product({'title': '', 'slug': '', 'description': '', 'unit_price': 22, 'inventory': 2, 'collection': 1})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_200(self, authenticate, create_product):
        authenticate(is_staff=True)

        response = create_product({'title': 'a', 'slug': 'a', 'description': 'a', 'unit_price': 22, 'inventory': 2, 'collection': 1})

        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestRetriveProduct:

    def test_if_product_exists_returns_200(self, api_client):
        product = baker.make(Product)
        response = api_client.get(f"/store/products/{product.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == product.id
        assert response.data['title'] == product.title

    def test_if_product_does_not_exists_returns_404(self, api_client):
        response = api_client.get("/store/products/999/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_product_list_exists_returns_empty_list(self, api_client):
        response = api_client.get('/store/products/')

        assert response.status_code == status.HTTP_200_OK

    def test_if_product_lists_exists_returns_200(self, api_client):
        baker.make(Product, _quantity=3)

        response = api_client.get('/store/products/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3


@pytest.mark.django_db
class TestUpdateProduct:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.patch("/store/products/1/", {'title': 'a', 'slug': 'a', 'description': 'a', 'unit_price': 22, 'inventory': 2, 'collection': 1})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_not_admin_returns_403(self, authenticate, api_client):
        authenticate(is_staff=False)

        response = api_client.patch("/store/products/1/", {'title': 'a', 'slug': 'a', 'description': 'a', 'unit_price': 22, 'inventory': 2, 'collection': 1})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_product_does_not_exist_returns_404(self, authenticate, api_client):
        authenticate(is_staff=True)

        response = api_client.patch("/store/products/999/", {'title': 'a', 'slug': 'a', 'description': 'a', 'unit_price': 22, 'inventory': 2, 'collection': 1})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_admin_updates_product_returns_200(self, authenticate, api_client):
        authenticate(is_staff=True)
        product = baker.make(Product)

        response = api_client.patch(f'/store/products/{product.id}/', {'title': 'New Title'})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == "New Title"


@pytest.mark.django_db
class TestDestroyProduct:

    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.delete('/store/products/999/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_admin_returns_403(self, authenticate, api_client):
        authenticate()

        response = api_client.delete('/store/products/1/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_product_has_orderitem_returns_400(self, authenticate, api_client):
        authenticate(is_staff=True)

        product = baker.make(Product)

        customer_user = baker.make('core.User', _fill_optional=True)
        customer = Customer.objects.get(user=customer_user)

        order = baker.make(Order, customer=customer)
        baker.make(OrderItem, order=order, product=product)

        response = api_client.delete(f'/store/products/{product.id}/')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == 'Cannot delete product with associated order items.'

    def test_if_product_has_no_orderitem_returns_204(self, authenticate, api_client):
        authenticate(is_staff=True)

        product = baker.make(Product)

        response = api_client.delete(f"/store/products/{product.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
    

    