from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.id = self.scope['url_route']['kwargs']['id']
        self.room_group_name = f'game_{self.id}'

        # add the current channel to the group specified in the route
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # whenever we receive a message from the client,
        # re-broadcast this event to all channels in the group.
        # 'chat_message' refers to the name of the function
        # to call when each member of the group receives the
        # event
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'update',
                'message': text_data
            }
        )

    # receive event from group
    async def update(self, event):
        await self.send(text_data=event['message'])