import spotyUtils
import plotUtils
import requests
import json

bot_token = 'xxxxxxxxxxxxxxxxxxxxxxxx'

UPDATES_URL = 'https://api.telegram.org/'+bot_token+'/getUpdates'
SEND_MESSAGE_URL = 'https://api.telegram.org/'+bot_token+'/sendMessage'
SEND_AUDIO_URL = 'https://api.telegram.org/'+bot_token+'/sendAudio'
SEND_PHOTO_URL = 'https://api.telegram.org/'+bot_token+'/sendPhoto'


def getLastUpdateId():

    r = requests.get(UPDATES_URL).json()
    last_update_id = r['result'][len(r['result'])-1]['update_id'] + 1

    return last_update_id


def getUpdates(last_update_id):
    #5 min timeout
    payload = {'offset': last_update_id, 'timeout': 3000}

    #print('se deberia quedar parado hasta notificacion')
    r = requests.get(UPDATES_URL, params = payload).json()


    num_updates = len(r['result'])

    return r, num_updates


def getIds(r):

    from_id = r['result'][0]['message']['from']['id']

    try:
        from_username = r['result'][0]['message']['from']['username']
    except KeyError:
        from_username = r['result'][0]['message']['from']['first_name']

    return from_id, from_username


def print_and_send(payload, log_msg):

    if payload['text'] != 'null':
        r = requests.post(SEND_MESSAGE_URL, params=payload)
    print(log_msg)

def check_text(r):
    if 'text' in r['result'][0]['message']:
        return True

    else:
        return False

def handleMessage(r):

    from_id, from_username = getIds(r)
    log_msg = ''
    payload = {'chat_id': from_id, 'text': ''}
    command = ''

    #hay texto
    if check_text(r):

        text = r['result'][0]['message']['text']

        if text == '/gettoptracks':

            payload['text'] = 'Introduce el nombre el artista'
            log_msg = '{} solicita getTopTracks'.format(from_username)
            command = '/gettoptracks'

        elif text == '/artistinfo':

            payload['text'] = 'Introduce el nombre el artista'
            log_msg = '{} solicita artistInfo'.format(from_username)
            command = '/artistinfo'

        elif text == '/albuminfo':

            payload['text'] = 'Introduce el nombre del album'
            log_msg = '{} solicita albumInfo'.format(from_username)
            command = '/albuminfo'

        elif text == '/playlistinfo':

            payload['text'] = 'Introduce el nombre de la playlist'
            log_msg = '{} solicita playlistInfo'.format(from_username)
            command = '/playlistinfo'

        elif text == '/trackinfo':

            payload['text'] = 'Introduce el nombre de la canción'
            log_msg = '{} solicita trackInfo'.format(from_username)
            command = '/trackinfo'

        elif text == '/trackfeatures':

            payload['text'] = 'Introduce el nombre de la canción'
            log_msg = '{} solicita trackFeatures'.format(from_username)
            command = '/trackfeatures'

        elif text == '/trackpreview':

            payload['text'] = 'Introduce el nombre de la canción'
            log_msg = '{} solicita trackPreview'.format(from_username)
            command = '/trackpreview'

        elif text == '/playliststats':

            payload['text'] = 'Introduce el nombre de la playlist'
            log_msg = '{} solicita playlistStats'.format(from_username)
            command = '/playliststats'

        elif text == '/albumstats':

            payload['text'] = 'Introduce el nombre del álbum'
            log_msg = '{} solicita albumStats'.format(from_username)
            command = '/albumstats'

        else:
            payload['text'] = 'Lo siento, no te he entendido, prueba con otro comando!'
            log_msg = '{} ha introducido comando no existente: {}'.format(from_username,text)


    #se envia imagen, audio
    else:
        payload['text'] = 'Lo siento, intenta hablarme con texto únicamente'
        log_msg = '{} ha enviado otro formato al permitido: texto'.format(from_username)

    print_and_send(payload, log_msg)
    return command


