#include<iostream>
#include<algorithm>
#include <iomanip>
#include<string>
#include<ctime>
#include<vector>
#include<time.h>
#include <cstdlib>
#include <fstream>
#include<sstream>

class Node {
public:
	Node(int aState = 0, std::string aName = "") : nodeName(aName), state(aState) {}
	Node(const Node& aCopy) : nodeName(aCopy.nodeName), state(aCopy.state) {}
	~Node(){}
	Node& operator=(const Node& aCopy){
		nodeName = aCopy.nodeName;
		state = aCopy.state;
		return *this;
	}
	void printTheNode() {
		for (int i = 0; i < 15; ++i) {
			std::cout << '-';
		}
		std::cout << '\n';

		std::cout << '|' << std::setw(13) << std::left << nodeName << '|' << std::endl;
		std::cout << '|' << std::setw(14) << std::right << '|' << '\n';
		std::cout << '|' << std::setw(13) << std::left << state << '|' << '\n';

		for (int i = 0; i < 15; ++i) {
			std::cout << '-';
		}
		std::cout << '\n';
	}
	void setNodeState(int anInt) {
		state = anInt;
	}
	void setNodeName(std::string aName) {
		nodeName = aName;
	}
	int getNodeState() {
		return state;
	}
	void printNodeInfo() {
		std::cout << "Node: " << nodeName << " state: " << state << std::endl;
	}
	void randomlyInitializeNodeState() { /*50% set to 1, 50% set to 0*/
		int randomnum = rand() % 2;
		setNodeState(randomnum);
	}
	std::string getNodeName() {
		return nodeName;
	}
protected:
	std::string nodeName;
	int state; // if state is 1 the node is active, if state is 0 the node is inactive
};

class Minterm { // minterm has format of: abc, (~a)(b)(~c)...
public:
	Minterm& addRegularNode(Node &anActiveNode){ /*add regular node reference in a minterm*/
		regularNodesInMinterm.push_back(&anActiveNode); /*get the address of the target node*/
		return *this;
	}
	Minterm& addNotNode(Node &anInactiveNode){ /*add logical not node reference in a minterm*/
		notNodesInMinterm.push_back(&anInactiveNode); /*get the address of the target node*/
		return *this;
	}
	int evaluateMinterm() {
		int temp = 1;
		if (regularNodesInMinterm.size() + notNodesInMinterm.size() == 0) {
			std::cout << "Error: there is noting in the minterm, please check setup!\n";
			return 0;
		}
		for (int i = 0; i < regularNodesInMinterm.size(); ++i) {
			temp = temp && regularNodesInMinterm[i]->getNodeState();
		}
		for (int i = 0; i < notNodesInMinterm.size(); ++i) {
			temp = temp && !(notNodesInMinterm[i]->getNodeState());
		}
		return temp;
	}
	void printOutMinterm() {
		if (regularNodesInMinterm.size() + notNodesInMinterm.size() == 0) {
			std::cout << "failed to print out all minterms, because there is 0 node in this minterm\n";
			return;
		}
		if (regularNodesInMinterm.size() == 0) {
			for (int i = 0; i < notNodesInMinterm.size() - 1; ++i) {
				std::cout << "~" << notNodesInMinterm[i]->getNodeName() << " & ";
			}
			std::cout << "~" << notNodesInMinterm[notNodesInMinterm.size() - 1]->getNodeName();
		}
		else if (notNodesInMinterm.size() == 0) {
			for (int i = 0; i < regularNodesInMinterm.size() - 1; ++i) {
				std::cout << regularNodesInMinterm[i]->getNodeName() << " & ";
			}
			std::cout << regularNodesInMinterm[regularNodesInMinterm.size() - 1]->getNodeName();
		}
		else {
			for (int i = 0; i < regularNodesInMinterm.size(); ++i) {
				std::cout << regularNodesInMinterm[i]->getNodeName() << " & ";
			}
			for (int i = 0; i < notNodesInMinterm.size() - 1; ++i) {
				std::cout << "~" << notNodesInMinterm[i]->getNodeName() << " & ";
			}
			std::cout << "~" << notNodesInMinterm[notNodesInMinterm.size() - 1]->getNodeName();
		}
	}
	void printOutMintermInFile(std::ofstream& aFile) {
		if (regularNodesInMinterm.size() + notNodesInMinterm.size() == 0) {
			aFile << "failed to print out all minterms, because there is 0 node in this minterm\n";
			return;
		}
		if (regularNodesInMinterm.size() == 0) {
			for (int i = 0; i < notNodesInMinterm.size() - 1; ++i) {
				aFile << "~" << notNodesInMinterm[i]->getNodeName() << " & ";
			}
			aFile << "~" << notNodesInMinterm[notNodesInMinterm.size() - 1]->getNodeName();
		}
		else if (notNodesInMinterm.size() == 0) {
			for (int i = 0; i < regularNodesInMinterm.size() - 1; ++i) {
				aFile << regularNodesInMinterm[i]->getNodeName() << " & ";
			}
			aFile << regularNodesInMinterm[regularNodesInMinterm.size() - 1]->getNodeName();
		}
		else {
			for (int i = 0; i < regularNodesInMinterm.size(); ++i) {
				aFile << regularNodesInMinterm[i]->getNodeName() << " & ";
			}
			for (int i = 0; i < notNodesInMinterm.size() - 1; ++i) {
				aFile << "~" << notNodesInMinterm[i]->getNodeName() << " & ";
			}
			aFile << "~" << notNodesInMinterm[notNodesInMinterm.size() - 1]->getNodeName();
		}
	}
protected:
	//~a&b&~c
	std::vector<Node*> regularNodesInMinterm; // storing all the nodes' pointers that do not have not logic in front
	std::vector<Node*> notNodesInMinterm; // storing all the nodes' pointers that have not logic in front
};

class BooleanEquation { /*a boolean equation in the form of sum of minterms*/
public:
	BooleanEquation(Node* aNode = NULL) : targetNode(aNode) {}
	BooleanEquation(const BooleanEquation& aCopy) {
		targetNode = aCopy.targetNode;
		for (int i = 0; i < aCopy.allMintermList.size(); ++i) {
			allMintermList.push_back(aCopy.allMintermList[i]);
		}
	}
	~BooleanEquation(){}
	BooleanEquation& operator=(const BooleanEquation& aCopy) {
		targetNode = aCopy.targetNode;
		for (int i = 0; i < aCopy.allMintermList.size(); ++i) {
			allMintermList.push_back(aCopy.allMintermList[i]);
		}
		return *this;
	}
	BooleanEquation& addMinterm(Minterm& aMinterm) { /*pass in a reference of a minterm object*/
		allMintermList.push_back(&aMinterm); /*get the address of the reference of the actual minterm and store into the vector*/
		return *this;
	}
	int evaluateBooleanEquation() {
		if (allMintermList.size() == 0) {
			std::cout << "Error: 0 minterms in the boolean equation, cannot be evaluated!\n";
			return 0;
		}
		else {
			int temp = 0;
			for (int i = 0; i < allMintermList.size(); ++i) {
				temp = temp || allMintermList[i]->evaluateMinterm();
			}
			return temp;
		}
	}
	BooleanEquation& setTargetNode(Node& aNode) {
		targetNode = &aNode;
		return *this;
	}
	BooleanEquation& setTargetNodeState(int aState) {
		if (targetNode == NULL) {
			std::cout << "Error: target node cannot be found!\n";
			return *this;
		}
		else {
			targetNode->setNodeState(aState);
			return *this;
		}
	}
	BooleanEquation& evaluateBooleanEquationAndSetTargetNodeState() {
		setTargetNodeState(evaluateBooleanEquation());
		return *this;
	}
    Node* getTargetNodeAddress() {
		if (targetNode == NULL) {
			std::cout << "ERROR: Target node is not set for this boolean equation, cannot get target node!\n";
			return NULL;
		}
		else {
			return targetNode;	
		}
	}
	void printOutBooleanEquation() {
		if (targetNode == NULL || allMintermList.size() == 0) {
			std::cout << "ERROR: boolean equation cannot be printed, either because target is not set or 0 minterm in the boolean equation\n";
			return;
		}
		std::cout << targetNode->getNodeName() << " = ";
		for (int i = 0; i < allMintermList.size() - 1; ++i) {
			allMintermList[i]->printOutMinterm();
			std::cout << " | ";
		}
		allMintermList[allMintermList.size() - 1]->printOutMinterm();
		std::cout << std::endl;
	}
	void printOutBooleanEquationInFile(std::ofstream& aFile) {
		if (targetNode == NULL || allMintermList.size() == 0) {
			aFile << "ERROR: boolean equation cannot be printed, either because target is not set or 0 minterm in the boolean equation\n";
			return;
		}
		aFile << targetNode->getNodeName() << " = ";
		for (int i = 0; i < allMintermList.size() - 1; ++i) {
			allMintermList[i]->printOutMintermInFile(aFile);
			aFile << " | ";
		}
		allMintermList[allMintermList.size() - 1]->printOutMintermInFile(aFile);
		aFile << std::endl;
	}
protected:
	//~a&b&~c|~a&b&~c
	Node* targetNode; /*storing the boolean equation's target nodes' address*/
	std::vector<Minterm*> allMintermList; /*storing all minterms' pointers in a boolean equation*/
};

