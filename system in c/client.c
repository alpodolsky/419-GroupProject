#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netdb.h>
#include <errno.h>
/**Note:
 * this is just to test with server and not necessarily what alice/bob will look like
 * should be able to connect to the server at bare minimum, talking between users will need testing
 */
int i;
int globErr=0;
//sends the command
void sendCmd(char* cmd, int socfd){
	printf("Command to be sent is: %s", cmd);
	int i = 0;
	while (i < strlen(cmd)){
		int numBytes = write(socfd, cmd, strlen(cmd)+1);
		if (numBytes == -1){
			printf("WRITE ERROR in sendCmd()\n");
			printf("error: '%d'\n", errno);
			break;
		}
		else{
			printf("send '%d' bytes successfully\n", numBytes);
			i += numBytes;
		}
	}
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
	printf("   Server sent: %s, %d bytes, %c\n",input, strlen(input)+1,input[strlen(input)-1]);
	return input;
}
//creates one string for the whole of user's input
char* createInput(){
	char* input = NULL;
	char buff[2];
	size_t inputlen = 0, templen = 0;
	do{
		fgets(buff,2,stdin);
		templen = strlen(buff);
		input = realloc(input, inputlen+templen+1);
		strcpy(input+inputlen,buff);
		inputlen += templen;
		//i dont remember totally but this while might be a bit funky
	} while(templen ==1&&buff[0]!='\n');
	input[strlen(input)-1]='\0';
	printf("created input: %s length %d\n", input, strlen(input));
	return input;
}

int main(int argc, char*argv[]){
    if(argc<3){  //no hostname/IP address, missing port, or missing both
		printf("MISSING ARGUMENTS\n");
	}
	//create socket
	int socketfd = socket(AF_INET, SOCK_STREAM, 0); //not sure if correct parameters
	if (socketfd < 0){
		printf("SOCKET COULD NOT BE CREATED\n");
	}
	int portno = atoi(argv[2]);
	struct hostent* serverIPAddress = gethostbyname(argv[1]);
	struct sockaddr_in serverAddressInfo;
	bzero((char *)&serverAddressInfo, sizeof(serverAddressInfo));
	serverAddressInfo.sin_family = AF_INET;
	serverAddressInfo.sin_port = htons(portno);
	bcopy((char*)serverIPAddress->h_addr, (char*)&serverAddressInfo.sin_addr.s_addr, serverIPAddress->h_length);
	i = 0;
	char *cmd;
	while (i<3){
		if (connect(socketfd, (struct sockaddr*)&serverAddressInfo, sizeof(serverAddressInfo)) == 0){
			sendCmd("HELLO", socketfd);
			cmd = readCmd(socketfd);
			if(strcmp(cmd,"HELLO connected to the server!")!=0){
				printf("something went horribly wrong, dear God\n");
				return 0;
			}
			free(cmd);
			break;
		}
		printf("Connection failed '%d' times", i);
		i++;
	}
    	//all the stuff for being connected with the server
	//should only break after a quit
	while(1){
		printf(">");
		cmd = createInput();
		char *newCmd;
		char*serverMessage;
		if(strcmp(cmd, "help")==0){
			helpMe();
			free(cmd);
			continue;
		}
		if(strcmp(cmd, "quit")==0){
			free(cmd);
			sendCmd("GDBYE", socketfd);
			//this probably needs to be changed
			if (connect(socketfd, &serverAddressInfo, sizeof(serverAddressInfo)) != 0){
				//need to send GDBYE prompt to server
				printf("Succesfully diconnected \n");
				break;
			}
		}
        else{
			//any message sent between people
			printf("  serverMessage to be sent: %s\n",cmd);
			sendCmd(cmd, socketfd);
			free(cmd);

			cmd=readCmd(socketfd);
			
			if(strcmp(cmd, "OK!")!=0){
				printf("%s", errorCheck(cmd));
			}
			free(cmd);
			continue;
		}
}