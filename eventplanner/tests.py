from django.contrib.auth import models as auth_models
from rest_framework import test


class BasicTests(test.APITestCase):
    def test_get_event__empty(self):
        response = self.client.get("http://testserver/events/")

        assert response.status_code == 200
        assert response.json()["count"] == 0

    def test_get_session__empty(self):
        response = self.client.get("http://testserver/sessions/")

        assert response.status_code == 200
        assert response.json()["count"] == 0

    def test_set__unauthenticated(self):
        response_session = self.client.post("http://testserver/sessions/", data={"name": "Event name"})
        response_event = self.client.post("http://testserver/sessions/", data={"name": "Event name"})

        assert response_event.status_code == response_session.status_code == 403
        assert (
            response_event.json()["detail"]
            == response_session.json()["detail"]
            == "Authentication credentials were not provided."
        )


class AuthenticatedTests(test.APITestCase):
    def setUp(self):
        super().setUp()
        auth_models.User.objects.create_user("testing_user", password="foo")
        self.client.login(username="testing_user", password="foo")

    def test_create_event(self):
        response = self.client.post(
            "http://testserver/events/",
            data={
                "name": "Event name",
                "start_date": "2020-04-01T09:00:00+00:00",
                "end_date": "2020-04-03T18:00:00+00:00",
            },
        )
        assert response.status_code == 201
        assert response.json()["id"] == 1
        assert response.json()["start_date"] == "2020-04-01T09:00:00Z"
        assert response.json()["timezone"] == "UTC"
        assert response.json()["sessions"] == []
        assert response.json()["owner"] == "testing_user"

    def test_create_event__different_timezone(self):
        response = self.client.post(
            "http://testserver/events/",
            data={
                "name": "Event name",
                "start_date": "2020-04-01T09:00:00+05:00",
                "end_date": "2020-04-03T18:00:00+05:00",
            },
        )

        # Automatic conversion to UTC
        assert response.json()["start_date"] == "2020-04-01T04:00:00Z"
        assert response.json()["timezone"] == "UTC"

    def test_create_event__wrong_end_date(self):
        response = self.client.post(
            "http://testserver/events/",
            data={
                "name": "Event name",
                "start_date": "2020-04-01T09:00:00+00:00",
                "end_date": "2020-04-01T09:00:00+00:00",  # end date needs to be after start date
            },
        )

        assert response.status_code == 400
        assert response.json()["non_field_errors"] == ["End date has to be later than the start date."]

    def test_create_session(self):
        self.client.post(
            "http://testserver/events/",
            data={
                "name": "Event name",
                "start_date": "2020-04-01T09:00:00+00:00",
                "end_date": "2020-04-03T18:00:00+00:00",
            },
        )
        session_response = self.client.post(
            "http://testserver/sessions/",
            data={
                "name": "Event name",
                "start_date": "2020-04-01T09:00:00+00:00",
                "end_date": "2020-04-01T10:00:00+00:00",
                "speaker": "Me",
                "event": "http://testingserver/events/1/",
            },
        )

        assert session_response.status_code == 201
        assert session_response.json()["id"] == 1
        assert session_response.json()["start_date"] == "2020-04-01T09:00:00Z"
        assert session_response.json()["speaker"] == "Me"
        assert session_response.json()["owner"] == "testing_user"
        # Session was linked to an instance of event created earlier
        assert session_response.json()["event"] == "http://testserver/events/1/"

        # Event will be linked to created session
        event_response = self.client.get("http://testserver/events/1/")
        assert event_response.json()["sessions"] == ["http://testserver/sessions/1/"]

    def test_modify_event(self):
        self.client.post(
            "http://testserver/events/",
            data={
                "name": "Event name",
                "start_date": "2020-04-01T09:00:00+00:00",
                "end_date": "2020-04-03T18:00:00+00:00",
            },
        )

        patch_response = self.client.patch("http://testserver/events/1/", data={"name": "New event name"})

        assert patch_response.status_code == 200
        assert patch_response.json()["name"] == "New event name"

    def test_delete_event(self):
        self.client.post(
            "http://testserver/events/",
            data={
                "name": "Event name",
                "start_date": "2020-04-01T09:00:00+00:00",
                "end_date": "2020-04-03T18:00:00+00:00",
            },
        )

        delete_response = self.client.delete("http://testserver/events/1/")
        assert delete_response.status_code == 204
        assert self.client.get("http://testserver/events/").json()["count"] == 0
