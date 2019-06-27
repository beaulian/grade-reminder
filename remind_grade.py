#coding=utf-8

import time
import schedule
import threading
from redis import Redis
from collections import defaultdict

import config as cfg
from fetch_grade import make_grade_fetcher
from send_email import (make_email_sender,
                        convert_list_to_email_text)


class RedisCache(object):
    def __init__(self, host='127.0.0.1', port=6379,
                 db=0, password=None, **kwargs):
        self.__redis_server = Redis(host=host, port=port, db=db,
                                    password=password, **kwargs)

    def __setitem__(self, key, value):
        self.__redis_server.set(key, value)

    def __getitem__(self, key):
        return self.__redis_server.get(key)

    def __contains__(self, key):
        return self.__redis_server.exists(key)


class GradeReminder(object):
    def __init__(self, cfg):
        self.cfg = cfg
        self._email_sender = make_email_sender(cfg)
        # cache classes which are already known.
        if cfg.use_redis:
            self.__cached_classes = RedisCache(cfg.redis_host, cfg.redis_port,
                                               cfg.redis_db, cfg.redis_password)
        else:
            self.__cached_classes = defaultdict(int)

    def remind_grade(self):
        def remind_job():
            grade_fetcher = make_grade_fetcher(cfg)
            classes = grade_fetcher.fetch_grade()
            remind_classes = []
            for class_ in classes:
                if class_[0] not in self.__cached_classes and \
                                    any([eng in class_[1] for eng in 'ABCDEFGH']):
                    self.__cached_classes[class_[0]] = 1
                    remind_classes.append(class_)
            # if exists classes which are not known yet.
            if len(remind_classes) != 0:
                text = convert_list_to_email_text(remind_classes)
                self._email_sender(text)

        assert len(cfg.strategy) == 1, 'wrong format for `strategy`, only support one key!'
        # execute the function for the first time
        remind_job()

        [[type_, number]] = cfg.strategy.items()
        if type_ == 'hours':
            schedule.every(number).hours.do(remind_job)
        elif type_ == 'minutes':
            schedule.every(number).minutes.do(remind_job)
        else:
            raise KeyError('wrong format for `strategy`, only support `hours` and `minutes`!')


def __check_network_connected():
    import socket

    def __is_network_connected():
        try:
            socket.create_connection(("www.qq.com", 80))
            return True
        except OSError:
            pass
        return False

    while not __is_network_connected():
        print('please connect the network first!')
        time.sleep(1)


def __start_schedule_deamon():
    def schedule_run():
        while True:
            schedule.run_pending()
            time.sleep(5)

    t = threading.Thread(target=schedule_run)
    t.start()
    t.join()


def main():
    # check if network is connected
    __check_network_connected()
    # register remind service
    grade_reminder = GradeReminder(cfg)
    grade_reminder.remind_grade()
    # start to run thread
    __start_schedule_deamon()


if __name__ == '__main__':
    main()

