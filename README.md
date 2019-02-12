# DS-final-project
raising awareness disease

## The ChatBox
In efforts of improving the chat assignment from class we created the chatbox, which supports:
- instant messaging (in the sense that there are no delays in delivering thanks to asynchronous p2plinks)
- connection to a chat server that keeps a list of the participants
- instant updates on any changes to participant list ("instant" again in the above meaning)

These improvements are work of Natalie!

## The Virus
In efforts to explore the vulnerability of our chatbox we created a virus that once ran on a machine acts as follows:
- searches through all python files that contain/begin/end with the word "chat"
- collects them and implants some malicious code (this is in a sence very setting specific since we only managed to complete a rough demo that works with our previously built classes for the abstractions p2plink and bebroadcast, as well as the chatbox class itself)
- creates an instance of the virus server and redirects all the previous connections, in a way isolating the infected client from the healthy system
- once a new infected chatbox client is made messages that have some common keywords (such as question words, do/go/hi, etc) will be altered to say something rather triggering (for the purposes of the project demo we picked to surprise with some social, political, economical awareness questions and thoughts)
- the message alterings are not visible to the participants of either the healthy or the infected side of the system 

## How to run
Everything needs to be run locally (preferably using an IDE like intelliJ)
- first run the chat server so it can start keeping track of participants
- then you can run the chatbox for as many members as you want following the prompt instructions
- after playing around with the features of the chat you can run the virus
- then create one more chatbox client following the prompts as before
- try the chat features again using the infected chat member
