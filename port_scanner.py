import optparse # imports standard option parser
from socket import * # import everything from socket module
from threading import * # imports everything from threading module

screenLock = Semaphore(value = 1)
# A factory function that returns a new semaphore object.
# A semaphore manages a counter representing the number of release() calls
# minus the number of acquire() calls plus an initial value.
# The acquire() method blocks if necessary until it can return without making the counter negative.
# If not given, value defaults to 1.

def main():
    parser = optparse.OptionParser("Usage: %prog -H <target host> -p <target port>") # Usage manual
    parser.add_option('-H', dest = 'tgtHost', type = 'string' , help = 'specify target host') # target host option
    parser.add_option('-p', dest = 'tgtPort', type = 'string' , help = 'specify target port[s] separated by comma')
    # target port option
    (options , args) = parser.parse_args() # telling that options will be the arguments
    tgtHost = options.tgtHost # init target host
    tgtPorts = str(options.tgtPort).split(',') # init target ports separated by comma
    if (tgtHost == None) | (tgtPorts[0] == None): # if one of this values is none
        print '[-]You must specify a target host and port[s].' # then print the manual
        exit(0) # exits the program
    portScan(tgtHost,tgtPorts) # run the portScan function with tgtHost and tgtPorts as parameters

# At this point we'll need two functions: connScan and portScan

# The connScan function will take two arguments: tgtHost and tgtPort and attempt to create a connection
# to the target host and port and If successful, connScan will print an open port message
# If not, it will print a port closed message

def connScan(tgtHost,tgtPort): # def connScan function which takes the target host and port
    try:
        connSocket = socket(AF_INET , SOCK_STREAM) # we create a new socket called connSocket
        connSocket.connect((tgtHost,tgtPort)) # the socket tries to connect to the host through the port
        connSocket.send('Something\r\n') # we just send saome data
        results = connSocket.recv(100) # we wait to receive some data for app banner grabbing purposes
        screenLock.acquire()
        # Acquire a lock, blocking or non-blocking.
        # When invoked with the blocking argument set to True (the default),
        # block until the lock is unlocked, then set it to locked and return True.
        # When invoked with the blocking argument set to False, do not block.
        # If a call with blocking set to True would block, return False immediately; otherwise, set the lock to locked and return True.
        print '[+]  %d/tcp open' %tgtPort # prints that the port is open because we used try
        print '[+] ', str(results) # we print what we grabbed to figure out the app
    except:
        screenLock.acquire()
        print '[+]  %d/tcp closed' %tgtPort # prints that the port is closed as we couldn't settle a connection
    finally:
        screenLock.release()
        # Release a lock.
        # When the lock is locked, reset it to unlocked, and return.
        # If any other threads are blocked waiting for the lock to become unlocked, allow exactly one of them to proceed.
        # When invoked on an unlocked lock, a ThreadError is raised.
        # There is no return value.
        connSocket.close() # we close the socket

# The portScan function takes the hostname and target port as arguments
# It will first attempt to resolve an IP address to a friendly hostname using the gethostbyname() function
# Next, it will print the hostname and enumerate through each individual port attempting to connect using the connScan function

def portScan(tgtHost,tgtPorts): # def portScan function which takes target host and ports as parameters
    try:
        tgtIP = gethostbyname(tgtHost) # translates a host name to IPv4 address format(ip resolve)
    except: # if it doesn't make it
        print "[-] Cannot resolve '%s': Unknown host" %tgtHost # prints an error message
        return
    try:
        tgtName = gethostbyaddr(tgtIP)
        # Return a triple (hostname, aliaslist, ipaddrlist) where hostname is the primary host name responding
        # to the given ip_address, aliaslist is a list of alternative host names for the same address
        # and ipaddrlist is a list of IPv4/v6 addresses for the same interface on the same host
        print "Scan results for: ", tgtName[0] # we print the first item in the list which is the hostname
    except: # if we don't make it
        print "Scan results for: ", tgtIP # we just print the IP address
    setdefaulttimeout(1)
    # Set the default timeout in seconds (float) for new socket objects
    # A value of None indicates that new socket objects have no timeout
    for tgtPort in tgtPorts: # for every port that we provide as input
        t = Thread(target = connScan, args = (tgtHost, int(tgtPort)))
        # Thread(group=None, target=None, name=None, args=(), kwargs={})¶
        # This constructor should always be called with keyword arguments. Arguments are:
        # group should be None; reserved for future extension when a ThreadGroup class is implemented.
        # target is the callable object to be invoked by the run() method. Defaults to None, meaning nothing is called.
        # name is the thread name. By default, a unique name is constructed of the form “Thread-N” where N is a small decimal number.
        # args is the argument tuple for the target invocation. Defaults to ().
        # kwargs is a dictionary of keyword arguments for the target invocation. Defaults to {}.
        # If the subclass overrides the constructor, it must make sure to invoke the base class constructor
        # (Thread.__init__()) before doing anything else to the thread.
        t.start()
        # Start the thread’s activity.
        # It must be called at most once per thread object.
        # It arranges for the object’s run() method to be invoked in a separate thread of control.
        # This method will raise a RuntimeError if called more than once on the same thread object.
        #Alternate Syntax without threading//print 'Scanning port ', tgtPort # prints a message that it is scanning the target port
        #Alternate Syntax without threading//connScan(tgtHost,int(tgtPort))
        #//it runs the connScan function to settle a connection
        #//and see if the port is open or closed

if __name__ == "__main__":
    main()
