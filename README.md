<h1> Sortable Auction Coding Challenge </h1>
This is my implementation of the Sortable interview challenge done in python. To run the docker image with the challenge, run:

~~~
docker build -t challenge .
$ docker run -i -v /path/to/test/config.json:/auction/config.json challenge < /path/to/test/input.json 
~~~

This will output (to STDOUT) the highest bidders of each unit on a site. When there are no valid bids or something results in the auction being invalid, an empty list will be printed.

<h2> Extra Info </h2>

There are assumptions and notes within the [notes.txt](https://github.com/pattybardo/auction-challenge-master/blob/main/notes.txt) file. There are also extra test cases I wrote within auction/test_cases, and a summation of all test cases into one input JSON file [input_all.json](https://github.com/pattybardo/auction-challenge-master/blob/main/auction/input_all.json). 

<h2>Example </h2> 

Input:

~~~
[
    {
        "site": "houseofcheese.com",
        "units": ["banner", "sidebar"],
        "bids": [
            {
                "bidder": "AUCT",
                "unit": "banner",
                "bid": 35
            },
            {
                "bidder": "BIDD",
                "unit": "sidebar",
                "bid": 60
            },
            {
                "bidder": "AUCT",
                "unit": "sidebar",
                "bid": 55
            }
        ]
    }
]
~~~

Output:

~~~
[[{"bidder": "AUCT", "bid": 35, "unit": "banner"}, {"bidder": "BIDD", "bid": 60, "unit": "sidebar"}]]
~~~

<h3> Feedback </h3>
Feel free to shoot me a message at patryk.bardo@gmail.com or call me if you'd like to discuss my implementation or have any questions!
