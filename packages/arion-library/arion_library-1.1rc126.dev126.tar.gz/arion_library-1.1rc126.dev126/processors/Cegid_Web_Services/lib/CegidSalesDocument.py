from .CegidBase import CegidBase
import zeep

class CegidSalesDocument(CegidBase):
    def __init__(self, wsdl_url, username, password) -> None:
        """
        Initializes the CegidSalesDocument with the given WSDL URL, username, and password.

        Args:
            wsdl_url (str): The URL to the WSDL of the web service.
            username (str): The username for authentication.
            password (str): The password for authentication.
        """
        super().__init__(wsdl_url, username, password)
        self.client = super().createSoapConnector()

    def getByReference(self, customer_id=None, internal_reference=None, reference_type=None, database_id=None):
        """
        Retrieves a sales document by reference.

        Args:
            customer_id (str, optional): The ID of the customer.
            internal_reference (str, optional): The internal reference of the document.
            reference_type (str, optional): The type of reference.
            database_id (str, optional): The ID of the database.

        Returns:
            dict: The response from the web service containing the sales document details.
        """
        client = self.createSoapConnector()
        request_data = {
            "searchRequest": {
                "Reference": {
                    "CustomerId": customer_id,
                    "InternalReference": internal_reference,
                    "Type": reference_type
                }
            },
            "clientContext": {
                "DatabaseId": database_id
            }
        }
        response = client.GetByReference(**request_data)
        return response

    def createSalesDocument(self, database_id):
        """
        Creates a new sales document in the system.

        Args:
            database_id (str): The ID of the database.

        Returns:
            dict: The response from the web service containing the created sales document details.

        Raises:
            zeep.exceptions.Fault: If there is an error with the SOAP request.
        """
        client = self.createSoapConnector()
        print(client)
        
        request_data = {
            "createRequest": {
                "Header": {
                    "Active": True,
                    "CurrencyId": "QAR",
                    "CustomerId": "SC102015",
                    "Date": "2024-06-20",
                    "InternalReference": "BS234331",
                    "LinesUnmodifiable": False,
                    "OmniChannel": {
                        "BillingStatus": "Pending",
                        "DeliveryType": "ShipByCentral",
                        "FollowUpStatus": "WaitingCommodity",
                        "PaymentStatus": "Partially",
                        "PreferCustomerDelivery": "1",
                        "ReturnStatus": "NotReturned",
                        "ShippingStatus": "Pending"
                    },
                    "Origin": "ECommerce",
                    "StoreId": "999",
                    "Type": "CustomerOrder"
                },
                "Lines": [
                    {
                        "Create_Line": {
                            "DiscountTypeId": "",
                            "ItemIdentifier": {
                                "Reference": "105006"
                            },
                            "Label": "",
                            "NetUnitPrice": 395.00,
                            "OmniChannel": {
                                "WarehouseId": "999"
                            },
                            "Origin": "ECommerce",
                            "Quantity": 1,
                            "UnitPrice": 395.00
                        }
                    },
                    {
                        "Create_Line": {
                            "DiscountTypeId": "",
                            "ItemIdentifier": {
                                "Reference": "105006"
                            },
                            "Label": "",
                            "NetUnitPrice": 205.00,
                            "OmniChannel": {
                                "WarehouseId": "999"
                            },
                            "Origin": "ECommerce",
                            "Quantity": 1,
                            "UnitPrice": 205.00
                        }
                    }
                ],
                "Payments": {
                    "Create_Payment": {
                        "Amount": 600.00,
                        "CurrencyId": "QAR",
                        "DueDate": "2024-06-20",
                        "Id": "1",
                        "IsReceivedPayment": False,
                        "MethodId": "CAS"
                    }
                }
            },
            "clientContext": {
                "DatabaseId": database_id
            }
        }
        
        try:
            response = client.Create(**request_data)
            return response
        except zeep.exceptions.Fault as e:
            # Print more details about the SOAP fault for debugging
            print(f"SOAP Fault: {e}")
            raise  # Re-raise the exception for further handling