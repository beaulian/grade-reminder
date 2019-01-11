#coding=utf-8

import time
import schedule
import threading
from collections import defaultdict

import config as cfg
from fetch_grade import make_grade_fetcher
from send_email import (make_email_sender,
                        convert_list_to_email_text)


class GradeReminder(object):
    def __init__(self, cfg):
        self.cfg = cfg
        self._email_sender = make_email_sender(cfg)
        self.__cached_classes = defaultdict(int)  # cache classes which are already known.

    def remind_grade(self):
        def remind_job():
            grade_fetcher = make_grade_fetcher(cfg)
            classes = grade_fetcher.fetch_grade()
            remind_classes = []
            for class_ in classes:
                if class_[0] not in self.__cached_classes and \
                                    class_[1] != '成绩未录入':
                    self.__cached_classes[class_[0]] = 1
                    remind_classes.append(class_)
            # if exists classes which are not known yet.
            if len(remind_classes) != 0:
                text = convert_list_to_email_text(remind_classes)
                self._email_sender(text)

        schedule.every().hour.do(remind_job)


def __start_schedule_deamon():
    def schedule_run():
        while True:
            schedule.run_pending()
            time.sleep(1)

    t = threading.Thread(target=schedule_run)
    t.start()
    t.join()


def main():
    grade_reminder = GradeReminder(cfg)
    grade_reminder.remind_grade()
    # start to run thread
    __start_schedule_deamon()


if __name__ == '__main__':
    main()

