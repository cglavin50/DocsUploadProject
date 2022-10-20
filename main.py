from Doc import Doc
import FileHandler


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # first, get keys
    print("Fetching keys")
    keys = FileHandler.getKeys()
    print(keys[0] + ", " + keys[1])

    # second, download objects from s3 to refresh local library (cwd for now)
    FileHandler.download_bucket(keys)

    # next, instantiate a document object so the user can create, save, and edit documents
    d = Doc("New Document")

    # finally, upload all the locally edited files to the bucket and quit
    FileHandler.upload_bucket(keys)
# end main
