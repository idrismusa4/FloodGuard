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
        Send SMS to a phone number (for demo purposes, always sends to Twilio number)
        
        Args:
            phone: Recipient phone number (ignored for demo)
            message: SMS message content
            from_number: Sender number (optional)
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            if not self.client:
                # For development, just log the message
                print(f"📱 SMS to {self.from_number} (demo): {message}")
                return True
            
            # For demo purposes, always send to the Twilio number
            demo_message = f"[DEMO - Originally for {phone}] {message}"
            
            message = self.client.messages.create(
                body=demo_message,
                from_=from_number or self.from_number,
                to=self.from_number  # Always send to Twilio number for demo
            )
            
            print(f"SMS sent successfully to {self.from_number} (demo). SID: {message.sid}")
            return True
            
        except Exception as e:
            print(f"Failed to send SMS to {self.from_number}: {e}")
            return False
    
    def send_bulk_sms(self, phone_numbers: list, message: str) -> dict:
        """
        Send SMS to multiple phone numbers (for demo purposes, sends to Twilio number)
        
        Args:
            phone_numbers: List of phone numbers (ignored for demo)
            message: SMS message content
            
        Returns:
            dict: Results with success/failure counts
        """
        results = {"sent": 0, "failed": 0, "errors": []}
        
        # For demo purposes, send one message to Twilio number with all recipients listed
        if phone_numbers:
            demo_message = f"[DEMO - Bulk alert for {len(phone_numbers)} recipients: {', '.join(phone_numbers)}] {message}"
            
            if self.send_sms(self.from_number, demo_message):
                results["sent"] = len(phone_numbers)  # Count as if sent to all
                results["failed"] = 0
            else:
                results["sent"] = 0
                results["failed"] = len(phone_numbers)
                results["errors"].append(f"Failed to send bulk SMS to {self.from_number}")
        
        return results

# Create a global instance
sms_service = SMSService()