class WholeNetwork {
public:
	WholeNetwork(){}
	WholeNetwork(const WholeNetwork& aCopy) {
		for (int i = 0; i < listOfNodes.size(); ++i) {
			listOfNodes.push_back(aCopy.listOfNodes[i]);
		}
		for (int i = 0; i < listOfBooleanEquations.size(); ++i) {
			listOfBooleanEquations.push_back(aCopy.listOfBooleanEquations[i]);
		}
	}
	~WholeNetwork(){}
	WholeNetwork& operator=(const WholeNetwork& aCopy) {
		for (int i = 0; i < listOfNodes.size(); ++i) {
			listOfNodes.push_back(aCopy.listOfNodes[i]);
		}
		for (int i = 0; i < listOfBooleanEquations.size(); ++i) {
			listOfBooleanEquations.push_back(aCopy.listOfBooleanEquations[i]);
		}
		return *this;
	}
	WholeNetwork& addNode(Node& aNode) {
		listOfNodes.push_back(&aNode);
		return *this;
	}
	WholeNetwork& addBooleanEquation(BooleanEquation& aBooleanEquation) {
		listOfBooleanEquations.push_back(&aBooleanEquation);
		return *this;
	}
	void setUpWholeNetwork() {
		Node* nodeAddress;
		std::cout << "Input node is initialized to 1\n";
		nodeAddress = new Node;
		nodeAddress->setNodeState(1);
		nodeAddress->setNodeName("input");
		listOfNodes.push_back(nodeAddress);
		std::cout << "Enter how many nodes are in the network, excluding input node and closure node\n";
		int nodeCount = promptUserInputAnInterger(); /*get node count number*/
		int i;
		for (i = 0; i < nodeCount; ++i) {
			std::cout << "Making node " << i + 1 << " in the network.\n";
			nodeAddress = new Node; /*making a new node on the heap*/
			listOfNodes.push_back(nodeAddress);
			std::cout << "node " << i + 1 << " now is randomly initialized.\n";
			nodeAddress->randomlyInitializeNodeState();
			std::cin.clear();
			std::cin.ignore(10000, '\n');
			std::cout << "Please name node " << i + 1 << ": ";
			std::string aName;
			std::cin >> aName;
			nodeAddress->setNodeName(aName);
		}
		std::cout << "now closure node is made and it is randomly initialized.\n";
		nodeAddress = new Node;
		listOfNodes.push_back(nodeAddress);
		nodeAddress->setNodeName("closure");
		nodeAddress->randomlyInitializeNodeState();
		std::cout << "input, closure, and " << i << " nodes are made in between input node and closure node.\n";
		std::cout << "now, set boolean equations for " << i << " intermediate nodes and closure node. No boolean equation for input node.\n";
		setAllBooleanEquations();
		runTimeSteps();
		freeAllMemory();
		return;
	}
	void setAllBooleanEquations() {
		BooleanEquation* booleanEquationAddress;
		std::cout << "total of " << listOfNodes.size() - 1 << " boolean equations are needed.\n";
		/*the following for loop creates all the boolean equations starting from node 1 until closure node*/
		for (int i = 0; i < listOfNodes.size() - 1; ++i) {
			booleanEquationAddress = new BooleanEquation;
			booleanEquationAddress->setTargetNode(*listOfNodes[i + 1]); /*skipping input node for total of (listOfNodes.size() - 1) boolean equations*/
			listOfBooleanEquations.push_back(booleanEquationAddress);
			std::cout << "boolean equation for node index " << i + 1 << " is set without minterms, target node name is: " << listOfNodes[i + 1]->getNodeName() << '\n';
		}
		std::cout << "setting boolean equations process now starts:\n";
		showSettingBooleanEquationRules();
		showInfoOfAllNodesInNetwork();
		std::cin.clear();
		std::cin.ignore(10000, '\n');
		for (int booleanEquationIndex = 0; booleanEquationIndex < listOfBooleanEquations.size(); ++booleanEquationIndex) {
			tryAgain:
			std::cout << "set boolean equation for target node index: " << booleanEquationIndex + 1 << " node name: " << listOfNodes[booleanEquationIndex + 1]->getNodeName() << " :\n";
			std::cout << booleanEquationIndex + 1 << " = ";
			std::string userInputString;
			char tempString[1001];
			std::cin.getline(tempString,1000);
			userInputString = tempString; /*now userInputString contains whatever user inputed boolean equation*/
			userInputString = removeSpaces(userInputString); /*remove all spaces from the string*/
			std::string userInputStringCopy = userInputString;
			if (!contains_number(userInputString)) {
				std::cout << "your input does not contain any number (no node index in your input), try again.\n";
				goto tryAgain;
			}
			for (int i = 0; i < userInputString.length(); ++i) {
				if (!isOneOfValidInputChar(userInputString[i])) {
					std::cout << "the first invalid input char is: " << userInputString[i] << ", try again.\n";
					goto tryAgain;
				}
			}
			if (!isNumber(userInputString[userInputString.length() - 1])) {
				std::cout << "the last inputed char (excluding spaces in the end) is not a part of node index, that is, the last inputed char is not a number, try again.\n";
				goto tryAgain;
			}
			if (userInputString[0] == '&' || userInputString[0] == '|') {
				std::cout << "the first char cannot be '&' or '|' (excluding spaces in the beginning), try again.\n";
				goto tryAgain;
			}
			for (int i = 0; i < userInputString.length(); ++i) {
				if (userInputString[i] == '~' && i + 1 < userInputString.length() && i + 1 >= 0) {
					if (!isNumber(userInputString[i + 1])) {
						std::cout << "'~' at position: " << i << " of the input string is not followed by a node index, try again.\n";
						goto tryAgain;
					}
				}
			}
			for (int i = 0; i < userInputString.length(); ++i) {
				if (userInputString[i] == '~' && i - 1 < userInputString.length() && i - 1 >= 0) {
					if (isNumber(userInputString[i - 1])) {
						std::cout << "'~' at position: " << i << " of the input string is not following an logical operation in front of it, try again.\n";
						goto tryAgain;
					}
				}
			}
			for (int i = 0; i < userInputString.length(); ++i) {
				if ((userInputString[i] == '&' || userInputString[i] == '|') && i - 1 < userInputString.length() && i - 1 >= 0) {
					if (!isNumber(userInputString[i - 1])) {
						std::cout << "'" << userInputString[i] << "' at position: " << i << " of the input string is not after a node index, try again.\n";
						goto tryAgain;
					}
				}
			}
			for (int i = 0; i < userInputString.length(); ++i) {
				if ((userInputString[i] == '&' || userInputString[i] == '|') && i + 1 < userInputString.length() && i + 1 >= 0) {
					if (!isNumber(userInputString[i + 1]) && userInputString[i + 1] != '~') {
						std::cout << "'" << userInputString[i] << "' at position: " << i << " of the input string is not followed by logical NOT operator '~' or a node index, try again.\n";
						goto tryAgain;
					}
				}
			}
			//===============================================================================================================================================
			// the following block of code extracts all numbers in the inputted string
			std::vector<int> nodeIndexesInUserInputtedString; /*vector stores each integer inputted in order*/
			std::vector<int> trackingFirstIndexOfEachNumberInputted; /*each index is associated with storing integer vector index, and stores that index's integer's position in the string*/
			int lastTrackedStringIndex;
			int counter = 0;
			int previousRoundEraseCount;
			while (contains_number(userInputStringCopy)) {
				nodeIndexesInUserInputtedString.push_back(stringToInt(userInputStringCopy));
				int eraseHowManyCharsCount = 1;
				while (userInputStringCopy.find_first_of("0123456789") + eraseHowManyCharsCount <= userInputStringCopy.length() - 1 && isNumber(userInputStringCopy[userInputStringCopy.find_first_of("0123456789") + eraseHowManyCharsCount])) {
					eraseHowManyCharsCount++;
				}
				//std::cout << "eraseHowManyCharsCount: " << eraseHowManyCharsCount << std::endl;
				if(counter == 0){
					trackingFirstIndexOfEachNumberInputted.push_back(userInputString.find_first_of(std::to_string(stringToInt(userInputStringCopy)))); /*from the original user inputted string to find the first index of the number inputed, then push into the tracking vector*/
				}
				else {
					trackingFirstIndexOfEachNumberInputted.push_back(userInputString.find_first_of(std::to_string(stringToInt(userInputStringCopy)), lastTrackedStringIndex + previousRoundEraseCount)); /*from the original user inputted string to find the first index of the number inputed, then push into the tracking vector*/
				}
				if (trackingFirstIndexOfEachNumberInputted.size() >= 1) {
					lastTrackedStringIndex = trackingFirstIndexOfEachNumberInputted[trackingFirstIndexOfEachNumberInputted.size() - 1];
					//std::cout << "lastTrackedStringIndex: " << lastTrackedStringIndex << std::endl;
				}
				previousRoundEraseCount = eraseHowManyCharsCount;
				userInputStringCopy.erase(userInputStringCopy.find_first_of("0123456789"), eraseHowManyCharsCount);
				++counter;
			}
			// ================================================================================================================================================
			std::cout << "all node indexes inputted extracted in order: \n";
			for (int i = 0; i < nodeIndexesInUserInputtedString.size(); ++i) {
				std::cout << nodeIndexesInUserInputtedString[i] << " at string position index (after removing all spaces): " << trackingFirstIndexOfEachNumberInputted[i] << std::endl;
			}
			for (int i = 0; i < nodeIndexesInUserInputtedString.size(); ++i) {
				if (nodeIndexesInUserInputtedString[i] < 0 || nodeIndexesInUserInputtedString[i] > listOfNodes.size() - 1) { /*check each inputted number is in range*/
					showInfoOfAllNodesInNetwork();
					std::cout << "inputted node index: " << nodeIndexesInUserInputtedString[i] << " is invalid, because it is out of range (refer to the above nodes in network), try again.\n";
					goto tryAgain;
				}
			}
			std::cout << "inputted boolean equation is valid.\n";
			std::cout << "inputted string was: " << userInputString << '\n';
			//==================================================================================================================================================
			std::vector<int> trackingLogicalNOTPosition;
			int found = userInputString.find_first_of('~');
			while (found != std::string::npos) {
				trackingLogicalNOTPosition.push_back(found);
				found = userInputString.find_first_of('~', found + 1);
			}
			std::cout << "all logical NOT ~ position: \n";
			for (int i = 0; i < trackingLogicalNOTPosition.size(); ++i) {
				std::cout << trackingLogicalNOTPosition[i] << std::endl;
			}
			std::vector<int> trackingLogicalORPosition;
			found = userInputString.find_first_of('|');
			while (found != std::string::npos) {
				trackingLogicalORPosition.push_back(found);
				found = userInputString.find_first_of('|', found + 1);
			}
			std::cout << "all logical OR | position: \n";
			for (int i = 0; i < trackingLogicalORPosition.size(); ++i) {
				std::cout << trackingLogicalORPosition[i] << std::endl;
			}
			std::vector<int> trackingLogicalANDPosition;
			found = userInputString.find_first_of('&');
			while (found != std::string::npos) {
				trackingLogicalANDPosition.push_back(found);
				found = userInputString.find_first_of('&', found + 1);
			}
			std::cout << "all logical AND & position: \n";
			for (int i = 0; i < trackingLogicalANDPosition.size(); ++i) {
				std::cout << trackingLogicalANDPosition[i] << std::endl;
			}
			std::vector<int> markingEachNodeIndexForLogicalNotApplied; /*vector that have the same size of nodeIndexesInUserInputtedString that records each node has logical not applied in the minterm, 1 for not applied, 0 for no not applied*/
			for (int i = 0; i < nodeIndexesInUserInputtedString.size(); ++i) {
				bool flag = false;
				for (int j = 0; j < trackingLogicalNOTPosition.size(); ++j) {
					if (trackingLogicalNOTPosition[j] + 1 == trackingFirstIndexOfEachNumberInputted[i]) {
						flag = true;
					}
				}
				if (flag) {
					markingEachNodeIndexForLogicalNotApplied.push_back(1);
				}
				else {
					markingEachNodeIndexForLogicalNotApplied.push_back(0);
				}
			}
			std::cout << "each node not applied situation:\n";
			for (int i = 0; i < markingEachNodeIndexForLogicalNotApplied.size(); ++i) {
				std::cout << markingEachNodeIndexForLogicalNotApplied[i] << std::endl;
			}
			std::cout << "for this boolean equation a total of " << trackingLogicalORPosition.size() + 1;
			if (trackingLogicalORPosition.size() == 0) std::cout << " minterm is needed\n";
			else std::cout << " minterms are needed\n";
			//=============================================================================================================================
			//the following codes set up the boolean equation by setting up minterms and pushing in minterms into boolean equations
			Minterm* mintermAddress;
			if (trackingLogicalORPosition.size() == 0) {
				mintermAddress = new Minterm;
				for (int j = 0; j < nodeIndexesInUserInputtedString.size(); ++j) {
					if (markingEachNodeIndexForLogicalNotApplied[j] == 1) {
						mintermAddress->addNotNode(*listOfNodes[nodeIndexesInUserInputtedString[j]]);
					}
					else if (markingEachNodeIndexForLogicalNotApplied[j] == 0) {
						mintermAddress->addRegularNode(*listOfNodes[nodeIndexesInUserInputtedString[j]]);
					}
				}
				listOfBooleanEquations[booleanEquationIndex]->addMinterm(*mintermAddress);
				trackingAllMinterms.push_back(mintermAddress);
			}
			else if (trackingLogicalORPosition.size() != 0) {
				mintermAddress = new Minterm;
				for (int j = 0; j < nodeIndexesInUserInputtedString.size(); ++j) {
					if (trackingFirstIndexOfEachNumberInputted[j] < trackingLogicalORPosition[0] && markingEachNodeIndexForLogicalNotApplied[j] == 1) {
						mintermAddress->addNotNode(*listOfNodes[nodeIndexesInUserInputtedString[j]]);
					}
					else if (trackingFirstIndexOfEachNumberInputted[j] < trackingLogicalORPosition[0] && markingEachNodeIndexForLogicalNotApplied[j] == 0) {
						mintermAddress->addRegularNode(*listOfNodes[nodeIndexesInUserInputtedString[j]]);
					}
				}
				listOfBooleanEquations[booleanEquationIndex]->addMinterm(*mintermAddress);
				trackingAllMinterms.push_back(mintermAddress);
				for (int i = 1; i < trackingLogicalORPosition.size(); ++i) {
					mintermAddress = new Minterm;
					for (int j = 0; j < nodeIndexesInUserInputtedString.size(); ++j) {
						if (trackingLogicalORPosition[i - 1] < trackingFirstIndexOfEachNumberInputted[j] && trackingFirstIndexOfEachNumberInputted[j] < trackingLogicalORPosition[i] && markingEachNodeIndexForLogicalNotApplied[j] == 1) {
							mintermAddress->addNotNode(*listOfNodes[nodeIndexesInUserInputtedString[j]]);
						}
						else if (trackingLogicalORPosition[i - 1] < trackingFirstIndexOfEachNumberInputted[j] && trackingFirstIndexOfEachNumberInputted[j] < trackingLogicalORPosition[i] && markingEachNodeIndexForLogicalNotApplied[j] == 0) {
							mintermAddress->addRegularNode(*listOfNodes[nodeIndexesInUserInputtedString[j]]);
						}
					}
					listOfBooleanEquations[booleanEquationIndex]->addMinterm(*mintermAddress);
					trackingAllMinterms.push_back(mintermAddress);
				}
				mintermAddress = new Minterm;
				for (int j = 0; j < nodeIndexesInUserInputtedString.size(); ++j) {
					if (trackingFirstIndexOfEachNumberInputted[j] > trackingLogicalORPosition[trackingLogicalORPosition.size() - 1] && markingEachNodeIndexForLogicalNotApplied[j] == 1) {
						mintermAddress->addNotNode(*listOfNodes[nodeIndexesInUserInputtedString[j]]);
					}
					else if (trackingFirstIndexOfEachNumberInputted[j] > trackingLogicalORPosition[trackingLogicalORPosition.size() - 1] && markingEachNodeIndexForLogicalNotApplied[j] == 0) {
						mintermAddress->addRegularNode(*listOfNodes[nodeIndexesInUserInputtedString[j]]);
					}
				}
				listOfBooleanEquations[booleanEquationIndex]->addMinterm(*mintermAddress);
				trackingAllMinterms.push_back(mintermAddress);
			}
			std::cout << "boolean equation is set for target node index: " << booleanEquationIndex + 1 << " node name: " << listOfNodes[booleanEquationIndex + 1]->getNodeName() << " :\n";
			listOfBooleanEquations[booleanEquationIndex]->printOutBooleanEquation();
		}
	}
	void runTimeSteps() {
		/*std::cin.clear();
		std::cin.ignore(10000, '\n');*/
		std::cout << "Run howmany time steps?\n";
		int timeStepCount = promptUserInputAnInterger();
		std::vector<int> randomBooleanEquationOrder;
		int randomIndex;
		std::ofstream resultFile;
		resultFile.open("result.txt");
		for (int i = 0; i < timeStepCount; ++i) {
			std::cout << "time step " << i + 1 << " : \n";
			resultFile << "time step " << i + 1 << " : \n";
			std::cout << "initial nodes' state:\n";
			resultFile << "initial nodes' state:\n";
			randomlizeAllNodesStateExceptInputNode();
			showInfoOfAllNodesInNetworkWithTheirStates(resultFile);
			randomBooleanEquationOrder.clear();
			for (int j = 0; j < listOfBooleanEquations.size() - 1; ++j) {
				generateAgain:
				randomIndex = rand() % (listOfBooleanEquations.size() - 1);
				for (int k = 0; k < randomBooleanEquationOrder.size(); ++k) {
					if (randomBooleanEquationOrder[k] == randomIndex) {
						goto generateAgain;
					}
				}
				randomBooleanEquationOrder.push_back(randomIndex);
			}
			std::cout << "boolean equations evaluated in the random order:\n";
			resultFile << "boolean equations evaluated in the random order:\n";
			for (int h = 0; h < randomBooleanEquationOrder.size(); ++h) {
				std::cout << "equation index: " << randomBooleanEquationOrder[h] << " equation: ";
				resultFile << "equation index: " << randomBooleanEquationOrder[h] << " equation: ";
				listOfBooleanEquations[randomBooleanEquationOrder[h]]->printOutBooleanEquation();
				listOfBooleanEquations[randomBooleanEquationOrder[h]]->printOutBooleanEquationInFile(resultFile);
				listOfBooleanEquations[randomBooleanEquationOrder[h]]->evaluateBooleanEquationAndSetTargetNodeState();
			}
			std::cout << "equation index: " << listOfBooleanEquations.size() - 1 << " equation: ";
			resultFile << "equation index: " << listOfBooleanEquations.size() - 1 << " equation: ";
			listOfBooleanEquations[listOfBooleanEquations.size() - 1]->printOutBooleanEquation();
			listOfBooleanEquations[listOfBooleanEquations.size() - 1]->printOutBooleanEquationInFile(resultFile);
			listOfBooleanEquations[listOfBooleanEquations.size() - 1]->evaluateBooleanEquationAndSetTargetNodeState();
			std::cout << "nodes' state after evaluating boolean equations in the above order:\n";
			resultFile << "nodes' state after evaluating boolean equations in the above order:\n";
			showInfoOfAllNodesInNetworkWithTheirStates(resultFile);
		}
		resultFile.close();
	}
	int promptUserInputAnInterger() {
		int num; //variable to store the number entered by the user.

        //Prompt the user to enter an integer.
		std::cout << "Enter an integer: ";
		std::cin >> num;

		//While the input entered is not an integer, prompt the user to enter an integer.
		while (!std::cin)
		{
			std::cout << "That was not an integer! or the integer entered was too big!\nPlease enter an integer: ";
			std::cin.clear();
			std::cin.ignore(10000, '\n');
			std::cin >> num;
		}

		//Print the integer entered by the user to the screen.
		std::cout << "The integer entered is " << num << std::endl;
		return num;
	}
	void showInfoOfAllNodesInNetwork() {
		std::cout << "\nNow showing all nodes in the network:\n";
		for (int i = 0; i < listOfNodes.size(); ++i) {
			std::cout << "node index: " << i << " node name: " << listOfNodes[i]->getNodeName() << "\n";
		}
		std::cout << std::endl;
		return;
	}
	void showInfoOfAllNodesInNetworkWithTheirStates(std::ofstream& aFile) {
		//std::cout << "\nNow showing all nodes in the network:\n";
		for (int i = 0; i < listOfNodes.size(); ++i) {
			//std::cout << "node index: " << i << " node name: " << listOfNodes[i]->getNodeName() << " state: " << listOfNodes[i]->getNodeState() << "\n";
			aFile << "node index: " << i << " node name: " << listOfNodes[i]->getNodeName() << " state: " << listOfNodes[i]->getNodeState() << "\n";
		}
		std::cout << std::endl;
		return;
	}
	void randomlizeAllNodesStateExceptInputNode() {
		for (int i = 1; i < listOfNodes.size(); ++i) {
			listOfNodes[i]->randomlyInitializeNodeState();
		}
	}
	void showSettingBooleanEquationRules() {
		std::cout << "symbol definition: bitwise NOT '~', bitwise AND '&', bitwise OR '|'\n";
		std::cout << "operator precedence: bitwise NOT '~' over bitwise AND '&' over bitwise OR '|'\n";
		std::cout << "the allowed input characters are : '~', '&', '|', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ' '\n";
		std::cout << "use node indexes instead of node name in setting up boolean equations\n";
		return;
	}

