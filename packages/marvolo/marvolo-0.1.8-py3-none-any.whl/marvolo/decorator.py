import time

def cal_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"[{func.__name__}] took {end_time - start_time:.5f} seconds")
        return result
    return wrapper

def main():
    @cal_time
    def test():
        for i in range(100000):
            x = 1
        
    test()

if __name__ == '__main__':
    main()
