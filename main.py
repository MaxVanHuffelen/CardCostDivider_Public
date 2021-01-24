#IMPORTS
#No imports are needed? Welp, that's a first...

#Define Collections
 #Tuples containing the names of all vendors and buyers, respectively.
listVendors = ('Vendor1', 'Vendor2', 'Vendor3', 'Vendor4', 'Vendor5', 'Vendor6', 'Vendor7', 'Vendor8', 'Vendor9', 'Vendor10', 'Vendor11', 'Vendor12', 'Vendor13', 'Vendor14', 'Vendor15', 'Vendor16', 'Vendor17', 'Vendor18')
listBuyers = ('Buyer1', 'Buyer2', 'Buyer3')
 #These are dictionaries containing all the vendors, cards and buyers, respectively. The indices are strings of the names of vendors/cards/buyers. Values are (pointers to) the relevant object.
allVendorsDict = dict()
allCards = dict()
allBuyersDict = dict()

#Define Classes
class Card:
	'''
	A class that is used to represent cards (duh). Has the parameters and function:
	name: the name of the card(s)
	totalQuantity: the total amount of this cards bought at all vendors
	totalPrice: the combined price at which we bought all of these cards
	allVendors: a set containing the names of all vendors from which we bought these card(s)
	registeredBought: the total amount of these cards that are registered as being bought by buyers. This should be equal to self.totalQuantity. If this is not the case, something went wrong
	'''
	def __init__(self, name, totalQuantity, totalPrice, firstVendorName):
		self.name = name.lower()
		self.totalQuantity = totalQuantity
		self.totalPrice = totalPrice
		self.allVendors = {firstVendorName}
		self.registeredBought = 0
	def __str__(self):
		return f'{self.name}; total qty:{self.totalQuantity}, total price:{self.totalPrice}, vendors:{self.allVendors}'
	def checkSoldBought(self):
		'''
		Checks if the amount of this card that are registered as sold by a vendor is equal to the amount of this card registered as bought by a buyer. If these are not equal, an AssertionError is raised.
		'''
		assert self.totalQuantity == self.registeredBought

class Vendor:
	'''
	This describes one vendor that sold us cards. It has a number of parameters;
	name : what the vendor is called. The document in the vendors folder that lists what we bought from the guy has the same name.
	shipping : the shipping cost from this vendor.
	soldCards : a dictionary with the cards we bought from the vendor as indices, and the number of those cards we bought as values related to the indices.
	'''
	def __init__(self, name):
		self.name = name.lower()
		self.shipping = 'TBD'
		self.soldCards = dict()
		self.totalPrice = 0
	def __str__(self):
		return f' - - = {self.name} = - - \nShipping: {round(self.shipping,2)} \nTotal Costs: {round(self.totalPrice,2)} \nCards Sold: {self.soldCards}\n '

class Buyer:
	'''
	A class that represents a person buying cards. It has two parameters:
	name: the name of the buyer.
	boughtCards: a dictionary containing all the cards bought by this buyer. Indices are strings of the cardnames. Values are the cards
	spentCards: the total amount of money spent on cards
	spentShipping: the total amount of money spent on shipping
	'''
	def __init__(self, name):
		self.name = name.lower()
		self.boughtCards = dict()
		self.spentCards = 0
		self.spentShipping = 0
	def __str__(self):
		return f'Expenses of {self.name}: Cards: {round(self.spentCards,2)}, Shipping: {round(self.spentShipping,2)}'

#Define Functions
def price2float(price):
	'''
	A simple function to transform a string of a price to a float of that price
	:param price: a string of the price, formatted as '123 EUR' or '123'
	:return: a float of that same price, so e.g. 123.
	'''
	return float(price.strip('EUR').replace(',', '.'))

