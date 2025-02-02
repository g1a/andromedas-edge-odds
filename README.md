# andromedas-edge-odds

Calculate the odds of winning a battle in Andromeda's Edge.

In Andromeda's Edge, combat is resolved by rolling dice. Each participant has between one and six dice, and also has a "targeting" value ranging from one to five. The player with the single highest die result is the winner; in the case of a tie, the tied dice are discarded, and the next-highest die is used to determine the result. If all of the dice come up exactly the same, then everyone loses.

The table below shows the odds of the "attacker" in a combat winning, given different targeting and number of dice. Click on the desired targeting values and then find the cell matching the number of dice being rolled by the two players.

[TODO: Table here]

The background color of the cell indicates the likelyhood of the attacker winning, in case you just want to "go by vibe".

Note that in Andromeda's Edge, combats can involve more than two players.

## Why

This project started out as an experiment to determine if Chatgpt could be coerced into calculating the odds of winning a combat in Andromeda's Edge with targeting. Initial attempts were done via brute force, and resulted in the AI telling me I had used too much compute time, and locking me out of further experiments for 24 hours. After that, I was able to get it to write the binomial_probability function that is at the core of this program today. My theory was that, in using probability theory instead of brute force, Chatgpt would have enough available processing power to complete the assignment. While it was able to calculate the combinatorics involved with two players rolling six dice (resulting in the probability_table function), the recursion required to calculate outcomes was beyond it, and I was forced to finish the algorithm and add the targeting calculations myself.

## License

No rights are reserved over any of the code presented in this project; see the [License](LICENSE) for more information. The copyright to Andromeda's Edge is held by its publisher, [Cardboard Alchemy](https://cardboardalchemy.com/).

Portions of the css styling used in this project are distributed under the [MIT License](GITHUB-FORK-RIBBON-CSS-LICENSE).

## Acknowledgments

Everyone in my gaming group is immensely grateful to Luke and Maximus Laurie for designing [Andromda's Edge](https://boardgamegeek.com/boardgame/358661/andromedas-edge), which is, perhaps, the best board game ever made. The biggest controversy among our members is whether Andromeda's Edge or its predicessor, [Dwellings of Eldervale](https://boardgamegeek.com/boardgame/271055/dwellings-of-eldervale), is the better game. We are, however, all agreed that both games are absolutely amazing, and will both continue to be brought to our table often. 

Prior art for [calculating combat odds in Dwellings of Eldervale](https://boardgamegeek.com/thread/2240247/odds-of-winning-combat) was presented by [Jonathan /
@Arcanist Lupu](https://boardgamegeek.com/user/Arcanist%20Lupus), which was very useful for confirming that the results produced by the binomial_probability were accurate.

Thanks to Simon Whitaker for [github-fork-ribbon-css](https://github.com/simonwhitaker/github-fork-ribbon-css).