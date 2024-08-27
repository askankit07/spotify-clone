from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from requests import post,get
import requests
import json
import base64

rapidapiKey="fd7b21bf88msha8fa49f7d9b78cdp16d31ejsnd6b648d19af2"

def get_token():
    client_id="1be6773226b941b0848da092cce99e5d"
    client_secret="b6a95bf8262445e580b7cc0675a78aae"

    auth_string=f"{client_id}:{client_secret}"
    auth_bytes=auth_string.encode("utf-8")

    auth_base64=str(base64.b64encode(auth_bytes),"utf-8")
    url="https://accounts.spotify.com/api/token"
    try:
        headers={
            "Authorization":"Basic " + auth_base64,
            "Content-Type":"application/x-www-form-urlencoded"
        }
        data={"grant_type":"client_credentials"}
        result=post(url,headers=headers,data=data)
        json_result=json.loads(result.content)
        token=json_result["access_token"]
        return token
    except Exception as e:
        print(e)

def get_auth_header(token):
    return {"Authorization":"Bearer " +token}

def get_artists(token):
    
    artist_ids = ["3b9iVRjKkiC4oIHXB7pbzJ","7uIbLdzzSEqnX0Pkrb56cR","4YRxDV8wJFPHPTeXepOstw","5f4QpKfy7ptCHwTqspnSJI","13ubrt8QOOCPljQ2FL1Kca","0y59o4v8uw5crbN9M3JiL1","1mYsTxnqsietFxj1OgoGbG","4IKVDbCSBTxBeAsMKjAuTs","2oSONSC9zQ4UonDKnLqksx","6KImCVD70vtIoJWnq6nGn3",]
    url = "https://api.spotify.com/v1/artists"

    try:
        headers = get_auth_header(token)
        params = {
        "ids": ",".join(artist_ids)  # Join the artist IDs with commas
        }
        response = get(url, headers=headers,params=params)
        
        top_artists=[]
        if response.status_code == 200:

            artists_info=response.json()
            for artist in artists_info['artists']:
                id=artist.get('id')
                name=artist.get('name')
                img=artist.get('images')[0].get('url')
                top_artists.append({"id":id,"name":name,"url":img})
            return top_artists
        else:
            return top_artists
    except Exception as e:
        print(e)

        
def get_several_tracks(token):
    track_ids = ["3JWVwlr9TfKMdlBdKPYlKT","56zZ48jdyY2oDXHVnwg5Di","6clAHjokFftNtzUjOfH7WK","0Ms1V2flsPzr2bVqImelCB","15Vuw407y6UWIPUfGrpJ1e","0dLbrlAVPPjpPqnYfmJsWk","2sl6IYSXAOQbEcU1mdqhvR","4i3MgUew8ynhf49Qwr4IP4","1VrheK4CdhX74nrOSNIFtH","3ci9YeXRulpmFPDvqneVwc","05nP1Tsu6yFQ4uP6eSRq4R","6eO9LvEiMqh1CAsa6y3wXP","5zKRKQwLVBT1WDJE7XJrnm","3WJQXRiZQNpasi3i4Tp8U1","6E9UwSfT80age2xknoMS7Y","1EjxJHY9A6LMOlvyZdwDly","2iNqdCchlUZEgjJbQyZf8T","3bzGpKX05I7JADHfbYTBKt","5IKal8GgD5uV7vVtoSTZ4r"]
    url = "https://api.spotify.com/v1/tracks"
    
    try: 
        headers = {
            "Authorization": f"Bearer {token}"
        }
        params = {
            "ids": ",".join(track_ids)
        }
        response = requests.get(url, headers=headers, params=params)

        tracks=[]
        if response.status_code == 200:

            top_tracks=response.json()
            for track in top_tracks['tracks']:
                id=track["id"]
                name=track["name"]
                img=track['album']['images'][0]['url']
                tracks.append({"id":id,"name":name,"url":img})
            return tracks
        
        else:
            return tracks

    except Exception as e:
        print(e)
 

def get_song_metadata(song_id, token):
    url = f"https://api.spotify.com/v1/tracks/{song_id}"

    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.get(url, headers=headers)

        song_metadata=[]
        if response.status_code == 200:
            track = response.json()
            song_metadata = [{
                "id": track["id"],
                "name": track["name"],
                "artists":track['artists'][0]['name'],
                "artist_id":track['artists'][0]['id'],
                "image_url": track['album']['images'][0]['url'] if track['album']['images'] else None,
            }]
            return song_metadata
        else:
            return song_metadata
            
    except Exception as e:
        print(e)

