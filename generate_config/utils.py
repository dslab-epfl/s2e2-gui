

def write_string_to_disk_and_close(path, string):
    with open(path, 'wb+') as destination:
            destination.write(string)
    destination.close()