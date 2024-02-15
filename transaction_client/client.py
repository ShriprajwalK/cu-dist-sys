from zeep import Client

def call_process_transaction(user_name, credit_card_number):
    # Replace the URL with the actual WSDL URL of your SOAP service
    wsdl_url = 'http://127.0.0.1:8000/?wsdl'

    client = Client(wsdl_url)

    # Assuming the service and method names; adjust these as necessary
    response = client.service.process_transaction(user_name, credit_card_number)
    return response

if __name__ == "__main__":
    # Example usage
    user_name = "John Doe"
    credit_card_number = "1234567890123456"

    response = call_process_transaction(user_name, credit_card_number)
    print("Transaction Response:", response)
