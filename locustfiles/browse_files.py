from random import randint
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):

    wait_time = between(1, 5)
    host = "http://127.0.0.1:8000" 

    @task(2)
    def view_products(self):
        collection_id = randint(1, 3)
        self.client.get(f"/store/products/?collection_id={collection_id}", name="/store/products")

    @task(4)
    def view_product(self):
        product_id = randint(1, 3)
        self.client.get(f"/store/products/{product_id}", name="/store/products/:id")

    @task(1)
    def add_to_cart(self):
        product_id = randint(1,2)
        self.client.get(f"/store/carts/{self.cart_id}/items", name="/store/carts/items", json={"product_id": product_id, "quantity": 1})

    @task
    def say_hello(self):
        self.client.get("/playground/hello/")

    def on_start(self):
        response = self.client.post("/store/carts/")
        print("Cart creation response:", response.status_code, response.text)

        if response.status_code == 201:  # created
            try:
                result = response.json()
                self.cart_id = result["id"]
            except Exception as e:
                print("Failed to parse JSON:", e, "Response was:", response.text)
                self.cart_id = None
        else:
            print("Cart creation failed with status:", response.status_code)
            self.cart_id = None
