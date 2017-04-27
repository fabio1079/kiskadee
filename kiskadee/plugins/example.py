from kiskadee.monitor import watcher

message = 'message structure goes here'


@watcher
def watch():
    print("watch function")
    return {}


def callback():
    pass


def to_firehose():
    pass


print('example plugin module loaded')