def sendTopTracks(r):

    from_id, from_username = getIds(r)
    log_msg = ''
    payload = {'chat_id': from_id, 'text': ''}


    if check_text(r):
        text = r['result'][0]['message']['text']

        top_track_info, name, id = spotyUtils.top_tracks_artist(text)

        if not top_track_info:
            payload['text'] = 'Lo siento, no he encontrado ese artista'
            log_msg = 'No se ha encontrado ese artista'
            print_and_send(payload, log_msg)
            return 'null','null'

        songs_pop = ' '
        for i,list in enumerate(top_track_info):
            song = ''.join(list[0])
            song = song.replace('"','')
            pop = list[1]
            songs_pop += str(i+1)+ '. '+song + '. Popularidad: '+pop+ '\n'

        payload['text'] = songs_pop
        log_msg = 'Se han pedido canciones de {} con Id artista {}'.format(name,id)


    else:
        payload['text'] = 'Lo siento, no te he entendido, prueba con otro comando'
        log_msg = 'No se ha enviado texto'

    print_and_send(payload, log_msg)

    return top_track_info, name

#para /trackpreview
def handle_preview(r):

    from_id, from_username = getIds(r)
    log_msg = ''
    payload = {'chat_id': from_id, 'text': ''}


    if check_text(r):
        text = r['result'][0]['message']['text']

        track_preview_info, artist_name = spotyUtils.track_preview(text)

        if not track_preview_info:
            payload['text'] = 'Lo siento, no he encontrado esa canción'
            log_msg = 'No se ha encontrado esa canción'
            print_and_send(payload, log_msg)
            return 'null','null'

        payload['text'] = 'null'
        log_msg = 'Se ha pedido preview de {}'.format(track_preview_info[0][0].replace('"',''))


    else:
        payload['text'] = 'Lo siento, no te he entendido, prueba con otro comando'
        log_msg = 'No se ha enviado texto'

    print_and_send(payload, log_msg)

    return track_preview_info, artist_name

def handle_preview_option(text, song_list, alone):

    try:
        num =int(text)

        if 0 < num <= len(song_list):
            index = num - 1
            return index, False, '', ''
        else:
            log_msg = 'Se ha pedido preview de canción no en la lista'
            payload_text = 'Se ha pedido preview de canción no en la lista'
            return 'null', False, log_msg, payload_text

    except ValueError:
        #viene de comando /trackpreview
        if alone:
            return 0, False, '',''

        if text.lower() == 'todas':
            return 0, True, '', ''

        elif text.lower() == 'no':
            payload_text = '¿En que puedo ayudarte?'
            log_msg = 'No se ha querido previews'
            return 'null', False, log_msg, payload_text

        elif text.lower() == 'si':
            index = 0
            return index, False, '', ''

        else:
            payload_text = 'Lo siento, no te he entendido!'
            log_msg = 'no se ha enviado todas ó no (ó sí para /trackpreview)'
            return 'null', False, log_msg, payload_text



