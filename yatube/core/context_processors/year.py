from django.utils import timezone


def year(request):
    current_year = timezone.now().year
    """Добавляет переменную с текущим годом."""
    return {
        'year': current_year,
    }
