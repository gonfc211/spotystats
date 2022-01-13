import requests
import json
import time
import spotyUtils
import telegramUtils

def main():
    last_update_id = telegramUtils.getLastUpdateId()

    while(1):

        num_updates = 0
        while(num_updates == 0):
            r, num_updates = telegramUtils.getUpdates(last_update_id)

        last_update_id += 1


        command = telegramUtils.handleMessage(r)

        if command == '/gettoptracks':

            num_updates = 0
            while(num_updates == 0):
                r, num_updates = telegramUtils.getUpdates(last_update_id)

            last_update_id += 1

            top_track_info, name = telegramUtils.sendTopTracks(r)

            if top_track_info != 'null' and name != 'null':

                from_id, from_username = telegramUtils.getIds(r)
                payload = {'chat_id': from_id, 'text': ''}
                payload['text'] = '¿Quieres escuchar el preview de alguna de estas canciones? (Introduce el número de la canción de la lista anterior. Introduce [todas] para todas las previews. Introduce [no] para ninguna preview)'
                r = requests.post(telegramUtils.SEND_MESSAGE_URL, params=payload)

                num_updates = 0
                while(num_updates == 0):
                    r, num_updates = telegramUtils.getUpdates(last_update_id)

                last_update_id += 1

                telegramUtils.sendPreview(r, top_track_info, name, False)

        elif command == '/artistinfo':

            num_updates = 0
            while(num_updates == 0):
                r, num_updates = telegramUtils.getUpdates(last_update_id)

            last_update_id += 1

            telegramUtils.sendArtistInfo(r)


        elif command == '/albuminfo':

            num_updates = 0
            while(num_updates == 0):
                r, num_updates = telegramUtils.getUpdates(last_update_id)

            last_update_id += 1

            telegramUtils.sendAlbumInfo(r)


        elif command == '/playlistinfo':

            num_updates = 0
            while(num_updates == 0):
                r, num_updates = telegramUtils.getUpdates(last_update_id)

            last_update_id += 1

            telegramUtils.sendPlaylistInfo(r)

        elif command == '/trackinfo':

            num_updates = 0
            while(num_updates == 0):
                r, num_updates = telegramUtils.getUpdates(last_update_id)

            last_update_id += 1

            telegramUtils.sendTrackInfo(r)

        elif command == '/trackfeatures':

            num_updates = 0
            while(num_updates == 0):
                r, num_updates = telegramUtils.getUpdates(last_update_id)

            last_update_id += 1

            telegramUtils.sendTrackFeatures(r)

        elif command == '/trackpreview':

            num_updates = 0
            while(num_updates == 0):
                r, num_updates = telegramUtils.getUpdates(last_update_id)

            last_update_id += 1

            top_track_info, artist_name = telegramUtils.handle_preview(r)

            telegramUtils.sendPreview(r, top_track_info, artist_name, True)

        elif command == '/playliststats':

            num_updates = 0
            while(num_updates == 0):
                r, num_updates = telegramUtils.getUpdates(last_update_id)

            last_update_id += 1
            try:
                telegramUtils.sendPlotStats(r,'playlist')
            except:
                from_id, from_username = telegramUtils.getIds(r)
                info = 'Lo siento, ha ocurrido un error mientras se procesaba esa playlist, prueba con otra!'
                payload = {'chat_id': from_id, 'text': ''}
                payload['text'] = info
                log_msg = 'Error, la playlist contenía canciones con carácteres especiales: #, ?, $...'
                telegramUtils.print_and_send(payload, log_msg)


        elif command == '/albumstats':

            num_updates = 0
            while(num_updates == 0):
                r, num_updates = telegramUtils.getUpdates(last_update_id)

            last_update_id += 1
            try:
                telegramUtils.sendPlotStats(r,'album')
            except:
                from_id, from_username = telegramUtils.getIds(r)
                info = 'Lo siento, ha ocurrido un error mientras se procesaba es álbum, prueba con otro!'
                payload = {'chat_id': from_id, 'text': ''}
                payload['text'] = info
                log_msg = 'Error, el álbum contenía canciones con carácteres especiales: #, ?, $...'
                telegramUtils.print_and_send(payload, log_msg)

if __name__ == "__main__":
    main()
