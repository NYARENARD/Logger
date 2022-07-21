import discum
from threading import Thread
import time

class Logger:
    
    def __init__(self, cfg):
        self._token = cfg["token"]
        self._prefix = cfg["prefix"]
        self._log_channel = cfg["logchannel"]

        self.bot = discum.Client(token = self._token, log=False)
        self._thread = Thread(target=self._commands_launch)
        self._thread.start()
        self._logging("`>>> Подключение успешно.`", [])

    def __del__(self):
        self.bot.gateway.close()
        self._thread.join()
        self._logging("`>>> Соединение сброшено.`", [])
	
    def _logging(self, message, attachments):
        print(message)
        self.bot.sendMessage(self._log_channel, '`' + message + '`')
        for url in attachments:
            self.bot.sendFile(self._log_channel, url, isurl=True)

    
    def _commands_launch(self):

        command_list = {self._prefix + "логировать" : ["логировать", "Логирую"],\
                        self._prefix + "нелогировать" : ["нелогировать", "Принял."]}
        flag_log_gl = 1

        def command_handle(config, channelID):
            command_name = config[0]
            ans_gotit = config[1]
            nonlocal flag_log_gl
            if command_name == "логировать":
                flag_log_gl = 1
            elif command_name == "нелогировать":
                flag_log_gl = 0 
            self._type_send(channelID, ans_gotit)

        @self.bot.gateway.command
        def log(resp):
            if resp.event.message and flag_log_gl:
                m = resp.parsed.auto()
                channelID = m["channel_id"]
                username = m["author"]["username"]
                discriminator = m["author"]["discriminator"]
                self_id = self.bot.gateway.session.user["id"]
                timestamp = self._timestamp_parse(m["timestamp"])
                content = m["content"]
                attachments = []
                for dict in m['attachments']:
                    attachments.append(dict['url'])

                try:
                    bot_flag = m["author"]["bot"]
                except:
                    bot_flag = False
                command_towrite = 'C' if content in command_list.keys() else ''
                mentioned = False
                for i in m["mentions"]:
                    if self_id == i["id"]:
                        mentioned = True
                        break
                mentioned_towrite = 'M' if mentioned else ''

                if not bot_flag and channelID != self._log_channel:
                    self._logging('> ' + "[{}{}]".format(command_towrite, mentioned_towrite).rjust(4) + ' ' + \
                                  "{}".format(channelID).rjust(18) + " | " + "{}".format(timestamp).rjust(23) + " | " + \
                                  "{}#{}".format(username, discriminator).rjust(21) + ": " + " {}".format(content), attachments)

        @self.bot.gateway.command
        def read_command(resp):
            if resp.event.message:
                m = resp.parsed.auto()
                channelID = m["channel_id"]
                content = m["content"]

                for command in command_list:
                    if content.lower() == command:
                        command_handle(command_list[command], channelID)
                        break
                
        @self.bot.gateway.command
        def logchannel_commands(resp):
            if resp.event.message:
                m = resp.parsed.auto()
                channelID = m["channel_id"]  
                messageID = m["id"]
                content = m["content"]
                self_id = self.bot.gateway.session.user["id"]
                himself = (m["author"]["id"] == self_id)
                attachments = []
                for dict in m['attachments']:
                    attachments.append(dict['url'])

                if channelID == self._log_channel and not himself:
                    content_arr = content.split(' ', 2)
                    command = content_arr[0].lower()
                    if command == "отправить":
                        channel = content_arr[1] 
                        content = content_arr[2]
                        time = len(content) // 5 + 1 
                        self.bot.addReaction(channelID, messageID, '💬') 
                        Thread(target=imit, args=(channel, time)).start().join()
                        self.bot.sendMessage(channel, content)
                        for url in attachments:
                            self.bot.sendFile(channel, url, isurl=True)
                        self.bot.addReaction(channelID, messageID, '✅') 
                    elif command == "удалить":
                        channel = content_arr[1] 
                        msg_id = content_arr[2]
                        self.bot.deleteMessage(channel, msg_id)
                        self.bot.addReaction(channelID, messageID, '✅') 
                    elif command == "ответить":
                        extra_arr = content_arr[2].split(' ', 1)
                        channel = content_arr[1] 
                        msg_to_reply = extra_arr[0]
                        content = extra_arr[1]
                        time = len(content) // 5 + 1 
                        self.bot.addReaction(channelID, messageID, '💬') 
                        Thread(target=imit, args=(channel, time)).start().join()
                        self.bot.reply(channel, msg_to_reply, content)
                        for url in attachments:
                            self.bot.sendFile(channel, url, isurl=True) 
                        self.bot.addReaction(channelID, messageID, '✅') 
                    elif command == "редактировать":
                        extra_arr = content_arr[2].split(' ', 1)
                        channel = content_arr[1] 
                        msg_to_edit = extra_arr[0]
                        message = extra_arr[1]
                        self.bot.editMessage(channel, msg_to_edit, message) 
                        self.bot.addReaction(channelID, messageID, '✅') 
                    else:
                        self.bot.addReaction(channelID, messageID, '❔') 

        def imit(channel, time):
            for counter in range(time):
                self.bot.typingAction(channel)
                time.sleep(1)

        self.bot.gateway.run()

    def _timestamp_parse(self, raw):
        sec = raw[17:22]
        minu = raw[14:16]
        hr = int(raw[11:13]) + 3
        day = str(int(raw[8:10]) + hr // 24)
        hr = str(hr % 24)
        mon = raw[5:7]
        year = raw[0:4]
        timestamp = hr+':'+minu+':'+sec+' '+day+'-'+mon+'-'+year
        return timestamp
