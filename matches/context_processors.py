from .models import TournamentTable

def table_data(request):
    return {
        'table_stats': TournamentTable.objects.all().order_by('league', '-points', '-wins')
    }