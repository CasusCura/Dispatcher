import getopt
import sys
import enum
import requests


def usage():
    print("""lol""")


class Actions(enum.Enum):
    REQUEST = 1
    STATUS = 2
    UPDATE = 3
    CANCEL = 4


def send(action, device, issue, requesttype, data, url):
    if action is Actions.REQUEST:
        json = {
            'device_id': device,
            'request_id': requesttype,
            'data': data,
        }
        req = requests.post(url+'/patient/request', json=json)
        print(req.text)
    elif action is Actions.STATUS:
        json = {
            'uuid': device,
        }
        req = requests.get(url+'/patient/request', params=json)
        print(req.text)
    elif action is Actions.UPDATE:
        json = {
            'device_id': device,
            'issue_id': issue,
            'data': data,
        }
        req = requests.post(url+'/patient/request', json=json)
        print(req.text)
    elif action is Actions.CANCEL:
        json = {
            'uuid': device,
        }
        req = requests.delete(url+'/patient/request', params=json)
        print(req.text)


def main():
    for action in Actions:
        print(action)
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            'ha:d:i:t:d:r:u:',
            [
                'help',
                'action='
                'device=',
                'issue=',
                'requesttype=',
                'requestdata='
                'url='
            ])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    action = None
    device = None
    issue = None
    requesttype = None
    requestdata = {}
    url = 'http://localhost'
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-a", "--action"):
            action = a
        elif o in ("-d", "--device"):
            device = a
        elif o in ("-i", "--issue"):
            issue = a
        elif o in ("-t", "--requesttype"):
            requesttype = a
        elif o in ("-r", "--requestdata"):
            requestdata = a
        elif o in ("-u", "--url"):
            url = a
        else:
            assert False, "unhandled option"
    print(action)
    try:
        send(Actions[action], device, issue, requesttype, requestdata, url)
    except Exception as e:
        print(e)
        assert False, 'unhandled action'


if __name__ == '__main__':
    main()