def sendPreview(r, top_track_info, name, alone):

    from_id, from_username = getIds(r)
    log_msg = ''
    payload = {'chat_id': from_id, 'text': ''}

    if check_text(r):
        text = r['result'][0]['message']['text']
        song_list = [item[0].replace('"','') for item in top_track_info]
        prev_list = [item[2].replace('"','') for item in top_track_info]
        imag_list = [item[3].replace('"','') for item in top_track_info]

        index, all, log_msg, payload_text = handle_preview_option(text, song_list, alone)

        payload['text'] = payload_text

        #se introduce todas, no o indice
        if index != 'null':
            #todas
            if all:
                if prev_list.count('null') == len(prev_list) and all:
                     payload['text'] = 'Lo siento, no existe ninguna preview para este artista, prueba con otro!'
                     log_msg = 'No existe ninguna preview'
                else:
                    for i in range(len(prev_list)):

                        song_name = song_list[i]
                        prev_url = prev_list[i]
                        image_url = imag_list[i]

                        if prev_url == 'null':
                            continue

                        log_msg = send_audio_thumb(song_name, name, prev_url, image_url, from_id)

                    payload['text'] = 'Aquí tienes las previews!'
            #numero
            else:
                song_name = song_list[index]
                prev_url = prev_list[index]
                image_url = imag_list[index]

                if prev_url == 'null':
                    payload['text'] = 'Lo siento, no existe el preview de {}'.format(song_list[index])
                    log_msg = 'No existe preview de {}'.format(song_list[index])
                else:

                    log_msg = send_audio_thumb(song_name, name, prev_url, image_url, from_id)
                    payload['text'] = 'Aquí tienes el preview!'
                    if log_msg == 'null':
                        log_msg = 'Ha fallado open de archivo musica {}/cancion {}'.format(song_name, song_name)

    else:
        payload['text'] = 'Lo siento, no te he entendido, prueba con otro comando'
        log_msg = 'No se ha enviado texto'

    print_and_send(payload, log_msg)







def send_audio_thumb(audio_name, artist, audio_url, image_url, from_id):


    payload2 = {'chat_id': from_id,'caption':audio_name,'performer':artist,'title':audio_name}

    audio = download_open(audio_name, audio_url, 'music')
    image = download_open(audio_name, image_url, 'images')

    if audio != 'null' and image != 'null':

        files = {'audio':audio, 'thumb':image}
        r = requests.post(SEND_AUDIO_URL, params = payload2, files = files)
        log_msg = 'Preview de cancion {} enviado'.format(audio_name)
        return log_msg

    else:

        log_msg = 'null'
        return log_msg



def sendArtistInfo(r):

    from_id, from_username = getIds(r)
    log_msg = ''
    payload = {'chat_id': from_id, 'text': ''}

    if check_text(r):
        text = r['result'][0]['message']['text']

        artist_info, artist_image_url = spotyUtils.artist_info(text)

        if artist_info == 'null':
            payload['text'] = 'Lo siento, no he encontrado ese artista'
            log_msg = 'No se ha encontrado ese artista'
            print_and_send(payload, log_msg)
            return

        name = artist_info[0].replace('"','')
        followers = artist_info[1]
        popularity = artist_info[2]
        genres = artist_info[3].replace('"','').replace('[','').replace(']','')

        info = 'Nombre: {}\nSeguidores: {}\nPopularidad: {}\nGéneros: {}'.format(name,followers,popularity,genres)

        log_msg = send_image(name, artist_image_url, from_id)

        payload['text'] = info
        log_msg = 'Se ha pedido info de {}'.format(name)


    else:
        payload['text'] = 'Lo siento, no te he entendido, prueba con otro comando'
        log_msg = 'No se ha enviado texto'

    print_and_send(payload, log_msg)



def sendAlbumInfo(r):

    from_id, from_username = getIds(r)
    log_msg = ''
    payload = {'chat_id': from_id, 'text': ''}

    if check_text(r):
        text = r['result'][0]['message']['text']

        album_info, album_image_url = spotyUtils.album_info(text)

        if album_info == 'null':
            payload['text'] = 'Lo siento, no he encontrado ese álbum'
            log_msg = 'No se ha encontrado ese album'
            print_and_send(payload, log_msg)
            return

        name = album_info[0].replace('"','')
        artists = ', '.join(album_info[1]).replace('"','')
        type = album_info[2].replace('"','')
        date = album_info[3].replace('"','')
        tracks = album_info[4]

        info = 'Nombre del álbum: {}\nArtistas: {}\nTipo: {}\nFecha de lanzamiento: {}\nTotal de canciones: {}'.format(name,artists,type,date,tracks)

        log_msg = send_image(name, album_image_url, from_id)

        payload['text'] = info
        log_msg = 'Se ha pedido info de {} de {}'.format(name,artists)+log_msg


    else:
        payload['text'] = 'Lo siento, no te he entendido, prueba con otro comando'
        log_msg = 'No se ha enviado texto'

    print_and_send(payload, log_msg)


