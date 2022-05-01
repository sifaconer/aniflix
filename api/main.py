from flask import Flask, request, jsonify
from .play import episode_list, episode_server
import asyncio
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return jsonify({"server": "animeflv", "version": "beta"})


@app.route('/animeflv/episode')
def episode():
    url = request.args.get('url')
    total = int(request.args.get('total'))
    episodes = asyncio.run(episode_list(url_anime=url, total=total))
    return jsonify(episodes)


@app.route('/animeflv/server')
def server():
    url = request.args.get('url')
    server = asyncio.run(episode_server(url_episode=url))
    return jsonify(server)
