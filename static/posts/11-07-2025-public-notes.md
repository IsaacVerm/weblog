# 11-07-2025

I like reading the [Construction Physics blog](https://www.construction-physics.com/) and I notice the author often uses [Datawrapper](https://www.datawrapper.de/). It seems to be [a German company](https://www.datawrapper.de/faq#who-is-behind-datawrapper) even.
The idea behind it is to make creating graphs very easy.
Just like with Django, the people behind it have a newsroom background.

I immediately liked there's no hurdle of setting up an account.
A simple wizard is presented:

![](/static/images/posts/11-07-2025-public-notes/wizard-datawrapper.png)

To publish the end result I did have to create an account though.
The [end result](https://www.datawrapper.de/_/mZ7ba/) looks quite good and was easy to make. I could just provide a GitHub URL containing the CSV of chess puzzle data I gathered. I come to like this idea of using GitHub as a sort of database more and more.

---

Maybe I can do even better and integrate things with GitHub Codespaces.
This way you could do a basic analysis completely in the browser:

- data is [saved in CSV format](https://github.com/IsaacVerm/track-puzzle-storm/blob/main/puzzles.csv) in a GitHub repo
- [sqlite-utils](https://sqlite-utils.datasette.io/en/stable/) is used to aggregate the data how we want to
- visualisation is created in Datawrapper

Say I want to know if I improved over time in Lichess Puzzle Storm.
I can group by date and calculate the percentage of solved puzzles by date in `sqlite`.

Exact steps to take:

- Open codespace in [track-puzzle-storm repo](https://github.com/IsaacVerm/track-puzzle-storm)
- Install `sqlite-utils` in this codespace: `npx install sqlite-utils`
- Calculate the percentage of puzzles solved by day
    - `sqlite-utils memory puzzles.csv --csv "select date, avg(solved) as perc_solved from puzzles group by date"`
    - There's [no need to create an intermediate `sqlite` table](https://sqlite-utils.datasette.io/en/stable/cli.html#running-queries-directly-against-csv-or-json).
    - I use DD-MM-YYYY as date format. There's no date format in `sqlite` so the date will be saved as text meaning the ordering won't be done chronologically. You can sidestep this problem by using `YYYY-MM-DD` (the inverse) as date format instead.
- Save and commit result to GitHub:
    - `{sql command outputing to csv} > perc_solved_by_date.csv`
    - `git add -A`
    - `git commit -m "add perc_solved_by_date.csv"`
    - `git push`
- Get [link to raw CSV file on GitHub](https://raw.githubusercontent.com/IsaacVerm/track-puzzle-storm/refs/heads/main/perc_solved_by_date.csv)
- Create graph in Datawrapper

With a bit of practice this can all be done rather quickly.
And best of all, you can do all of it in your browser.
The [final result](https://www.datawrapper.de/_/PdD9C/) looks rather good out of the box.

---

My current approach to these public notes works well:

- when I come across something interesting I add it to the `PUBLIC NOTES` chat group
- based on these entries I start adding notes for the day
- whenever I notice I keep working on the same thing, I can compile these notes into a bigger project note

Added benefit: never have to start from scratch with a project note since I can build upon the daily notes already created by that time.