def sendPlaylistInfo(r):

    from_id, from_username = getIds(r)
    log_msg = ''
    payload = {'chat_id': from_id, 'text': ''}

    if check_text(r):
        text = r['result'][0]['message']['text']

        playlist_info, playlist_image_url = spotyUtils.playlist_info(text)

        if playlist_info == 'null':
            payload['text'] = 'Lo siento, no he encontrado esa playlist'
            log_msg = 'No se ha encontrado esa playlist'
            print_and_send(payload, log_msg)
            return

        name = playlist_info[0].replace('"','')
        description = playlist_info[1].replace('"','')
        owner = playlist_info[2].replace('"','')
        followers = playlist_info[3]
        tracks = playlist_info[4]

        if playlist_image_url != 'null':
            log_msg = send_image(name, playlist_image_url, from_id)


        info = 'Nombre de la playlist: {}\nDescripción: {}\nDueño: {}\nSeguidores: {}\nTotal de canciones: {}'.format(name,description,owner,followers,tracks)

        payload['text'] = info
        log_msg = 'Se ha pedido info de {} de {}'.format(name,owner)+log_msg


    else:
        payload['text'] = 'Lo siento, no te he entendido, prueba con otro comando'
        log_msg = 'No se ha enviado texto'

    print_and_send(payload, log_msg)

def sendTrackInfo(r):

    from_id, from_username = getIds(r)
    log_msg = ''
    payload = {'chat_id': from_id, 'text': ''}

    if check_text(r):
        text = r['result'][0]['message']['text']

        track_info, track_image_url = spotyUtils.track_info(text)

        if track_info == 'null':
            payload['text'] = 'Lo siento, no he encontrado esa canción'
            log_msg = 'No se ha encontrado esa canción'
            print_and_send(payload, log_msg)
            return

        name = track_info[0].replace('"','')
        artists = ', '.join(track_info[1]).replace('"','')
        album = track_info[2].replace('"','')
        popularity = track_info[3]

        info = 'Nombre de la canción: {}\nArtistas: {}\nÁlbum: {}\nPopularidad: {}\n'.format(name,artists,album,popularity)
        preview_msg = 'Si quieres escuchar un preview de {} prueba el comando /trackpreview!'.format(name)

        log_msg = send_image(name, track_image_url,from_id)

        payload['text'] = info + preview_msg
        log_msg = 'Se ha pedido info de {} de {}'.format(name,artists)+log_msg


    else:
        payload['text'] = 'Lo siento, no te he entendido, prueba con otro comando'
        log_msg = 'No se ha enviado texto'

    print_and_send(payload, log_msg)



