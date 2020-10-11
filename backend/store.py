from tinydb import TinyDB, Query, where
from tinydb.operations import delete, increment
from util import json_to_datetime, datetime_to_json
from datetime import datetime as dt


def add_event_ids(search_result):
    return [{'EventId': x.doc_id, 'Event': dict(x)} for x in search_result]


class Store(object):
    def __init__(self, db_filename):
        self.db = TinyDB(db_filename)
        self.events = self.db.table('Events')

    def add_event(self, event_data):
        """Creates an event and saves it in the data store. Returns the event id.
        """
        return self.events.insert(event_data)

    def delete_event(self, event_id):
        self.events.delete(doc_ids=[event_id])

    def update_event(self, event_id, event_data):
        self.events.insert(event_data, doc_id=event_id)

    def get_event(self, event_id):
        return self.events.get(doc_id=event_id)

    def __getitem__(self, event_id):
        return self.events.get_event(event_id)

    def get_all_events(self):
        """Queries all events from the database.

        Returns a list with elements paired in the form:
            {'EventId': id, 'Event': dict}
        """
        all_events = self.events.all()
        return add_event_ids(all_events)

    def get_upcoming_events(self, n=4, now=None):
        """Queries up to n upcoming events from the database.

        Returns a list with elements paired in the form:
            {'EventId': id, 'Event': dict}
        """
        if now is None:
            now = dt.now()

        now = datetime_to_json(now)

        # JSON date string format is temporally sortable
        # using the usual alpha (dictionary) order
        Event = Query()
        future_events = self.events.search(Event.StartTime > now)
        future_events = sorted(future_events, key=lambda x: x['StartTime'])
        return add_event_ids(future_events[:n])

    # TODO: do we need this?
    # def patch_event(self, event_id, event_data):
    #     pass
