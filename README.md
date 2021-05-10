# HistoryGuesser

## Install

```
pip3 install -r requirements.txt
```

## Running

```
export OPENAI_API_KEY=<your-api-key> 
export OPENAI_API_ORG_ID=<your-org-id>
export DBPASS=<your-db-password>
export DBUSER=<your-db-username>
export URI=<your-db-uri>
cd src && python3 app.py
```

## Testing questions

You can test questions like this.

```
# Run five tests
python3 test.py 5 "Did you know how to use a sword?"
```

```
Nelson Mandela:  Yes, I did.
Rene Descartes:  I did not know how to use a sword. 
Henry VIII:  Yes, I was a good swordsman.
Toni Morrison:  Yes, I did.
Abraham Lincoln:  Yes, I did.
```