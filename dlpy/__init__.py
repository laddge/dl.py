import requests
from tqdm import tqdm
import sys


def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
        if len(sys.argv) == 2:
            local_path = './'
        elif len(sys.argv) == 3:
            local_path = sys.argv[2]
        else:
            print('Usage: {} url [path]'.format(sys.argv[0]))
            return 1
    else:
        print('Usage: {} url [path]'.format(sys.argv[0]))
        return 1
    local_filename = url.split('/')[-1]
    path = local_path + local_filename
    pbar = None
    headers = requests.head(url).headers
    if 'content-length' in headers.keys():
        fs = int(headers['content-length'])
        pbar = tqdm(total=fs, unit='B', unit_scale=True)
    res = requests.get(url, stream=True)
    with open(path, 'wb') as file:
        for chunk in res.iter_content(chunk_size=1024):
            file.write(chunk)
            if pbar:
                pbar.update(len(chunk))
        if pbar:
            pbar.close()
    print('Saved to {}'.format(path))


if __name__ == '__main__':
    main()
