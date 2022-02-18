from django.core.management.base import BaseCommand
from app.service.data_provider import DataProvider
from app.service.decision import DecisionService


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--from')
        parser.add_argument('--to')

    def handle(self, *args, **options):
        data_provider = DataProvider()
        service = DecisionService(data_provider)

        service.learn()
        service.test_model()
