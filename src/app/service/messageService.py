from app.utils.messagesUtil import MessagesUtil
from app.service.llmService import LLMService

class MessageService:
    def __init__(self):
        self.messageUtil = MessagesUtil()
        self.llmService = LLMService()
    
    def process_message(self, message):
        if self.messageUtil.isBankSms(message):
            result = self.llmService.runLLM(message)
            msg_lower = message.lower()
            if result and result.amount:
                # If it's an expense, make the amount negative
                if "spent" in msg_lower or "debited" in msg_lower or "sent" in msg_lower:
                    if not result.amount.startswith("-"):
                        result.amount = "-" + result.amount
                # If it's income, make sure it's positive
                elif "received" in msg_lower or "credited" in msg_lower:
                    if result.amount.startswith("-"):
                        result.amount = result.amount[1:]
            return result
        else:
            return None