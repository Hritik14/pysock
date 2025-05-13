from sock import Sock

def sock_main(sock: Sock):
    sock.output("Welcome to my simple python socket echo server\n")
    while True:
        try:
            input = sock.input()
            sock.output(input + "\n")
        except Exception as e:
            sock.output("Error: " + str(e))

if __name__ == "__main__":
    Sock.listen(sock_main, host="0.0.0.0", port=1337)