	void simulation() {
		std::ofstream test;
		std::ofstream resultFile;
		resultFile.open("result.txt");
		//std::cout << "Run howmany initializations?\n";

		std::ifstream theFile1("Initialization Setting.txt");
		std::string theInitializationsNumber;
		while (theFile1.good()) {
			theInitializationsNumber += theFile1.get();
		}

		int initializationsCount = stringToInt(theInitializationsNumber);

		std::ifstream theFile2("Time Steps Setting.txt");
		std::string theTimeStepsNumber;
		while (theFile2.good()) {
			theTimeStepsNumber += theFile2.get();
		}

		//std::cout << "Run howmany time steps in each initialization?\n";
		int timeStepCount = stringToInt(theTimeStepsNumber);

		std::vector<int> outOfInitializationsCountEachTimeStepClosureTrueNumber;

		for (int i = 0; i < initializationsCount; ++i) {
			resultFile << "initialization " << i + 1 << std::endl;
			initializeNodesInNetworkFromAFile();
			setAllBooleanEquationsFromAFile();
			showInfoOfAllNodesInNetworkWithTheirStates(test);
			std::vector<int> temp = runTimeStepWithoutResetEachTime(resultFile, timeStepCount);
			if (0 == i) {
				outOfInitializationsCountEachTimeStepClosureTrueNumber = temp;
			}
			else {
				for (int j = 0; j < outOfInitializationsCountEachTimeStepClosureTrueNumber.size(); ++j) {
					outOfInitializationsCountEachTimeStepClosureTrueNumber[j] += temp[j];
				}
			}
			freeAllMemory();
			listOfBooleanEquations.clear();
			listOfNodes.clear();
			trackingAllMinterms.clear();
		}

		std::vector<float> resultingCurveClosurePercentageVSTimeSteps;
		for (int i = 0; i < outOfInitializationsCountEachTimeStepClosureTrueNumber.size(); ++i) {
			resultingCurveClosurePercentageVSTimeSteps.push_back(float(outOfInitializationsCountEachTimeStepClosureTrueNumber[i])/float(initializationsCount)*100);
		}

		std::ofstream plotingFile;
		plotingFile.open("ploting points file.txt");
		for (int i = 0; i < resultingCurveClosurePercentageVSTimeSteps.size(); ++i) {
			plotingFile << i + 1 << ' ';
			plotingFile << resultingCurveClosurePercentageVSTimeSteps[i] << std::endl;
		}

		return;
	}

