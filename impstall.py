import pip._internal as pip

def install(package):
    pip.main(['install', package])

if __name__ == '__main__':
    try:
        from tracardi_time_blocker.time_blocker_action import TimeBlockerAction
    except ImportError:
        install('tracardi_time_blocker')
        from tracardi_time_blocker.time_blocker_action import TimeBlockerAction

    a = TimeBlockerAction()
    a.run(None)