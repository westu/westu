#include <cstdio>
#include <iostream>
#include <set>
#include <vector>
#include <queue>
#include <string>
#include <cstring>
using namespace std;

class HuffmanNode
{
  private:
	double probablity;
	int fa, lc, rc;
	bool isLeafNode;
    string huffmanCode;
    int No;

  public:
  	HuffmanNode()
  	{
  	}
  	HuffmanNode(double p, bool isLeafNode, int n = 0)
  	{
  		probablity = p;
  		this->isLeafNode = isLeafNode;
  		No = n;
  		lc = rc = fa = -1;
  	}
  	HuffmanNode(double p, bool iLN, const int lc, const int rc)
  	{
  		probablity = p;
  		this->lc = lc;
  		this->rc = rc;
  		isLeafNode = iLN;
  	}

  	void setLcRc(const int lc, const int rc)
  	{
  		this->lc = lc;
  		this->rc = rc;
  	}

  	void setFather(const int fa)
  	{
  		this->fa = fa;
  	}

  	double getProbablity() const
  	{
  		return probablity;
  	}

  	int getLeftChild() const
  	{
  		return lc;
  	}

  	int getRightChild() const
  	{
  		return rc;
  	}

    int getFather() const
  	{
  		return fa;
  	}

  	void setHuffmanCode(const string &s)
  	{
  		huffmanCode = s;
  	}

  	string& getHuffmanCode()
  	{
  		return huffmanCode;
  	}

  	bool getIsLeafNode() const
  	{
  		return isLeafNode;
  	}

  	int getNo()
  	{
  	    return No;
  	}

  	~HuffmanNode()
  	{

  	}
};

class HuffmanNode4Compare
{
	private:
		double probablity;
		int p2Node;
	public:
	    HuffmanNode4Compare()
	    {

	    }
		HuffmanNode4Compare(double p, const int p2N)
		{
			probablity = p;
			p2Node = p2N;
		}

		int getP2Node() const
		{
			return p2Node;
		}

		double getProbablity() const
		{
			return probablity;
		}

		bool operator < (const HuffmanNode4Compare &b) const
		{
			return probablity < b.probablity;
		}

		HuffmanNode4Compare & operator = (const HuffmanNode4Compare &b)
		{
		    probablity = b.probablity;
		    p2Node = b.p2Node;
		}
};

void code_nodes(vector<HuffmanNode> &HuffmanNodes)
{
	(*(HuffmanNodes.end() - 1)).setHuffmanCode("");//set the root's huffman code
	queue<int> HuffmanNodes2;
	HuffmanNodes2.push(HuffmanNodes.size() - 1);

	while (HuffmanNodes2.empty() == false)
	{
		int tmp = HuffmanNodes2.front();
		HuffmanNodes2.pop();

		if (HuffmanNodes.at(tmp).getIsLeafNode() == false)
		{
			int tlc, trc;
			tlc = HuffmanNodes.at(tmp).getLeftChild();
			trc = HuffmanNodes.at(tmp).getRightChild();

			HuffmanNodes.at(tlc).setHuffmanCode( HuffmanNodes.at(tmp).getHuffmanCode() + "0" );
			HuffmanNodes.at(trc).setHuffmanCode( HuffmanNodes.at(tmp).getHuffmanCode() + "1" );

			HuffmanNodes2.push(tlc);
			HuffmanNodes2.push(trc);
		}
	}
}

void print_huffman_code(vector<HuffmanNode> &HuffmanNodes, int numOfNodes)
{
	freopen("huffmanCodes.txt", "w", stdout);
    int i = 0;
    cout << numOfNodes << endl;
	for(vector<HuffmanNode>::iterator it = HuffmanNodes.begin(); it != HuffmanNodes.end() && (*it).getIsLeafNode() == true; it++, i++)
		cout << i << ": " << (*it).getProbablity() << " " <<(*it).getHuffmanCode() << endl;
	fclose(stdout);
}

int main()
{
	multiset<HuffmanNode4Compare> HuffmanTree;
	HuffmanTree.clear();
	vector<HuffmanNode> HuffmanNodes;

	freopen("LenaProbablities.txt", "r", stdin);
	int numOfNodes;
	cin >> numOfNodes;

	if (numOfNodes < 1)
	{
		return 0;
	}
	if (numOfNodes == 1)
	{
		cout << "0" << endl;
		return 0;
	}


	for (int i = 0; i < numOfNodes; i++)
	{
		try
		{
			double p;

			cin >> p;
			if (p < -0.001)
				throw 1;

			HuffmanNode tmp(p, true);//is leaf node
			HuffmanNodes.push_back(tmp);

			HuffmanNode4Compare tmp2(p, i);
			HuffmanTree.insert(tmp2);
		}
        catch(int& errMessage)
        {
        	cerr << "Out of range" << endl;
        	return 0;
        }
	}

	for (int i = 1; i < numOfNodes; i++)//Build the huffman tree
	{
		multiset<HuffmanNode4Compare>::iterator it1, it2;
		it1 = HuffmanTree.begin();
		it2 = HuffmanTree.begin();// + 1;
		it2 ++;

		HuffmanNode node1, node2;//node1 , node2 are the two small nodes
		node1 = HuffmanNodes.at( (*it1).getP2Node() );
		node2 = HuffmanNodes.at( (*it2).getP2Node() );
		HuffmanNode tmp(node1.getProbablity() + node2.getProbablity(), false, (*it1).getP2Node(), (*it2).getP2Node());//creat the new node, and it isn't a leaf node
		HuffmanNodes.push_back(tmp);

		//set the two nodes' father
		HuffmanNodes.at( (*it1).getP2Node() ).setFather(HuffmanNodes.size() - 1);
		HuffmanNodes.at( (*it2).getP2Node() ).setFather(HuffmanNodes.size() - 1);

		HuffmanTree.erase(it1);//erase the two old, add the new one
		HuffmanTree.erase(it2);
		HuffmanNode4Compare tmp2(node1.getProbablity() + node2.getProbablity(), HuffmanNodes.size() - 1);
		HuffmanTree.insert(tmp2);
	}

	code_nodes(HuffmanNodes);
	print_huffman_code(HuffmanNodes, numOfNodes);
	fclose(stdin);

	return 0;
}