	void initializeNodesInNetworkFromAFile() {
		Node* nodeAddress;
		nodeAddress = new Node;

		std::ifstream theFile("Input Setting.txt");
		std::string theNumber;
		while (theFile.good()) {
			theNumber += theFile.get();
		}

		int InputNodeInitialState = stringToInt(theNumber);

		nodeAddress->setNodeState(InputNodeInitialState); // ABA stste here
		nodeAddress->setNodeName("input");
		listOfNodes.push_back(nodeAddress);
		//std::cout << "node " << 0 << " node name: " << nodeAddress->getNodeName() << " is set to: " << 1 << std::endl;

		int number_of_lines = 0;
		{
			std::string line;
			std::ifstream myfile("Node Name and their initial state.txt");
			if (myfile.is_open()) {
				while (!myfile.eof()) {
					getline(myfile, line);
					number_of_lines++;
				}
				myfile.close();
			}
		}

		int nodeCount = number_of_lines; /*get node count number*/
		int i;
		std::string line;
		std::ifstream theNodesFile("Node Name and their initial state.txt");
		for (i = 0; i < nodeCount; ++i) {
			//std::cout << "Making node " << i + 1 << " in the network.\n";
			nodeAddress = new Node; /*making a new node on the heap*/
			listOfNodes.push_back(nodeAddress);
			getline(theNodesFile, line);
			std::stringstream theStringStream(line);
			std::string nodename;
			int nodeState;
			theStringStream >> nodename;
			nodeAddress->setNodeName(nodename);
			if (theStringStream.good()) {
				theStringStream >> nodeState;
				nodeAddress->setNodeState(nodeState);
				//std::cout << "node " << i + 1 << " node name: " << nodeAddress->getNodeName() << " is set to: " << nodeState << std::endl;
			}
			else {
				//std::cout << "node " << i + 1 << " node name: " << nodeAddress->getNodeName() << " now is randomly initialized.\n";
				nodeAddress->randomlyInitializeNodeState();
			}
		}
		//std::cout << "input, closure, and " << i - 1 << " nodes are made in between input node and closure node.\n";
		//std::cout << "now, set boolean equations for " << i - 1 << " intermediate nodes and closure node. No boolean equation for input node.\n";
	}

