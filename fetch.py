import rest
import exe_WP_only
from time import sleep

while True:
    request_data = rest.get()

    for entry in request_data:
        rest.is_fetched(entry)

        if "WP" in entry['data']:
            if "pi" in entry['data']:
                print("Waveplate rotates")
                exe_WP_only.exe_WP_only(90)
                rest.put_result(entry)

        else:
            print("Unknown command")

        sleep(5)

    print("fetched")
    sleep(10)
