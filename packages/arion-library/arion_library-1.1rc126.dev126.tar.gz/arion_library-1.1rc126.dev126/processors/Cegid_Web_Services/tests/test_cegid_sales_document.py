import pytest
from ..lib.CegidSalesDocument import CegidSalesDocument

@pytest.fixture
def cegid_sales_document():
    """
    Fixture for initializing a CegidSalesDocument instance.

    Returns:
        CegidSalesDocument: An instance of CegidSalesDocument initialized with test credentials.
    """
    wsdl_url = 'wsdl_url'
    username = 'username'
    password = 'password'
    return CegidSalesDocument(wsdl_url, username, password)

def test_get_customer_id_by_reference(cegid_sales_document):
    """
    Tests the getByReference method of CegidSalesDocument.

    Args:
        cegid_sales_document (CegidSalesDocument): The fixture providing a CegidSalesDocument instance.

    Asserts:
        The response is not None.
        The response has an attribute 'CustomerId'.
    """
    customer_id = "SC102015"
    internal_reference = "BS23433"
    reference_type = "CustomerOrder"
    database_id = "test"

    response = cegid_sales_document.getByReference(customer_id, internal_reference, reference_type, database_id)
    print(response)
    assert response is not None
    assert hasattr(response, 'CustomerId')

def test_create_sales_document(cegid_sales_document):
    """
    Tests the createSalesDocument method of CegidSalesDocument.

    Args:
        cegid_sales_document (CegidSalesDocument): The fixture providing a CegidSalesDocument instance.

    Asserts:
        The response is not None.
        The response has an attribute 'DocumentId'.
    """
    database_id = "test"
    response = cegid_sales_document.createSalesDocument(database_id)
    print(response)
    assert response is not None
    assert hasattr(response, 'DocumentId')