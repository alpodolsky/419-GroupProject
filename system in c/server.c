#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netdb.h>
#include <pthread.h>
#include <string.h>
#include <errno.h>

struct input {
	char* cmd;
	char* arg;
	int argLength;
};
void quit(int socfd){
	//close any open message box
	close(socfd);
	pthread_exit(NULL);
}
struct threadInfo{
    int id;//use to distinguish one user from another, reserve 0 for chuck?
};
//function that sends the message, may need  tweaking to get two people to talk to each other
int sendMsg(int socfd, char* msg, int msgLength){
	printf("message to be sent is: %s", msg);
	int i = 0;
	while (i < msgLength){
		int bytesSent = write(socfd, msg+i, msgLength-i);
		if (bytesSent == -1){
			printf("WRITE ERROR\n");
			return -1;
		}
		printf("was able to write '%d' bytes\n", bytesSent);
		i += bytesSent;
		printf("have sent a total of '%d' bytes\n", i);
	}
	return 0;
}
int interpretCmd(char* thisInput, int socfd, struct threadInfo* thisThreadInfo){
	char* goodbye = "GDBYE";
	char* hello = "HELLO";
	char* create = "CHUCK";

    char* cmd = thisInput;
	if (strcmp(cmd, goodbye) == 0){
		printf("client called the 'quit' command\n");
		//call quit fnction
		quit(socfd);
		return 1;
	}
    //can be changed here to accept a key from alice/bob
    else if (strcmp(cmd, hello) == 0){
		printf("client tried to connect to the server");
		char helloResponse[3] = "OK\0";
		sendMsg(socfd, helloResponse, sizeof(helloResponse));
		return 0;
	}
    else{ //the  message sent from bob/alice
		printf("client sent the string: %s\n", cmd);
		//at this point call encryption and do everything necessary
            //includes encrypting the message, storing for referencing by chuck
            //and sending the message to the  recepiant. 
		//sendMsg(socfd, err, sizeof(err));
		return;
	}
    //we would need another command/condition for chuck
}

//reads the command
char* readCmd(int socfd){
	printf("  made it into read cmd\n");
	char *input=malloc(1*sizeof(char));
	char buff[1];
	size_t inputlen = 0;
	do{
		int bytesRead = 0;
		bytesRead = read(socfd,buff,1);
		if (bytesRead == 0){ //server disconected socket
			printf("The server has disconnected\n");
			exit(0);
		}
		input = realloc(input, inputlen+1);
		strcpy(input+inputlen,buff);
		inputlen += 1;
	} while(buff[0]!='\0');	
	printf("   Server got sent: %s, %d bytes, %c\n",input, strlen(input)+1,input[strlen(input)-1]);
	return input;
}
int j = 0;
void* communicate(void* socfd){
    struct threadInfo thisThreadInfo;
    thisThreadInfo.id = j++;
    int* clientfd = (int*)socfd;
    int client = *clientfd;
    while(1){
       	char* thisIn = readCmd(client);
	    int i;
        i = interpretCmd(thisIn, client, &thisThreadInfo);
		if (i == 1){
			break;
		}
    }

}
int main (int argc, char* argv[]){
	if (argc < 2){ //no port number given
		printf("PORT ERROR\n");
	}
    //create socket
	int socketfd = socket(AF_INET, SOCK_STREAM, 0);
	if (socketfd < 0) { //socket could not be created
		printf("SOCKET COULD NOT BE CREATED\n"); 
	}
	int portno = atoi(argv[1]);
	printf("portno: '%d'\n", portno);
	
	struct sockaddr_in serverAddressInfo, clientAddressInfo;
	bzero((char*)&serverAddressInfo, sizeof(serverAddressInfo));
	serverAddressInfo.sin_family = AF_INET;
	serverAddressInfo.sin_addr.s_addr = INADDR_ANY;
	serverAddressInfo.sin_port = htons(portno);

	//bind address to socket
	if (bind(socketfd,(struct sockaddr*)&serverAddressInfo, sizeof(serverAddressInfo)) < 0){
		printf("BINDING ERROR\n");
	}
	while(1){
		//listen
		if (listen(socketfd, 5) != 0){
			printf("LISTEN FAILED\n");
		}
		else{
			printf("server listening\n");
		}	

		int clientlen = sizeof(clientAddressInfo);
		int clientfd = accept(socketfd,(struct sockaddr*)&clientAddressInfo, &clientlen);
		if (clientfd < 0){
			printf("ACCEPT ERROR\n");
		}
		else{
			printf("server accepted client\n");
		}
	
		//make new thread
        //this will just spawn a new thread for everyone who joins,
        //instead we want at minimum 3 threads, (chuck, alice, and bob).
		pthread_t thread_id;
		int t = pthread_create(&thread_id, NULL, communicate, &clientfd);
		if (t != 0){
			printf("error creating thread\n");
		}
	}
		
}//end of main
