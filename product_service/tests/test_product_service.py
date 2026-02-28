import uuid

from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status


async def test_health(client: AsyncClient, fastapi_app: FastAPI) -> None:
    url = fastapi_app.url_path_for("health_check")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK


async def test_products_crud(client: AsyncClient) -> None:
    create_response = await client.post(
        "/api/products",
        json={"name": "iPhone 17", "stock": 12},
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    product = create_response.json()
    product_id = product["id"]
    assert product["name"] == "iPhone 17"
    assert product["stock"] == 12

    get_response = await client.get(f"/api/products/{product_id}")
    assert get_response.status_code == status.HTTP_200_OK

    list_response = await client.get("/api/products", params={"name": "iPhone"})
    assert list_response.status_code == status.HTTP_200_OK
    list_payload = list_response.json()
    assert list_payload["total"] >= 1

    patch_response = await client.patch(
        f"/api/products/{product_id}",
        json={"stock": 7},
    )
    assert patch_response.status_code == status.HTTP_200_OK
    assert patch_response.json()["stock"] == 7

    delete_response = await client.delete(f"/api/products/{product_id}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    get_deleted = await client.get(f"/api/products/{product_id}")
    assert get_deleted.status_code == status.HTTP_404_NOT_FOUND


async def test_reservation_flow(client: AsyncClient) -> None:
    create_product = await client.post(
        "/api/products",
        json={"name": "AirPods", "stock": 10},
    )
    product_id = create_product.json()["id"]

    order_id = str(uuid.uuid4())
    create_reservation = await client.post(
        "/api/reservations",
        json={
            "product_id": product_id,
            "order_id": order_id,
            "qty": 4,
        },
    )
    assert create_reservation.status_code == status.HTTP_201_CREATED
    reservation = create_reservation.json()
    reservation_id = reservation["id"]

    product_after_reserve = await client.get(f"/api/products/{product_id}")
    assert product_after_reserve.status_code == status.HTTP_200_OK
    assert product_after_reserve.json()["stock"] == 6

    list_reservations = await client.get(
        "/api/reservations",
        params={"product_id": product_id},
    )
    assert list_reservations.status_code == status.HTTP_200_OK
    assert list_reservations.json()["total"] >= 1

    delete_reservation = await client.delete(f"/api/reservations/{reservation_id}")
    assert delete_reservation.status_code == status.HTTP_204_NO_CONTENT

    product_after_delete = await client.get(f"/api/products/{product_id}")
    assert product_after_delete.status_code == status.HTTP_200_OK
    assert product_after_delete.json()["stock"] == 10