	/*istream& diy_getline(istream& is, std::string& s, char delim = '\n')
	{
		s.clear();
		int ch;
		while ((ch = is.get()) != EOF && ch != delim)
			s.push_back(ch);
		return is;
	}*/

	void setAllBooleanEquationsFromAFile() {
		BooleanEquation* booleanEquationAddress;
		//std::cout << "total of " << listOfNodes.size() - 1 << " boolean equations are needed.\n";
		/*the following for loop creates all the boolean equations starting from node 1 until closure node*/
		for (int i = 0; i < listOfNodes.size() - 1; ++i) {
			booleanEquationAddress = new BooleanEquation;
			booleanEquationAddress->setTargetNode(*listOfNodes[i + 1]); /*skipping input node for total of (listOfNodes.size() - 1) boolean equations*/
			listOfBooleanEquations.push_back(booleanEquationAddress);
			//std::cout << "boolean equation for node index " << i + 1 << " is set without minterms, target node name is: " << listOfNodes[i + 1]->getNodeName() << '\n';
		}
		//std::cout << "setting boolean equations process now starts:\n";
		//showSettingBooleanEquationRules();
		//showInfoOfAllNodesInNetwork();
		//std::cin.clear();
		//std::cin.ignore(10000, '\n');
		std::ifstream theEquationFile("Boolean Equations File.txt");
		std::string userInputString;

		std::vector<std::string> userInputStrings;

		while (theEquationFile.good()) {
			getline(theEquationFile, userInputString);
			userInputStrings.push_back(userInputString);
			userInputString.clear();
		}


		for (int booleanEquationIndex = 0; booleanEquationIndex < listOfBooleanEquations.size(); ++booleanEquationIndex) {
		tryAgain:
			//std::cout << "set boolean equation for target node index: " << booleanEquationIndex + 1 << " node name: " << listOfNodes[booleanEquationIndex + 1]->getNodeName() << " :\n";
			//std::cout << booleanEquationIndex + 1 << " = ";
			std::string userInputString;
			//char tempString[1001];
			//std::cin.getline(tempString, 1000);
			//userInputString = tempString; /*now userInputString contains whatever user inputed boolean equation*/
			//getline(theEquationFile, userInputString);
			//std::cout << userInputString << std::endl;
			userInputString = userInputStrings[booleanEquationIndex];
			//std::cout << userInputString << std::endl;
			userInputString = removeSpaces(userInputString); /*remove all spaces from the string*/
			std::string userInputStringCopy = userInputString;
			if (!contains_number(userInputString)) {
				std::cout << "your input does not contain any number (no node index in your input), try again.\n";
				goto tryAgain;
			}
			for (int i = 0; i < userInputString.length(); ++i) {
				if (!isOneOfValidInputChar(userInputString[i])) {
					std::cout << "the first invalid input char is: " << userInputString[i] << ", try again.\n";
					goto tryAgain;
				}
			}
			/*if (!isNumber(userInputString[userInputString.length() - 1])) {
				std::cout << "the last inputed char (excluding spaces in the end) is not a part of node index, that is, the last inputed char is not a number, try again.\n";
				goto tryAgain;
			}
			if (userInputString[0] == '&' || userInputString[0] == '|') {
				std::cout << "the first char cannot be '&' or '|' (excluding spaces in the beginning), try again.\n";
				goto tryAgain;
			}
			for (int i = 0; i < userInputString.length(); ++i) {
				if (userInputString[i] == '~' && i + 1 < userInputString.length() && i + 1 >= 0) {
					if (!isNumber(userInputString[i + 1])) {
						std::cout << "'~' at position: " << i << " of the input string is not followed by a node index, try again.\n";
						goto tryAgain;
					}
				}
			}
			for (int i = 0; i < userInputString.length(); ++i) {
				if (userInputString[i] == '~' && i - 1 < userInputString.length() && i - 1 >= 0) {
					if (isNumber(userInputString[i - 1])) {
						std::cout << "'~' at position: " << i << " of the input string is not following an logical operation in front of it, try again.\n";
						goto tryAgain;
					}
				}
			}
			for (int i = 0; i < userInputString.length(); ++i) {
				if ((userInputString[i] == '&' || userInputString[i] == '|') && i - 1 < userInputString.length() && i - 1 >= 0) {
					if (!isNumber(userInputString[i - 1])) {
						std::cout << "'" << userInputString[i] << "' at position: " << i << " of the input string is not after a node index, try again.\n";
						goto tryAgain;
					}
				}
			}
			for (int i = 0; i < userInputString.length(); ++i) {
				if ((userInputString[i] == '&' || userInputString[i] == '|') && i + 1 < userInputString.length() && i + 1 >= 0) {
					if (!isNumber(userInputString[i + 1]) && userInputString[i + 1] != '~') {
						std::cout << "'" << userInputString[i] << "' at position: " << i << " of the input string is not followed by logical NOT operator '~' or a node index, try again.\n";
						goto tryAgain;
					}
				}
			}*/
			//===============================================================================================================================================
			// the following block of code extracts all numbers in the inputted string
			std::vector<int> nodeIndexesInUserInputtedString; /*vector stores each integer inputted in order*/
			std::vector<int> trackingFirstIndexOfEachNumberInputted; /*each index is associated with storing integer vector index, and stores that index's integer's position in the string*/
			int lastTrackedStringIndex;
			int counter = 0;
			int previousRoundEraseCount;
			while (contains_number(userInputStringCopy)) {
				nodeIndexesInUserInputtedString.push_back(stringToInt(userInputStringCopy));
				int eraseHowManyCharsCount = 1;
				while (userInputStringCopy.find_first_of("0123456789") + eraseHowManyCharsCount <= userInputStringCopy.length() - 1 && isNumber(userInputStringCopy[userInputStringCopy.find_first_of("0123456789") + eraseHowManyCharsCount])) {
					eraseHowManyCharsCount++;
				}
				//std::cout << "eraseHowManyCharsCount: " << eraseHowManyCharsCount << std::endl;
				if (counter == 0) {
					trackingFirstIndexOfEachNumberInputted.push_back(userInputString.find_first_of(std::to_string(stringToInt(userInputStringCopy)))); /*from the original user inputted string to find the first index of the number inputed, then push into the tracking vector*/
				}
				else {
					trackingFirstIndexOfEachNumberInputted.push_back(userInputString.find_first_of(std::to_string(stringToInt(userInputStringCopy)), lastTrackedStringIndex + previousRoundEraseCount)); /*from the original user inputted string to find the first index of the number inputed, then push into the tracking vector*/
				}
				if (trackingFirstIndexOfEachNumberInputted.size() >= 1) {
					lastTrackedStringIndex = trackingFirstIndexOfEachNumberInputted[trackingFirstIndexOfEachNumberInputted.size() - 1];
					//std::cout << "lastTrackedStringIndex: " << lastTrackedStringIndex << std::endl;
				}
				previousRoundEraseCount = eraseHowManyCharsCount;
				userInputStringCopy.erase(userInputStringCopy.find_first_of("0123456789"), eraseHowManyCharsCount);
				++counter;
			}
			// ================================================================================================================================================
			//std::cout << "all node indexes inputted extracted in order: \n";
			for (int i = 0; i < nodeIndexesInUserInputtedString.size(); ++i) {
				//std::cout << nodeIndexesInUserInputtedString[i] << " at string position index (after removing all spaces): " << trackingFirstIndexOfEachNumberInputted[i] << std::endl;
			}
			for (int i = 0; i < nodeIndexesInUserInputtedString.size(); ++i) {
				if (nodeIndexesInUserInputtedString[i] < 0 || nodeIndexesInUserInputtedString[i] > listOfNodes.size() - 1) { /*check each inputted number is in range*/
					showInfoOfAllNodesInNetwork();
					std::cout << "inputted node index: " << nodeIndexesInUserInputtedString[i] << " is invalid, because it is out of range (refer to the above nodes in network), try again.\n";
					goto tryAgain;
				}
			}
			//std::cout << "inputted boolean equation is valid.\n";
			//std::cout << "inputted string was: " << userInputString << '\n';
			//==================================================================================================================================================
			std::vector<int> trackingLogicalNOTPosition;
			int found = userInputString.find_first_of('~');
			while (found != std::string::npos) {
				trackingLogicalNOTPosition.push_back(found);
				found = userInputString.find_first_of('~', found + 1);
			}
			//std::cout << "all logical NOT ~ position: \n";
			for (int i = 0; i < trackingLogicalNOTPosition.size(); ++i) {
				//std::cout << trackingLogicalNOTPosition[i] << std::endl;
			}
			std::vector<int> trackingLogicalORPosition;
			found = userInputString.find_first_of('|');
			while (found != std::string::npos) {
				trackingLogicalORPosition.push_back(found);
				found = userInputString.find_first_of('|', found + 1);
			}
			//std::cout << "all logical OR | position: \n";
			for (int i = 0; i < trackingLogicalORPosition.size(); ++i) {
				std::cout << trackingLogicalORPosition[i] << std::endl;
			}
			std::vector<int> trackingLogicalANDPosition;
			found = userInputString.find_first_of('&');
			while (found != std::string::npos) {
				trackingLogicalANDPosition.push_back(found);
				found = userInputString.find_first_of('&', found + 1);
			}
			//std::cout << "all logical AND & position: \n";
			for (int i = 0; i < trackingLogicalANDPosition.size(); ++i) {
				//std::cout << trackingLogicalANDPosition[i] << std::endl;
			}
			std::vector<int> markingEachNodeIndexForLogicalNotApplied; /*vector that have the same size of nodeIndexesInUserInputtedString that records each node has logical not applied in the minterm, 1 for not applied, 0 for no not applied*/
			for (int i = 0; i < nodeIndexesInUserInputtedString.size(); ++i) {
				bool flag = false;
				for (int j = 0; j < trackingLogicalNOTPosition.size(); ++j) {
					if (trackingLogicalNOTPosition[j] + 1 == trackingFirstIndexOfEachNumberInputted[i]) {
						flag = true;
					}
				}
				if (flag) {
					markingEachNodeIndexForLogicalNotApplied.push_back(1);
				}
				else {
					markingEachNodeIndexForLogicalNotApplied.push_back(0);
				}
			}
			//std::cout << "each node not applied situation:\n";
			for (int i = 0; i < markingEachNodeIndexForLogicalNotApplied.size(); ++i) {
				//std::cout << markingEachNodeIndexForLogicalNotApplied[i] << std::endl;
			}
			//std::cout << "for this boolean equation a total of " << trackingLogicalORPosition.size() + 1;
			//if (trackingLogicalORPosition.size() == 0) std::cout << " minterm is needed\n";
			//else std::cout << " minterms are needed\n";
			//=============================================================================================================================
			//the following codes set up the boolean equation by setting up minterms and pushing in minterms into boolean equations
			Minterm* mintermAddress;
			if (trackingLogicalORPosition.size() == 0) {
				mintermAddress = new Minterm;
				for (int j = 0; j < nodeIndexesInUserInputtedString.size(); ++j) {
					if (markingEachNodeIndexForLogicalNotApplied[j] == 1) {
						mintermAddress->addNotNode(*listOfNodes[nodeIndexesInUserInputtedString[j]]);
					}
					else if (markingEachNodeIndexForLogicalNotApplied[j] == 0) {
						mintermAddress->addRegularNode(*listOfNodes[nodeIndexesInUserInputtedString[j]]);
					}
				}
				listOfBooleanEquations[booleanEquationIndex]->addMinterm(*mintermAddress);
				trackingAllMinterms.push_back(mintermAddress);
			}
			else if (trackingLogicalORPosition.size() != 0) {
				mintermAddress = new Minterm;
				for (int j = 0; j < nodeIndexesInUserInputtedString.size(); ++j) {
					if (trackingFirstIndexOfEachNumberInputted[j] < trackingLogicalORPosition[0] && markingEachNodeIndexForLogicalNotApplied[j] == 1) {
						mintermAddress->addNotNode(*listOfNodes[nodeIndexesInUserInputtedString[j]]);
					}
					else if (trackingFirstIndexOfEachNumberInputted[j] < trackingLogicalORPosition[0] && markingEachNodeIndexForLogicalNotApplied[j] == 0) {
						mintermAddress->addRegularNode(*listOfNodes[nodeIndexesInUserInputtedString[j]]);
					}
				}
				listOfBooleanEquations[booleanEquationIndex]->addMinterm(*mintermAddress);
				trackingAllMinterms.push_back(mintermAddress);
				for (int i = 1; i < trackingLogicalORPosition.size(); ++i) {
					mintermAddress = new Minterm;
					for (int j = 0; j < nodeIndexesInUserInputtedString.size(); ++j) {
						if (trackingLogicalORPosition[i - 1] < trackingFirstIndexOfEachNumberInputted[j] && trackingFirstIndexOfEachNumberInputted[j] < trackingLogicalORPosition[i] && markingEachNodeIndexForLogicalNotApplied[j] == 1) {
							mintermAddress->addNotNode(*listOfNodes[nodeIndexesInUserInputtedString[j]]);
						}
						else if (trackingLogicalORPosition[i - 1] < trackingFirstIndexOfEachNumberInputted[j] && trackingFirstIndexOfEachNumberInputted[j] < trackingLogicalORPosition[i] && markingEachNodeIndexForLogicalNotApplied[j] == 0) {
							mintermAddress->addRegularNode(*listOfNodes[nodeIndexesInUserInputtedString[j]]);
						}
					}
					listOfBooleanEquations[booleanEquationIndex]->addMinterm(*mintermAddress);
					trackingAllMinterms.push_back(mintermAddress);
				}
				mintermAddress = new Minterm;
				for (int j = 0; j < nodeIndexesInUserInputtedString.size(); ++j) {
					if (trackingFirstIndexOfEachNumberInputted[j] > trackingLogicalORPosition[trackingLogicalORPosition.size() - 1] && markingEachNodeIndexForLogicalNotApplied[j] == 1) {
						mintermAddress->addNotNode(*listOfNodes[nodeIndexesInUserInputtedString[j]]);
					}
					else if (trackingFirstIndexOfEachNumberInputted[j] > trackingLogicalORPosition[trackingLogicalORPosition.size() - 1] && markingEachNodeIndexForLogicalNotApplied[j] == 0) {
						mintermAddress->addRegularNode(*listOfNodes[nodeIndexesInUserInputtedString[j]]);
					}
				}
				listOfBooleanEquations[booleanEquationIndex]->addMinterm(*mintermAddress);
				trackingAllMinterms.push_back(mintermAddress);
			}
			//std::cout << "boolean equation is set for target node index: " << booleanEquationIndex + 1 << " node name: " << listOfNodes[booleanEquationIndex + 1]->getNodeName() << " :\n";
			//listOfBooleanEquations[booleanEquationIndex]->printOutBooleanEquation();
		}
	}
	std::vector<int> runTimeStepWithoutResetEachTime(std::ofstream& resultFile, int timeStepCount) { // return back out the closure states recording vector, this vector has however many time steps elements, each element records the closure state at the end of that time step
		std::vector<int> recordingClosureState;
		//std::cout << "Run howmany time steps?\n";
		//int timeStepCount = promptUserInputAnInterger();
		//int timeStepCount = 20; // 20 time steps in each initialization
		std::vector<int> randomBooleanEquationOrder;
		int randomIndex;
		
		for (int i = 0; i < timeStepCount; ++i) {
			//std::cout << "time step " << i + 1 << " : \n";
			resultFile << "time step " << i + 1 << " : \n";
			//std::cout << "initial nodes' state:\n";
			resultFile << "initial nodes' state:\n";
			//randomlizeAllNodesStateExceptInputNode();
			showInfoOfAllNodesInNetworkWithTheirStates(resultFile);
			randomBooleanEquationOrder.clear();
			for (int j = 0; j < listOfBooleanEquations.size() - 1; ++j) {
			generateAgain:
				randomIndex = rand() % (listOfBooleanEquations.size() - 1);
				for (int k = 0; k < randomBooleanEquationOrder.size(); ++k) {
					if (randomBooleanEquationOrder[k] == randomIndex) {
						goto generateAgain;
					}
				}
				randomBooleanEquationOrder.push_back(randomIndex);
			}
			//std::cout << "boolean equations evaluated in the random order:\n";
			resultFile << "boolean equations evaluated in the random order:\n";
			for (int h = 0; h < randomBooleanEquationOrder.size(); ++h) {
				//std::cout << "equation index: " << randomBooleanEquationOrder[h] << " equation: ";
				resultFile << "equation index: " << randomBooleanEquationOrder[h] << " equation: ";
				//listOfBooleanEquations[randomBooleanEquationOrder[h]]->printOutBooleanEquation();
				listOfBooleanEquations[randomBooleanEquationOrder[h]]->printOutBooleanEquationInFile(resultFile);
				listOfBooleanEquations[randomBooleanEquationOrder[h]]->evaluateBooleanEquationAndSetTargetNodeState();
			}
			//std::cout << "equation index: " << listOfBooleanEquations.size() - 1 << " equation: ";
			resultFile << "equation index: " << listOfBooleanEquations.size() - 1 << " equation: ";
			//listOfBooleanEquations[listOfBooleanEquations.size() - 1]->printOutBooleanEquation();
			listOfBooleanEquations[listOfBooleanEquations.size() - 1]->printOutBooleanEquationInFile(resultFile);
			listOfBooleanEquations[listOfBooleanEquations.size() - 1]->evaluateBooleanEquationAndSetTargetNodeState();
			//std::cout << "nodes' state after evaluating boolean equations in the above order:\n";
			resultFile << "nodes' state after evaluating boolean equations in the above order:\n";
			showInfoOfAllNodesInNetworkWithTheirStates(resultFile);
			recordingClosureState.push_back(listOfNodes[listOfNodes.size()-1]->getNodeState()); // recording closure node states in steps
		}
		return recordingClosureState;
	}
	

