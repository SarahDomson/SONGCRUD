import re
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import Artiste, Song, Lyric
from rest_framework import status

class AddArtiste(APIView):
    def post(self, request, *args, **kwargs):
        # Get artiste details
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        age = request.data.get('age')
        
        # Check if an already extisting artiste has both the first and last names
        try:
            Artiste.objects.get(first_name=first_name, last_name=last_name)
            # Return an error message to show artiste already exists
            return JsonResponse({'status': 'error', 'message': 'Artiste already exists with given first and last names'}, status=status.HTTP_403_FORBIDDEN, safe=False) 
        except Artiste.DoesNotExist:
            # If no artiste already exists for both first and last names, create an instance in the database
            details = {
                'first_name': first_name,
                'last_name': last_name,
                'age': age
            }  
            Artiste.objects.create(**details)
            # Return a success message after successful creation of artiste instance
            return JsonResponse({'status': 'success', 'message': 'Artiste details successfully saved'}, status=status.HTTP_201_CREATED, safe=False) 


class DeleteArtiste(APIView):
    def delete(self, request, *args, **kwargs):
        # Get artiste ID from request parameter
        artiste_id = self.kwargs['artiste_id']
        
        # Search the database if artiste with given ID exists
        try:
            artiste = Artiste.objects.get(id=artiste_id)
            # Delete artiste from the database
            artiste.delete()
            # Return a success message after deletion
            return JsonResponse({'status': 'success', 'message': 'Artiste deleted successfully'}, status=status.HTTP_200_OK, safe=False) 
        except Artiste.DoesNotExist:
            # If artiste with the given ID does not exist, return an error with a message
            return JsonResponse({'status': 'error', 'message': 'Artiste does not exist'}, status=status.HTTP_403_FORBIDDEN, safe=False) 
            
class UpdateArtiste(APIView):
    def put(self, request, *args, **kwargs):
         # Get artiste ID from request parameter
        artiste_id = self.kwargs['artiste_id']
        
        # Search the database if artiste with given ID exists
        try:
            artiste = Artiste.objects.get(id=artiste_id)
            # Update the given details if they exist in the request body
            if 'first_name' in request.data:
                artiste.first_name = request.data['first_name']
            if 'last_name' in request.data:
                artiste.last_name = request.data['last_name']
            if 'age' in request.data:
                artiste.age = request.data['age']
            # Save updated artiste details in the database
            artiste.save()
            # Return a success message after updating
            return JsonResponse({'status': 'success', 'message': 'Artiste updated successfully'}, status=status.HTTP_200_OK, safe=False) 
        except Artiste.DoesNotExist:
            # If artiste with the given ID does not exist, return an error with a message
            return JsonResponse({'status': 'error', 'message': 'Artiste does not exist'}, status=status.HTTP_403_FORBIDDEN, safe=False) 

class GetAllArtistes(APIView):
    def get(self, request, *args,**kwargs):
        
        # Retrieve all artistes from the database
        artistes = Artiste.objects.filter().values() 
        
        # Check if there is data in the database and return a corresponding data and message
        if len(artistes) == 0:
            return JsonResponse({'status': 'success', 'message': 'No artistes in the database'}, status=status.HTTP_200_OK, safe=False) 
        else:   
            return JsonResponse({'status': 'success', 'message': 'All artistes retrieved', 'data': list(artistes)}, status=status.HTTP_200_OK, safe=False) 
            

class AddSongs(APIView):
    def post(self, request, *args,**kwargs):
        # Get song details in request body and artiste name in request params
        artiste_id = self.kwargs['artiste_id']
        date_released = request.data.get('date_released')
        title = request.data.get('title')
        
        try:
            # Search the database for artiste with given ID
            Artiste.objects.get(id=artiste_id)
            Song.objects.get(title=title, date_released=date_released)
             # If artiste with the given ID does not exist, return an error with a message
            return JsonResponse({'status': 'error', 'message': 'Song already exists'}, status=status.HTTP_403_FORBIDDEN, safe=False) 
        except Song.DoesNotExist:
            details = {
                'artiste_id': artiste_id,
                'date_released': date_released,
                'title': title
            }
            # Create a song instance in the database with the details
            Song.objects.create(**details)
            # Return a success message after successful creation of song instance
            return JsonResponse({'status': 'success', 'message': 'Song details successfully saved'}, status=status.HTTP_201_CREATED, safe=False)
        except Artiste.DoesNotExist:
            # If artiste with the given ID does not exist, return an error with a message
            return JsonResponse({'status': 'error', 'message': 'Artiste does not exist'}, status=status.HTTP_403_FORBIDDEN, safe=False) 

 
