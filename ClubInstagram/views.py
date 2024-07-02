from django.shortcuts import render , redirect
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
from ClubInstagram.models import ClubInstagramMedia

# Create your views here.
def initiate_instagram_auth(request):
    app_id = '1600510753850672'
    redirect_uri = 'https://13.201.134.179/instagram/callback/'
    scope = 'instagram_graph_user_profile,instagram_graph_user_media'
    scope = 'user_profile,user_media'
    
    # auth_url = f"https://api.instagram.com/oauth/authorize?client_id={app_id}&redirect_uri={redirect_uri}&scope={scope}&response_type=code"
    auth_url = f"https://api.instagram.com/oauth/authorize?client_id={app_id}&redirect_uri={redirect_uri}&scope={scope}&response_type=code&api_version=v12.0"
    return redirect(auth_url)

def handle_instagram_callback(request):
    code = request.GET.get('code')
    # code='AQA6Lkl7ElWsXgEz30CWW5a7exdRqfA84P4c46QazAT_BA_a35vzXoY5ijVWQBeBUJHqpoSVDsrN0wN7HT1luOrhR8TimCXb-kCoMhUe8MUXxmBf9q8FmstIWBhv03YLbq2A2yBnMU0EFjLfLLwOKo_6JRGFjcMhSVuO_AGS_d41T-pftM9l1lzrZjjz5cEHAqotGnAY1b87DFsjEw1vuBiGKT5Zm7HQsPNeGYHLNH2AMQ'
    token_url = 'https://api.instagram.com/oauth/access_token'
    data = {
        'client_id': '1600510753850672',
        'client_secret': 'e1523bd685399d4e777ca46c7fb7fded',
        'grant_type': 'authorization_code',
        'redirect_uri': 'https://13.201.134.179/instagram/callback/',  # Use the same URI here
        'code': code
    }

    response = requests.post(token_url, data=data)
    
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        # Use this access_token to make API calls
        print("access_token  " ,access_token)
        # get_instagram_data(access_token)
        all_media=[]
        # get_instagram_data(access_token)
        save_instagram_data(access_token)
        return JsonResponse({"media": "Data Added Successfully"})
    else:
        return JsonResponse({"error": "Failed to obtain access token"}, status=400)
    

@api_view(['GET'])
def get_instagram_data(request):
    user_id = "me"
    access_token = 'IGQWRPVHgtcDlzWFdiNDVMdGc1VmtfYVI0NUlWVmpsUmRBdGVhVTFNNnE2aTRWQ09WcnFObE56Y3NqcFY5WUNIcG1KTUhqcnF2aUswNF84QTNpeEdfdEFya2dsVlZATXzl5UzktRm9ybXdkampsLVc1OE5rS3FjenVCaVlsMkNuODhDdwZDZD'
    # access_token = access_token
    base_url = 'https://graph.instagram.com/me/media'
    
    params = {
        'fields': 'id,caption,media_type,media_url,thumbnail_url,permalink,timestamp',
        'access_token': access_token
    }

    all_media = []
    
    while True:
        response = requests.get(base_url, params=params)
        
        if response.status_code != 200:
            return JsonResponse({'error': 'Failed to fetch data from Instagram', 'details': response.text}, status=400)
        
        data = response.json()
        all_media.extend(data.get('data', []))
        
        paging = data.get('paging', {})
        if 'next' not in paging:
            break
        
        params['after'] = paging['cursors']['after']

    return JsonResponse({'media': all_media})




def save_instagram_data(request,access_token):
    # access_token = request.GET.get('access_token')
    # club_id = request.GET.get('club_id')  # Fetch clubId from request
    club_id='Club001'
    access_token = access_token

    if not access_token:
        return JsonResponse({'error': 'Access token is required'}, status=400)
    
    if not club_id:
        return JsonResponse({'error': 'Club ID is required'}, status=400)

    base_url = 'https://graph.instagram.com/me/media'
    params = {
        'fields': 'id,caption,media_type,media_url,thumbnail_url,permalink,timestamp',
        'access_token': access_token
    }

    all_media = []

    while True:
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            return JsonResponse({'error': 'Failed to fetch data from Instagram', 'details': response.text}, status=400)

        data = response.json()
        media_items = data.get('data', [])
        
        for item in media_items:
            media, created = ClubInstagramMedia.objects.update_or_create(
                media_id=item['id'],
                defaults={
                    'club_id': club_id,  # Save the clubId
                    'caption': item.get('caption'),
                    'media_type': item['media_type'],
                    'media_url': item['media_url'],
                    'thumbnail_url': item.get('thumbnail_url'),
                    'permalink': item['permalink'],
                    'timestamp': item['timestamp']
                }
            )
            all_media.append(media)

        paging = data.get('paging', {})
        if 'next' not in paging:
            break

        params['after'] = paging['cursors']['after']

    return JsonResponse({'media': [media.id for media in all_media]})


def verify_token(access_token):
    debug_url = f"https://graph.instagram.com/debug_token?input_token={access_token}&access_token={access_token}"
    response = requests.get(debug_url)
    if response.status_code == 200:
        data = response.json()
        scopes = data.get('data', {}).get('scopes', [])
        print(f"Token scopes: {scopes}")
        return scopes
    else:
        print("Failed to verify token")
        return None