	// checks if a string contains number
	bool contains_number(const std::string& c)
	{
		return (c.find_first_of("0123456789") != std::string::npos);
	}
	// this function checks the char is a number or not
	bool isNumber(char aChar) {
		static std::string number("0123456789");
		return std::string::npos == number.find(aChar) ? false : true;
	}
	// this function checks the char is valid
	bool isOneOfValidInputChar(char aChar) {
		static std::string punct("1234567890~&|");
		punct += ' ';
		return std::string::npos == punct.find(aChar) ? false : true;
	}
	// this function converts a string with numbers to an integer, only the first appearing number is being converted to int
	int stringToInt(std::string aStr) {
		int d = stoi(aStr.substr(aStr.find_first_of("0123456789"), aStr.find_last_of("0123456789") + 1));
		return d;
	}
	// Function to remove all spaces from a given string 
	std::string removeSpaces(std::string str)
	{
		str.erase(remove(str.begin(), str.end(), ' '), str.end());
		return str;
	}
	// Function to extract all numbers in a string
	std::vector<int> extractIntegersInAString(std::string userInputStringCopy) {
		std::vector<int> nodeIndexesInUserInputtedString;
		while (contains_number(userInputStringCopy)) {
			nodeIndexesInUserInputtedString.push_back(stringToInt(userInputStringCopy));
			int eraseHowManyCharsCount = 1;
			while (userInputStringCopy.find_first_of("0123456789") + eraseHowManyCharsCount <= userInputStringCopy.length() - 1 && isNumber(userInputStringCopy[userInputStringCopy.find_first_of("0123456789") + eraseHowManyCharsCount])) {
				eraseHowManyCharsCount++;
			}
			std::cout << "eraseHowManyCharsCount: " << eraseHowManyCharsCount << std::endl;
			userInputStringCopy.erase(userInputStringCopy.find_first_of("0123456789"), eraseHowManyCharsCount);
		}
		for (int i = 0; i < nodeIndexesInUserInputtedString.size(); ++i) {
			std::cout << nodeIndexesInUserInputtedString[i] << std::endl;
		}
	}

