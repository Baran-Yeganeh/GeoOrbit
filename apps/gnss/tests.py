from datetime import timedelta
from django.contrib.auth.models import User
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django.utils import timezone

from .forms import MissionForm
from .models import Mission, ProcessingReport, Receiver, SatelliteSystem


class MissionWebViewTests(TestCase):
    """HTML views: public read access, login required for changes."""

    def setUp(self):
        self.user = User.objects.create_user('baran', password='pass-12345')
        self.receiver = Receiver.objects.create(
            receiver_name='R12', manufacturer='Trimble', receiver_model='R12i')
        self.gps = SatelliteSystem.objects.create(
            satellite_name='GPS', satellite_country='USA')
        self.mission = Mission.objects.create(
            project_name='Tehran Network', project_location='Tehran',
            receiver=self.receiver)
        self.mission.satellite_systems.add(self.gps)

    def test_home_page_shows_counts(self):
        response = self.client.get(reverse('mainPage'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['mission_count'], 1)
        self.assertEqual(response.context['receiver_count'], 1)

    def test_list_and_detail_are_public(self):
        self.assertContains(self.client.get(reverse('mission_list')), 'Tehran Network')
        detail = self.client.get(reverse('mission_detail', args=[self.mission.pk]))
        self.assertContains(detail, 'Tehran Network')

    def test_detail_remembers_last_mission_in_session(self):
        self.client.get(reverse('mission_detail', args=[self.mission.pk]))
        self.assertEqual(self.client.session['last_mission_id'], self.mission.pk)

    def test_detail_shows_processing_report(self):
        ProcessingReport.objects.create(
            method='Static', accuracy='2 mm', description='ok', mission=self.mission)
        response = self.client.get(reverse('mission_detail', args=[self.mission.pk]))
        self.assertContains(response, 'Static')

    def test_create_edit_delete_require_login(self):
        for name, args in [('mission_create', []),
                           ('mission_edit', [self.mission.pk]),
                           ('mission_delete', [self.mission.pk])]:
            response = self.client.get(reverse(name, args=args))
            self.assertEqual(response.status_code, 302, name)
            self.assertIn('/accounts/login/', response['Location'])

    def test_anonymous_cannot_delete(self):
        self.client.post(reverse('mission_delete', args=[self.mission.pk]))
        self.assertTrue(Mission.objects.filter(pk=self.mission.pk).exists())

    def test_logged_in_user_can_delete(self):
        self.client.login(username='baran', password='pass-12345')
        self.client.post(reverse('mission_delete', args=[self.mission.pk]))
        self.assertFalse(Mission.objects.filter(pk=self.mission.pk).exists())

    def test_list_uses_constant_number_of_queries(self):
        for i in range(5):
            m = Mission.objects.create(project_name=f'M{i}', project_location='X',
                                       receiver=self.receiver)
            m.satellite_systems.add(self.gps)
        with CaptureQueriesContext(connection) as queries:
            self.client.get(reverse('mission_list'))
        # missions + receiver (one JOIN) and one prefetch for satellite systems
        self.assertLessEqual(len(queries), 3)


class MissionSearchTests(TestCase):
    def setUp(self):
        Mission.objects.create(project_name='Alpha Survey', project_location='Tabriz')
        Mission.objects.create(project_name='Beta Survey', project_location='Shiraz')

    def test_search_matches_name(self):
        data = self.client.get(reverse('mission_search'), {'name': 'alpha'}).json()
        self.assertEqual([m['name'] for m in data['mission']], ['Alpha Survey'])

    def test_search_matches_location(self):
        data = self.client.get(reverse('mission_search'), {'name': 'shiraz'}).json()
        self.assertEqual(len(data['mission']), 1)

    def test_empty_or_missing_query_returns_empty_list(self):
        self.assertEqual(self.client.get(reverse('mission_search')).json(), {'mission': []})
        self.assertEqual(
            self.client.get(reverse('mission_search'), {'name': '  '}).json(), {'mission': []})


class MissionFormTests(TestCase):
    def test_end_date_before_start_date_is_rejected(self):
        now = timezone.now().replace(microsecond=0, second=0)
        form = MissionForm(data={
            'project_name': 'X', 'project_location': 'Y',
            'surveying_start_date': now.strftime('%Y-%m-%dT%H:%M'),
            'surveying_end_date': (now - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'),
        })
        self.assertFalse(form.is_valid())
        self.assertIn('surveying_end_date', form.errors)
