# Steam Races Update

Welcome to the steam races! 
The goal of this project is two-fold:
1. for me to practice my data analysis and data science skills outside of my day [job](https://drcwadaniels.github.io/)
2. to gain some insight into player dynamics on steam. 

Now, admittedly, because I am scraping the steam statistics page to get player counts it will not be as reliable as using their API. Nonetheless, we should be able to glean some insights from just visually inspecting our data. 


**What's on as of 4/20/2021 @ 11:59pm ?**

![AbsolutePlayers](https://github.com/drcwadaniels/steamraces/blob/master/AbsolutePlayers.png)

*Figure 1* The figure above shows the cumulative sum of the absolute current players at the bottom of every hour (i.e., ~ at the 30 minute mark of each hour). Data were sorted based on the maximum number of cumulative sum players such that each panel in the figure contains 20 games going left to right, top to bottom from game with most current players to least current players.

![RelativePlayers](https://github.com/drcwadaniels/steamraces/blob/master/RelativePlayers.png)

*Figure 2* The figure above  shows the same data as in *Figure 1*, except now the data have been rescaled to the minimum number of players. 

**What to make of this data**

I think there are a few take aways based on *Figure 1*

1. The top games are not surprising as they are multiplayer juggernauts with broad appeal. 
2. Most games have a period in which the slope is relatively steep and constant indicating maintenance of player counts 
3. More often than not this is followed by a reduction in the slope indicating some individuals have perhaps turned in for the night
4. Other times the slope increases! Indicating a surge in popularity. For example, Source SDK in the third panel, top row
5. Overall, the slopes of these cumulative sums seems to indicate strong nonlinearities and game differences 

However, inspection of *Figure 2* qualifies these observations

1. When data are normalized by the initial number of players we find that most of the cumulative sums are actually fairly linear with similar slopes
2. Normalization reveals who the true stand outs are within each set of games. For example, Sid Meier's Civ VI, World of Tanks Blitz, and Farming Simulator all develop slopes steeper than the rest of their cohort. 
3. Rather than reflecting game differences, the changes in slope seem to occur around the time that perhaps most steam users are signing off for the night. 

Return here to see updates to the graphs and revisions of conclusions.