	void deleteAllNodesInNetwork(){
		if (listOfNodes.size()) {
			for (int i = 0; i < listOfNodes.size(); ++i) {
				delete listOfNodes[i];
			}
		}
	}
	void deleteAllMintermsInNetwork(){
		if (trackingAllMinterms.size()) {
			for (int i = 0; i < trackingAllMinterms.size(); ++i) {
				delete trackingAllMinterms[i];
			}
		}
	}
	void deleteAllBooleanEquationsInNetwork(){
		if (listOfBooleanEquations.size()) {
			for (int i = 0; i < listOfBooleanEquations.size(); ++i) {
				delete listOfBooleanEquations[i];
			}
		}
	}
	void freeAllMemory(){
		deleteAllNodesInNetwork();
		deleteAllMintermsInNetwork();
		deleteAllBooleanEquationsInNetwork();
		std::cout << "All allocated memory is freed!\n";
	}
protected:
	std::vector<Node*> listOfNodes; /*first item in vector is input node, last item in vector is closure node*/
	std::vector<Minterm*> trackingAllMinterms; /*record down all minterms' addressess*/
	std::vector<BooleanEquation*> listOfBooleanEquations; /*except input node, all other nodes (including closure node) have an associated boolean equation*/
};

class Connection {
public:
	Connection(int aValue = 0) : type(aValue) {}
	Connection(Node aNode1, int aValue, Node aNode2) : origin(aNode1), type(aValue), target(aNode2) {}
	Connection(const Connection& aCopy) : origin(aCopy.origin), type(aCopy.type), target(aCopy.target) {}
	~Connection(){}
	Connection& operator=(const Connection& aCopy) {
		origin = aCopy.origin;
		type = aCopy.type;
		target = aCopy.target;
		return *this;
	}
	void printTheConnection() {
		origin.printTheNode();
		for (int j = 0; j < 5; ++j) {
			for (int i = 0; i < 8; ++i) {
				std::cout << " ";
			}
			if (type == 0) {
				std::cout << "|\n";
			}
			else if (type == 1) {
				std::cout << "+\n";
			}
		}
		for (int i = 0; i < 8; ++i) {
			std::cout << " ";
		}
		std::cout << "V\n";
		target.printTheNode();
	}
	int getConnectionType() {
		return type;
	}
	void update() {
		if (origin.getNodeState() == 1 && type == 0) {
			target.setNodeState(0);
		}
		if (origin.getNodeState() == 1 && type == 1) {
			target.setNodeState(1);
		}
	}
protected:
	Node origin;
	Node target;
	int type;
};

class Logic_Operation {
public:
	Logic_Operation(){}
	Logic_Operation(const Logic_Operation& aCopy){}
	~Logic_Operation(){}
	Logic_Operation& operator=(const Logic_Operation& aCopy) {
		return *this;
	}
	virtual int execute_logic() = 0;
	virtual int getResult() = 0;
protected:
};

class Logic_And : public Logic_Operation{
public:
	Logic_And(int aValue1 = 1, int aValue2 = 1) : logicAndReturnValue(0), firstValue(aValue1), secondValue(aValue2) {}
	Logic_And(const Logic_And& aCopy) : logicAndReturnValue(aCopy.logicAndReturnValue), theNodesAndTogether(aCopy.theNodesAndTogether), firstValue(aCopy.firstValue), secondValue(aCopy.secondValue) {}
	~Logic_And(){}
	Logic_And& operator=(const Logic_And& aCopy) {
		firstValue = aCopy.firstValue;
		secondValue = aCopy.secondValue;
		logicAndReturnValue = aCopy.logicAndReturnValue;
		theNodesAndTogether = aCopy.theNodesAndTogether;
		return *this;
	}
	Logic_And& push_in_nodes(Node aNode) {
		theNodesAndTogether.push_back(aNode);
		return *this;
	}
	int execute_logic() override { // this function update and together nodes result
		if (theNodesAndTogether.size() == 0) {
			logicAndReturnValue = firstValue && secondValue;
			return logicAndReturnValue;
		}
		else if (theNodesAndTogether.size() == 1) {
			logicAndReturnValue = firstValue && secondValue && theNodesAndTogether[0].getNodeState();
			return logicAndReturnValue;
		}
		else {
			for (Node& theNode : theNodesAndTogether) {
				if (theNode.getNodeState() == 0) {
					logicAndReturnValue = 0;
					return 0;
				}
			}
			logicAndReturnValue = firstValue && secondValue;
			return logicAndReturnValue;
		}
	}
	Logic_And& setFirst(int i){
		firstValue = i;
		return *this;
	}
	Logic_And& setSecond(int i) {
		secondValue = i;
		return *this;
	}
	int getResult() override {
		return logicAndReturnValue;
	}
protected:
	int logicAndReturnValue;
	int firstValue;
	int secondValue;
	std::vector<Node> theNodesAndTogether;
};

class Logic_Or : public Logic_Operation{
public:
	Logic_Or(int aValue1 = 0, int aValue2 = 0) : logicOrReturnValue(0), firstValue(aValue1), secondValue(aValue2) {}
	Logic_Or(const Logic_Or& aCopy) : logicOrReturnValue(aCopy.logicOrReturnValue), theNodesOrTogether(aCopy.theNodesOrTogether), firstValue(aCopy.firstValue), secondValue(aCopy.secondValue) {}
	~Logic_Or() {}
	Logic_Or& operator=(const Logic_Or& aCopy) {
		firstValue = aCopy.firstValue;
		secondValue = aCopy.secondValue;
		logicOrReturnValue = aCopy.logicOrReturnValue;
		theNodesOrTogether = aCopy.theNodesOrTogether;
		return *this;
	}
	int execute_logic() override { // this function update and together nodes result
		if (theNodesOrTogether.size() == 0) {
			logicOrReturnValue = firstValue || secondValue;
			return logicOrReturnValue;
		}
		else if (theNodesOrTogether.size() == 1) {
			logicOrReturnValue = firstValue || secondValue || theNodesOrTogether[0].getNodeState();
			return logicOrReturnValue;
		}
		else {
			for (Node& theNode : theNodesOrTogether) {
				if (theNode.getNodeState() == 1) {
					logicOrReturnValue = 1;
					return 1;
				}
			}
			logicOrReturnValue = firstValue || secondValue;
			return logicOrReturnValue;
		}
	}
	Logic_Or& push_in_nodes(Node aNode) {
		theNodesOrTogether.push_back(aNode);
		return *this;
	}
	Logic_Or& setFirst(int i) {
		firstValue = i;
		return *this;
	}
	Logic_Or& setSecond(int i) {
		secondValue = i;
		return *this;
	}
	int getResult() override {
		return logicOrReturnValue;
	}
protected:
	int logicOrReturnValue;
	int firstValue;
	int secondValue;
	std::vector<Node> theNodesOrTogether;
};

