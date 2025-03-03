import datetime

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from apps.projects.models import ProjectPhase
from apps.users.models import User


class ProjectPhaseDeletionTests(APITestCase):
    def setUp(self):
        ############################
        # create users
        self.project_manager = User.objects.create_user(
            username='manager', email='managermail@test.com', password='securepassword123'
        )
        self.manager_client = APIClient()
        self.manager_client.force_authenticate(user=self.project_manager)
        self.project_member = User.objects.create_user(
            username='member', email='membermail@test.com', password='securepassword123'
        )
        self.member_client = APIClient()
        self.member_client.force_authenticate(user=self.project_member)

       ####################################
        # create an organization.
        organization_url = reverse('create_organization')
        organization_data = {'organization_name': 'Test org',
                             'organization_password': 'securepassword123',
                             'password2': 'securepassword123'
                             }
        self.organization = self.manager_client.post(
            organization_url, organization_data, format='json')

        ##################################
        # create a project.
        project_data = {
            'organization': f'{self.organization.data['organization_id']}',
            'project_name': 'test project',
            'description': 'project description',
            'deadline': f'{datetime.date.today() + datetime.timedelta(days=1)}'
        }
        project_url = reverse('create_project')
        project_res = self.manager_client.post(
            project_url, project_data, format='json')

        self.project = project_res.data
        ###################################
        # create a project phase
        self.project_phase = ProjectPhase.objects.create(
            project_id=self.project['project_id'],
            phase_name='custom_phase'
        )

        self.url = reverse('rename_project_phase', kwargs={
            'phase_id': self.project_phase.pk
        })

    def test_phase_is_renamed(self):
        response = self.manager_client.put(self.url, {
            'name': 'new_phase_name'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRaises(
            ProjectPhase.DoesNotExist,
            lambda: ProjectPhase.objects.get(
                pk=self.project_phase.pk,
                phase_name='custom_phase')
        )
        self.assertTrue(ProjectPhase.objects.filter(
            pk=self.project_phase.pk, phase_name='new_phase_name').exists())

    def test_only_manager_can_rename_phase(self):
        response = self.member_client.put(self.url, {
            'name': 'new_phase_name'
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_new_name_must_match_pattern(self):
        bad_names = ['bad>name', 'bad=name',
                     'bad_name!', 'example$string']

        for bad_name in bad_names:
            response = self.manager_client.put(self.url, {
                'name': bad_name
            })
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        valid_names = ['valid_name', 'validname',
                       'valid_name1', 'valid--name', '@validname']

        for valid_name in valid_names:
            response = self.manager_client.put(self.url, {
                'name': valid_name
            })
            self.assertEqual(response.status_code, status.HTTP_200_OK)
