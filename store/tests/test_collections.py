import pytest
from rest_framework import status
from model_bakery import baker
from store.models import Collection, Product

@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collections/', collection)
    return do_create_collection


@pytest.mark.django_db
class TestCreateCollection:

    def test_if_user_is_anonymous_returns_401(self, create_collection):
        #AAA(Arrange, Act, Assert)

        response = create_collection({"title": "a"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, create_collection, authenticate):
        authenticate()

        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, create_collection, authenticate):
        authenticate(is_staff=True)
        response = create_collection({'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_returns_201(self, create_collection, authenticate):
        authenticate(is_staff=True)
        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetriveCollection:
    def test_if_collection_exists_returns_200(self, api_client):

        collection = baker.make(Collection)


        response = api_client.get(f'/store/collections/{collection.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'product_count': 0,
        }

    def test_if_collection_does_not_exists_returns_404(self, api_client):
        response = api_client.get(f'/store/collections/99/')

        assert response.status_code == status.HTTP_404_NOT_FOUND
    

    def test_if_collection_list_exists_returns_empty_list(self, api_client):
        response = api_client.get('/store/collections/')

        assert response.status_code == status.HTTP_200_OK

    def test_if_collection_list_exists_returns_200(self, api_client):
        Collection.objects.all().delete()

        baker.make(Collection, _quantity=3)

        response = api_client.get(f'/store/collections/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3


@pytest.mark.django_db
class TestUpdateCollection:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.patch('/store/collections/1/', {'title': 'New title'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client, authenticate):
        authenticate(is_staff=False)
        collection = baker.make(Collection)

        response = api_client.patch(f"/store/collections/{collection.id}/", {'title': 'New Title'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_collection_does_not_exist_returns_404(self, api_client, authenticate):
        authenticate(is_staff=True)

        response = api_client.patch("/store/collections/999/", {"title": "New Title"})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_admin_updates_collection_returns_200(self, api_client, authenticate):
        authenticate(is_staff=True)
        collection = baker.make(Collection)

        response = api_client.patch(f"/store/collections/{collection.id}/", {"title": "New Title"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'New Title'



@pytest.mark.django_db
class TestDestroyCollection:
    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.delete('/store/collections/1/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client, authenticate):
        authenticate(is_staff=False)
        collection = baker.make(Collection)

        response = api_client.delete(f'/store/collections/{collection.id}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_collection_does_not_exist_returns_404(self, api_client, authenticate):
        authenticate(is_staff=True)

        response = api_client.delete(f'/store/collections/999/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_collection_has_no_products_returns_204(self, api_client, authenticate):
        authenticate(is_staff=True)
        collection = baker.make(Collection)

        response = api_client.delete(f'/store/collections/{collection.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_collection_has_products_returns_400(self, api_client, authenticate):
        authenticate(is_staff=True)
        collection = baker.make(Collection)
        baker.make(Product, collection=collection)

        response = api_client.delete(f"/store/collections/{collection.id}/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST