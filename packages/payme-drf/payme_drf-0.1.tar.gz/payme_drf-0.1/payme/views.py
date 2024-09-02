from payme.methods.merchant.validation_classes import BaseMerchantValidationClass
from payme.methods.merchant.views import BaseMerchantAPIView


class MerchantValidationClass(BaseMerchantValidationClass):
    """
    MerchantValidationClass implements abstract methods from BaseMerchantValidationClass
    to handle specific payment validation logic.

    Exceptions Handled:
        - OrderNotFoundException: Raised when the order is not found.
        - InvalidAmountException: Raised when the transaction amount is invalid.

    Methods:
        check_order(amount, account, **kwargs): Validates the existence and correctness of the order.
        successful_payment(params, *args, **kwargs): Processes actions for a successful payment.
        cancel_payment(params, *args, **kwargs): Processes actions for canceling a payment.
    """

    def check_order(self, amount, account, **kwargs):
        """Validates the existence and correctness of the order."""
        ...

    def successful_payment(self, params, *args, **kwargs):
        """Processes actions for a successful payment."""
        ...

    def cancel_payment(self, params, *args, **kwargs):
        """Processes actions for canceling a payment."""
        ...


class PaymeMerchantAPIView(BaseMerchantAPIView):
    """
    PaymeMerchantAPIView handles API requests for Payme merchant operations
    by using the MerchantValidationClass to validate transactions.

    Attributes:
        validation_class (type): The validation class used for processing merchant transactions.
    """
    validation_class = MerchantValidationClass

