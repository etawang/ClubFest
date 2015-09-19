from parakeet.models import Club

def load_clubs(club_file):
    context = {}
    if club_file.multiple_chunks():
        context['uploadMsg'] = 'Uploaded file is too large.'
        return context

    for line in club_file:
        info = line.split(',')
        info = map(lambda x : x.strip(), info)
        if Club.objects.filter(club_name=info[0]):
            continue
        c = Club(club_name=info[0], table_id=-1, category=info[1])
        c.save()
    context['uploadMsg'] = 'Uploaded file was successfully processed.'
    return context
