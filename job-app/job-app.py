import os

JOB_TYPE = os.getenv('JOB_TYPE', 'stateless')
EDGE_API_URL = os.getenv('EDGE_API_URL', 'http://cluster-dns.edge.edge-app')


def do_the_job(job_type):
    print(f'Working hard on {job_type}')


if __name__ == "__main__":
    do_the_job(JOB_TYPE)
