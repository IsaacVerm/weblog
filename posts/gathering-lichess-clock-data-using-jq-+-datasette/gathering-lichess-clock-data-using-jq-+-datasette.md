# Gathering Lichess clock data using jq + Datasette

## What's the problem I want to tackle?

I have wanted to improve my chess time management for a while now. [Time management](https://zwischenzug.substack.com/p/time-management) is a very important topic, but a blind spot for a lot of people (not just me):

> It was easy to make major progress in this area, because of where I was starting from: no intentional time management strategy whatsoever... I firmly believe that if you have trouble with either moving too fast or moving too slow, you should fix that before you work on any other area of chess improvement, because time trouble sabotages everything else you’re working on. ([Dan Bock](https://chessimprovementlab.substack.com/p/11-things-i-did-to-take-my-uscf-rating))

In a first stage (covered by this post) I want to get all time-related data of chess games I played and use [Datasette](https://datasette.io/) to inspect what the data looks like. At a later stage I want to take the analysis a bit further. What types of moves do I spend a lot of time on? If I blitz out a move, is it often a bad one?

## Where to get the data from?

I usually play chess on [Lichess](https://lichess.org/). Lichess offers an API which gives you exactly the data you need to solve these questions. If you call the [`/games/user/{username}`](https://chessimprovementlab.substack.com/p/11-things-i-did-to-take-my-uscf-rating) endpoint, you get the following data for all games played. Below is a complete example of a single game:

```json
{
    "id": "5FVTi1qN",
    "rated": true,
    "variant": "standard",
    "speed": "blitz",
    "perf": "blitz",
    "createdAt": 1742832718107,
    "lastMoveAt": 1742833012388,
    "status": "mate",
    "source": "pool",
    "players": {
      "white": {
        "user": {
          "name": "ja9xn97a",
          "id": "ja9xn97a"
        },
        "rating": 1541,
        "ratingDiff": 7,
        "analysis": {
          "inaccuracy": 4,
          "mistake": 0,
          "blunder": 0,
          "acpl": 27
        }
      },
      "black": {
        "user": {
          "name": "indexinator",
          "flair": "nature.full-moon-face",
          "id": "indexinator"
        },
        "rating": 1535,
        "ratingDiff": -6,
        "analysis": {
          "inaccuracy": 4,
          "mistake": 0,
          "blunder": 1,
          "acpl": 71
        }
      }
    },
    "winner": "white",
    "moves": "e4 e5 Nf3 Nc6 d4 exd4 Nxd4 Nf6 Nxc6 bxc6 Nc3 Bc5 Bg5 Be7 Bc4 O-O O-O Kh8 Re1 Ng8 Bxe7 Nxe7 Qh5 Ng6 Rad1 d6 h3 Be6 Bxe6 fxe6 Ne2 Qf6 Nd4 Qxf2+ Kh1 Nf4 Qg4 h5 Qg5 e5 Nf5 g6 Qh6+ Kg8 Qg7#",
    "clocks": [
      30003,
      30003,
      29947,
      ...
    ],
    "analysis": [
      {
        "eval": 18
      },
      {
        "eval": 21
      },
      ...
      {
        "mate": 2,
        "best": "f8f7",
        "variation": "Rf7",
        "judgment": {
          "name": "Blunder",
          "comment": "Checkmate is now unavoidable. Rf7 was best."
        }
    ],
    "clock": {
      "initial": 300,
      "increment": 0,
      "totalTime": 300
    }
  }
```

Not all of these fields are relevant to us. The fields needed for a time management analysis are:

- `id`: the game id
- `players.{color}.user.id`: what color each player is playing with
- `moves`: moves in [algebraic notation](https://en.wikipedia.org/wiki/Algebraic_notation_(chess))
- `clocks`: time remaining till the end of the game on the clock in 1/100 of a second the moment a move was made. Strangely enough it starts at 30003 instead of 30000 in the example above. This is strange because the game I played was 5 minutes so 5 * 60 * 100 would make 30000 and not 30003.
- `evals`: evaluation of the position in [centipawns](https://zwischenzug.substack.com/p/centipawns-suck)

Run this command if you want to check the data out for yourself:

```bash
curl -X GET \
  -H "Accept: application/x-ndjson" \
  --get \
  --data "max=5" \
  --data "clocks=true" \
  --data "evals=true" \
  https://lichess.org/api/games/user/indexinator
```

The default data type is [PGN](https://en.wikipedia.org/wiki/Portable_Game_Notation) if you don't specify the `Accept` header. I want to work with JSON data so have to specify this in the `Accept` header. I'm interested in the move times (derived from the clock times) and evaluations of the moves. Both of these aren't returned by the endpoint by default so have to be specified as well. If you don't provide the `max` parameter, the endpoint will stream thousands of games.

## How to fetch the data

Originally I was planning on just using [jq](https://jqlang.org/) to do all the data wrangling and data transformations (creating news fields, filtering, ...). However when reading [this comment on Hacker News](https://news.ycombinator.com/item?id=39782356) I changed my mind:

>   As an old Unix guy this is exactly how I see jq: a gateway to a fantastic library of text processing tools. I see a lot of complicated things done inside the language, which is a valid approach. But I don’t need it to be a programming language itself, just a transform to meet my next command after the pipe.

I noticed as well you start to struggle when you try to use `jq` for tasks too complex. It's not like it's impossible but you're pushing `jq` to do something it doesn't seem meant to be used for. Better to use several tools, each one tailored to the task. This fits in with the [Unix philosophy](https://en.wikipedia.org/wiki/Unix_philosophy):

> Make each program do one thing well. To do a new job, build afresh rather than complicate old programs by adding new "features".

So instead of using `jq` for everything, now I'm planning to use `jq` just to transform the JSON data to a tabular format. Additional cleaning can be done later on in the `sqlite` database itself. At the end `sqlite-utils` allows to [insert this JSON data into a `sqlite` database](https://sqlite-utils.datasette.io/en/stable/cli.html#inserting-json-data). This allows me to take advantage of [all Datasette has to offer](https://datasette.io/for). 

![](/static/images/posts/26-03-2025---gathering-lichess-clock-data-using-jq-+-datasette/pipeline-chess-games.png)

## Using `jq` to transform the data in tabular format

There are 2 types of fields to extract from `/games/user/{username}`:

- fields relevant on the game level
	- `id`
	- `players.{color}.user.id`
- fields relevant on the move level
	- `moves`
	- `clocks`
	- `evals`

We'll first focus on fields relevant on the move level since the movel level will be the basic unit of analysis. 

Fetching the move fields can be done in a rather elegant way in `jq` using [map](https://jqlang.org/manual/#map-map_values):

```bash
cat games.json |
    jq 'map({
	    moves,
	    clocks,
	    evals: (.analysis | map(.eval))
	})'
```

We loop over all the games using `map` and [create an object](https://jqlang.org/manual/#object-construction) for each game. Note you can combine the shortcut version for creating an object (just specifying `moves` or `clocks`) with a more elaborate specification for `evals`.  Extracting `evals` is a bit more involved than extracting `moves` or `clocks` because the evaluation numbers themselves are nested 1 level deeper than the `moves` and `clocks`.

The problem now however is `moves`, `clocks` and `evals` have different data types:

- `moves`: string
- `clocks`: array of integers
- `evals`: array of integers

It makes sense to use an array for `moves` so we transform the `moves` string into an array of strings. This can be done very easily with [split](https://jqlang.org/manual/#split-1):

```bash
moves: (.moves | split(" "))
```

We're working with fields relevant on a move level, but at the moment we're still working at the game level. Transforming these games into moves can be done in `jq` using the [transpose](https://jqlang.org/manual/#transpose) function. If you've got an array of arrays it will unite elements with the same index in a single array like in this simplified example:

```bash
jq 'transpose' <<< [[1,2,3],[4,5,6]]

[
  [
    1,
    4
  ],
  [
    2,
    5
  ],
  [
    3,
    6
  ]
]
```
Applied to our data this looks like this:

```bash
... | map([.moves, .clocks, .evals] | transpose | map({move: .[0], clock: .[1], eval: .[2]}))
```

The data now looks like this:

```json
[
    {
      "move": "e4",
      "clock": 30003,
      "eval": 18
    },
    {
      "move": "e5",
      "clock": 30003,
      "eval": 21
    },
    ...
```

We're done for fields relevant at the move level. For each move I'd also like to see some game fields repeated to make later analysis easier:

- `game_id`: game in which the move took place
- `player_id`: player who made the move
- `player_color`

The key here is the [Variable Operator](https://jqlang.org/manual/#variable-symbolic-binding-operator): you can save the `game_id` early on in the pipeline and reuse it later when working at the move level:

> The expression `exp as $x | ...` means: for each value of expression `exp`, run the rest of the pipeline with the entire original input, and with `$x` set to that value. Thus `as` functions as something of a foreach loop.

In practice:

```bash
... | map(.id as $game_id | [.moves, .clocks, .evals] | transpose | map({game_id: $game_id, move: .[0], clock: .[1], eval: .[2]})
```

The game id as saved as `$game_id` and injected at the end in the last `map`.

Note in this data format we don't know which player made which move. We just know what color each player belongs to, Black or White. Since in chess the moves with an odd index will always be made by White (since a player can just make a single move at a time), we can deduct which player made which move but to get there seems rather involved. For now I'll just save the Black and White player separately and I'll deal with the problem later using `sqlite`.

After [flattening](https://jqlang.org/manual/#flatten) (we no longer have to keep a separate array for each game since the game id is now available at the move level), the data now looks like this:

```json
[
    {
      "game_id": "5FVTi1qN",
      "player_white": "ja9xn97a",
      "player_black": "indexinator",
      "move": "e4",
      "clock": 30003,
      "eval": 18
    },
    {
      "game_id": "5FVTi1qN",
      "player_white": "ja9xn97a",
      "player_black": "indexinator",
      "move": "e5",
      "clock": 30003,
      "eval": 21
    },
    ...
```

This is exactly the data format Datasette expects to [insert JSON into a `sqlite` database](https://sqlite-utils.datasette.io/en/stable/cli.html#inserting-json-data): an array of objects with each key being a field name in the `sqlite` table.

The final code to gather data [can be found here](https://github.com/IsaacVerm/track-lichess/blob/94641362bbff20a115389e3d061627a4a28facda/games-table.sh).

## Exploring the data in Datasette

As usual the data wrangling part was the hard part. From now on it's smooth sailing. Converting the move times in JSON to `sqlite` is a simple command:

```
sqlite-utils insert move-times.db move_times move-times.json 
```

We can inspect data in `move-times.db` with this simple Datasette command:

```
datasette serve move-times.db
```

This [opens the Datasette web interface](https://github.com/simonw/datasette) wrapping our data:

![](/static/images/posts/26-03-2025---gathering-lichess-clock-data-using-jq-+-datasette/datasette-move-times.png)

This is a great start but a quick inspection of the data makes clear some essential data is still missing:

- There's no move number: if we want to analyse just the opening for example we'd like to filter rows with a row number smaller than 10. [ROW_NUMBER](https://www.sqlitetutorial.net/sqlite-window-functions/sqlite-row_number/) seems like an easy way to add this move number in `sqlite`.
- There are 2 player fields, one for Black and one for White. Filtering is easier if there'd be just a single player field for the player who made the move.
- The raw `eval` value isn't that interesting. What's interesting is how the evaluation of the position changed by making a move.
- Not strictly necessary but based on the algebraic notation you could add some fields like `type_move` (capture if `x`, checkmate if `#`, ...) or which piece has moved (e.g. queen moves if move is Qc2).
- Not strictly necessary either but a field with a URL pointing to the position of the move could be easy to create based on the game id and move number. This would allow you to quickly test hypothesis.

## Takeaways

### You can use pipes within object construction

```bash
map({
    ...
    evals: (.analysis | map(.eval))
})
```

This way you can be very concise.

### You can get very far with `map`

`jq` is a functional language so having a function to apply another function to each input is very powerful.

### Think about data structure before implementing any `jq` code

Implementing the script to extract the data was straightforward because I first made sure all the relevant move data was placed in arrays. After that I could leverage `jq` using [transpose](https://jqlang.org/manual/#transpose) and I quickly got a working solution.

### It's a bad idea to ask an LLM to create an entire `jq` command

The result is always too verbose and very often doesn't work (completely). In itself this is not a big problem if you could curate the solution afterwards but often I find debugging of these LLM commands later on near impossible. It's better to know a few basic concepts well and try to combine these in more creative ways.

### But you can let an LLM help with explaining and debugging simple commands

You give it the input you have and the output you want:
```bash
llm "I'm using jq and I've got an input object {id: 'a', moves: [1,2,3]}. I want to turn this into [['a','a','a'], [1,2,3]]."
```

This way you learn and you can build the command step by step which makes it easier to debug afterwards. It also allows you to select from several different approaches. This avoids choosing an approach you don't completely understand.

Debugging by doing `cat {jq-file} | llm "why doesn't this work?"` works wonders as well.

### Some basic things are very hard in `jq`

It's [rather complex to repeat a string a number of times into an array](https://stackoverflow.com/a/65540354). For example creating an array which contains n elements, all of which are the same string. Pay attention with LLMs here. The LLM will claim you can do this but the solution works only for strings and not arrays of strings.

### `jq` concepts/commands to remember

These are important concepts/commands to know inside out:
- [`map`](https://jqlang.org/manual/#map-map_values)
- [`transpose`](https://jqlang.org/manual/#transpose): this is like `zip` in other programming languages
- [Variable Operator](https://jqlang.org/manual/#variable-symbolic-binding-operator): if you want to reuse a value for each element of an array.

## CHANGELOG

- 26-03-2025: initial draft