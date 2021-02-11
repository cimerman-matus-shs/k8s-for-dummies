import os

JOB_TYPE = os.getenv('JOB_TYPE', 'stateless')
EDGE_API_URL = os.getenv('EDGE_API_URL', 'http://cluster-dns.edge.edge-app')
DISK_PATH = '/mnt/storage'
FIB_N = 35


def do_the_job(job_type):
    print(f'Working hard on {job_type}')

    if job_type == 'stateless':
        n = fib(FIB_N)

        print(f'Before disk write: {os.listdir(DISK_PATH)}')

        with open(os.path.join(DISK_PATH, str(n) + '.txt'), 'w') as f:
            f.write(str(n))

        print(f'After disk write: {os.listdir(DISK_PATH)}')

        return n
    elif job_type == 'stateful':
        # TODO: try to read from disk
        pass


def fib(n):
    if n <= 0:
        return 0
    elif n == 1 or n == 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)


if __name__ == "__main__":
    do_the_job(JOB_TYPE)
