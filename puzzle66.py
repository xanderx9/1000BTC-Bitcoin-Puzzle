
import bitcoin
from bitcoin import privtopub, pubtoaddr
import multiprocessing
import random
import sys

# Function to check a range of keys, with randomization by sampling
def check_key_range(start_key, stop_key, target_address, process_id, randomize=False):
    key_range_size = stop_key - start_key + 1
    
    checked_keys = set()  # To avoid duplicate checks
    
    for i in range(key_range_size):
        if randomize:
            key = random.randint(start_key, stop_key)  # Random key within the range
            while key in checked_keys:
                key = random.randint(start_key, stop_key)  # Ensure no duplicates
        else:
            key = start_key + i
        
        checked_keys.add(key)
        priv_key_hex = format(key, '064x')
        pub_key = privtopub(priv_key_hex)
        generated_address = pubtoaddr(pub_key)
        
        # Progress feedback for this process
        if i % 1000 == 0:  # Adjust frequency as needed
            progress = (i / key_range_size) * 100
            print(f"Process {process_id}: Checked {i}/{key_range_size} keys ({progress:.4f}% complete)")
            sys.stdout.flush()

        if generated_address == target_address:
            print(f"Private key found by Process {process_id}: {priv_key_hex}")
            sys.stdout.flush()
            return priv_key_hex
    return None

if __name__ == '__main__':
    target_address = "1ErZWg5cFCe4Vw5BzgfzB74VNLaXEiEkhk"
    start_key_hex = "0000000000000000000000000000000000000000000000000000000000002000"
    stop_key_hex = "00000000000000000000000000000000000000000000000200000000000000ff"
    
    start_key = int(start_key_hex, 16)
    stop_key = int(stop_key_hex, 16)
    
    # Determine the number of processes to run in parallel
    num_processes = multiprocessing.cpu_count()  # Use all available CPU cores
    key_range = stop_key - start_key + 1
    range_per_process = key_range // num_processes
    
    processes = []
    for i in range(num_processes):
        range_start = start_key + i * range_per_process
        range_stop = start_key + (i + 1) * range_per_process - 1 if i != num_processes - 1 else stop_key
        p = multiprocessing.Process(target=check_key_range, args=(range_start, range_stop, target_address, i + 1, True))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    print("Search completed.")