def sendTrackFeatures(r):

    from_id, from_username = getIds(r)
    log_msg = ''
    payload = {'chat_id': from_id, 'text': ''}

    if check_text(r):
        text = r['result'][0]['message']['text']

        track_features = spotyUtils.track_audio_features(text)

        if track_features == 'null':
            payload['text'] = 'Lo siento, no he encontrado esa canción'
            log_msg = 'No se ha encontrado esa canción'
            print_and_send(payload, log_msg)
            return

        track_features = [round((i*100),4) for i in track_features]

        acousticness = track_features[0]
        danceability = track_features[1]
        energy = track_features[2]
        instrumentalness = track_features[3]
        speechiness = track_features[4]
        valence = track_features[5]

        acousticness_description = 'Acousticness (acústica): Medida de confianza de 0 a 100 de si la pista es acústica. 100 representa una alta confianza en que la pista es acústica.'
        dancebility_description = 'Danceability (dancabilidad): Describe la capacidad de baile de una canción. Determina qué tan adecuada es una canción para bailar en función de elementos musicales como el temo, estabilidad, ritmo. Un valor de 0 es el menos bailable y un valor de 100 el que más.'
        energy_description = 'Energy (energía): Es una medida de 0 a 100 que representa una medida de intensidad y actividad. En general las pistas enérgicas se sienten rápidas, altas y ruidosas, por ejemplo el death metal, mientras que un preludio de Bach tiene una puntuación baja en la escala. Las caracterísitcas que contribuyen a la energía incluyen el rango dinámico, volumen, timbre, frecuencia de incio y entropía general.'
        instrumentalness_description = 'Instrumentalness (instrumentalidad): Predice si una pista no contiene voces. Por ejemplo, canciones de rap son claramente vocales. Cuanto más cercano esté el valor a 100, mayor será la probabilidad de que la canción no contenga contenido vocal.'
        speachiness_description = 'Speachiness (vocalidad): Detecta la presencia de palabras habladas en una canción. Los valores superiores a 66 describen pistas que probablemente estén compuestas en su totalidad por palabras habladas. Los valores entre 33 y 66 describen pistas que pueden contener tanto música como voz, y las cancione spor debajo e 33 probablemente representen música que no contenga vocales.'
        valence_description = 'Valence (positividad): Medida de 0 a 100 que describe la positividad musical que transmite una canción. Las canciones con positividad más alta suenan mas positivas, mientras que las canciones con positividad más baja suenan más negativas.'

        features = 'Nombre de la canción: {}\nAcousticness: {}\nDanceability: {}\nEnergy: {}\nInstrumentalness: {}\nSpeechiness: {} \nValence: {}'.format(text,acousticness,danceability,energy,instrumentalness,speechiness,valence)

        info = '{}\n\n{}\n\n{}\n\n{}\n\n{}\n\n{}\n\n\n{}'.format(acousticness_description,dancebility_description,energy_description,instrumentalness_description,speachiness_description,valence_description,features)

        payload['text'] = info
        log_msg = 'Se ha pedido info de {}'.format(text)


    else:
        payload['text'] = 'Lo siento, no te he entendido, prueba con otro comando'
        log_msg = 'No se ha enviado texto'

    print_and_send(payload, log_msg)


def send_image(image_name, image_url, from_id):

    payload2 = {'chat_id': from_id,'caption':image_name}

    image = download_open(image_name, image_url,'images')

    if image != 'null':

        files = {'photo':image}
        r = requests.post(SEND_PHOTO_URL, params = payload2, files = files)
        log_msg = ' Imagen de cancion {} enviado'.format(image_name)
        return log_msg

    else:

        log_msg = ' Ha fallado open de archivo imagen {}'.format(image_name)
        return log_msg


def get_feature(features, feature_name):

    if feature_name == 'Acousticness':
        i = 0
    elif feature_name == 'Danceability':
        i = 1
    elif feature_name == 'Energy':
        i = 2
    elif feature_name == 'Instrumentalness':
        i = 3
    elif feature_name == 'Speechiness':
        i = 4
    elif feature_name == 'Valence':
        i = 5
    else:
        return 'null'

    try:
        int_feature = [float(item[0][i]) for item in features]
        feature = [int(round(item*100,4)) for item in int_feature]

        song_name = [item[1].replace('"','') for item in features]
        song_name = [i.replace('$','') for i in song_name]
        song_name = [i.replace('/','') for i in song_name]


        final_feature = [feature, song_name]

        return final_feature

    except:

        return 'null'


