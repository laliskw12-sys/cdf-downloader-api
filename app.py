import os
from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def extract_video():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'Missing URL parameter'}), 400

    youtube_url = data.get('url')
    is_audio = data.get('isAudio', False)

    ydl_opts = {
        'format': 'bestaudio/best' if is_audio else 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            direct_url = info.get('url')
            if not direct_url and 'formats' in info:
                direct_url = info['formats'][-1].get('url')

            return jsonify({
                'status': 'success',
                'url': direct_url,
                'title': info.get('title', 'CDF_Media')
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
