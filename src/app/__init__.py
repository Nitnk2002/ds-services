from flask import Flask
from flask import request, jsonify
from .service.messageService import MessageService
from kafka import KafkaProducer
import os
import json

app = Flask(__name__)
app.config.from_pyfile('config.py')

messageService = MessageService()

print(f"Kafka Bootstrap Servers: {app.config.get('KAFKA_BOOTSTRAP_SERVERS')}")
print("\n")

producer = KafkaProducer(
    bootstrap_servers=app.config.get('KAFKA_BOOTSTRAP_SERVERS'),
    security_protocol='SASL_SSL',
    sasl_mechanism='PLAIN',
    sasl_plain_username=app.config.get('KAFKA_USERNAME'),
    sasl_plain_password=app.config.get('KAFKA_PASSWORD'),
    ssl_cafile=app.config.get('KAFKA_SSL_CA_LOCATION'),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
@app.route('/v1/ds/message', methods=['POST'])
def handle_message():
    message = request.json.get('message')
    user_id = request.json.get('user_id')
    result = messageService.process_message(message)
    if result is None:
        return jsonify({"error": "Not a bank SMS or could not process message"}), 400
    
    if user_id:
        result.user_id = user_id
    
    serialized_result = result.serialize()
        
    producer.send('expense_service', serialized_result)
    producer.flush()
    return jsonify(result.model_dump())

@app.route('/', methods=['GET'])
def handle_get():
    return 'Hello world'

@app.route('/v1/ds/chat', methods=['POST'])
def handle_chat():
    query = request.json.get('query')
    expenses = request.json.get('expenses', [])
    
    if not query:
        return jsonify({"error": "Query is required"}), 400
        
    context = json.dumps(expenses)
    try:
        from .service.llmService import LLMService
        llm_service = LLMService()
        reply = llm_service.runChatLLM(query, context)
        return jsonify({"reply": reply})
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8010, debug=True)