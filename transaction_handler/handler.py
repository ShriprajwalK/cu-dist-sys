from spyne.application import Application
from spyne.decorator import rpc
from spyne.model.primitive import String
from spyne.model.complex import Iterable
from spyne.service import ServiceBase
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

import random

class FinancialTransactionsService(ServiceBase):
    @rpc(String, String, _returns=Iterable(String))
    def process_transaction(ctx, user_name, credit_card_number):
        # Simulate a transaction decision with 90% probability of "Yes" and 10% probability of "No"
        response = "Yes" if random.random() < 0.9 else "No"
        yield response

# Create the SOAP application
application = Application([FinancialTransactionsService],
                          tns='spyne.examples.financial_transactions',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

# Wrap the Spyne application with WsgiApplication
wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    # Run the application on http://127.0.0.1:8000
    server = make_server('127.0.0.1', 8000, wsgi_application)
    print("SOAP service running on http://127.0.0.1:8000")
    server.serve_forever()