def createVendor(vendorName):
	'''
	Given the name of a vendor, this will automatically do the following:
	- Create a Vendor object for this vendor using vendorName as the name parameter of the Vendor.
	- Open the file with named vendorName in the vendors directory and extract:
		- the shipping cost from this vendor
		- the cards, their cost (per card) and their quantity
		- NOTE: it should be noted that some information is discarded, most notably the version of the card (denoted by '(V.x)', where x is the version, in the card's name) in addition to the set, rarity, condition and language of the card.
	- Place the extracted cards in the allCards dictionary, updating the totalQuantity, totalPrice and allVendors parameters as necessary
	- Place the extracted cards in the Vendor's soldCards and updates Vendor's parameters
	:param vendorName: the name of the vendor, as a string
	:return: vendor: the object of Vendor class representing the vendor
	'''

	lines = open('vendors/'+vendorName, 'r').readlines()
	vendor = Vendor(vendorName)
	allVendorsDict[vendorName] = vendor

	for line in lines:  #Not the prettiest but it works ¯\_(ツ)_/¯
		if line[:8] == 'Shipping':
			vendor.shipping = price2float(line.split()[-2])
		else:
			quantity, rest = line.strip().split(' ', 1)
			quantity = int(quantity.strip('x'))
			name, rest = rest.lower().rsplit(' (', 1)
			price = rest.split()[-2]
			price = price2float(price)
			if '(v.' in name:
				name = name[:-6]
			if name not in allCards:
				allCards[name] = Card(name, quantity, quantity*price, str(vendorName))
			else:
				allCards[name].totalQuantity += quantity
				allCards[name].totalPrice += quantity*price
				allCards[name].allVendors.add(vendorName)
			vendor.soldCards[name] = (quantity, price, allCards[name])
			vendor.totalPrice += price*quantity
	return vendor

def createBuyer(buyerName):
	'''
	Given the name of a buyer, this will do the following:
	- Create a Buyer object with the name of the buyer. This Buyer is then placed in the allBuyersDict (index is buyerName, value is the Buyer object)
	- Open the file with buyerName in the buyers folder and extract the cards bought by this vendor and the quantity in which they are bought
		- NOTE: it should be noted that some information is discarded, most notably the version of the card (denoted by '(V.x)', where x is the version, in the card's name) in addition to the set, rarity, condition and language of the card.
	- Store all the bought cards in the boughtCards library (index is the card's name, value is the quantity in which the card is bought)
	:param buyerName: the name of the buyer, as a string
	:return: buyer: the object of Buyer class representing the buyer
	'''
	lines = open('buyers/'+buyerName, 'r').readlines()
	buyer = Buyer(buyerName)
	allBuyersDict[buyerName] = buyer

	for line in lines:      #We iterate over the lines to keep register which cards buyer buys, and how many of each
		quantity = 1        #The amount of the card is assumed to be 1 unless the first character(s) is a number
		if line[0] >= '0' and line[0] <= '9':       #check if the first character of the line is a digit. Since card names don't have digits in them, this checks if a non-one quantity of hte card is bought.
			quantity, line = line.strip().split(' ', 1)
			quantity = int(quantity.strip('x'))
		cardName = line.lower().rsplit(' (', 1)[0].strip()
		if '(v.' in cardName:           #remove the version tag from the cardName
			cardName = cardName[:-6]
		buyer.boughtCards[cardName] = quantity
	return buyer

