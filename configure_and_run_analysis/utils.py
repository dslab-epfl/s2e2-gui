def write_string_to_disk_and_close(path, string):
    """
    Write a string to the given path and close the file.
    """
    with open(path, 'wb+') as destination:
            destination.write(string)
    destination.close()
    
def write_file_to_disk_and_close(path, w_file):
    """
    Write the file to the given path and close the file.
    Handle file in a memory efficient way.
    """
    with open(path, 'wb+') as destination:
        for chunk in w_file.chunks():
            destination.write(chunk)
    destination.close()
    w_file.close()
    