from shop import Order
from shop import OrderService
from shop import CONFIG
import pytest
def test_order_normal():

    products = [
        {
            "name": "Teclado",
            "price": 800,
            "quantity": 1
        },
        {
            "name": "Mouse",
            "price": 300,
            "quantity": 1
        }
    ]

    order = Order(products)

    service = OrderService(CONFIG)

    #order_processed = service.process_order(order)

    result = service.calculate_total(order)

    #assert order_processed['payment']['status'] == 'approved'
    assert result["subtotal"] == 1100
    assert result["discount"] == 110
    assert result["tax"] == 158.4
    assert result["total"] == 1148.4

def test_order_monkP_setattr(monkeypatch):

    products = [
        {
            "name": "Teclado",
            "price": 800,
            "quantity": 1
        }
    ]
    class FakePaymentGateway:
        def charge(self, amount):
            return{
                "status": "approved",
                "transaction_id": "FAKE-001",
                "amount": amount
            }

    order = Order(products)
    service = OrderService(CONFIG)
    monkeypatch.setattr(service,'payment_gateway',FakePaymentGateway())
    order_processed = service.process_order(order)
    assert order_processed['payment']['status'] == 'approved'

@pytest.mark.system
def test_order_monkP_setitem(monkeypatch):

    products = [
        {
            "name": "Teclado",
            "price": 800,
            "quantity": 1
        }
    ]

    order = Order(products)
    monkeypatch.setitem(CONFIG,'tax_rate',0.2)
    service = OrderService(CONFIG)
    result = service.calculate_total(order)
    assert result["subtotal"] == 800
    assert result["discount"] ==40
    assert result["tax"] == 152
    assert result["total"] == 912

@pytest.mark.wip
def test_order_monkP_delattr(monkeypatch):

    products = [
        {
            "name": "Teclado",
            "price": 800,
            "quantity": 1
        }
    ]

    order = Order(products)
    service = OrderService(CONFIG)
    monkeypatch.delattr(service, 'discount_service')
    result = service.calculate_total(order)
    assert result["subtotal"] == 800
    assert result["discount"] ==0
    assert result["tax"] == 128
    assert result["total"] == 928