import csv
from parakeet.models import Club

def load_clubs(club_file):
    context = {}
    if club_file.multiple_chunks():
        context['uploadMsg'] = 'Uploaded file is too large.'
        return context

    rows = csv.reader(club_file)
    for line in rows:
        # Handle incorrectly parsed lines better
        if len(line) != 2:
            continue
        # info = list(csv.reader(line, delimiter=','))
        info = map(lambda x : x.strip(), line)
        if Club.objects.filter(club_name=info[0]):
            continue
        for (short, hread) in Club.CATEGORY_CHOICES:
            if info[1] == hread:
                c = Club(club_name=info[0], table_id=-1, category=short)
                c.save()
    context['uploadMsg'] = 'Uploaded file was successfully processed.'
    return context
