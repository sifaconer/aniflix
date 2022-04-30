# Aniflix (beta)

Api web scraper para obtener los capítulos y servidores disponible para un anime actualmente solo disponible para Animeflv.

## Run Server

__Build Image Docker__

```bash
docker image build -t aniflix:v1 .
```

__Run Container Docker__
```bash
docker run -d -p 5000:5000 --name aniflix aniflix:v1
```

## Api

__[GET]: Lista de episodio__
```bash
curl localhost:5000/animeflv/episode?total=20&url=https://www3.animeflv.net/anime/pokemon-2019
```

__[GET]: Server de episodio__
```bash
curl localhost:5000/animeflv/server?url=https://www3.animeflv.net/ver/pokemon-2019-108
```