def get_audio_details(query):

    url = "https://spotify-scraper.p.rapidapi.com/v1/track/download"

    querystring = {"track":query}

    try:
        headers = {
        	"x-rapidapi-key": rapidapiKey,
        	"x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        audio_details=[]

        if response.status_code==200:
            response_data=response.json()
            audio_list=response_data['youtubeVideo']['audio']

            audio_url=audio_list[0]['url']
            durationText=audio_list[0]['durationText']

            audio_details={
                'audio_url':audio_url,
                'durationText':durationText
            }
            return audio_details
        else:
            audio_details
    except Exception as e:
        print(e)
         
def search_query(query,token):
    url = 'https://api.spotify.com/v1/search'

    try:
        headers = get_auth_header(token)
        params = {
            'q': query,
            'type': 'track',
            'limit': 50 # You can adjust the limit to get more or fewer tracks
        }

        response = requests.get(url, headers=headers, params=params)
        track_data=[]

        if response.status_code == 200:
            data=response.json()

            for track in data['tracks']['items']:
                track_id=track['id']
                track_name=track['name']

                ms=track['duration_ms']     #convert ms into min
                sec=ms//1000
                min=sec//60
                rem_sec=sec % 60
                durationText= f"{min}:{rem_sec}"

                track_img=track['album']['images'][0]['url']
                artist_name=track['artists'][0]['name']

                track_data.append({
                    'Id':track_id,
                    'Name':track_name,
                    'durationText':durationText,
                    'url':track_img,
                    'artistName':artist_name,
                })
            return track_data

        else:
            print(f"Failed to retrieve tracks: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(e)
 
def artist_overview(id):

    url = "https://spotify-scraper.p.rapidapi.com/v1/artist/overview"

    querystring = {"artistId":id}

    headers = {
    	"x-rapidapi-key": rapidapiKey,
    	"x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        artist_data={}
        if response.status_code==200:
            data=response.json()

            artistName=data['name']
            followers=data['stats']['followers']
            img_url=data['visuals']['avatar'][2]['url']

            top_tracks=[]
            for track in data['discography']['topTracks']:

                id=track['id']
                trackName=track['name']

                durationText=track['durationText']
                playCount=track['playCount']

                trackArtist=track['artists'][0]['name']
                top_tracks.append({                 #Top tracks of the artist
                                'trackId':id,
                                'trackName':trackName,
                                'durationText':durationText,
                                'playCount':playCount,
                                'trackArtist':trackArtist,
                                'imgUrl':img_url
                            }) 

            artist_data={                   #This is the data of the artist
                    'name':artistName,
                    'followers':followers,
                    'imgUrl':img_url,
                    'topTracks':top_tracks,
                }

            return artist_data
        else:
            print(response.status_code)
    except Exception as e:
        print(e)
       
def home(request):
    token=get_token()   # Getting the token from spotify web api
    top_artists = get_artists(token)

    tracks = get_several_tracks(token)   # Top songs
    
    context={
        'top_artists':top_artists,
        'tracks':tracks,
    }
    
    if request.user.is_authenticated:
        name=request.user.first_name
        firstName=name.split(' ')
        return render(request,'index.html',{'name':firstName[0],"top_artists":top_artists,'tracks':tracks,})
    else:
        return render(request,'index.html',context)    

@csrf_protect
def signup(request):
    if request.method=="POST":
        first_name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')   
        username=email
        
        user=User.objects.filter(email=email)

        if user.exists():
            messages.info(request,"Email already used")
            return redirect('signup')

        user=User.objects.create(
            first_name=first_name,
            email=email,
            username=username
        )

        user.set_password(password)
        user.save()

        messages.info(request,"Account created successfully")
        
        return redirect('login')

    return render(request,"signUp.html")


@csrf_protect
def login_page(request):
    if request.method=="POST":
        username=request.POST.get('email')
        password=request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            messages.error(request,'Invalid Email')
            return redirect('login')
        
        user=authenticate(request,username=username,password=password)
        if user is None:
            messages.error(request,'Invalid Password')
            return redirect('login')
        
        else:
            login(request,user)
            return redirect('home')

    return render(request,'login.html')

@login_required(login_url='login')
def logout_page(request):
    logout(request)
    return redirect('login')

# @login_required(login_url='login')
def search(request):
    
    if request.method=="POST":
        
        query=request.POST.get('query')
        token=get_token()

        tracks=search_query(query,token)
        context={
            'tracks':tracks,
            'query':query
        }
        
        return render(request,'search.html',context)
    return render(request,'search.html')
         
# @login_required(login_url='login')
def music(request,id):
    
    token=get_token()
    try:
        
        metadata=get_song_metadata(id,token) #Getting the metadata of the song

        track_name=metadata[0].get('name')
        artists_name=metadata[0].get('artists')

        query=f"{track_name} {artists_name}"         #Create a query for the song
        # audio_details=get_audio_details(query)      

        context={
            'metadata':metadata,
            # 'audio_details':audio_details
        }
        return render(request,'music.html',context)
    except:
        return render(request,'music.html')
    
# @login_required(login_url='login')
def profile(request,id):
    
    artist=artist_overview(id)
    context={
        "artist_data":artist
    }
    return render(request,'profile.html',context)

 
