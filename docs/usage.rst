=====
Usage
=====

To use RTE Player video downloader::

    pip install rteplayer-dl


Drag  `Get RTE Player MP4
<javascript:(function()%7Bfunction%20callback()%7B(function(%24)%7Bvar%20jQuery%3D%24%3Bfunction%20callback()%7Bfunction%20getParameterByName(name%2C%20url)%20%7Bif%20(!url)%20url%20%3D%20window.location.href%3Bname%20%3D%20name.replace(%2F%5B%5C%5B%5C%5D%5D%2Fg%2C%20'%5C%5C%24%26')%3Bvar%20regex%20%3D%20new%20RegExp('%5B%3F%26%5D'%20%2B%20name%20%2B%20'(%3D(%5B%5E%26%23%5D*)%7C%26%7C%23%7C%24)')%2Cresults%20%3D%20regex.exec(url)%3Bif%20(!results)%20return%20null%3Bif%20(!results%5B2%5D)%20return%20''%3Breturn%20decodeURIComponent(results%5B2%5D.replace(%2F%5C%2B%2Fg%2C%20'%20'))%3B%7Dvar%20video_embed_url%20%3D%20getParameterByName(%22pid%22%2C%20%24(%22%23playerpdk%22).attr(%22src%22))%3Bvar%20auth_cookie%20%3D%20Cookies.get('mpx_token')%3Bvar%20auth_video_embed_url%20%3D%20video_embed_url%20%2B%20'%3Fauth%3D'%20%2B%20auth_cookie%20%2B'%26formats%3Dmpeg-dash%26format%3DSMIL%26embedded%3Dtrue%26tracking%3Dtrue'%3Bconsole.log(auth_video_embed_url)%3Bprompt(%22Video%20embed%20URL%20for%20use%20with%20https%3A%2F%2Frteplayer-dl.readthedocs.io%3A%22%2C%20auth_video_embed_url)%7Dvar%20s%3Ddocument.createElement(%22script%22)%3Bs.src%3D%22https%3A%2F%2Fcdn.jsdelivr.net%2Fnpm%2Fjs-cookie%402%2Fsrc%2Fjs.cookie.min.js%22%3Bif(s.addEventListener)%7Bs.addEventListener(%22load%22%2Ccallback%2Cfalse)%7Delse%20if(s.readyState)%7Bs.onreadystatechange%3Dcallback%7Ddocument.body.appendChild(s)%3B%7D)(jQuery.noConflict(true))%7Dvar%20s%3Ddocument.createElement(%22script%22)%3Bs.src%3D%22https%3A%2F%2Fajax.googleapis.com%2Fajax%2Flibs%2Fjquery%2F1.11.1%2Fjquery.min.js%22%3Bif(s.addEventListener)%7Bs.addEventListener(%22load%22%2Ccallback%2Cfalse)%7Delse%20if(s.readyState)%7Bs.onreadystatechange%3Dcallback%7Ddocument.body.appendChild(s)%3B%7D)()>`_ link to your bookmark bar.

When viewing a programme on RTE player click on this bookmarklet and copy the
URL you are prompted with.

You can then run the following::

    rteplayer_dl --debug --video-directory="DIRECTORY ON YOUR LOCAL FILESYSTEM" --video-xml="VIDEO EMBED URL"

This will download an mp4 video to your local filesystem.
