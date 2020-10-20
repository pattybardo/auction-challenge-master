FROM python:3.9

ADD auction.py /

CMD ["python", "-m", "auction"]
