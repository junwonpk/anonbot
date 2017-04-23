import os
import re
import app
import time
import redis
import cPickle

class Anonbot:

    def __init__(self):
        self.redis = redis.from_url(os.environ.get("REDISCLOUD_URL"))
        self.user_id = 0

    def chat(self, input, user_id):
        #debugging
        #self.redis.flushall()
        if input == 'redis flushall':
            self.redis.flushall()
        #debugging

        self.user_id = user_id
        if user_id not in self.redis.keys(): # if user first time talking
            self.initUser(user_id)

        user_data = self.getData(user_id)

        user_data['test'] = 1
        self.setData(user_id, user_data)
        return

    def send_message(self, message):
        app.send_message(self.user_id, message, "text")

    def delete(self, user_id):
        self.redis.delete(user_id)

    def initUser(self, user_id):
        user_data = {"test": 0}
        self.redis.set(user_id, cPickle.dumps(user_data))

    def getData(self, user_id):
        return cPickle.loads(self.redis.get(user_id))

    def setData(self, user_id, user_data):
        self.redis.set(user_id, cPickle.dumps(user_data))
