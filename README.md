# CardCostDivider_Public
The public variant of CardCostDivider. All names are removed and replaced by something generic.

This code was made after some friends and me decided we wanted to buy a number of cards for a game we play called Magic: The Gathering. We chose to bundle our orders together in order to save on shipping costs (and being greener was a nice bonus too :D).
However, the question arose on how to split shipping costs. A number of us eagerly jumped at this puzzle, aiming to dissect the intricacies of this seemingly simple puzzle. Between someone having recently completed a minor in cooperative game theory and wanting to put their new knowledge to use, the collective interest in not overpaying and myself having an interest in the various ways of analysing this it is no surprise that various methods were quickly proposed, and oftentimes rejected just as quickly.
After we settled on an algorithm to divide the costs we still needed to actually execute this, however. This seemed like a fun side project (and it was) so I wrote this. While I sadly didn't get to implement any of the more complicated algorithms (it turned out they all were either unfeasible due to us having too little information or they were not applicable to our situation), this did give me more time to make a system that's applicable more broadly than just for our one specific use case.
#... So, how does it work?
To get set up, you're going to need to make a few .txt files. I could just copy-paste stuff for this application, but I might make a script to automize this later. Regardless, you'll want to make .txt files for both the vendors and the buyers. All cards should be given the name of the vendor/buyer. In it, you're going to want to write the quantity of each product (in our case, copies of each card), the name of the product and, in the case of the vendor document, also the price of the product (per item). Lastly, put the shipping cost of that vendor in each vendor's document.
Then, run the code. It will (or should, at least) output how much each buyer has to pay, both for their products and for the shipping of those products.

Well, that's about it, so enjoy!
