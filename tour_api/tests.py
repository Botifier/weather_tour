from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .enums import DestinationTypes
from .models import Package, Tour, Destination


class TestPackageList(APITestCase):

    def setUp(self):
        dest1 = Destination.objects.create(
            city='test_city_1',
            destination_type=DestinationTypes.ADVENTURE.value, 
            danger_score=100
        )
        dest2 = Destination.objects.create(
            city='test_city_2',
            destination_type=DestinationTypes.ADVENTURE.value, 
            danger_score=10
        )
        dest3 = Destination.objects.create(
            city='test_city_3',
            destination_type=DestinationTypes.CULTURAL.value, 
            danger_score=1
        )
        package1 = Package.objects.create(name='test_package_1', price=100, description='test_desc1')
        package2 = Package.objects.create(name='test_package_2', price=1000, description='test_desc2')
        package1.destination.add(dest1)
        package1.destination.add(dest2)
        package2.destination.add(dest2)
        package2.destination.add(dest3)
        package1.save()
        package2.save()
        tour1 = Tour.objects.create(date="2050-10-20", capacity=1, package=package1)
        tour2 = Tour.objects.create(date="2050-10-21", capacity=10, package=package1)
        tour3 = Tour.objects.create(date="2050-10-22", capacity=100, package=package2)
        tour4 = Tour.objects.create(date="2050-10-23", capacity=1000, package=package2)

    def test_danger_score(self):
        response = self.client.get(reverse('package-tour-list'), {
            'start': '2050-10-20', 'end': '2050-10-23', 'danger_score':1}
        )
        # danger_scores should be the max
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        response = self.client.get(reverse('package-tour-list'), {
            'start': '2050-10-20', 'end': '2050-10-23', 'danger_score':100}
        )
        # 2 tours for this score
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # 2 destinations per tour
        self.assertEqual(len(response.data[0]['destinations']), 2)

    def test_ranges(self):
        # Empty range
        response = self.client.get(reverse('package-tour-list'), {
            'start': '2050-10-11', 'end': '2050-10-12', 'danger_score':100}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        # Normal range
        response = self.client.get(reverse('package-tour-list'), {
            'start': '2050-10-20', 'end': '2050-10-21', 'danger_score':100}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)