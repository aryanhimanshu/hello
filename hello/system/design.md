Assumptions:
- Notifications are not real time (A delay of few seconds is bearable)
- User cannot send the same message within ~15 minutes (We will ignore if the message is sent again)
- Message will be already personalized
- Entities
  - Sender
  - Message


Request Schema : 
  {
    "sender": "sender_info",
    "receiver": "receiver_info",
    "message": "personalized_message",
    "creation_timestamp": "request_creation_time"
  }

SQS message schema
{
    "sender": "sender_info",
    "receiver" "receiver_info",
    "message" "personalized_message",
    "message_hash" hash(sender + receiver + message + (creation_timestamp in seconds/1000))
    "creation_timestamp": "creation_time in request schema"
}

Message db schema
{
    message_hash: "message_hash",
    "TTL": "creation_timestamp + 900 seconds"
}


                                                                        Message db
                                                                            ^
                                                                            |

API endpoint -> Message processing Lambda -> Intermediate SQS queue -> Notification delivery Lambda 

Diagram Link: https://drive.google.com/file/d/1oOJYc9efH40E7HOwdZcrBqcaVP9WRB88/view?usp=sharing

                                                                            

Flow chart

1. Subscriber of the service hits API endpoint with Request
2. Message processeing lambda verifies the request
3. Adds unique message_hash and pushes the message to SQS
4. Delivery lambda verifies the message_hash is not present in DDB
5. If message hash is present it verifies the TTL against the current time
6. Sends the notification if either message_hash is not present or if the TTL has expired


Use of Message ddb
- To ensure duplicate notification is not sent
- Using TTL we can remove older messages, but since this is not always time consistent. We will make use of this TTL to verify in step 5 of flow chart