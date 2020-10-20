__version__ = "1.0"
__author__ = "Patrick Bardo"

import json
import sys

def auction():
    adjustment_dict, sites_dict = load_config('/auction/config.json')

    # Load the auction inputs from STDIN
    auctions = json.load(sys.stdin)

    output = []
    output_keys = ["bidder", "bid", "unit"]

    for auction in auctions:

        max_bids = {}

        if (is_valid_site(auction["site"], sites_dict)):
            bids = auction["bids"]
            units = auction["units"]
            site = sites_dict[auction["site"]]

            for bid in bids:

                if (is_valid_bid(bid, adjustment_dict, site, units)):
                    adjustment = (1+adjustment_dict[bid["bidder"]])
                    adjusted_bid = bid["bid"]*adjustment

                    # If a bid for the specified unit has already been made
                    if (max_bids.get(bid["unit"]) != None):
                        current_max = max_bids[bid["unit"]]["adjusted_bid"]

                        #Check if this is the max bid
                        if (current_max < adjusted_bid):
                            max_bids[bid["unit"]] = bid
                            max_bids[bid["unit"]]["adjusted_bid"] = adjusted_bid

                    # Create the first bid when it doesn't exist
                    else:
                        max_bids[bid["unit"]] = bid
                        max_bids[bid["unit"]]["adjusted_bid"] = adjusted_bid

        units_list = []
        for unit_key in max_bids:
            output_dict = {output_key:max_bids[unit_key][output_key] for output_key in output_keys}
            units_list.append(output_dict)

        output.append(units_list)

    print(json.dumps(output))



def load_config(file):
    """Loads the config.json file located in this directory. This configuration contains the valid sites and bidders including other configurations about each.

    Keyword arguments:
    file -- A string containing the location of the config.json file

    Returns:
    adjustment_dict -- A dictionary containing all adjustments with keys being bidder names
    sites_dict -- A dictionary with all site configurations. ex. {
        "name": {
            "bidders": [],
            "floor": int
        }
    }
    """
    adjustment_dict = {}
    sites_dict = {}
    with open(file) as json_file:
        data = json.load(json_file)
        sites = data["sites"]
        bidders = data["bidders"]

        for site in sites:
            sites_dict[site["name"]] = {}
            sites_dict[site["name"]]["bidders"] = site["bidders"]
            sites_dict[site["name"]]["floor"] = site["floor"]

        for bidder in bidders:
            adjustment_dict[str(bidder["name"])] = bidder["adjustment"]


    return adjustment_dict, sites_dict

def is_valid_site(input_site, sites_dict):
    """Validate whether the current auction site is in the configuration list of sites

    Keyword arguments:
    input_site -- A string with the name of the current auction site
    sites_dict -- A dict of all sites in the configuration file

    Returns:
    Boolean
    """

    for name in sites_dict:
        if (name == input_site):
            return True;

    return False

def is_valid_bid(bid, adjustment_dict, site, units):
    """This function checks if the current bid is a valid bid based on the following criteria:
    - permission to bid on the site in question
    - bid must be made on a unit involved in the auction
    - the bidder must be known
    - the adjusted bid must be greater than or equal to the floor of the site

    Keyword arguments:
    bid -- The bid being validated. ex. {"bidder": "AUCT","unit": "banner","bid": 35}

    adjustment_dict -- Dictionary containing the adjustment configurations of each bidder

    site -- The site information of the auction in question. ex. {
    "name": "houseofcheese.com","bidders": ["AUCT", "BIDD"],"floor": 32
    }

    units -- the units involved in the current auction

    Returns:
    Boolean

    """
    bidder = bid["bidder"]

    if (bidder not in site["bidders"]):
        return False

    if (bid["unit"] not in units):
        return False

    # Bidder must be known, what does this mean? Doesn't permission already cover this?
    if (bidder == None):
        return False

    if (bid["bid"]*(1+adjustment_dict[bidder]) < site["floor"]):
        return False

    return True

if __name__ == "__main__":
    auction()
