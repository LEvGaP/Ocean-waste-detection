from pathlib import Path
import boto3
import tqdm
import threading
import math

class ThreadedLoader:
    __instance = None

    def __init__(self, aws_access_key_id, aws_secret_access_key, 
                 endpoint_url="https://storage.yandexcloud.net", bucket_name="waste"):
        self.resource = boto3.resource(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        self.bucket_name = bucket_name
        self.bucket = self.resource.Bucket(bucket_name)
        ThreadedLoader.__instance = self
        pass

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            raise RuntimeError("threaded loader was not created yet")
        instance: ThreadedLoader = cls.__instance
        return instance
    
    def download_list(self, object_keys, on_complete = lambda: None):
        for key in object_keys:
            directory = Path(key).parent
            if not directory.exists():
                directory.mkdir(parents=True, exist_ok=True)
            self.bucket.download_file(key, key)
            on_complete()
        pass


    def load_by_paths_threaded(self, object_keys, num_workers=10):
        n = len(object_keys)
        print(f'loading {n} objects')
        step = math.ceil(n / num_workers)
        workers = []
        with tqdm.tqdm(total=n) as pbar:
            advance = lambda: pbar.update()
            for i in range(num_workers):
                t = threading.Thread(target=lambda: self.download_list(object_keys[i * step: (i + 1) * step], advance),
                                    daemon=True)
                workers.append(t)
                t.start()
            for t in workers:
                t.join()
        pass

    def download_folder_threaded(self, folder_name, num_workers = 10):
        keys = [obj.key for obj in self.bucket.objects.filter(Prefix=folder_name)]
        self.load_by_paths_threaded(keys, num_workers)
        pass
    pass