#!/usr/bin/env python3


import argparse
import json
import requests
from datetime import datetime


class Eventbrite():
    API_BASE_URI = 'https://www.eventbrite.com/json/'
    EVENT_NEW_URI = 'event_new'
    EVENT_GET_URI = 'event_get'
    EVENT_UPDATE_URI = 'event_update'
    EVENT_ATTENDEES_URI = 'event_list_attendees'

    def __init__(self, appKey, userKey=''):
        self.auth = {'app_key': appKey}
        if userKey:
            self.auth['user_key'] = userKey

    def _request(self, uri, params):
        params.update(self.auth)
        response = requests.get(self.API_BASE_URI + uri, params=params).json()
        if 'process' in response:
            return response['process']['id']
        else:
            return response['error']

    def create(self, name, start, end, description):
        event = {'title': name, 'start_date': start, 'end_date': end, 'description': description}
        # TODO: 'status': 'live'
        return self._request(self.EVENT_NEW_URI, event)

    def update(self, eventId, name='', start='', end='', description=''):
        event = {'id': eventId}
        if name:
            event['title'] = name
        if start:
            event['start_date'] = start
        if end:
            event['end_date'] = end
        if description:
            event['description'] = description

        return self._request(self.EVENT_UPDATE_URI, event)

    def details(self, eventID):
        details = {}
        guests = {}
        params = {'id': eventID}
        params.update(self.auth)

        event = requests.get(self.API_BASE_URI + self.EVENT_GET_URI, params=params).json()
        attendees = requests.get(self.API_BASE_URI + self.EVENT_ATTENDEES_URI, params=params).json()

        details['title'] = event['event']['title']
        details['desc'] = event['event']['description']
        for attendee in attendees['attendees']:
            idMail = attendee['attendee']['email'] if 'email' in attendee['attendee'] else attendee['attendee']['id']
            fullName = ''
            for name in ['prefix', 'first_name', 'last_name', 'suffix']:
                if name in attendee['attendee']:
                    fullName += attendee['attendee'][name] + ' '
            guests[idMail] = fullName[:-1]
            print(fullName)
        details['guests'] = guests

        return details


if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument('action', choices=('create', 'update', 'details'),
                           help='''use "create" to create a new event, "update" to update an event and
                           "details" to get the event info''')
    argParser.add_argument('--title', help='event title')
    argParser.add_argument('--desc', help='event description')
    argParser.add_argument('--filedesc', type=argparse.FileType('r'),
                           help='path to the text file containing event description')
    argParser.add_argument('--date', help='''event date, for example 2013-11-11 16:16''')
    argParser.add_argument('--enddate', help='''event date, for example 2013-11-11 17:16''')
    argParser.add_argument('--id', help='event id or event url')
    args = argParser.parse_args()

    with open('config.json', 'r') as configFile:
        config = json.loads(configFile.read())
    eventbrite = Eventbrite(config['appKey'], config['userKey'])

    # fix input
    if args.date:
        args.date = datetime.strptime(args.date, '%Y-%m-%d %H:%M').strftime('%Y-%m-%d %H:%M:%S')
    if args.enddate:
        args.enddate = datetime.strptime(args.enddate, '%Y-%m-%d %H:%M').strftime('%Y-%m-%d %H:%M:%S')
    if args.filedesc and not args.desc:
        args.desc = args.filedesc.read()

    if args.action == 'create':
        eventId = eventbrite.create(args.title, args.date, args.enddate, args.desc)
        print('Created event id: ' + str(eventId))
    if args.action == 'update':
        eventbrite.update(args.id, args.title, args.date, args.enddate, args.desc)
        print('Event updated.')
    if args.action == 'details':
        print(eventbrite.details(args.id))