def calculateExpenses(buyerName):
	'''
	This is used to calculate the total amount of money expended by a buyer, split into money spent on cards and the shipping of those cards. If multiple buyers buy from one vendor, the shipping cost is weighted by money spent and divided amongst the buyers (that is; if you would buy from a vendor for 80% of the total amount of money spent there, you would also pay 80% of the shipping cost of that vendor)
	:param buyerName: the name of the buyer, as a string
	:return: costCards, costShipping: the amount of money spent on the cards and the shipping thereof, respectively. Both values are in Euro's, just like the inputs.
	'''
	costCards = 0
	costShipping = 0
	buyer = allBuyersDict[buyerName]
	for cardName in buyer.boughtCards:
		#add cost of cards
		card = allCards[cardName]
		costCards += card.totalPrice / card.totalQuantity * buyer.boughtCards[cardName]     #This is written such that if multiple vendors and buyers sell and buy the card, every buyer pays the average price of the card (vendors might have different prices after all)
		card.registeredBought += buyer.boughtCards[cardName]
		#calculate weighted cost of shipping
		for vendorName in card.allVendors:
			vendor = allVendorsDict[vendorName]
			costShipping += vendor.shipping * vendor.soldCards[cardName][1]*vendor.soldCards[cardName][0]/vendor.totalPrice * buyer.boughtCards[cardName]/card.totalQuantity     #Contribution to shipping cost is the total shipping cost from this vendor * (value all copies of this card / value all cards sold by this vendor) * (number of copies of this card bought by this buyer / total number of copies bought by all buyers)
	return costCards, costShipping

def createBuyersVendors():
	'''
	This function simply creates a vendor for each name in listVendors and a buyer for each name in listBuyers. Calcultes the cardCost and shippingCost for each buyer
	:return: totalCardCost, totalShippingCost: the total amount spent on cards and shipping, respectively. Both are rounded to two digits
	'''
	for vendor in listVendors:
		createVendor(vendor)
	totalShippingCost, totalCardCost = 0, 0
	for buyerName in listBuyers:
		buyer = createBuyer(buyerName)
		spentCards, spentShipping = calculateExpenses(buyerName)
		buyer.spentCards, buyer.spentShipping = spentCards, spentShipping
		totalCardCost += spentCards
		totalShippingCost += spentShipping
	return round(totalCardCost,2), round(totalShippingCost,2)

def check_allSoldBought():
	'''
	Checks if each card has the same amount of copies registered sold and bought. Raises an error if any cards have discrepancies (N.B. it will raise an error the first time this is encountered (not for every card where discrepancies are present). Then interrupts the code after raising the error because y'know errors.
	'''
	for cardName in allCards:
		allCards[cardName].checkSoldBought()
	pass

def assert_totalShipping(referenceShipping):
	'''
	Checks if the total amount charged for shipping and asserts whether it's equal to a reference value
	:param referenceShipping: the value to which the total amount charged for shipping should be equal
	'''
	totalShipping = 0
	for vendorName in allVendorsDict:
		vendor = allVendorsDict[vendorName]
		shipping = vendor.shipping
		totalShipping += shipping
	assert round(totalShipping,2) == referenceShipping

def assert_totalCardCost(referenceCardCost):
	'''
	Checks the total amount charged for cards and asserts whether it's equal to a reference value
	:param referenceCardCost: the value to which the total amount charged for cards should be equal
	'''
	totalCardCost = 0
	for vendorName in allVendorsDict:
		vendor = allVendorsDict[vendorName]
		vendorCardCost = 0
		for cardName in vendor.soldCards:
			quantity, price = vendor.soldCards[cardName][0:2]
			vendorCardCost += quantity*price

		totalCardCost += vendorCardCost
	assert round(totalCardCost,2) == referenceCardCost

def printExpenses(totalCardExpenses, totalShippingExpenses):
	'''
	This function prints the expenses of every Buyer as well as the total expenses by everyone combined.
	:param totalCardExpenses: The total expenses on cards
	:param totalShippingExpenses: The total expenses on shipping
	'''
	for buyerName in allBuyersDict:
		print(allBuyersDict[buyerName])
	print(f'The combined expenses are:\nCards: {totalCardExpenses}\nShipping: {totalShippingExpenses}\nAlltogether:{round(totalCardExpenses+totalShippingExpenses, 2)}')

#Actually run stuff
if __name__ == '__main__':

	totalCardCost, totalShippingCost = createBuyersVendors()

	check_allSoldBought()

	assert_totalShipping(totalShippingCost)

	assert_totalCardCost(totalCardCost)

	printExpenses(totalCardCost, totalShippingCost)
