# andromedas-edge-odds

Calculate the odds of winning a battle in Andromeda's Edge.

## License

No rights are reserved over any of the code presented in this project; see the [License](LICENSE) for more information. The copyright to Andromeda's Edge is held by its publisher, [Cardboard Alchemy](https://cardboardalchemy.com/).

Portions of the css styling used in this project are distributed under the [MIT License](GITHUB-FORK-RIBBON-CSS-LICENSE).

## Acknowledgments

[Andromda's Edge](https://boardgamegeek.com/boardgame/358661/andromedas-edge), designed by Luke and Maximus Laurie is, perhaps, the best board game ever made.

ChatGPT wrote the binomial_probability function. This project started as an experiment to determine if ChatGPT could calculate the probability of the different outcomes of a combat in Andromda's Edge, with the addition of the targeting mechanic. Its initial attempts used so much computational time that I was blocked from further queries for 24 hours. After that, with some prompting, it was able to produce the aforementioned function, and a routine that printed the odds of each combination of results (the probability_table function). However, it wasn't able to manage targeting or the recusive function call.

There is some prior art, [Odds of Winning Combat](https://boardgamegeek.com/thread/2240247/odds-of-winning-combat), a post on Board Game Geek that outlines the odds of winning a combat in [Dwellings of Eldervale](https://boardgamegeek.com/boardgame/271055/dwellings-of-eldervale), the predecessor game to Andromeda's Edge. This post also includes calculations for multiple combatants.

Thanks to Simon Whitaker for [github-fork-ribbon-css](https://github.com/simonwhitaker/github-fork-ribbon-css).