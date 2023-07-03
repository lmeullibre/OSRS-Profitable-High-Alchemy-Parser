import multiprocessing

bind = "0.0.0.0:5000"  # The address and port where your Flask app will be served
workers = multiprocessing.cpu_count() * 2 + 1  # Number of Gunicorn worker processes
threads = 2  # Number of threads per worker
timeout = 120  # Timeout value in seconds