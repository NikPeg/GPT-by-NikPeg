from cloudpayments import CloudPayments, Order, CloudPaymentsError
import enum


class SubscriptionBehavior(enum.Enum):
    WEEKLY = "CreateWeekly"
    MONTHLY = "CreateMonthly"


class SubscriptionStatus(enum.Enum):
    ACTIVE = "Active"
    CANCELLED = "Cancelled"


class CloudPaymentsMixin(CloudPayments):
    def create_order(self, amount, currency, description, email=None,
                     send_email=None, require_confirmation=None,
                     invoice_id=None, account_id=None, phone=None,
                     send_sms=None, send_whatsapp=None, culture_info=None,
                     subscription_behavior: SubscriptionBehavior | None = None):
        params = {
            'Amount': amount,
            'Currency': currency,
            'Description': description,
        }
        if email is not None:
            params['Email'] = email
        if require_confirmation is not None:
            params['RequireConfirmation'] = require_confirmation
        if send_email is not None:
            params['SendEmail'] = send_email
        if invoice_id is not None:
            params['InvoiceId'] = invoice_id
        if account_id is not None:
            params['AccountId'] = account_id
        if phone is not None:
            params['Phone'] = phone
        if send_sms is not None:
            params['SendSms'] = send_sms
        if send_whatsapp is not None:
            params['SendWhatsApp'] = send_whatsapp
        if culture_info is not None:
            params['CultureInfo'] = culture_info
        if subscription_behavior is not None:
            params['SubscriptionBehavior'] = subscription_behavior.value

        response = self._send_request('orders/create', params)

        if response['Success']:
            return Order.from_dict(response['Model'])
        raise CloudPaymentsError(response)
