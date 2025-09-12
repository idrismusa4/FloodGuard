from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

class SMSService:
    """
    Service to send SMS alerts using Twilio
    """
    
    def __init__(self):
        self.account_sid = TWILIO_ACCOUNT_SID
        self.auth_token = TWILIO_AUTH_TOKEN
        self.from_number = TWILIO_PHONE_NUMBER
        self.client = None
        
        # Initialize Twilio client if credentials are available
        if (self.account_sid and self.auth_token and 
            self.account_sid != "your-account-sid-here" and 
            self.auth_token != "your-auth-token-here"):
            try:
                self.client = Client(self.account_sid, self.auth_token)
                print("✅ Twilio SMS service initialized successfully")
            except Exception as e:
                print(f"❌ Failed to initialize Twilio client: {e}")
        else:
            print("⚠️  Twilio credentials not configured - SMS will be simulated")
    
    def send_sms(self, phone: str, message: str, from_number: str = None) -> bool:
        """
        Send SMS to a phone number
        
        Args:
            phone: Recipient phone number
            message: SMS message content
            from_number: Sender number (optional)
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            if not self.client:
                # For development, just log the message
                print(f"📱 SMS to {phone}: {message}")
                return True
            
            message = self.client.messages.create(
                body=message,
                from_=from_number or self.from_number,
                to=phone
            )
            
            print(f"SMS sent successfully. SID: {message.sid}")
            return True
            
        except Exception as e:
            print(f"Failed to send SMS to {phone}: {e}")
            return False
    
    def send_bulk_sms(self, phone_numbers: list, message: str) -> dict:
        """
        Send SMS to multiple phone numbers
        
        Args:
            phone_numbers: List of phone numbers
            message: SMS message content
            
        Returns:
            dict: Results with success/failure counts
        """
        results = {"sent": 0, "failed": 0, "errors": []}
        
        for phone in phone_numbers:
            if self.send_sms(phone, message):
                results["sent"] += 1
            else:
                results["failed"] += 1
                results["errors"].append(f"Failed to send to {phone}")
        
        return results

# Create a global instance
sms_service = SMSService()
