
from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from .models import Mission, Receiver, SatelliteSystem,ProcessingReport
from .serializers import MissionSerializer



class ReceiverAPIPermissionTests(APITestCase):


    def test_employee_cannot_delete_receiver(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.employee_token.key}'
        )

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        self.assertTrue(
            Receiver.objects.filter(pk=self.receiver.pk).exists()
        )


    def test_manager_can_delete_receiver(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.manager_token.key}'
        )

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertFalse(
            Receiver.objects.filter(pk=self.receiver.pk).exists()
        )

    def setUp(self):
        self.employee_group, _ = Group.objects.get_or_create(
            name='Employees'
        )
        self.manager_group, _ = Group.objects.get_or_create(
            name='Managers'
        )

        self.employee = User.objects.create_user(
            username='test_employee',
            password='test-password-123'
        )
        self.employee.groups.add(self.employee_group)

        self.manager = User.objects.create_user(
            username='test_manager',
            password='test-password-123'
        )
        self.manager.groups.add(self.manager_group)

        self.employee_token = Token.objects.create(
            user=self.employee
        )
        self.manager_token = Token.objects.create(
            user=self.manager
        )

        self.receiver = Receiver.objects.create(
            receiver_name='Test Receiver',
            manufacturer='Test Manufacturer',
            receiver_model='TR-100'
        )

        self.list_url = reverse('receiver_api_list_create')
        self.detail_url = reverse(
            'receiver_api_detail',
            kwargs={'pk': self.receiver.pk}
        )

    def test_guest_can_view_receivers(self):
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_guest_cannot_create_receiver(self):
        response = self.client.post(
            self.list_url,
            {
                'receiver_name': 'New Receiver',
                'manufacturer': 'Test Company',
                'receiver_model': 'TR-200'
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_employee_can_create_receiver(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.employee_token.key}'
        )

        response = self.client.post(
            self.list_url,
            {
                'receiver_name': 'Employee Receiver',
                'manufacturer': 'Test Company',
                'receiver_model': 'TR-300'
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_employee_cannot_update_receiver(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.employee_token.key}'
        )

        response = self.client.patch(
            self.detail_url,
            {'manufacturer': 'Unauthorized Change'},
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_manager_can_update_receiver(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.manager_token.key}'
        )

        response = self.client.patch(
            self.detail_url,
            {'manufacturer': 'Updated by Manager'},
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.receiver.refresh_from_db()

        self.assertEqual(
            self.receiver.manufacturer,
            'Updated by Manager'
        )


class MissionAPITests(APITestCase):

    def setUp(self):
        self.employee_group, _ = Group.objects.get_or_create(
            name='Employees'
        )
        self.manager_group, _ = Group.objects.get_or_create(
            name='Managers'
        )

        self.employee = User.objects.create_user(
            username='mission_employee',
            password='test-password-123'
        )
        self.employee.groups.add(self.employee_group)

        self.manager = User.objects.create_user(
            username='mission_manager',
            password='test-password-123'
        )
        self.manager.groups.add(self.manager_group)

        self.employee_token = Token.objects.create(
            user=self.employee
        )
        self.manager_token = Token.objects.create(
            user=self.manager
        )

        self.receiver = Receiver.objects.create(
            receiver_name='Leica',
            manufacturer='Leica Geosystems',
            receiver_model='GS18'
        )

        self.system = SatelliteSystem.objects.create(
            satellite_name='GPS',
            satellite_country='United States'
        )

        self.mission = Mission.objects.create(
            project_name='Test Mission',
            project_location='Tehran',
            receiver=self.receiver
        )
        self.mission.satellite_systems.add(self.system)

        self.list_url = reverse('mission_api_list')
        self.create_url = reverse('mission_api_create')
        self.detail_url = reverse(
            'mission_api_detail',
            kwargs={'pk': self.mission.pk}
        )

    def test_guest_can_view_missions(self):
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_employee_can_create_mission_with_relations(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.employee_token.key}'
        )

        response = self.client.post(
            self.create_url,
            {
                'project_name': 'New GNSS Survey',
                'project_location': 'Berlin',
                'receiver_id': self.receiver.pk,
                'satellite_system_ids': [self.system.pk]
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        mission = Mission.objects.get(
            project_name='New GNSS Survey'
        )

        self.assertEqual(
            mission.receiver_id,
            self.receiver.pk
        )
        self.assertIn(
            self.system,
            mission.satellite_systems.all()
        )

    def test_employee_cannot_update_mission(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.employee_token.key}'
        )

        response = self.client.patch(
            self.detail_url,
            {'project_name': 'Unauthorized Update'},
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_manager_can_update_mission(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.manager_token.key}'
        )

        response = self.client.patch(
            self.detail_url,
            {'project_name': 'Manager Updated Mission'},
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.mission.refresh_from_db()

        self.assertEqual(
            self.mission.project_name,
            'Manager Updated Mission'
        )

    def test_invalid_receiver_id_is_rejected(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.employee_token.key}'
        )

        response = self.client.post(
            self.create_url,
            {
                'project_name': 'Invalid Receiver Mission',
                'project_location': 'Tehran',
                'receiver_id': 999999,
                'satellite_system_ids': [self.system.pk]
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_employee_cannot_delete_mission(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.employee_token.key}'
        )

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        self.assertTrue(
            Mission.objects.filter(pk=self.mission.pk).exists()
        )


    def test_manager_can_delete_mission(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.manager_token.key}'
        )

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertFalse(
            Mission.objects.filter(pk=self.mission.pk).exists()
        )

    def test_invalid_satellite_system_id_is_rejected(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.employee_token.key}'
        )

        mission_count_before = Mission.objects.count()

        response = self.client.post(
            reverse('mission_api_create'),
            {
                'project_name': 'Invalid Satellite Test',
                'project_location': 'Test Location',
                'satellite_system_ids': [999999],
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertIn('satellite_system_ids', response.data)
        self.assertEqual(
            Mission.objects.count(),
            mission_count_before
        )

    def test_guest_cannot_create_mission(self):
        response = self.client.post(
            reverse('mission_api_create'),
            {
                'project_name': 'Guest Test',
                'project_location': 'Test Location',
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )


class ProcessingReportAPITests(APITestCase):

    def setUp(self):
        self.employee_group, _ = Group.objects.get_or_create(
            name='Employees'
        )
        self.manager_group, _ = Group.objects.get_or_create(
            name='Managers'
        )

        self.employee = User.objects.create_user(
            username='report_employee',
            password='test-password-123'
        )
        self.employee.groups.add(self.employee_group)

        self.manager = User.objects.create_user(
            username='report_manager',
            password='test-password-123'
        )
        self.manager.groups.add(self.manager_group)

        self.employee_token = Token.objects.create(
            user=self.employee
        )
        self.manager_token = Token.objects.create(
            user=self.manager
        )

        self.mission = Mission.objects.create(
            project_name='Report Test Mission',
            project_location='Tehran'
        )

        self.report = ProcessingReport.objects.create(
            method='Static GNSS Processing',
            accuracy='5 mm',
            description='Automated API test report',
            mission=self.mission
        )

        self.list_url = reverse(
            'processing_report_api_list_create'
        )
        self.detail_url = reverse(
            'processing_report_api_detail',
            kwargs={'pk': self.report.pk}
        )

    def test_guest_can_view_reports(self):
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_employee_can_create_report(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.employee_token.key}'
        )

        response = self.client.post(
            self.list_url,
            {
                'method': 'Static GNSS Processing',
                'accuracy': '8 mm',
                'description': 'Created by automated test',
                'mission': None
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_employee_cannot_update_report(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.employee_token.key}'
        )

        response = self.client.patch(
            self.detail_url,
            {'accuracy': 'Unauthorized Change'},
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_manager_can_update_report(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.manager_token.key}'
        )

        response = self.client.patch(
            self.detail_url,
            {'accuracy': 'Updated accuracy'},
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.report.refresh_from_db()

        self.assertEqual(
            self.report.accuracy,
            'Updated accuracy'
        )

    def test_guest_can_view_report_detail(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_employee_cannot_delete_report(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.employee_token.key}'
        )

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        self.assertTrue(
            ProcessingReport.objects.filter(pk=self.report.pk).exists()
        )


    def test_manager_can_delete_report(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.manager_token.key}'
        )

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertFalse(
            ProcessingReport.objects.filter(pk=self.report.pk).exists()
        )


    def test_guest_cannot_create_report(self):
        response = self.client.post(
            reverse('processing_report_api_list_create'),
            {
                'method': 'Guest Test',
                'accuracy': 'Test Accuracy',
                'description': 'Test report',
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )






class SatelliteSystemAPITests(APITestCase):

    def setUp(self):
        self.employee_group, _ = Group.objects.get_or_create(
            name='Employees'
        )
        self.manager_group, _ = Group.objects.get_or_create(
            name='Managers'
        )

        self.employee = User.objects.create_user(
            username='satellite_employee',
            password='test-password-123'
        )
        self.employee.groups.add(self.employee_group)

        self.manager = User.objects.create_user(
            username='satellite_manager',
            password='test-password-123'
        )
        self.manager.groups.add(self.manager_group)

        self.employee_token = Token.objects.create(
            user=self.employee
        )
        self.manager_token = Token.objects.create(
            user=self.manager
        )

        self.system = SatelliteSystem.objects.create(
            satellite_name='GPS',
            satellite_country='United States'
        )

        self.list_url = reverse(
            'satellite_system_api_list_create'
        )
        self.detail_url = reverse(
            'satellite_system_api_detail',
            kwargs={'pk': self.system.pk}
        )

    def test_guest_can_view_satellite_systems(self):
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_guest_cannot_create_satellite_system(self):
        response = self.client.post(
            self.list_url,
            {
                'satellite_name': 'Guest Test Satellite',
                'satellite_country': 'Test Country',
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_employee_can_create_satellite_system(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.employee_token.key}'
        )

        response = self.client.post(
            self.list_url,
            {
                'satellite_name': 'Galileo',
                'satellite_country': 'European Union',
            },
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_guest_can_view_satellite_system_detail(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_employee_cannot_update_satellite_system(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.employee_token.key}'
        )

        response = self.client.patch(
            self.detail_url,
            {'satellite_country': 'Unauthorized Change'},
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_manager_can_update_satellite_system(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.manager_token.key}'
        )

        response = self.client.patch(
            self.detail_url,
            {'satellite_country': 'Updated by Manager'},
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.system.refresh_from_db()

        self.assertEqual(
            self.system.satellite_country,
            'Updated by Manager'
        )

    def test_employee_cannot_delete_satellite_system(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.employee_token.key}'
        )

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertTrue(
            SatelliteSystem.objects.filter(
                pk=self.system.pk
            ).exists()
        )

    def test_manager_can_delete_satellite_system(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.manager_token.key}'
        )

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            SatelliteSystem.objects.filter(
                pk=self.system.pk
            ).exists()
        )