class Logic_Not : public Logic_Operation {
public:
	Logic_Not(int aValue = 0) : logicNotReturnValue(0), Value(aValue) {}
	Logic_Not(const Logic_Not& aCopy) : inputNode(aCopy.inputNode),logicNotReturnValue(aCopy.logicNotReturnValue), Value(aCopy.Value){}
	~Logic_Not(){}
	Logic_Not& operator=(const Logic_Not& aCopy) {
		inputNode = aCopy.inputNode;
		Value = aCopy.Value;
		logicNotReturnValue = aCopy.logicNotReturnValue;
		return *this;
	}
	Logic_Not& setValue(int i) {
		Value = i;
		return *this;
	}
	Logic_Not& push_in_nodes(Node aNode) {
		inputNode.push_back(aNode);
		return *this;
	}
	int execute_logic() override {
		if (inputNode.size() == 0) {
			logicNotReturnValue = !Value;
			return logicNotReturnValue;
		}
		else {
			logicNotReturnValue = !inputNode[0].getNodeState();
			return logicNotReturnValue;
		}
	}
	int getResult() override {
		return logicNotReturnValue;
	}
protected:
	int logicNotReturnValue;
	int Value;
	std::vector<Node> inputNode;
};

class Logic_Equal : public Logic_Operation {
public:
	Logic_Equal(int aValue = 0) : logicEqualReturnValue(0), Value(aValue) {}
	Logic_Equal(const Logic_Equal& aCopy) : inputNode(aCopy.inputNode), logicEqualReturnValue(aCopy.logicEqualReturnValue), Value(aCopy.Value) {}
	~Logic_Equal() {}
	Logic_Equal& operator=(const Logic_Equal& aCopy) {
		inputNode = aCopy.inputNode;
		Value = aCopy.Value;
		logicEqualReturnValue = aCopy.logicEqualReturnValue;
		return *this;
	}
	Logic_Equal& setValue(int i) {
		Value = i;
		return *this;
	}
	Logic_Equal& push_in_nodes(Node aNode) {
		inputNode.push_back(aNode);
		return *this;
	}
	int execute_logic() override {
		if (inputNode.size() == 0) {
			logicEqualReturnValue = Value;
			return logicEqualReturnValue;
		}
		else {
			logicEqualReturnValue = inputNode[0].getNodeState();
			return logicEqualReturnValue;
		}
	}
	int getResult() override {
		return logicEqualReturnValue;
	}
protected:
	int logicEqualReturnValue;
	int Value;
	std::vector<Node> inputNode;
};

class BooleanFunction {
public:
	BooleanFunction() = default;
	BooleanFunction(Node& aTargetNode) : theTarget(aTargetNode) {}
	BooleanFunction(const BooleanFunction& aCopy) : theTarget(aCopy.theTarget), LogicOperations(aCopy.LogicOperations){}
	~BooleanFunction(){
		for (Logic_Operation* theOperation : LogicOperations) {
			delete theOperation;
		}
	}
	BooleanFunction& operator=(const BooleanFunction& aCopy) {
		theTarget = aCopy.theTarget;
		LogicOperations = aCopy.LogicOperations;
		return *this;
	}
	int executeFunction() {
		for (Logic_Operation* theOperation : LogicOperations) {
			theOperation->execute_logic();
		}
		theTarget.setNodeState(LogicOperations[LogicOperations.size() - 1]->execute_logic());
		return LogicOperations[LogicOperations.size() - 1]->execute_logic(); // make sure the last operation in the operation logic is final logic
	}
	BooleanFunction& push_in_operations(Logic_Or anOperation) {
		Logic_Operation* aPtr = new Logic_Or(anOperation);
		LogicOperations.push_back(aPtr);
		return *this;
	}
	BooleanFunction& push_in_operations(Logic_And anOperation) {
		Logic_Operation* aPtr = new Logic_And(anOperation);
		LogicOperations.push_back(aPtr);
		return *this;
	}
	BooleanFunction& push_in_operations(Logic_Not anOperation) {
		Logic_Operation* aPtr = new Logic_Not(anOperation);
		LogicOperations.push_back(aPtr);
		return *this;
	}
	BooleanFunction& push_in_operations(Logic_Equal anOperation) {
		Logic_Operation* aPtr = new Logic_Equal(anOperation);
		LogicOperations.push_back(aPtr);
		return *this;
	}
protected:
	Node& theTarget;
	std::vector<Logic_Operation*> LogicOperations; 
};

class Network { // this network class has a vector of Nodes
public:
	Network() {}
	Network(const Network& aCopy) : theNodesInNetwork(aCopy.theNodesInNetwork) {}
	~Network() {}
	Network& operator=(const Network& aCopy) {
		theNodesInNetwork = aCopy.theNodesInNetwork;
		return *this;
	}
	Network& push_in_nodes(Node aNode) {
		theNodesInNetwork.push_back(aNode);
		return *this;
	}
	Network& push_in_functions(BooleanFunction aFunction) {
		booleanFunctionsInNetwork.push_back(aFunction);
		return *this;
	}
	Network& executeAllFunctionsInTheNetwork() {
		for (BooleanFunction& aFunction : booleanFunctionsInNetwork) {
			aFunction.executeFunction();
		}
		return *this;
	}
	void printOutNetWork() {
		for (Node aNode : theNodesInNetwork) {
			aNode.printNodeInfo();
		}
	}
	Node& getNodeInNetwork(int i) {
		return theNodesInNetwork[i];
	}
	Node getTNodeInNetwork(int i) {
		return theNodesInNetwork[i];
	}
	int getNodesCount() {
		return theNodesInNetwork.size();
	}
protected:
	std::vector<Node> theNodesInNetwork;
	std::vector<BooleanFunction> booleanFunctionsInNetwork;
};

std::string getUserInputNodeName() {
	fflush(stdin);
	std::cout << "Please enter a Node name: ";
	std::string userInputtedString;
	again:
	char theCharString[13] = { 0 }; // user input can be most 29 characters, more than that will be truncated
	std::cin.getline(theCharString, 12);
	userInputtedString = theCharString;
	fflush(stdin);
	if (userInputtedString == "") {
		goto again;
	}
	return userInputtedString;
}

int getUserInputNodeState() {
	std::cout << "Please enter the Node's state (either input 1 or 0): ";
	int userInputNodeState;
	std::cin >> userInputNodeState;
	if ((userInputNodeState != 0) && (userInputNodeState != 1)) {
		std::cout << "Invalid input, you can only input 0 or 1, try again.\n";
		getUserInputNodeState();
	}
	else {
		fflush(stdin);
		return userInputNodeState;
	}
}

int getUserInputConnectionState() {
	std::cout << "Please enter the inbetween Nodes' connection's state (either input 1 or 0): ";
	int userInputNodeState;
	std::cin >> userInputNodeState;
	if ((userInputNodeState != 0) && (userInputNodeState != 1)) {
		std::cout << "Invalid input, you can only input 0 or 1, try again.\n";
		getUserInputNodeState();
	}
	else {
		fflush(stdin);
		return userInputNodeState;
	}
}

int generateState() {
	return rand() % 2;
}


int main() {
	srand(time(NULL));
	/*Node theNode1(1, "1");
	Node theNode2(1, "2");
	Node theNode3(0, "3");
	Node theNode4(0, "4");
	std::cout << "theNode4: " << theNode4.getNodeState() << std::endl;
	Minterm theMinterm;
	theMinterm.addRegularNode(theNode1).addRegularNode(theNode2).addNotNode(theNode3).addNotNode(theNode4);
	std::cout << "theMinterm.printOutMinterm(): "; theMinterm.printOutMinterm(); std::cout << '\n';
	std::cout << "evaluated minterm is: " << theMinterm.evaluateMinterm() << std::endl;
	theNode4.setNodeState(1);
	std::cout << "theNode4: " << theNode4.getNodeState() << std::endl;
	std::cout << "evaluated minterm is: " << theMinterm.evaluateMinterm() << std::endl;
	std::cout << "theNode2: " << theNode2.getNodeState() << std::endl;
	std::cout << "theNode3: " << theNode3.getNodeState() << std::endl;
	std::cout << "theNode4: " << theNode4.getNodeState() << std::endl;
	Minterm minterm1;
	minterm1.addRegularNode(theNode2);
	Minterm minterm2;
	minterm2.addNotNode(theNode3);
	BooleanEquation theBooleanEquation;
	theBooleanEquation.setTargetNode(theNode3);
	theBooleanEquation.addMinterm(minterm1).addMinterm(minterm2);
	theBooleanEquation.printOutBooleanEquation();
	theBooleanEquation.evaluateBooleanEquationAndSetTargetNodeState();
	std::cout << "the boolean equation is evaluated!\n";
	std::cout << "theNode2: " << theNode2.getNodeState() << std::endl;
	std::cout << "theNode3: " << theNode3.getNodeState() << std::endl;
	std::cout << "theNode4: " << theNode4.getNodeState() << std::endl;*/
	WholeNetwork aNetwork;
	aNetwork.simulation();
	return 0;
}