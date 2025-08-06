# Choosing data format for data saved to GitHub repo

## What can go wrong when saving data?

Previously I wrote a [post about using GitHub Actions to scrape Flemish government job postings](https://mini-computer.tail1ad9dd.ts.net/static/posts/tracking-job-postings-flemish-government-using-github-actions.html). The results are saved on [GitHub](https://github.com/IsaacVerm/track-werken-voor-vlaanderen) in JSON format. This was the first time I did so and I do regret some choices (or lack of thinking about how to handle these):

- I'm keeping all the data in one big object: should have just kept the job postings and discarded the metadata.
- Each job posting is spread over multiple lines: `git` excels at comparing files line-by-line so if each job posting would be on a line of its own, it'd be much easier to check how many job postings were added or removed at any given point in time.

## Is JSON always the best option?

Next to this the project also got me wondering whether JSON is the right format for my needs. CSV especially seems attractive because it would allow to leverage `git`'s ability to make line-by-line comparison. Although that's true, [CSV has its disadvantages](https://jsonlines.org/examples/):

- Data has to be flat: `JSON` allows to have objects nested within objects or arrays within objects, when using CSV there's no such thing.
- Everything is text: there are no data types (numeric, string, boolean, ...).
- This means how the data is handled depends on the system you're using, you can never be sure the application you're using will interpret the data the way you want.

## JSON Lines, the ideal solution

These are pretty big disadvantages, all of this to have line-by-line comparisons. Luckily this is one of those rare cases where you can have your cake and eat it too. A format called [JSON Lines](https://jsonlines.org/), sometimes also called NDJSON (newline-delimited JSON), exists (I was vaguely aware of its existence since [the Lichess API uses it](https://lichess.org/api). The main idea of JSON Lines is each line contains a valid [JSON value](https://www.json.org/json-en.html) and these lines are separate by newlines. This solves the main issue I had with using JSON as a format to save data in. Now it's easy to see at a glance what data has been added or removed. Take for example the data added in [this commit](https://github.com/IsaacVerm/track-vrt-nws/commit/40f765e018a6a729afb5928cf23afcdff496375f) in the `track-vrt-nws` repository (in which I scrape new news articles and if there are any I add them to the file below):

![](/static/images/posts/19-03-2025---choosing-data-format-for-data-saved-to-github-repo/git-changes-main-events-track-vrt-nws.png)

The remaining question is how to get there. I had fun using `jq` when [tracking job postings](https://github.com/IsaacVerm/track-werken-voor-vlaanderen) or [new subsidies](https://github.com/IsaacVerm/track-subsidieregister), so I was happy to discover `jq` offers the [`--compact-output` option](https://jqlang.org/manual/#invoking-jq) which offers exactly what I need:

> By default, jq pretty-prints JSON output. Using this option will result in more compact output by instead putting each JSON object on a single line.

For example, [this](https://github.com/IsaacVerm/track-werken-voor-vlaanderen/blob/ea9d6a976f31cf492b54cd632e9db6a8521af705/curl-overview-search-min.sh#L24) shows how it's applied in the `track-werken-voor-vlaanderen` repo. 
A small flag and you can always revert back to JSON.

## Conclusion

JSON Lines perfectly suits my needs: it's the best combination of JSON and having each element on a single line to easily compare data changes. Thanks to `jq` transforming JSON to JSON Lines or the inverse is a breeze.

## CHANGELOG

- 19-03-2025: initial draft