class GetAllSongs(APIView):
    def get(self, request, *args,**kwargs):
        data = []
        
        # Retrieve all songs from the database
        songs = Song.objects.filter().values('id', 'title', 'date_released', 'likes', 'artiste__first_name', 'artiste__last_name')
        
        for song in songs:
            lyric = Lyric.objects.filter(song_id=song['id']).values('id', 'content')
            
            new_song = {
                'song': song,
                'lyrics': list(lyric)
            }
            data.append(new_song)
        # Check if there is data in the database and return a corresponding data and message
        if len(data) == 0:
            return JsonResponse({'status': 'success', 'message': 'No songs in the database'}, status=status.HTTP_200_OK, safe=False) 
        else:   
            return JsonResponse({'status': 'success', 'message': 'All songs retrieved', 'data': data}, status=status.HTTP_200_OK, safe=False) 

class GetSingleSong(APIView):
    def get(self, request, *args, **kwargs):
        # Get song ID from request parameter
        song_id = self.kwargs['song_id']
        data = []
        
        # Search the database if artiste with given ID exists
        try:
            song = Song.objects.filter(id=song_id).values('id', 'title', 'date_released', 'likes', 'artiste__first_name', 'artiste__last_name')
            lyric = Lyric.objects.filter(song_id=song[0]['id']).values('id', 'content')
            
            new_song = {
                'song': list(song),
                'lyrics': list(lyric)
            }
            data.append(new_song) 
            # Return a success message after retrieving song
            return JsonResponse({'status': 'success', 'message': 'Song retrieved successfully', 'song_details': data[0]}, status=status.HTTP_200_OK, safe=False) 
        except IndexError:
            # If song with the given ID does not exist, return an error with a message
            return JsonResponse({'status': 'error', 'message': 'Song does not exist'}, status=status.HTTP_403_FORBIDDEN, safe=False) 

class UpdateSong(APIView):
    def put(self, request, *args, **kwargs):
        # Get song ID from request parameter
        song_id = self.kwargs['song_id']
        
        # Search the database if artiste with given ID exists
        try:
            song = Song.objects.get(id=song_id)
            if 'title' in request.data:
                song.title = request.data['title']
            if 'date_released' in request.data:
                song.date_released = request.data['date_released']
            song.save()
            # Return a success message after updating the song
            return JsonResponse({'status': 'success', 'message': 'Song updated successfully'}, status=status.HTTP_200_OK, safe=False) 
        except Song.DoesNotExist:
            # If song with the given ID does not exist, return an error with a message
            return JsonResponse({'status': 'error', 'message': 'Song does not exist'}, status=status.HTTP_403_FORBIDDEN, safe=False) 
        

class AddLyrics(APIView):
    def post(self, request, *args, **kwargs):
        # Get song ID from request parameter and content from request body
        song_id = self.kwargs['song_id']
        content = request.data.get('content')
        
        try:
            # Check if lyric exists already
            Lyric.objects.get(content=content)
            # If lyric with the given contents exists, return an error with a message
            return JsonResponse({'status': 'error', 'message': 'Lyric already exists'}, status=status.HTTP_403_FORBIDDEN, safe=False) 
        except Lyric.DoesNotExist:
            # If lyric does not exist, create it
            details = {
                'song_id': song_id,
                'content': content
            }
            Lyric.objects.create(**details)
            return JsonResponse({'status': 'success', 'message': 'Lyric added successfully'}, status=status.HTTP_200_OK, safe=False) 
            
class DeleteSong(APIView):
    def delete(self, request, *args, **kwargs):
       # Get song ID from request parameter
        song_id = self.kwargs['song_id']   
        
        # Check if song exists
        try:
            song = Song.objects.get(id=song_id)
            lyrics = Lyric.objects.filter(song_id=song.id).delete()
            # Delete songs
            song.delete()
            return JsonResponse({'status': 'success', 'message': 'Song deleted successfully'}, status=status.HTTP_200_OK, safe=False)  
        except Song.DoesNotExist:
           # If song with the given ID does not exist, return an error with a message
            return JsonResponse({'status': 'error', 'message': 'Song does not exist'}, status=status.HTTP_403_FORBIDDEN, safe=False)  

class GetAllLyrics(APIView):
    def get(self, request, *args,**kwargs):
        
        # Retrieve all lyrics from the database
        lyrics = Lyric.objects.filter().values('id', 'song__title', 'content') 
        
        # Check if there is data in the database and return a corresponding data and message
        if len(lyrics) == 0:
            return JsonResponse({'status': 'success', 'message': 'No songs in the database'}, status=status.HTTP_200_OK, safe=False) 
        else:   
            return JsonResponse({'status': 'success', 'message': 'All lyrics retrieved', 'data': list(lyrics)}, status=status.HTTP_200_OK, safe=False) 
