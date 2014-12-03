import re
import sys
import xbmcaddon
from urllib import unquote
from resources.lib import scraper, utils

server = 'http://www.ezequielescobar.com/servicios/thenewboston/'

T_ERROR_TITLE = 30001
T_ERROR_SERVER = 30002
T_ERROR_COURSES = 30003
T_ERROR_VIDEOS = 30004

def main(params):
    if not params.has_key('mode') or params['mode'] == 'list_curses':

        json = scraper.get_url(server + 'cursos.php', True)
        status = json['status']
        first = True
        if status == 1:
            categories = json['categories']
            for category in categories:
                category['name'] = category['name'].encode('utf8')
                if first == True:
                    utils.add_heading(category['name'])
                    first = False
                else:
                    utils.add_heading(category['name'], True)

                for course in category['courses']:
                    course['name'] = course['name'].encode('utf8')
                    course['cat'] = course['cat'].encode('utf8')
                    utils.add_directory_link(course['name'],
                                             'list_videos',
                                             course['cat'],
                                             is_folder=True,
                                             is_playable=False)
        else:
            utils.alert(utils.get_localized_string(T_ERROR_TITLE), utils.get_localized_string(T_ERROR_SERVER))

    elif params['mode'] == 'list_videos':
        cat = params['url']
        json = scraper.get_url(server +  'videos.php?cat=' + cat, True)
        status = json['status']
        if status == 1:
            videos = json['videos']
            for video in videos:
                video['name'] = video['name'].encode('utf8')
                video['video'] = video['video'].encode('utf8')
                utils.add_directory_link(unquote(video['name']),
                                         'play_video',
                                         video['video'],
                                         is_folder=False,
                                         is_playable=True)
        else:
            utils.alert(utils.get_localized_string(T_ERROR_TITLE), utils.get_localized_string(T_ERROR_SERVER))

    elif params['mode'] == 'play_video':
        video = params['url']
        youtube_id = scraper.get_url(server + 'video.php?video=' + video)
        vurl = ("plugin://plugin.video.youtube/?path=/root/video"
               "&action=play_video&videoid={0}").format(youtube_id)
        utils.play_video(vurl)

    utils.end_directory()

if __name__ == '__main__':
    params = utils.get_params()
    main(params)