from lib import create_serializer, SERIALIZERS

def main():
    print(create_serializer("json"))

if __name__ == "__main__":
    main()

    # members = getmembers(some())
    # for mem in members:
    #     if not mem[0].startswith("__"):
    #         if type(mem[1]) is not str: 
    #             print(mem[1])