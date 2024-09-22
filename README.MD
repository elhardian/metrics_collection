# Metrics Collection Decorator

Collect function time execution and store to sqlite database.

## Usage

1. Installing dependencies
```pip install -r requirements.txt```
2. Run app
```python main.py```

## Folder Structure

```plaintext
metrics_collection/
│
├── helpers/             # Main application code
│   └── logger.py        # Logger helper
│
├── integrations/         # Integration to other services
│   ├── database/         # Database folder
│   │   ├── __init__.py   # Database configuration
│   │   └── exception.py  # Exception related to database error
│   └── queue/            # Messaging Queue
│       └── collection_consumer.py   # Consumer that listen to metric event
|
├── models/               # Database models
│   ├── base.py           # Base database configuration
│   └── metric.py         # Metric model
|
├── usecases/             # Some logic per module
│   ├── metric_collection.py  # Matric collection related functions
│   └── sample_function.py    # Sample function that implement metric collection decorator
│
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── .gitignore            # Git ignore file