def sendPlotStats(r,type):

    from_id, from_username = getIds(r)
    log_msg = ''
    payload = {'chat_id': from_id, 'text': ''}

    if check_text(r):
        text = r['result'][0]['message']['text']

        if type == 'playlist':
            playlist_info, playlist_image_url = spotyUtils.playlist_info(text)

            if playlist_info == 'null':
                payload['text'] = 'Lo siento, no he encontrado esa playlist'
                log_msg = 'No se ha encontrado esa playlist'
                print_and_send(payload, log_msg)
                return
        #album
        else:
            album_info, album_image_url = spotyUtils.album_info(text)

            if album_info == 'null':
                payload['text'] = 'Lo siento, no he encontrado ese álbum'
                log_msg = 'No se ha encontrado ese álbum'
                print_and_send(payload, log_msg)
                return

        payload['text'] = 'Analizando datos de {}...\nEste proceso puede tardar unos instantes, dependiendo del número de canciones de la lista, ya que se están obteniendo a través da la API de Spotify las caracterísitcas de cada canción de la lista: bailibilidad, popularidad, instrumentalidad...\nTras analizar todos los parámetros, obtendrás varias gráficas que te permitirán visualizar como se distribuyen las caracterísitcas de estas canciones y un gráfico de barras con la media de todas las canciones de la lista.\nPor último obtendrás las correlaciones de cada caracterísitca con la popularidad para ver cuál de todas ellas influye más en la popularidad. Esto dependerá de la canción y del artista'.format(type)
        log_msg = 'Se envía mensaje de info de función'
        print_and_send(payload, log_msg)

        if type == 'playlist':
            t_name = playlist_info[0].replace('"','')
            popularity, features = spotyUtils.playlist_popularity_vs_feature(t_name)
        else:
            t_name = album_info[0].replace('"','')
            popularity, features = spotyUtils.album_popularity_vs_feature(t_name)


        feature_names = ['Acousticness','Danceability','Energy','Instrumentalness','Speechiness','Valence']

        for i in range(6):

            feature = get_feature(features,feature_names[i])

            if feature != 'null':

                plot_title = plotUtils.plotStat(popularity,feature,feature_names[i], t_name)
                log_msg = send_plot(plot_title,from_id)
                if log_msg != 'null':

                    info = 'Aquí tienes la gráfica {}'.format(plot_title)
                    payload['text'] = info
                    print_and_send(payload, log_msg)
                else:
                    info = 'No se ha podido obtener la gráfica {}'.format(t_name)
                    payload['text'] = info
                    log_msg = 'Ha fallado open de archivo imagen {}'.format(plot_title)
                    print_and_send(payload, log_msg)


        hist_title = plotUtils.plot_histogram(features, popularity, t_name)
        log_msg = send_plot(hist_title,from_id)
        if log_msg == 'null':
            info = 'No se ha podido obtener el histograma {}'.format(t_name)
            payload['text'] = info
            log_msg = 'Ha fallado open de archivo imagen {}'.format(hist_title)
            print_and_send(payload, log_msg)

        correlations = plotUtils.correlation(features, popularity)
        corr = ''
        for i in range(6):
            corr += 'Correlación de popularity con '+feature_names[i]+ ': '+str(round(correlations[i+1],4))+'\n'

        info = 'Aquí tienes las correlaciones de la popularidad con cada variable:\n {}'.format(corr)
        payload['text'] = info
        print_and_send(payload, log_msg)

        info = 'Aquí tienes todas estadísticas de {}!'.format(t_name)

        payload['text'] = info
        log_msg = 'Se han enviado estadísticas de {}'.format(t_name)


    else:
        payload['text'] = 'Lo siento, no te he entendido, prueba con otro comando'
        log_msg = 'No se ha enviado texto'

    print_and_send(payload, log_msg)



def send_plot(plot_name, from_id):

    payload2 = {'chat_id': from_id,'caption':plot_name}

    try:
        file = open('plots/'+plot_name+'.jpg','rb')

    except OSError:
        file = 'null'

    if file != 'null':

        files = {'photo':file}
        r = requests.post(SEND_PHOTO_URL, params = payload2, files = files)
        log_msg = 'Plot de gráfica {} enviado'.format(plot_name)
        return log_msg

    else:

        log_msg = 'null'
        return log_msg


def download_open(file_name, file_url, type):

    file_name = file_name.replace('/','')
    file = requests.get(file_url)

    with open(type+'/'+file_name, 'wb') as f:
        f.write(file.content)

    f.close()

    try:
        file = open(type+'/'+file_name,'rb')
        return file
    except OSError:

        file = 'null'
        return file
