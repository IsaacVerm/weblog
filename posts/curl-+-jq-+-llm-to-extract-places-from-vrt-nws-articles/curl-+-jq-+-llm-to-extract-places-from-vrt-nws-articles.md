# curl + jq + llm to extract places from VRT NWS articles

## What exactly are we trying to accomplish?

1. fetch latest articles from VRT NWS
2. extract titles from these articles
3. create list of places mentioned in titles of these articles

## Fetching the articles

The first step of fetching the articles is as easy as can be. No authentication or anything, just passing the URL is enough (got the URL the same way as I did in [my previous post](https://mini-computer.tail1ad9dd.ts.net/static/posts/tracking-job-postings-flemish-government-using-github-actions.html#find-the-url-of-the-api-endpoint-returning-job-postings)):

```bash
curl https://www.vrt.be/vrtnws/_next/data/lOVEAve2b6oRA8in28B4v/nl/net-binnen.json
```
![](/static/images/posts/14-03-2025---curl-+-jq-+-llm-to-extract-places-from-vrt-nws-articles/net-binnen-json.png)

## Extracting the article titles

To extract the titles we use [jq](https://jqlang.org/), a tool to filter and transform JSON data. Using `jq` isn't hard, but [there's a lot of functionality you don't need right away](https://devdocs.io/jq/). As usual I found DigitalOcean guides, [How To Transform JSON Data with jq](https://www.digitalocean.com/community/tutorials/how-to-transform-json-data-with-jq) in this case, offer a good introduction without having to bite off more than you can chew. Reading that article is enough to [know enough to be dangerous](https://www.learnenough.com/our-philosophy).

Extracting the titles from the `net-binnen.json` file fetched in the step before consists of two problems:

- `net-binnen.json`is deeply nested: you have to drill down the hierarchy (`data` > `compositions` > ...) to eventually get to the text of the title.
- Articles are saved in an array in the `compositions` key: you need to do the extraction for each article.

The `jq` [Object Identifier-Index](https://jqlang.org/manual/#object-identifier-index) helps a lot tackling the nesting problems by allowing you to chain keys. The example below shows how this works in order to get the title of the first article:

```bash
curl https://www.vrt.be/vrtnws/_next/data/lOVEAve2b6oRA8in28B4v/nl/net-binnen.json | jq '.pageProps.data.compositions[0].compositions[0].title.text'
```

We don't need multiple pipes like `jq '.pageProps | '.data' | ...` but can do it all in a single call.

Having solved the first nesting problem, how can we do this extraction for all articles and not just the first one? `jq` offers an excellent solution to this problem, avoiding any loops. By using the [Array Value Iterator](https://jqlang.org/manual/#array-object-value-iterator)  `[]` `jq` will split an array into it's individual elements. In our case the articles array will now return each article separately. In itself this does nothing, but the magic happens when you combine it with the  [pipe](https://jqlang.org/manual/#pipe) `|` operator. The pipe will apply the same action (extracting the title in our case) to each article:

```bash
cat net-binnen.json | jq -r '.pageProps.data.compositions[0].compositions[] | .title.text'
```

The result looks like this with each article title on a new line:

![](/static/images/posts/14-03-2025---curl-+-jq-+-llm-to-extract-places-from-vrt-nws-articles/titles-without-quotation-marks.png)

Note the `-r` flag. If we don't specify this flag, `jq` will keep string quotation marks in the output:

![](/static/images/posts/14-03-2025---curl-+-jq-+-llm-to-extract-places-from-vrt-nws-articles/titles-with-quotation-marks.png)

We want to pass the titles to an LLM so we have no use for these quotation marks.

## Extracting places from these titles

Most titles contain references to geographical places. Just have a look at the first article titles:

> - Gewapende overval op tankstation in **Houthalen-Helchteren**: "Bediende gedwongen geldkoffer af te geven" 
> - Zoekactie naar lichaam Heidi De Schepper in **Balen** wordt stopgezet, onderzoek gaat door
> - Wekelijkse markt in **Halle** verhuist tijdens carnavalsfoor:"Alle pleinen staan vol met kermisattracties"

In a later project I'm planning to do something more interesting with these places like show them on a map so you can see where news events took place. For now I just want to be able to extract them. The [Datasette LLM utility](https://llm.datasette.io/en/stable/) [since a few weeks](https://simonwillison.net/2025/Feb/28/llm-schemas/) offers an easy way to extract structured output using a [concise syntax](https://llm.datasette.io/en/stable/schemas.html#schemas-dsl). You provide the titles, a schema of what you want the output data to look like , a prompt to extract the places and you get all the places mentioned in the titles.

A quick test with the first 5 articles shows just how good this works (the result of the previous step has been saved as `articles-titles.txt`):

```bash
cat article-titles.txt | head -n 5 | llm --schema-multi 'places,article_title' 'extract geographical places from these article titles' | jq '.'
```

Which gives:

![](/static/images/posts/14-03-2025---curl-+-jq-+-llm-to-extract-places-from-vrt-nws-articles/places-from-titles-sonnet.png)

This really feels like magic and it feels like it's important. I do concur with [Simon Willison](https://simonwillison.net/2025/Feb/28/llm-schemas/) on this one:

> I’ve suspected for a while that the single most commercially valuable application of LLMs is turning unstructured content into structured data. That’s the trick where you feed an LLM an article, or a PDF, or a screenshot and use it to turn that into JSON or CSV or some other structured format.

Some small remarks about the command above:

- You need to use `--schema-multi` instead of `--schema` if you want the schema to be applied to all article titles. If you use `--schema` instead you'll only get a result for the first article.
- Note I say "places" and not "place" in the schema. LLMs take things very literal. Sometimes multiple places are mentioned in the same title. If you use "place" in the schema the LLM will only provide the first place it finds, ignoring other places mentioned in the same title. It's very interesting how debugging these days often means speaking proper English.
- `jq .` refers to the [identity operator](https://jqlang.org/manual/#identity). The point is to print the resulting JSON in a readable way (spread over multiple lines, keys and values in different colors,...).

## Which model to use?

By default I use Claude 3.7 Sonnet as LLM model. I was curious if the cheaper Haiku 3.5 model would be able to offer the same  level of quality. This would be a good thing since [Haiku 3.5 only costs about 1/4 of Sonnet 3.7](https://www.anthropic.com/pricing#anthropic-api). And luckily this does seem the case. In some ways it even does a better job than Sonnet. This is what Haiku returns using the same command as above:

![](/static/images/posts/14-03-2025---curl-+-jq-+-llm-to-extract-places-from-vrt-nws-articles/places-from-titles-haiku.png)

Haiku by default seems a bit less strict than Sonnet, but unfortunately not in a consistent way. For example for "Trump vraagt Poetin met aandrang levens van Oekraïense militairen te sparen" Sonnet only identifies "Oekraïne" (the only country really specified in the title), while Haiku identifies both Ukraine and Russia. I get why it extracts Russia since Putin is mentioned in the title, but in that case the USA should be extracted as well since Trump is mentioned too in the title. It's clear some prompt engineering is still required being very explicit about the output: define what language the output should be in and how strict the LLM should be about what exactly constitutes mentioning a place.

Tying it all together this is what the final command combining all steps looks like:

```bash
curl https://www.vrt.be/vrtnws/_next/data/lOVEAve2b6oRA8in28B4v/nl/net-binnen.json | jq -r '.pageProps.data.compositions[0].compositions[] | .title.text' | llm --schema-multi 'places,article_title' 'extract geographical places from these article titles' | jq '.'
```

A short one-liner to go from the URL pointing to a list of articles to a list of all the places mentioned in all of the articles in the list of articles.

## Conclusion

Some reflections upon writing this post:

- You can get quite far if you use the right tools, even in a very basic way.
- It's about [technical sophistication](https://www.learnenough.com/our-philosophy): you don't need to know everything in detail but you should be able to figure out how to use a tool like `jq` in a productive way.
- Working in the command line is always fun because you get instant feedback.
- You can get data from all kinds of sources: who would have thought VRT article titles could be a source of geographical data?
- LLMs open up a lot of new data sources which previously would be hard to access.
- Keeping a post limited is very hard: I tried to limit myself to 200 words and now this post approaches 1400 words while I don't feel like there's a lot I could remove without making the story less clear.
- Next time I should keep the scope of a short post even more limited: just focus on a small topic (schemas in `llm`,  the `Array Value Iterator` in `jq`,...) without integrating those in a larger project.

## CHANGELOG

- 14-03-2025: initial draft