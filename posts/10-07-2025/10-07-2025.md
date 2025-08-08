# 10-07-2025

I was intrigued by this article series [Building a SNAP LLM eval](https://www.propel.app/insights/building-a-snap-llm-eval-part-1/).
It's something I struggled with myself: how do you properly test an LLM?

> While evaluation can be a fairly technical topic, we hope these posts reduce barriers to more domain-specific evaluations being created by experts in these high-impact — but complex — areas.

In the end everyone can write some test examples, you don't need any technical knowhow for that. Just give the input and what's expected.

> One of the more interesting aspects of building an eval is that defining what "good" means is usually not as simple as you might think. Generally people think first of accuracy. And accuracy is important in most scenarios but, as we’ll discuss, there are dimensions beyond strict accuracy we also want to evaluate models.

It's not like mathematics where you just check if 1+1=2 or UI testing where you check if an element is present or not. If you ask a chatbot something, how do you determine if the answer is good or not?
It's easy if the answer is very factual but most questions have nuances and a context.

> We can effectively measure baselines on things like the pace of improvement on SNAP questions of a given class of model (GPT-3 vs. 3.5 vs. 4 vs. o1-mini…).

Excellent counterargument against AI hype: this new model helps us this much but not more.
I should create a test of cases on information I find very interesting and use that as a personal benchmark.

> By building an eval, we are more rigorously defining what "good" is for users’ needs. With that bar set, we can then try lots of different approaches to designing systems that use AI to meet those needs.
The different things we might try include:
> - Underlying foundation models (OpenAI, Anthropic, Google, open source models like Llama and Deepseek)
> - Prompts (“Act like a SNAP policy analyst…” vs. “Act like a public benefits attorney…”)
> - Context/documents (like regulations or policy manuals)

There are a lot of moving parts you can change. If you don't have evals (rigorous definitions of what's good or not), you can't confidently make changes. Checking the results manually each time isn't feasible.

> The boring yet crucial secret behind good system prompts is test-driven development. You don't write down a system prompt and find ways to test it. You write down tests and find a system prompt that passes them.

Return of TDD.

> Meaningful, real problem spaces inevitably have a lot of nuance. 

It's easy to think "oh it's all so easy and straightforward".

> Just using the models and taking notes on the nuanced “good”, “meh”, “bad!” is a much faster way to get to a useful starting eval set than writing or automating evals in code.

It's nice you can test things out with an LLM before moving on to something more permanent.
Allows for an iterative approach.

> The broad categories I’ve used for SNAP, for illustration, have included things like:
> - Strict program accuracy questions (“What is the income limit for a household size of 2?”)
> - Practical SNAP client problems and navigation advice (“I didn’t get my SNAP deposit this month, what should I do?”)
> - Questions where state variability exists
> - Questions where the answer might differ if you are the state agency (thinking about the effects across all of the state’s clients) vs. a legal aid attorney (focused on doggedly serving that specific client’s interests)

Define categories of problems instead of example by example.

> When I do this, I take notes on the subtle problems (and outstanding positive aspects) of the answers, just to build a general sense of where in the SNAP information space more rigorous testing would be useful.

By thinking through these examples, you get to know where you lack knowledge about a topic.
Might be a good approach to learn a new topic, by adding test cases for LLM evals for that topic.

> As an aside, to make this faster, and easier for others, I also built a small internal tool I call Hydra — a Slackbot that lives in a channel and which anyone can prompt in Slack and get back responses from multiple frontier language models, to get a sense of their differences.

Would be cool to have access to a personal chatbot on my phone.

> Strict accuracy needs to be balanced against providing information that actually helps people navigate SNAP.

Accuracy is very rough, real usability is about a lot more.

> In terms of turning this into an eval test, you could imagine two potential versions:
> 1. Making sure the response includes a word like “eliminated” or “BBCE”. This could be done easily in code, but you can imagine how that implementation might mislabel some answers as good or bad.
> 2. Check that the output substantively says that asset limits don’t apply in most states. That’s harder. How do I write code to check that in a string? That’s where we could use a language model to evaluate another model’s output.

This seems very intuitive.

---

The SNAP article above links to [this very interesting article on the same topic of AI evals](https://hamel.dev/blog/posts/evals/). Something to read up on as well.